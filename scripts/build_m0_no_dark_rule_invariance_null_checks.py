#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
TERM_GENERATION = DERIVED / "m0_no_dark_rule_term_generation_record_summary_v14.csv"


FIELDNAMES = [
    "check_id",
    "term_record_id",
    "check_class",
    "check_rule",
    "null_behavior",
    "gauge_behavior",
    "fallback_behavior",
    "forbidden_inputs",
    "check_status",
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


def term_generation_ready() -> bool:
    if not TERM_GENERATION.exists():
        return False
    rows = read_csv(TERM_GENERATION)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_RULE_TERM_GENERATION_RECORD_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def check_rows() -> list[dict[str, object]]:
    common_forbidden = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_exception"
    rows = [
        {
            "check_id": "M0NDINC14_INPUT_DOMAIN_NULL_CHECK",
            "term_record_id": "M0NDTG14_INPUT_DOMAIN_TERM",
            "check_class": "input_domain_null_check",
            "check_rule": "input-domain placeholders must vanish or remain inert when required frozen source fields are absent",
            "null_behavior": "null_input_yields_no_prediction_term",
            "gauge_behavior": "source-label relabeling cannot create a new term class",
            "fallback_behavior": "missing domain remains blocked, not imputed from endpoint residuals",
        },
        {
            "check_id": "M0NDINC14_NO_DARK_EXCLUSION_CHECK",
            "term_record_id": "M0NDTG14_NO_DARK_EXCLUSION_TERM",
            "check_class": "family_exclusion_null_check",
            "check_rule": "M0 exclusion flags cannot be converted into compensating dark-response terms",
            "null_behavior": "no_explicit_dark_response_survives_as_absence_constraint",
            "gauge_behavior": "family relabeling cannot reintroduce a hidden response term",
            "fallback_behavior": "violation blocks M0 rather than adding a correction term",
        },
        {
            "check_id": "M0NDINC14_MORPHOLOGY_SOURCE_INVARIANCE_CHECK",
            "term_record_id": "M0NDTG14_MORPHOLOGY_SOURCE_TERM_CLASS",
            "check_class": "morphology_source_invariance_check",
            "check_rule": "morphology/readout source-term classes must be invariant under non-substantive label changes",
            "null_behavior": "absent morphology label yields unresolved source class",
            "gauge_behavior": "null/gauge-equivalent morphology labels cannot create distinct fitted terms",
            "fallback_behavior": "unresolved class is left blocked until admissibility checks are available",
        },
        {
            "check_id": "M0NDINC14_U_READ_INCOMPARABILITY_CHECK",
            "term_record_id": "M0NDTG14_U_READ_ADMISSIBILITY_MARKER",
            "check_class": "u_read_null_gauge_check",
            "check_rule": "finite-local U_read markers preserve incomparability instead of forcing a scalar order",
            "null_behavior": "empty local closure diagnostic yields unresolved marker",
            "gauge_behavior": "gauge-equivalent closure labels share the same admissibility marker",
            "fallback_behavior": "incomparability blocks promotion rather than selecting a best family",
        },
        {
            "check_id": "M0NDINC14_BARYONIC_BINDING_CHECK",
            "term_record_id": "M0NDTG14_BARYONIC_BINDING_TERM_CLASS",
            "check_class": "source_input_binding_check",
            "check_rule": "source-input binding classes cannot introduce fitted normalizations before dimensional precheck",
            "null_behavior": "missing frozen source input leaves binding unresolved",
            "gauge_behavior": "unit-label or source-column relabeling cannot alter binding class identity",
            "fallback_behavior": "unbound inputs remain blocked until dimensional precheck",
        },
        {
            "check_id": "M0NDINC14_FAILURE_ROUTE_CHECK",
            "term_record_id": "M0NDTG14_FAILURE_ROUTE_TERM",
            "check_class": "failure_route_null_check",
            "check_rule": "failure-route markers must dominate post-hoc exception creation",
            "null_behavior": "underdetermined route remains blocked",
            "gauge_behavior": "equivalent failure labels map to the same blocked route",
            "fallback_behavior": "blocked route persists without endpoint-selected exceptions",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["check_status"] = "READY"
        row["source_rule_claim_allowed"] = "false"
        row["expression_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_rule_invariance_null_checks_only_no_expression_no_formula_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["check_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    return [
        {
            "summary_id": "M0_NO_DARK_RULE_INVARIANCE_NULL_CHECKS_V14",
            "check_artifact": "m0_no_dark_rule_invariance_null_checks_v14",
            "term_generation_status": "READY" if term_generation_ready() else "BLOCKED",
            "check_rows": len(rows),
            "ready_check_rows": ready,
            "blocked_check_rows": blocked,
            "source_rule_claim_allowed": "false",
            "expression_claim_allowed": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_RULE_INVARIANCE_NULL_CHECKS_READY"
            if blocked == 0 and term_generation_ready()
            else "M0_NO_DARK_RULE_INVARIANCE_NULL_CHECKS_BLOCKED",
            "next_required_artifact": "m0_no_dark_rule_dimensional_precheck_v14",
            "claim_boundary": "m0_no_dark_rule_invariance_null_checks_only_no_expression_no_formula_no_scores",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_rule_invariance_null_checks_v14.md").write_text(
        """# M0 No-Dark Rule Invariance and Null Checks v14

**Doc class:** no-dark M0 invariance/null check record
**Status:** invariance/null checks ready; dimensional precheck still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_rule_invariance_null_checks.py
```

Derived outputs:

```text
data/derived/m0_no_dark_rule_invariance_null_checks_v14.csv
data/derived/m0_no_dark_rule_invariance_null_checks_summary_v14.csv
```

This artifact records source-side invariance, null, gauge, and fallback checks
for the term classes generated by the M0 no-dark route. It does not define an
expression, assign units, choose coefficients, compute velocities, or score
families.

## Current Result

The expected status is:

```text
M0_NO_DARK_RULE_INVARIANCE_NULL_CHECKS_READY
```

Six check rows are ready:

- input-domain null behavior;
- M0 no-dark exclusion preservation;
- morphology/readout label invariance;
- finite-local `U_read` incomparability preservation;
- frozen source-input binding checks;
- no-promotion failure-route behavior.

The next missing artifact is:

```text
m0_no_dark_rule_dimensional_precheck_v14
```

## Claim Boundary

This check record does not define the M0 no-dark expression, does not perform
dimensional closure, does not write a formula, does not compute predicted
velocities, does not score galaxies, and does not decide the dark-sector
question. It only authorizes the next source-side artifact: a pre-expression
dimensional precheck.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = check_rows()
    write_csv(DERIVED / "m0_no_dark_rule_invariance_null_checks_v14.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_rule_invariance_null_checks_summary_v14.csv",
        summary(rows),
        [
            "summary_id",
            "check_artifact",
            "term_generation_status",
            "check_rows",
            "ready_check_rows",
            "blocked_check_rows",
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
    print("PAPER11_M0_NO_DARK_RULE_INVARIANCE_NULL_CHECKS_V14_BUILT")


if __name__ == "__main__":
    main()
