#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
PARENT_BASIS = DERIVED / "m0_no_dark_rule_parent_assumption_basis_summary_v14.csv"


FIELDNAMES = [
    "selection_id",
    "source_basis_id",
    "selection_class",
    "candidate_rule_role",
    "selection_rule",
    "allowed_output",
    "forbidden_inputs",
    "selection_status",
    "source_rule_claim_allowed",
    "expression_claim_allowed",
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


def parent_basis_ready() -> bool:
    if not PARENT_BASIS.exists():
        return False
    rows = read_csv(PARENT_BASIS)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_RULE_PARENT_ASSUMPTION_BASIS_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def selection_rows() -> list[dict[str, object]]:
    common_forbidden = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_term_selection"
    rows = [
        {
            "selection_id": "M0NDRSM14_SOURCE_FREEZE_TO_INPUT_DOMAIN",
            "source_basis_id": "M0NDPB14_SOURCE_FREEZE",
            "selection_class": "input_domain_selection",
            "candidate_rule_role": "freeze pre-endpoint source fields before expression construction",
            "selection_rule": "source-freeze basis can select input-domain constraints only",
            "allowed_output": "input_domain_constraint",
        },
        {
            "selection_id": "M0NDRSM14_NO_DARK_TO_RESPONSE_EXCLUSION",
            "source_basis_id": "M0NDPB14_NO_DARK_RESPONSE_EXCLUSION",
            "selection_class": "family_exclusion_selection",
            "candidate_rule_role": "exclude explicit Tau-dark-sector response terms from the M0 candidate family",
            "selection_rule": "no-dark response exclusion can select only M0-family exclusion constraints",
            "allowed_output": "m0_family_exclusion_constraint",
        },
        {
            "selection_id": "M0NDRSM14_MORPHOLOGY_TO_SOURCE_TERMS",
            "source_basis_id": "M0NDPB14_MORPHOLOGY_READOUT",
            "selection_class": "source_term_selection",
            "candidate_rule_role": "route declared morphology/readout labels to later source-term generation",
            "selection_rule": "morphology/readout basis can select source-term classes but not coefficients or fitted curves",
            "allowed_output": "source_term_class_candidates",
        },
        {
            "selection_id": "M0NDRSM14_U_READ_TO_ADMISSIBILITY_ORDER",
            "source_basis_id": "M0NDPB14_LOCAL_CLOSURE_DIAGNOSTIC",
            "selection_class": "admissibility_order_selection",
            "candidate_rule_role": "use restricted local U_read only to order admissibility candidates",
            "selection_rule": "local closure diagnostic can select a finite-local admissibility order, with incomparable cases left unresolved",
            "allowed_output": "finite_local_admissibility_order",
        },
        {
            "selection_id": "M0NDRSM14_BARYONIC_BOUNDARY_TO_BINDINGS",
            "source_basis_id": "M0NDPB14_BARYONIC_INPUT_BOUNDARY",
            "selection_class": "input_binding_selection",
            "candidate_rule_role": "route frozen baryonic/source inputs to later dimensional binding checks",
            "selection_rule": "baryonic input boundary can select source-input bindings but not fitted normalizations",
            "allowed_output": "source_input_binding_candidates",
        },
        {
            "selection_id": "M0NDRSM14_FAILURE_POLICY_TO_BLOCK_ROUTE",
            "source_basis_id": "M0NDPB14_FAILURE_POLICY",
            "selection_class": "failure_route_selection",
            "candidate_rule_role": "preserve blocked status if later term generation is underdetermined",
            "selection_rule": "failure policy selects a no-promotion route rather than adding post-hoc exceptions",
            "allowed_output": "blocked_without_posthoc_terms_route",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["selection_status"] = "READY"
        row["source_rule_claim_allowed"] = "false"
        row["expression_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_rule_selection_map_only_no_terms_no_formula_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["selection_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    return [
        {
            "summary_id": "M0_NO_DARK_RULE_SELECTION_MAP_V14",
            "selection_artifact": "m0_no_dark_rule_selection_map_v14",
            "parent_basis_status": "READY" if parent_basis_ready() else "BLOCKED",
            "selection_rows": len(rows),
            "ready_selection_rows": ready,
            "blocked_selection_rows": blocked,
            "source_rule_claim_allowed": "false",
            "expression_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_RULE_SELECTION_MAP_READY"
            if blocked == 0 and parent_basis_ready()
            else "M0_NO_DARK_RULE_SELECTION_MAP_BLOCKED",
            "next_required_artifact": "m0_no_dark_rule_term_generation_record_v14",
            "claim_boundary": "m0_no_dark_rule_selection_map_only_no_terms_no_formula_no_scores",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_rule_selection_map_v14.md").write_text(
        """# M0 No-Dark Rule Selection Map v14

**Doc class:** no-dark M0 rule-selection map
**Status:** rule-selection map ready; term-generation record still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_rule_selection_map.py
```

Derived outputs:

```text
data/derived/m0_no_dark_rule_selection_map_v14.csv
data/derived/m0_no_dark_rule_selection_map_summary_v14.csv
```

This artifact maps the ready v14 parent-basis rows to pre-endpoint rule roles.
It does not generate expression terms, choose coefficients, define a velocity
formula, or compare candidate families.

## Current Result

The expected status is:

```text
M0_NO_DARK_RULE_SELECTION_MAP_READY
```

Six selection rows are ready:

- source-freeze basis to input-domain constraints;
- no-dark response exclusion to M0-family exclusion constraints;
- morphology/readout basis to source-term classes;
- restricted local `U_read` basis to finite-local admissibility ordering;
- baryonic/source boundary to input-binding candidates;
- failure policy to a no-promotion blocked route.

The next missing artifact is:

```text
m0_no_dark_rule_term_generation_record_v14
```

## Claim Boundary

This selection map does not derive the M0 no-dark expression, does not generate
terms, does not define a formula, does not compute predicted velocities, does
not score galaxies, and does not decide the dark-sector question. It only
authorizes the next source-side artifact: a pre-endpoint term-generation
record.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = selection_rows()
    write_csv(DERIVED / "m0_no_dark_rule_selection_map_v14.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_rule_selection_map_summary_v14.csv",
        summary(rows),
        [
            "summary_id",
            "selection_artifact",
            "parent_basis_status",
            "selection_rows",
            "ready_selection_rows",
            "blocked_selection_rows",
            "source_rule_claim_allowed",
            "expression_claim_allowed",
            "numeric_predictions_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_RULE_SELECTION_MAP_V14_BUILT")


if __name__ == "__main__":
    main()
