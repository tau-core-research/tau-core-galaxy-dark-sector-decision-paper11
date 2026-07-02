#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
PAYLOAD_SUMMARY = DERIVED / "m0_no_dark_frozen_expression_payload_summary_v11.csv"


FIELDNAMES = [
    "body_row_id",
    "body_component",
    "body_role",
    "frozen_expression_body_statement",
    "allowed_interpretation",
    "blocked_interpretation",
    "completion_status",
    "next_required_artifact",
    "forbidden_inputs",
    "expression_body_claim_allowed",
    "velocity_formula_claim_allowed",
    "numeric_prediction_allowed",
    "endpoint_scoring_allowed",
    "dark_sector_verdict_allowed",
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


def payload_ready() -> bool:
    if not PAYLOAD_SUMMARY.exists():
        return False
    rows = read_csv(PAYLOAD_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_READY_FOR_KERNEL_EXPRESSION"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def body_rows() -> list[dict[str, object]]:
    status = "READY" if payload_ready() else "BLOCKED_PAYLOAD_NOT_READY"
    common_forbidden = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_expression_switch"
    rows = [
        {
            "body_row_id": "M0NDFEB14_SCOPE",
            "body_component": "scope_and_family_binding",
            "body_role": "bind the expression body to the M0 no-dark family",
            "frozen_expression_body_statement": "E_M0 is a source-side no-dark readout body, not a dark-sector response and not an endpoint-fitted correction",
            "allowed_interpretation": "definition-level M0 expression-body envelope",
            "blocked_interpretation": "empirical claim that no dark sector is required",
        },
        {
            "body_row_id": "M0NDFEB14_ARGUMENT_VECTOR",
            "body_component": "argument_vector",
            "body_role": "declare the only admissible body arguments",
            "frozen_expression_body_statement": "X_M0 = (source_state, baryonic_input, radius_grid, readout_operator, guard_state, assembly_order)",
            "allowed_interpretation": "argument contract inherited from frozen source-side gates",
            "blocked_interpretation": "adding arguments selected from endpoint residuals or family comparison",
        },
        {
            "body_row_id": "M0NDFEB14_ASSEMBLY",
            "body_component": "assembly_body",
            "body_role": "state the non-numeric body assembly",
            "frozen_expression_body_statement": "E_M0(X_M0) := Assemble_M0[Readout_M0(source_state, readout_operator), Baryon(baryonic_input, radius_grid), Guard(guard_state), Order(assembly_order)]",
            "allowed_interpretation": "frozen symbolic/operator body awaiting later executable kernel promotion",
            "blocked_interpretation": "completed velocity formula, fitted curve, or executable prediction callable",
        },
        {
            "body_row_id": "M0NDFEB14_NO_DARK_EXCLUSION",
            "body_component": "no_dark_exclusion",
            "body_role": "exclude hidden dark-sector compensation inside M0",
            "frozen_expression_body_statement": "DarkCompensationTerm(E_M0) = forbidden; unresolved or inadmissible cases route to null/fallback states",
            "allowed_interpretation": "M0 family constraint and failure routing",
            "blocked_interpretation": "hidden density, halo, acceleration, or potential term fitted as an M0 rescue",
        },
        {
            "body_row_id": "M0NDFEB14_OUTPUT_CLASS",
            "body_component": "output_class",
            "body_role": "declare the later output target without producing predictions",
            "frozen_expression_body_statement": "OutputTarget(E_M0) = velocity-readout-compatible row class on the frozen radial grid",
            "allowed_interpretation": "output-class handoff for a later kernel/prediction writer",
            "blocked_interpretation": "numeric v_pred_km_s rows or endpoint scores",
        },
        {
            "body_row_id": "M0NDFEB14_FREEZE_GUARD",
            "body_component": "freeze_guard",
            "body_role": "fix the body before scoring-family comparison",
            "frozen_expression_body_statement": "E_M0 is frozen before prediction rows, heldout scoring, or family-winner inspection",
            "allowed_interpretation": "pre-score provenance and leakage guard",
            "blocked_interpretation": "posthoc term, branch, coefficient, or operator switch",
        },
    ]
    for row in rows:
        row["completion_status"] = status
        row["next_required_artifact"] = "m0_no_dark_kernel_expression_contract_v10"
        row["forbidden_inputs"] = common_forbidden
        row["expression_body_claim_allowed"] = "true" if status == "READY" else "false"
        row["velocity_formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["dark_sector_verdict_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_frozen_expression_body_definition_only_no_velocity_formula_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["completion_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    return [
        {
            "summary_id": "M0_NO_DARK_FROZEN_EXPRESSION_BODY_V14",
            "body_artifact": "m0_no_dark_frozen_expression_body_v14",
            "payload_status": "READY" if payload_ready() else "BLOCKED",
            "body_rows": len(rows),
            "ready_body_rows": ready,
            "blocked_body_rows": blocked,
            "expression_body_written": "true" if blocked == 0 else "false",
            "velocity_formula_written": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "M0_NO_DARK_FROZEN_EXPRESSION_BODY_READY_FOR_KERNEL_EXPRESSION_REVIEW"
            if blocked == 0
            else "M0_NO_DARK_FROZEN_EXPRESSION_BODY_BLOCKED",
            "next_required_artifact": "m0_no_dark_kernel_expression_contract_v10",
            "claim_boundary": "m0_no_dark_frozen_expression_body_definition_only_no_velocity_formula_no_scores_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_frozen_expression_body_v14.md").write_text(
        """# M0 No-Dark Frozen Expression Body v14

**Doc class:** M0 no-dark frozen-expression body definition
**Reader role:** reviewer-facing scoring-frontier bridge
**Status:** expression body formulated; no velocity formula; no scoring
**Canonical parent:** family prediction frontier trace v81

Script:

```text
scripts/build_m0_no_dark_frozen_expression_body.py
```

Derived outputs:

```text
data/derived/m0_no_dark_frozen_expression_body_v14.csv
data/derived/m0_no_dark_frozen_expression_body_summary_v14.csv
```

## Body Statement

The M0 no-dark frozen expression body is fixed at definition level as:

```text
X_M0 = (source_state, baryonic_input, radius_grid, readout_operator, guard_state, assembly_order)

E_M0(X_M0) :=
  Assemble_M0[
    Readout_M0(source_state, readout_operator),
    Baryon(baryonic_input, radius_grid),
    Guard(guard_state),
    Order(assembly_order)
  ]
```

This is a frozen source-side expression body. It says what the M0 no-dark
candidate is allowed to assemble from, and what it is not allowed to use.

## No-Dark Constraint

The body forbids hidden dark-sector compensation inside M0:

```text
DarkCompensationTerm(E_M0) = forbidden
```

Unresolved, inadmissible, null, gauge, or missing-input cases must route to the
declared null/fallback states rather than adding rescue terms.

## Claim Boundary

This artifact does not define an executable velocity formula, does not assign
coefficient values, does not write `v_pred_km_s` rows, does not compute endpoint
scores, and does not decide whether a dark-sector component is physically
required. It only formulates the M0 no-dark expression body that a later kernel
expression review may accept, refine, or reject.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = body_rows()
    write_csv(DERIVED / "m0_no_dark_frozen_expression_body_v14.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_frozen_expression_body_summary_v14.csv",
        summary(rows),
        [
            "summary_id",
            "body_artifact",
            "payload_status",
            "body_rows",
            "ready_body_rows",
            "blocked_body_rows",
            "expression_body_written",
            "velocity_formula_written",
            "numeric_predictions_written",
            "endpoint_scoring_allowed_anywhere",
            "dark_sector_verdict_allowed",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_FROZEN_EXPRESSION_BODY_V14_BUILT")


if __name__ == "__main__":
    main()
