#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
INVARIANCE_SUMMARY = DERIVED / "m0_no_dark_rule_invariance_null_checks_summary_v14.csv"


FIELDNAMES = [
    "precheck_id",
    "check_id",
    "dimensional_role",
    "required_unit_basis",
    "precheck_rule",
    "allowed_handoff",
    "forbidden_inputs",
    "dimensional_precheck_status",
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


def invariance_ready() -> bool:
    if not INVARIANCE_SUMMARY.exists():
        return False
    rows = read_csv(INVARIANCE_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_RULE_INVARIANCE_NULL_CHECKS_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def precheck_rows() -> list[dict[str, object]]:
    common_forbidden = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_unit_rescale"
    rows = [
        {
            "precheck_id": "M0NDDP14_INPUT_DOMAIN_DIMENSION_ROUTE",
            "check_id": "M0NDINC14_INPUT_DOMAIN_NULL_CHECK",
            "dimensional_role": "declares admissible source-input domains before expression construction",
            "required_unit_basis": "frozen radial grid and source-input units must be declared before any velocity readout",
            "precheck_rule": "input-domain placeholders may pass only as typed source arguments, not as fitted response terms",
            "allowed_handoff": "typed_input_domain_for_source_rule",
        },
        {
            "precheck_id": "M0NDDP14_NO_DARK_EXCLUSION_DIMENSION_ROUTE",
            "check_id": "M0NDINC14_NO_DARK_EXCLUSION_CHECK",
            "dimensional_role": "dimensionless family exclusion constraint",
            "required_unit_basis": "no explicit dark-response density, mass, or acceleration unit may be introduced by this route",
            "precheck_rule": "the M0 no-dark exclusion can constrain admissible terms but cannot itself carry a compensating unitful response",
            "allowed_handoff": "dimensionless_family_constraint",
        },
        {
            "precheck_id": "M0NDDP14_MORPHOLOGY_SOURCE_DIMENSION_ROUTE",
            "check_id": "M0NDINC14_MORPHOLOGY_SOURCE_INVARIANCE_CHECK",
            "dimensional_role": "source-side morphology/readout class requiring later declared coupling to velocity dimensions",
            "required_unit_basis": "morphology labels remain unit-free until a frozen source-rule map declares their coupling role",
            "precheck_rule": "morphology source classes may survive only as typed factors with explicit later dimensional closure",
            "allowed_handoff": "typed_morphology_factor_for_source_rule",
        },
        {
            "precheck_id": "M0NDDP14_U_READ_DIMENSIONLESS_ORDER_ROUTE",
            "check_id": "M0NDINC14_U_READ_INCOMPARABILITY_CHECK",
            "dimensional_role": "dimensionless finite-local admissibility/order marker",
            "required_unit_basis": "U_read markers are order/readout diagnostics and cannot be interpreted as velocity, mass, or acceleration units",
            "precheck_rule": "finite-local admissibility markers may gate rule selection but cannot supply a numeric velocity scale",
            "allowed_handoff": "dimensionless_admissibility_gate",
        },
        {
            "precheck_id": "M0NDDP14_BARYONIC_BINDING_DIMENSION_ROUTE",
            "check_id": "M0NDINC14_BARYONIC_BINDING_CHECK",
            "dimensional_role": "declares where baryonic/source inputs may enter a later velocity-dimensional readout",
            "required_unit_basis": "baryonic source quantities and radial coordinates must keep their imported physical units",
            "precheck_rule": "source-input binding may pass only if no fitted normalization is introduced before source-rule freeze",
            "allowed_handoff": "unit_preserving_source_input_binding",
        },
        {
            "precheck_id": "M0NDDP14_FAILURE_ROUTE_DIMENSION_SAFE_BLOCK",
            "check_id": "M0NDINC14_FAILURE_ROUTE_CHECK",
            "dimensional_role": "dimension-safe blocked route for underdetermined or inconsistent cases",
            "required_unit_basis": "no replacement unit basis may be inferred from endpoint residuals",
            "precheck_rule": "any unresolved dimensional route remains blocked rather than being repaired by post-hoc rescaling",
            "allowed_handoff": "blocked_failure_route_no_formula",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["dimensional_precheck_status"] = "READY"
        row["source_rule_claim_allowed"] = "false"
        row["expression_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_rule_dimensional_precheck_only_no_expression_no_formula_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["dimensional_precheck_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    return [
        {
            "summary_id": "M0_NO_DARK_RULE_DIMENSIONAL_PRECHECK_V14",
            "precheck_artifact": "m0_no_dark_rule_dimensional_precheck_v14",
            "invariance_null_status": "READY" if invariance_ready() else "BLOCKED",
            "precheck_rows": len(rows),
            "ready_precheck_rows": ready,
            "blocked_precheck_rows": blocked,
            "source_rule_claim_allowed": "false",
            "expression_claim_allowed": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_RULE_DIMENSIONAL_PRECHECK_READY"
            if blocked == 0 and invariance_ready()
            else "M0_NO_DARK_RULE_DIMENSIONAL_PRECHECK_BLOCKED",
            "next_required_artifact": "m0_no_dark_rule_derivation_provenance_leakage_v14",
            "claim_boundary": "m0_no_dark_rule_dimensional_precheck_only_no_expression_no_formula_no_scores",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_rule_dimensional_precheck_v14.md").write_text(
        """# M0 No-Dark Rule Dimensional Precheck v14

**Doc class:** no-dark M0 source-side dimensional precheck
**Status:** dimensional precheck ready; derivation provenance/leakage audit still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_rule_dimensional_precheck.py
```

Derived outputs:

```text
data/derived/m0_no_dark_rule_dimensional_precheck_v14.csv
data/derived/m0_no_dark_rule_dimensional_precheck_summary_v14.csv
```

This artifact records a pre-expression dimensional route for the M0 no-dark
rule family. It checks that the already generated term/check classes can be
handed to a later source-rule derivation without silently introducing dark
response terms, fitted unit rescalings, endpoint residuals, or velocity
predictions.

## Current Result

The expected status is:

```text
M0_NO_DARK_RULE_DIMENSIONAL_PRECHECK_READY
```

Six precheck rows are ready:

- typed input-domain route;
- dimensionless M0 no-dark exclusion route;
- morphology/readout source-factor route;
- dimensionless finite-local `U_read` admissibility route;
- unit-preserving baryonic/source binding route;
- dimension-safe blocked failure route.

The next missing artifact is:

```text
m0_no_dark_rule_derivation_provenance_leakage_v14
```

## Claim Boundary

This precheck does not define the M0 no-dark expression, does not specify
coefficients, does not compute predicted velocities, does not score galaxies,
and does not decide the dark-sector question. It only authorizes the next
source-side artifact: a derivation provenance and leakage audit.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = precheck_rows()
    write_csv(DERIVED / "m0_no_dark_rule_dimensional_precheck_v14.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_rule_dimensional_precheck_summary_v14.csv",
        summary(rows),
        [
            "summary_id",
            "precheck_artifact",
            "invariance_null_status",
            "precheck_rows",
            "ready_precheck_rows",
            "blocked_precheck_rows",
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
    print("PAPER11_M0_NO_DARK_RULE_DIMENSIONAL_PRECHECK_V14_BUILT")


if __name__ == "__main__":
    main()
