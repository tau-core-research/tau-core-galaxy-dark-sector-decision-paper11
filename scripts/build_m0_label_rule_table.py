#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDS = [
    "label_rule_id",
    "family_id",
    "formula_slot",
    "rule_component",
    "source_scope",
    "rule_statement",
    "allowed_values",
    "fallback_policy",
    "exception_policy",
    "frozen_before_scoring",
    "endpoint_scoring_allowed",
    "forbidden_inputs",
    "next_required_artifact",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "label_rule_artifact",
    "family_id",
    "formula_slot",
    "rule_components",
    "activated_rows_covered",
    "row_label_values_written",
    "label_rule_status",
    "endpoint_scoring_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]

NEXT_ARTIFACT = "m1_tau_response_formula_table_v06"
FORBIDDEN_INPUTS = "endpoint_residual;best_fit_curve;family_winner;posthoc_label_switch;heldout_score;numeric_score_value"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def activated_row_count() -> int:
    rows = read_csv(DERIVED / "activated_scoring_rows_v10.csv")
    return sum(row["activation_status"] == "ACTIVATED" for row in rows)


def rule_rows() -> list[dict[str, object]]:
    base = {
        "family_id": "M0",
        "formula_slot": "morphology_label_rule",
        "frozen_before_scoring": "true",
        "endpoint_scoring_allowed": "false",
        "forbidden_inputs": FORBIDDEN_INPUTS,
        "next_required_artifact": NEXT_ARTIFACT,
        "claim_boundary": "m0_label_rule_table_only_no_label_validation_no_scores_no_dark_sector_verdict",
    }
    return [
        {
            **base,
            "label_rule_id": "M0LR06_SOURCE_OBSERVABLES",
            "rule_component": "source_observables",
            "source_scope": "pre_score_source_records_and_reviewed_prescore_label_artifacts",
            "rule_statement": "M0 labels may depend only on source-side morphology/readout records frozen before endpoint scoring.",
            "allowed_values": "source_route_label;morphology_readout_label;baryonic_carrier_label;split_role_label;missing_or_unresolved_label",
            "fallback_policy": "missing_or_unreviewed_source_label_maps_to_M0_LABEL_UNRESOLVED",
            "exception_policy": "record_exception_without_row_drop_or_posthoc_relabel",
        },
        {
            **base,
            "label_rule_id": "M0LR06_LABEL_CATEGORIES",
            "rule_component": "label_categories",
            "source_scope": "activated_scoring_rows_v10_and_source_route_reviews",
            "rule_statement": "The label vocabulary is fixed before scoring and cannot be extended after seeing residuals.",
            "allowed_values": "M0_SOURCE_ROUTE_REVIEWED;M0_BARYONIC_CARRIER_AVAILABLE;M0_LABEL_UNRESOLVED;M0_SPLIT_ROLE_RECORDED",
            "fallback_policy": "unlisted_label_values_are_treated_as_M0_LABEL_UNRESOLVED",
            "exception_policy": "no endpoint-score-conditioned label category may be introduced",
        },
        {
            **base,
            "label_rule_id": "M0LR06_FALLBACK_LABELS",
            "rule_component": "fallback_labels",
            "source_scope": "rows_with_missing_ambiguous_or_unreviewed_label_inputs",
            "rule_statement": "Fallback labels preserve the row and mark unresolved label state without selecting or rescuing a model family.",
            "allowed_values": "M0_LABEL_UNRESOLVED;M0_LABEL_NOT_APPLICABLE;M0_LABEL_REVIEW_PENDING",
            "fallback_policy": "preserve_row_mark_unresolved_keep_endpoint_scoring_disabled",
            "exception_policy": "fallback labels cannot change v_pred_km_s or scoring inclusion",
        },
        {
            **base,
            "label_rule_id": "M0LR06_EXCEPTION_POLICY",
            "rule_component": "exception_policy",
            "source_scope": "all_M0_label_rule_applications",
            "rule_statement": "Exceptions must be explicit source-side audit facts, not post-score edits.",
            "allowed_values": "NO_EXCEPTION;SOURCE_LABEL_MISSING;SOURCE_LABEL_AMBIGUOUS;SOURCE_LABEL_REVIEW_PENDING",
            "fallback_policy": "exception_routes_to_unresolved_label_without_score_activation",
            "exception_policy": "posthoc_label_switch_is_forbidden",
        },
        {
            **base,
            "label_rule_id": "M0LR06_ROW_SELECTOR",
            "rule_component": "row_selector",
            "source_scope": "activated_scoring_rows_v10",
            "rule_statement": "The label rule covers activated scoring rows but does not authorize endpoint scoring or row dropping.",
            "allowed_values": "ACTIVATED_ROW_LABEL_SCOPE;NO_ROW_DROP_BY_LABEL_RULE",
            "fallback_policy": "uncovered_rows_remain_blocked_for_label_review",
            "exception_policy": "row selection cannot depend on heldout score or family winner",
        },
        {
            **base,
            "label_rule_id": "M0LR06_FREEZE_AUDIT",
            "rule_component": "freeze_audit",
            "source_scope": "protocol_manifest_and_reproduction_pipeline",
            "rule_statement": "The label rule table is a frozen pre-scoring contract and carries no empirical label-validation claim.",
            "allowed_values": "RULE_FROZEN_PRE_SCORING;NO_LABEL_VALIDATION_CLAIM;NO_DARK_SECTOR_VERDICT",
            "fallback_policy": "if_rule_changes_then_reproduce_before_scoring",
            "exception_policy": "changes after scoring activation are invalid without a new frozen artifact",
        },
    ]


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "M0_LABEL_RULE_TABLE_V06",
            "label_rule_artifact": "m0_label_rule_table_v06",
            "family_id": "M0",
            "formula_slot": "morphology_label_rule",
            "rule_components": len(rows),
            "activated_rows_covered": activated_row_count(),
            "row_label_values_written": 0,
            "label_rule_status": "M0_LABEL_RULE_TABLE_READY_NO_LABEL_VALUES",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_LABEL_RULE_TABLE_READY_SCORING_BLOCKED",
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": "m0_label_rule_table_only_no_label_validation_no_scores_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_label_rule_table_v06.md").write_text(
        f"""# M0 Label Rule Table v06

**Doc class:** M0 morphology-label rule table
**Status:** label rule ready; no label validation; scoring blocked

Script:

```text
scripts/build_m0_label_rule_table.py
```

Derived outputs:

```text
data/derived/m0_label_rule_table_v06.csv
data/derived/m0_label_rule_table_summary_v06.csv
```

This artifact fills the M0 `morphology_label_rule` formula slot with a frozen
pre-scoring rule table. It defines source-observable scope, label categories,
fallback labels, exception handling, row scope, and freeze audit requirements.

## Current Result

The expected status is:

```text
M0_LABEL_RULE_TABLE_READY_SCORING_BLOCKED
```

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This table defines a label rule only. It writes no row-level label values,
does not validate morphology labels, does not compute endpoint scores, does not
compare M0/M1/M2, and does not decide whether a dark-sector component is
required.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = rule_rows()
    write_csv(DERIVED / "m0_label_rule_table_v06.csv", rows, FIELDS)
    write_csv(DERIVED / "m0_label_rule_table_summary_v06.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER11_M0_LABEL_RULE_TABLE_V06_BUILT")


if __name__ == "__main__":
    main()
