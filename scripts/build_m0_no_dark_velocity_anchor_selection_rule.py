#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDNAMES = [
    "anchor_selection_check_id",
    "anchor_selection_component",
    "selection_rule_clause",
    "required_condition",
    "observed_status",
    "selection_rule_decision",
    "next_required_artifact",
    "forbidden_inputs",
    "anchor_selection_rule_written",
    "anchor_value_written",
    "velocity_formula_written",
    "numeric_prediction_rows_written",
    "endpoint_scoring_allowed",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def summary_row(path: str) -> dict[str, str]:
    rows = read_csv(DERIVED / path)
    if len(rows) != 1:
        raise ValueError(f"expected one summary row in {path}")
    return rows[0]


def selection_rule_rows() -> list[dict[str, object]]:
    candidate_basis = summary_row("m0_no_dark_velocity_anchor_candidate_basis_summary_v08.csv")
    dimensional_trace = summary_row("m0_no_dark_payload_dimensional_trace_summary_v12.csv")
    leakage_certificate = summary_row("m0_no_dark_payload_leakage_certificate_summary_v12.csv")
    provenance_audit = summary_row("source_import_provenance_audit_summary_v20.csv")
    common_forbidden = (
        "vobs;endpoint_residual;heldout_score;family_winner;best_fit_curve;"
        "posthoc_unit_rescale;posthoc_coefficient_fit;posthoc_anchor_choice;"
        "posthoc_selection_rule"
    )
    rows = [
        {
            "anchor_selection_check_id": "M0NDVASR08_CANDIDATE_BASIS_HANDOFF",
            "anchor_selection_component": "candidate_basis_handoff",
            "selection_rule_clause": "accept only the candidate classes declared by the candidate-basis gate",
            "required_condition": "candidate-basis gate is present and identifies selection rule as the next blocker",
            "observed_status": candidate_basis["overall_status"],
            "selection_rule_decision": "READY_FOR_ANCHOR_SELECTION_RULE_REVIEW",
            "next_required_artifact": "m0_no_dark_velocity_anchor_value_freeze_v08",
        },
        {
            "anchor_selection_check_id": "M0NDVASR08_PRIORITY_ORDER",
            "anchor_selection_component": "priority_order",
            "selection_rule_clause": "prefer source_side_baryonic_gravity_velocity_carrier, then source_side_dimensioned_field_carrier, then independent_imported_source_scale_carrier",
            "required_condition": "selection order must be declared before scoring and independent of endpoint fit quality",
            "observed_status": dimensional_trace["overall_status"],
            "selection_rule_decision": "ANCHOR_SELECTION_PRIORITY_RULE_DECLARED",
            "next_required_artifact": "m0_no_dark_velocity_anchor_value_freeze_v08",
        },
        {
            "anchor_selection_check_id": "M0NDVASR08_FALLBACK_RULE",
            "anchor_selection_component": "fallback_rule",
            "selection_rule_clause": "fall back only when the higher-priority class is absent, unprovenanced, dimensionally invalid, or leakage-blocked",
            "required_condition": "fallbacks must be source-side failures, not score-improving substitutions",
            "observed_status": leakage_certificate["overall_status"],
            "selection_rule_decision": "ANCHOR_SELECTION_FALLBACK_RULE_DECLARED",
            "next_required_artifact": "m0_no_dark_velocity_anchor_value_freeze_v08",
        },
        {
            "anchor_selection_check_id": "M0NDVASR08_PROVENANCE_RULE",
            "anchor_selection_component": "provenance_rule",
            "selection_rule_clause": "selected anchor class must have pre-scoring provenance before any value is frozen",
            "required_condition": "selection cannot use imported values unless provenance audit remains non-endpoint-derived",
            "observed_status": provenance_audit["overall_status"],
            "selection_rule_decision": "ANCHOR_SELECTION_PROVENANCE_RULE_DECLARED",
            "next_required_artifact": "m0_no_dark_velocity_anchor_value_freeze_v08",
        },
        {
            "anchor_selection_check_id": "M0NDVASR08_REJECTION_RULE",
            "anchor_selection_component": "rejection_rule",
            "selection_rule_clause": "reject observed_rotation_or_residual_fit_carrier under all M0 no-dark scoring paths",
            "required_condition": "rotation-fitted anchors must remain inadmissible even if they improve scoring",
            "observed_status": "ROTATION_FIT_CARRIER_REJECTED_BY_CANDIDATE_BASIS",
            "selection_rule_decision": "ANCHOR_SELECTION_REJECTION_RULE_DECLARED",
            "next_required_artifact": "m0_no_dark_velocity_anchor_value_freeze_v08",
        },
        {
            "anchor_selection_check_id": "M0NDVASR08_VALUE_FREEZE",
            "anchor_selection_component": "anchor_value_freeze",
            "selection_rule_clause": "freeze concrete anchor source/value only in a later pre-scoring artifact",
            "required_condition": "a selected anchor class still needs a value-freeze gate before a velocity formula can be written",
            "observed_status": "NO_VELOCITY_ANCHOR_VALUE_FREEZE_PRESENT",
            "selection_rule_decision": "BLOCKED_ANCHOR_VALUE_FREEZE_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_value_freeze_v08",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["anchor_selection_rule_written"] = "true"
        row["anchor_value_written"] = "false"
        row["velocity_formula_written"] = "false"
        row["numeric_prediction_rows_written"] = 0
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_velocity_anchor_selection_rule_gate_only_no_anchor_value_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked = sum(str(row["selection_rule_decision"]).startswith("BLOCKED") for row in rows)
    declared = sum(str(row["selection_rule_decision"]).endswith("_DECLARED") for row in rows)
    return [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_ANCHOR_SELECTION_RULE_V08",
            "anchor_selection_rule_artifact": "m0_no_dark_velocity_anchor_selection_rule_v08",
            "selection_rule_checks": len(rows),
            "declared_selection_rule_clauses": declared,
            "blocked_selection_rule_checks": blocked,
            "anchor_selection_rule_written": "true",
            "anchor_value_written": "false",
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": 0,
            "families_with_numeric_predictions": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_ANCHOR_SELECTION_RULE_PRESENT_BLOCKED_ANCHOR_VALUE_FREEZE_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_value_freeze_v08",
            "claim_boundary": "m0_no_dark_velocity_anchor_selection_rule_gate_only_no_anchor_value_no_velocity_formula_no_predictions_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_velocity_anchor_selection_rule_v08.md").write_text(
        """# M0 No-Dark Velocity-Anchor Selection Rule v08

**Doc class:** velocity-anchor selection-rule gate
**Status:** selection rule present; anchor value freeze missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_anchor_selection_rule.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_anchor_selection_rule_v08.csv
data/derived/m0_no_dark_velocity_anchor_selection_rule_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_anchor_selection_rule_v08`
presence blocker by declaring a pre-scoring priority and fallback rule over the
admissible anchor classes. The rule prefers source-side baryonic gravitational
velocity/acceleration carriers, then source-side dimensioned field carriers,
then independently imported source-scale carriers when provenance and leakage
guards allow them. It rejects observed-rotation or residual-fit carriers under
all M0 no-dark scoring paths.

The rule does not freeze a concrete anchor value. That remains the next
required gate.

## Current Result

The expected status is:

```text
M0_NO_DARK_ANCHOR_SELECTION_RULE_PRESENT_BLOCKED_ANCHOR_VALUE_FREEZE_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_anchor_value_freeze_v08
```

## Claim Boundary

This gate declares only the pre-scoring selection rule over candidate classes. It does not freeze an anchor value, does not assign coupling normalization, does not write a velocity formula, does not write prediction rows, does not run endpoint scoring, and does not decide whether a dark-sector component is required.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = selection_rule_rows()
    write_csv(DERIVED / "m0_no_dark_velocity_anchor_selection_rule_v08.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_velocity_anchor_selection_rule_summary_v08.csv",
        summary(rows),
        [
            "summary_id",
            "anchor_selection_rule_artifact",
            "selection_rule_checks",
            "declared_selection_rule_clauses",
            "blocked_selection_rule_checks",
            "anchor_selection_rule_written",
            "anchor_value_written",
            "velocity_formula_written",
            "numeric_prediction_rows_written",
            "families_with_numeric_predictions",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_VELOCITY_ANCHOR_SELECTION_RULE_V08_BUILT")


if __name__ == "__main__":
    main()
