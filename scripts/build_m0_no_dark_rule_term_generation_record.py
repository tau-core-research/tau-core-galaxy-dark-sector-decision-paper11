#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
SELECTION_MAP = DERIVED / "m0_no_dark_rule_selection_map_summary_v14.csv"


FIELDNAMES = [
    "term_record_id",
    "selection_id",
    "term_class",
    "generated_term_role",
    "generation_rule",
    "allowed_handoff",
    "forbidden_inputs",
    "term_generation_status",
    "source_rule_claim_allowed",
    "expression_claim_allowed",
    "formula_claim_allowed",
    "numeric_prediction_allowed",
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


def selection_map_ready() -> bool:
    if not SELECTION_MAP.exists():
        return False
    rows = read_csv(SELECTION_MAP)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_RULE_SELECTION_MAP_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def term_rows() -> list[dict[str, object]]:
    common_forbidden = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_coefficient"
    rows = [
        {
            "term_record_id": "M0NDTG14_INPUT_DOMAIN_TERM",
            "selection_id": "M0NDRSM14_SOURCE_FREEZE_TO_INPUT_DOMAIN",
            "term_class": "input_domain_term",
            "generated_term_role": "declare the frozen source-field domain available to later expression construction",
            "generation_rule": "generate domain placeholders only from pre-endpoint source-freeze constraints",
            "allowed_handoff": "input_domain_placeholders",
        },
        {
            "term_record_id": "M0NDTG14_NO_DARK_EXCLUSION_TERM",
            "selection_id": "M0NDRSM14_NO_DARK_TO_RESPONSE_EXCLUSION",
            "term_class": "family_exclusion_term",
            "generated_term_role": "carry the M0 no-explicit-dark-response constraint into later admissibility checks",
            "generation_rule": "generate exclusion flags, not compensating response terms",
            "allowed_handoff": "m0_exclusion_flags",
        },
        {
            "term_record_id": "M0NDTG14_MORPHOLOGY_SOURCE_TERM_CLASS",
            "selection_id": "M0NDRSM14_MORPHOLOGY_TO_SOURCE_TERMS",
            "term_class": "morphology_source_term_class",
            "generated_term_role": "declare source-side morphology/readout term classes without coefficients",
            "generation_rule": "generate symbolic source-term classes from declared morphology/readout labels only",
            "allowed_handoff": "symbolic_source_term_classes",
        },
        {
            "term_record_id": "M0NDTG14_U_READ_ADMISSIBILITY_MARKER",
            "selection_id": "M0NDRSM14_U_READ_TO_ADMISSIBILITY_ORDER",
            "term_class": "admissibility_order_marker",
            "generated_term_role": "preserve finite-local U_read ordering for later admissibility filtering",
            "generation_rule": "generate ordering markers and unresolved markers, not scalar fit weights",
            "allowed_handoff": "finite_local_admissibility_markers",
        },
        {
            "term_record_id": "M0NDTG14_BARYONIC_BINDING_TERM_CLASS",
            "selection_id": "M0NDRSM14_BARYONIC_BOUNDARY_TO_BINDINGS",
            "term_class": "source_input_binding_term_class",
            "generated_term_role": "declare which frozen baryonic/source inputs may bind to later dimensional checks",
            "generation_rule": "generate binding classes without fitted normalizations or endpoint-selected powers",
            "allowed_handoff": "source_input_binding_classes",
        },
        {
            "term_record_id": "M0NDTG14_FAILURE_ROUTE_TERM",
            "selection_id": "M0NDRSM14_FAILURE_POLICY_TO_BLOCK_ROUTE",
            "term_class": "failure_route_marker",
            "generated_term_role": "carry the no-promotion route if later checks cannot determine an admissible expression",
            "generation_rule": "generate blocked-route markers instead of post-hoc exception terms",
            "allowed_handoff": "no_promotion_failure_route",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["term_generation_status"] = "READY"
        row["source_rule_claim_allowed"] = "false"
        row["expression_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_rule_term_generation_record_only_no_expression_no_formula_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["term_generation_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    return [
        {
            "summary_id": "M0_NO_DARK_RULE_TERM_GENERATION_RECORD_V14",
            "term_generation_artifact": "m0_no_dark_rule_term_generation_record_v14",
            "selection_map_status": "READY" if selection_map_ready() else "BLOCKED",
            "term_rows": len(rows),
            "ready_term_rows": ready,
            "blocked_term_rows": blocked,
            "source_rule_claim_allowed": "false",
            "expression_claim_allowed": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_RULE_TERM_GENERATION_RECORD_READY"
            if blocked == 0 and selection_map_ready()
            else "M0_NO_DARK_RULE_TERM_GENERATION_RECORD_BLOCKED",
            "next_required_artifact": "m0_no_dark_rule_invariance_null_checks_v14",
            "claim_boundary": "m0_no_dark_rule_term_generation_record_only_no_expression_no_formula_no_scores",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_rule_term_generation_record_v14.md").write_text(
        """# M0 No-Dark Rule Term Generation Record v14

**Doc class:** no-dark M0 term-generation record
**Status:** term-generation record ready; invariance/null checks still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_rule_term_generation_record.py
```

Derived outputs:

```text
data/derived/m0_no_dark_rule_term_generation_record_v14.csv
data/derived/m0_no_dark_rule_term_generation_record_summary_v14.csv
```

This artifact records which source-side term classes may be generated from the
ready rule-selection map before endpoint residuals, held-out scores, family
winners, or best-fit curves are available. It does not choose coefficients,
write equations, compute velocities, or score families.

## Current Result

The expected status is:

```text
M0_NO_DARK_RULE_TERM_GENERATION_RECORD_READY
```

Six term-generation rows are ready:

- input-domain placeholders;
- M0 no-dark exclusion flags;
- morphology/readout symbolic source-term classes;
- finite-local `U_read` admissibility markers;
- frozen source-input binding classes;
- no-promotion failure-route markers.

The next missing artifact is:

```text
m0_no_dark_rule_invariance_null_checks_v14
```

## Claim Boundary

This term-generation record does not define the M0 no-dark expression, does
not choose coefficients, does not perform dimensional closure, does not compute
predicted velocities, does not score galaxies, and does not decide the
dark-sector question. It only authorizes the next source-side artifact:
pre-endpoint invariance, null, gauge, and fallback checks.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = term_rows()
    write_csv(DERIVED / "m0_no_dark_rule_term_generation_record_v14.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_rule_term_generation_record_summary_v14.csv",
        summary(rows),
        [
            "summary_id",
            "term_generation_artifact",
            "selection_map_status",
            "term_rows",
            "ready_term_rows",
            "blocked_term_rows",
            "source_rule_claim_allowed",
            "expression_claim_allowed",
            "formula_claim_allowed",
            "numeric_predictions_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_RULE_TERM_GENERATION_RECORD_V14_BUILT")


if __name__ == "__main__":
    main()
