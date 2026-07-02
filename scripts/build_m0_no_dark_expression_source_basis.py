#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
DERIVATION_CONTRACT_SUMMARY = DERIVED / "m0_no_dark_expression_rule_derivation_contract_summary_v13.csv"


FIELDNAMES = [
    "basis_id",
    "parent_basis_id",
    "basis_class",
    "source_basis_role",
    "allowed_source_basis_element",
    "allowed_handoff",
    "forbidden_inputs",
    "basis_status",
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


def derivation_contract_ready() -> bool:
    if not DERIVATION_CONTRACT_SUMMARY.exists():
        return False
    rows = read_csv(DERIVATION_CONTRACT_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_EXPRESSION_RULE_DERIVATION_READY_FOR_SOURCE_BASIS"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def basis_rows() -> list[dict[str, object]]:
    common_forbidden = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_label_switch"
    rows = [
        {
            "basis_id": "M0NDESB13_SOURCE_FREEZE_BASIS",
            "parent_basis_id": "M0NDPB14_SOURCE_FREEZE",
            "basis_class": "source_freeze_basis",
            "source_basis_role": "declares frozen source-side input domain for later rule construction",
            "allowed_source_basis_element": "typed_frozen_source_domain",
            "allowed_handoff": "source_rule_input_domain",
        },
        {
            "basis_id": "M0NDESB13_NO_DARK_EXCLUSION_BASIS",
            "parent_basis_id": "M0NDPB14_NO_DARK_RESPONSE_EXCLUSION",
            "basis_class": "no_dark_exclusion_basis",
            "source_basis_role": "declares no explicit dark-response term as a source-side family constraint",
            "allowed_source_basis_element": "dimensionless_no_dark_family_constraint",
            "allowed_handoff": "source_rule_family_constraint",
        },
        {
            "basis_id": "M0NDESB13_MORPHOLOGY_READOUT_BASIS",
            "parent_basis_id": "M0NDPB14_MORPHOLOGY_READOUT",
            "basis_class": "morphology_readout_basis",
            "source_basis_role": "declares morphology/readout factors available before expression construction",
            "allowed_source_basis_element": "typed_morphology_readout_factor",
            "allowed_handoff": "source_rule_morphology_factor",
        },
        {
            "basis_id": "M0NDESB13_U_READ_ADMISSIBILITY_BASIS",
            "parent_basis_id": "M0NDPB14_LOCAL_CLOSURE_DIAGNOSTIC",
            "basis_class": "u_read_admissibility_basis",
            "source_basis_role": "declares finite-local U_read as an admissibility marker rather than a fitted scale",
            "allowed_source_basis_element": "dimensionless_u_read_admissibility_marker",
            "allowed_handoff": "admissibility_rule_marker",
        },
        {
            "basis_id": "M0NDESB13_BARYONIC_BINDING_BASIS",
            "parent_basis_id": "M0NDPB14_BARYONIC_INPUT_BOUNDARY",
            "basis_class": "baryonic_binding_basis",
            "source_basis_role": "declares unit-preserving baryonic/source input bindings for later expression construction",
            "allowed_source_basis_element": "unit_preserving_baryonic_source_binding",
            "allowed_handoff": "source_rule_input_binding",
        },
        {
            "basis_id": "M0NDESB13_FAILURE_ROUTE_BASIS",
            "parent_basis_id": "M0NDPB14_FAILURE_POLICY",
            "basis_class": "failure_route_basis",
            "source_basis_role": "declares blocked route behavior for unresolved or inconsistent source-basis cases",
            "allowed_source_basis_element": "blocked_failure_route_marker",
            "allowed_handoff": "null_fallback_policy_route",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["basis_status"] = "READY"
        row["source_rule_claim_allowed"] = "false"
        row["expression_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_expression_source_basis_only_no_rule_no_formula_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["basis_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    return [
        {
            "summary_id": "M0_NO_DARK_EXPRESSION_SOURCE_BASIS_V13",
            "source_basis_artifact": "m0_no_dark_expression_source_basis_v13",
            "derivation_contract_status": "READY" if derivation_contract_ready() else "BLOCKED",
            "basis_rows": len(rows),
            "ready_basis_rows": ready,
            "blocked_basis_rows": blocked,
            "source_rule_claim_allowed": "false",
            "expression_claim_allowed": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EXPRESSION_SOURCE_BASIS_READY"
            if blocked == 0 and derivation_contract_ready()
            else "M0_NO_DARK_EXPRESSION_SOURCE_BASIS_BLOCKED",
            "next_required_artifact": "m0_no_dark_expression_admissibility_rule_v13",
            "claim_boundary": "m0_no_dark_expression_source_basis_only_no_rule_no_formula_no_scores",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_expression_source_basis_v13.md").write_text(
        """# M0 No-Dark Expression Source Basis v13

**Doc class:** no-dark M0 expression source-basis record
**Status:** source basis ready; admissibility rule still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_expression_source_basis.py
```

Derived outputs:

```text
data/derived/m0_no_dark_expression_source_basis_v13.csv
data/derived/m0_no_dark_expression_source_basis_summary_v13.csv
```

This artifact records the typed source-side basis elements that may be handed to
a later no-dark M0 source-rule construction. It does not choose coefficients,
write an expression, compute velocities, or score any galaxy.

## Current Result

The expected status is:

```text
M0_NO_DARK_EXPRESSION_SOURCE_BASIS_READY
```

Six source-basis rows are ready:

- frozen source-domain basis;
- dimensionless no-dark family constraint;
- morphology/readout source factor;
- dimensionless finite-local `U_read` admissibility marker;
- unit-preserving baryonic/source binding;
- blocked failure-route marker.

The next missing artifact is:

```text
m0_no_dark_expression_admissibility_rule_v13
```

## Claim Boundary

This source-basis record does not define the M0 no-dark source rule, does not
define an expression, does not write a formula, does not compute predicted
velocities, does not score galaxies, and does not decide the dark-sector
question. It only authorizes the next source-side construction artifact: the
admissibility rule.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = basis_rows()
    write_csv(DERIVED / "m0_no_dark_expression_source_basis_v13.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_expression_source_basis_summary_v13.csv",
        summary(rows),
        [
            "summary_id",
            "source_basis_artifact",
            "derivation_contract_status",
            "basis_rows",
            "ready_basis_rows",
            "blocked_basis_rows",
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
    print("PAPER11_M0_NO_DARK_EXPRESSION_SOURCE_BASIS_V13_BUILT")


if __name__ == "__main__":
    main()
