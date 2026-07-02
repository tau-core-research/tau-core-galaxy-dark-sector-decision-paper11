#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDNAMES = [
    "basis_id",
    "basis_class",
    "parent_assumption",
    "allowed_use",
    "forbidden_inputs",
    "basis_status",
    "endpoint_scoring_allowed",
    "source_rule_claim_allowed",
    "expression_claim_allowed",
    "numeric_prediction_allowed",
    "claim_boundary",
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def basis_rows() -> list[dict[str, object]]:
    common_forbidden = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_formula_switch"
    rows = [
        {
            "basis_id": "M0NDPB14_SOURCE_FREEZE",
            "basis_class": "source_freeze_boundary",
            "parent_assumption": "M0 no-dark rule construction must use only source-side assumptions frozen before endpoint scoring.",
            "allowed_use": "declare the pre-endpoint construction boundary for later rule-selection work",
        },
        {
            "basis_id": "M0NDPB14_NO_DARK_RESPONSE_EXCLUSION",
            "basis_class": "family_boundary",
            "parent_assumption": "The M0 family excludes an explicit Tau-dark-sector response term while still allowing source-side morphology/readout structure.",
            "allowed_use": "separate the no-dark source-rule path from later M1/M2 dark-sector response paths",
        },
        {
            "basis_id": "M0NDPB14_MORPHOLOGY_READOUT",
            "basis_class": "morphology_readout_basis",
            "parent_assumption": "Source-side morphology and readout labels may constrain a no-dark candidate rule only through declared pre-score fields.",
            "allowed_use": "provide admissible source categories for a later rule-selection map",
        },
        {
            "basis_id": "M0NDPB14_LOCAL_CLOSURE_DIAGNOSTIC",
            "basis_class": "local_scoring_anchor_basis",
            "parent_assumption": "The restricted local U_read closure-defect diagnostic may rank source-side admissibility only as a finite-local order primitive.",
            "allowed_use": "anchor later source-rule prioritization without promoting a physical readout claim",
        },
        {
            "basis_id": "M0NDPB14_BARYONIC_INPUT_BOUNDARY",
            "basis_class": "input_boundary",
            "parent_assumption": "Baryonic/source inputs must come from frozen source-import tables and cannot be tuned from endpoint residuals.",
            "allowed_use": "constrain later input binding and dimensional precheck records",
        },
        {
            "basis_id": "M0NDPB14_FAILURE_POLICY",
            "basis_class": "failure_boundary",
            "parent_assumption": "If the assumptions do not determine a rule-selection map, the M0 path remains blocked instead of adding post-hoc terms.",
            "allowed_use": "preserve a non-circular failure route for later derivation slots",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["basis_status"] = "READY"
        row["endpoint_scoring_allowed"] = "false"
        row["source_rule_claim_allowed"] = "false"
        row["expression_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_rule_parent_assumption_basis_only_no_rule_no_predictions_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["basis_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    return [
        {
            "summary_id": "M0_NO_DARK_RULE_PARENT_ASSUMPTION_BASIS_V14",
            "basis_artifact": "m0_no_dark_rule_parent_assumption_basis_v14",
            "basis_rows": len(rows),
            "ready_basis_rows": ready,
            "blocked_basis_rows": blocked,
            "source_rule_claim_allowed": "false",
            "expression_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_RULE_PARENT_ASSUMPTION_BASIS_READY"
            if blocked == 0
            else "M0_NO_DARK_RULE_PARENT_ASSUMPTION_BASIS_BLOCKED",
            "next_required_artifact": "m0_no_dark_rule_selection_map_v14",
            "claim_boundary": "m0_no_dark_rule_parent_assumption_basis_only_no_rule_no_predictions_no_scores",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_rule_parent_assumption_basis_v14.md").write_text(
        """# M0 No-Dark Rule Parent Assumption Basis v14

**Doc class:** no-dark M0 parent-assumption basis
**Status:** parent basis ready; rule-selection map still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_rule_parent_assumption_basis.py
```

Derived outputs:

```text
data/derived/m0_no_dark_rule_parent_assumption_basis_v14.csv
data/derived/m0_no_dark_rule_parent_assumption_basis_summary_v14.csv
```

This artifact closes only the first source-side prerequisite in the M0 no-dark
rule-derivation chain. It records the parent assumptions that a later
rule-selection map may use before endpoint residuals, held-out scores, family
winners, or best-fit curves are available.

## Current Result

The expected status is:

```text
M0_NO_DARK_RULE_PARENT_ASSUMPTION_BASIS_READY
```

Six parent-basis rows are ready:

- source-freeze boundary;
- no-dark response exclusion for the M0 family;
- morphology/readout source basis;
- restricted local `U_read` closure-diagnostic basis;
- baryonic/source input boundary;
- non-circular failure policy.

The next missing artifact is:

```text
m0_no_dark_rule_selection_map_v14
```

## Claim Boundary

This basis does not derive the M0 no-dark rule, does not choose a formula, does
not generate terms, does not compute predicted velocities, does not score
galaxies, and does not decide the dark-sector question. It only authorizes the
next source-side artifact: a pre-endpoint rule-selection map.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = basis_rows()
    write_csv(DERIVED / "m0_no_dark_rule_parent_assumption_basis_v14.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_rule_parent_assumption_basis_summary_v14.csv",
        summary(rows),
        [
            "summary_id",
            "basis_artifact",
            "basis_rows",
            "ready_basis_rows",
            "blocked_basis_rows",
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
    print("PAPER11_M0_NO_DARK_RULE_PARENT_ASSUMPTION_BASIS_V14_BUILT")


if __name__ == "__main__":
    main()
