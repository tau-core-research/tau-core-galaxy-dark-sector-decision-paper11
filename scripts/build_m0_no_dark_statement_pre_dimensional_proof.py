#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
CONSTRAINT_GUARDS_SUMMARY = DERIVED / "m0_no_dark_statement_constraint_guards_summary_v13.csv"
STATEMENT_CONTRACT_SUMMARY = DERIVED / "m0_no_dark_frozen_expression_statement_summary_v12.csv"


FIELDNAMES = [
    "proof_step_id",
    "proof_step_class",
    "proof_role",
    "required_condition",
    "blocked_operation",
    "completion_status",
    "next_required_artifact",
    "forbidden_inputs",
    "proof_claim_allowed",
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


def constraint_guards_ready() -> bool:
    if not CONSTRAINT_GUARDS_SUMMARY.exists() or not STATEMENT_CONTRACT_SUMMARY.exists():
        return False
    guards = read_csv(CONSTRAINT_GUARDS_SUMMARY)
    contract = read_csv(STATEMENT_CONTRACT_SUMMARY)
    return (
        len(guards) == 1
        and guards[0]["overall_status"] == "M0_NO_DARK_STATEMENT_CONSTRAINT_GUARDS_READY_FOR_PRE_DIMENSIONAL_PROOF"
        and guards[0]["endpoint_scoring_allowed_anywhere"] == "false"
        and len(contract) == 1
        and contract[0]["overall_status"]
        in {
            "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_PRE_DIMENSIONAL_PROOF_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_FREEZE_PROVENANCE_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_FOR_PAYLOAD",
        }
        and contract[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def proof_rows() -> list[dict[str, object]]:
    rows = [
        {
            "proof_step_id": "M0NDSPDP13_OUTPUT_CLASS_ROUTE",
            "proof_step_class": "output_class_route",
            "proof_role": "declare the intended output class before any algebraic formula body is written",
            "required_condition": "the route targets a later velocity-readout output class without defining its formula",
            "blocked_operation": "claiming a velocity formula or physical readout from the route alone",
        },
        {
            "proof_step_id": "M0NDSPDP13_ARGUMENT_DIMENSION_PLACEHOLDERS",
            "proof_step_class": "argument_dimension_placeholders",
            "proof_role": "attach source-side dimension placeholders to every declared argument slot",
            "required_condition": "source-state, baryonic, radius-grid, readout, guard, and assembly slots have pre-score dimension labels",
            "blocked_operation": "adding a missing unit label after endpoint residuals or family comparison",
        },
        {
            "proof_step_id": "M0NDSPDP13_OPERATOR_DIMENSION_RULE",
            "proof_step_class": "operator_dimension_rule",
            "proof_role": "require readout and assembly operators to carry an explicit dimensional mapping rule",
            "required_condition": "operator mappings are declared as obligations for the later formula body",
            "blocked_operation": "letting the later formula repair dimensional mismatch by fitted coefficients",
        },
        {
            "proof_step_id": "M0NDSPDP13_GUARD_DIMENSION_POLICY",
            "proof_step_class": "guard_dimension_policy",
            "proof_role": "prevent null, gauge, no-dark, and fallback guards from serving as unit fixes",
            "required_condition": "guards may block or route a statement but cannot change the target output dimension",
            "blocked_operation": "using a guard choice as a hidden dimensional rescaling",
        },
        {
            "proof_step_id": "M0NDSPDP13_NO_POSTHOC_UNIT_RESCALING",
            "proof_step_class": "no_posthoc_unit_rescaling",
            "proof_role": "forbid endpoint-driven unit rescaling before formula-body work starts",
            "required_condition": "all later scale choices must be source-side or provenance-frozen before scoring",
            "blocked_operation": "choosing units, scales, or normalizations from best-fit behavior",
        },
        {
            "proof_step_id": "M0NDSPDP13_HANDOFF_TO_FREEZE_PROVENANCE",
            "proof_step_class": "freeze_provenance_handoff",
            "proof_role": "handoff the pre-dimensional route to provenance freeze before formula construction",
            "required_condition": "the next artifact must record that the route was fixed before scoring access",
            "blocked_operation": "moving directly from dimensional route to scoring or dark-sector verdict",
        },
    ]
    for row in rows:
        row["completion_status"] = "READY"
        row["next_required_artifact"] = "m0_no_dark_statement_freeze_provenance_v13"
        row["forbidden_inputs"] = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_unit_rescale"
        row["proof_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_statement_pre_dimensional_proof_only_route_no_formula_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["completion_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    upstream_ready = constraint_guards_ready()
    return [
        {
            "summary_id": "M0_NO_DARK_STATEMENT_PRE_DIMENSIONAL_PROOF_V13",
            "pre_dimensional_proof_artifact": "m0_no_dark_statement_pre_dimensional_proof_v13",
            "constraint_guards_status": "READY" if upstream_ready else "BLOCKED",
            "proof_rows": len(rows),
            "ready_proof_rows": ready,
            "blocked_proof_rows": blocked,
            "pre_dimensional_proof_written": "true" if upstream_ready and blocked == 0 else "false",
            "formula_body_written": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_STATEMENT_PRE_DIMENSIONAL_PROOF_READY_FOR_FREEZE_PROVENANCE"
            if upstream_ready and blocked == 0
            else "M0_NO_DARK_STATEMENT_PRE_DIMENSIONAL_PROOF_BLOCKED",
            "next_required_artifact": "m0_no_dark_statement_freeze_provenance_v13",
            "claim_boundary": "m0_no_dark_statement_pre_dimensional_proof_only_route_no_formula_no_scores_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_statement_pre_dimensional_proof_v13.md").write_text(
        """# M0 No-Dark Statement Pre-Dimensional Proof v13

**Doc class:** no-dark M0 pre-dimensional proof-route contract
**Status:** pre-dimensional route ready; freeze provenance blocked; no formula; no scoring

Script:

```text
scripts/build_m0_no_dark_statement_pre_dimensional_proof.py
```

Derived outputs:

```text
data/derived/m0_no_dark_statement_pre_dimensional_proof_v13.csv
data/derived/m0_no_dark_statement_pre_dimensional_proof_summary_v13.csv
```

This artifact records the pre-dimensional proof route for the M0 no-dark
statement. It does not provide a formula body. It only states the obligations
that must be frozen before a later formula can claim dimensional admissibility.

## Current Result

The expected status is:

```text
M0_NO_DARK_STATEMENT_PRE_DIMENSIONAL_PROOF_READY_FOR_FREEZE_PROVENANCE
```

The next missing artifact is:

```text
m0_no_dark_statement_freeze_provenance_v13
```

## Claim Boundary

This pre-dimensional route does not define a velocity formula, does not assign
coefficients, does not compute predictions, does not score galaxies, and does
not decide the dark-sector question. It only blocks posthoc dimensional repair
before freeze-provenance and formula-body work.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = proof_rows()
    write_csv(DERIVED / "m0_no_dark_statement_pre_dimensional_proof_v13.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_statement_pre_dimensional_proof_summary_v13.csv",
        summary(rows),
        [
            "summary_id",
            "pre_dimensional_proof_artifact",
            "constraint_guards_status",
            "proof_rows",
            "ready_proof_rows",
            "blocked_proof_rows",
            "pre_dimensional_proof_written",
            "formula_body_written",
            "formula_claim_allowed",
            "numeric_predictions_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_STATEMENT_PRE_DIMENSIONAL_PROOF_V13_BUILT")


if __name__ == "__main__":
    main()
