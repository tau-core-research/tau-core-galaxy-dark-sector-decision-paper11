#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
TERM_LIST_SUMMARY = DERIVED / "m0_no_dark_statement_term_list_summary_v13.csv"
STATEMENT_CONTRACT_SUMMARY = DERIVED / "m0_no_dark_frozen_expression_statement_summary_v12.csv"


FIELDNAMES = [
    "argument_slot_id",
    "argument_class",
    "argument_role",
    "allowed_binding",
    "blocked_binding",
    "completion_status",
    "next_required_artifact",
    "forbidden_inputs",
    "argument_claim_allowed",
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


def term_list_ready() -> bool:
    if not TERM_LIST_SUMMARY.exists() or not STATEMENT_CONTRACT_SUMMARY.exists():
        return False
    term_list = read_csv(TERM_LIST_SUMMARY)
    contract = read_csv(STATEMENT_CONTRACT_SUMMARY)
    return (
        len(term_list) == 1
        and term_list[0]["overall_status"] == "M0_NO_DARK_STATEMENT_TERM_LIST_READY_FOR_ARGUMENT_SIGNATURE"
        and term_list[0]["endpoint_scoring_allowed_anywhere"] == "false"
        and len(contract) == 1
        and contract[0]["overall_status"]
        in {
            "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_ARGUMENT_SIGNATURE_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_CONSTRAINT_GUARDS_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_PRE_DIMENSIONAL_PROOF_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_FREEZE_PROVENANCE_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_FOR_PAYLOAD",
        }
        and contract[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def argument_rows() -> list[dict[str, object]]:
    rows = [
        {
            "argument_slot_id": "M0NDSAS13_SOURCE_STATE_ARGUMENT",
            "argument_class": "source_state_argument",
            "argument_role": "bind source-state term to approved source-side morphology/readout state",
            "allowed_binding": "source_state_id from pre-score source-basis and source-route records",
            "blocked_binding": "source state inferred from endpoint residual or family winner",
        },
        {
            "argument_slot_id": "M0NDSAS13_BARYONIC_INPUT_ARGUMENT",
            "argument_class": "baryonic_input_argument",
            "argument_role": "bind baryonic/source input term to imported observed-input fields",
            "allowed_binding": "baryonic_input_id with provenance and leakage-audit pass",
            "blocked_binding": "normalization repaired from best-fit rotation curve",
        },
        {
            "argument_slot_id": "M0NDSAS13_RADIUS_GRID_ARGUMENT",
            "argument_class": "radius_grid_argument",
            "argument_role": "bind radial grid argument without endpoint-selected resampling",
            "allowed_binding": "frozen radius_grid_id shared with observed input rows",
            "blocked_binding": "posthoc radial grid selected by fit quality",
        },
        {
            "argument_slot_id": "M0NDSAS13_READOUT_OPERATOR_ARGUMENT",
            "argument_class": "readout_operator_argument",
            "argument_role": "bind readout operator term to pre-score admissibility shell",
            "allowed_binding": "readout_operator_id selected by source-side admissibility only",
            "blocked_binding": "operator chosen after heldout score or family comparison",
        },
        {
            "argument_slot_id": "M0NDSAS13_GUARD_ARGUMENT",
            "argument_class": "guard_argument",
            "argument_role": "bind null, gauge, no-dark, and fallback guard identifiers",
            "allowed_binding": "guard_id with explicit no-dark and failure-route policy",
            "blocked_binding": "silent exception or missing-input patch added after scoring",
        },
        {
            "argument_slot_id": "M0NDSAS13_ASSEMBLY_ARGUMENT",
            "argument_class": "assembly_argument",
            "argument_role": "bind non-numeric assembly/order metadata for later formula body",
            "allowed_binding": "argument_order_id and assembly_id only; no expression body",
            "blocked_binding": "complete algebraic expression or executable prediction callable",
        },
    ]
    for row in rows:
        row["completion_status"] = "READY"
        row["next_required_artifact"] = "m0_no_dark_statement_constraint_guards_v13"
        row["forbidden_inputs"] = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_label_switch"
        row["argument_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_statement_argument_signature_only_bindings_no_formula_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["completion_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    upstream_ready = term_list_ready()
    return [
        {
            "summary_id": "M0_NO_DARK_STATEMENT_ARGUMENT_SIGNATURE_V13",
            "argument_signature_artifact": "m0_no_dark_statement_argument_signature_v13",
            "term_list_status": "READY" if upstream_ready else "BLOCKED",
            "argument_slots": len(rows),
            "ready_argument_slots": ready,
            "blocked_argument_slots": blocked,
            "argument_signature_written": "true" if upstream_ready and blocked == 0 else "false",
            "formula_body_written": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_STATEMENT_ARGUMENT_SIGNATURE_READY_FOR_CONSTRAINT_GUARDS"
            if upstream_ready and blocked == 0
            else "M0_NO_DARK_STATEMENT_ARGUMENT_SIGNATURE_BLOCKED",
            "next_required_artifact": "m0_no_dark_statement_constraint_guards_v13",
            "claim_boundary": "m0_no_dark_statement_argument_signature_only_bindings_no_formula_no_scores_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_statement_argument_signature_v13.md").write_text(
        """# M0 No-Dark Statement Argument Signature v13

**Doc class:** no-dark M0 statement argument-signature contract
**Status:** argument signature ready; constraint guards blocked; no formula; no scoring

Script:

```text
scripts/build_m0_no_dark_statement_argument_signature.py
```

Derived outputs:

```text
data/derived/m0_no_dark_statement_argument_signature_v13.csv
data/derived/m0_no_dark_statement_argument_signature_summary_v13.csv
```

This artifact records the allowed argument slots for the M0 no-dark statement
path. It binds term classes to source-side, baryonic, radial, readout, guard,
and assembly roles without writing an algebraic expression or executable
prediction function.

## Current Result

The expected status is:

```text
M0_NO_DARK_STATEMENT_ARGUMENT_SIGNATURE_READY_FOR_CONSTRAINT_GUARDS
```

The next missing artifact is:

```text
m0_no_dark_statement_constraint_guards_v13
```

## Claim Boundary

This argument-signature artifact does not define a velocity formula, does not
assign coefficients, does not compute predictions, does not score galaxies, and
does not decide the dark-sector question. It only freezes allowed argument
roles before constraint guards and dimensional checks are considered.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = argument_rows()
    write_csv(DERIVED / "m0_no_dark_statement_argument_signature_v13.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_statement_argument_signature_summary_v13.csv",
        summary(rows),
        [
            "summary_id",
            "argument_signature_artifact",
            "term_list_status",
            "argument_slots",
            "ready_argument_slots",
            "blocked_argument_slots",
            "argument_signature_written",
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
    print("PAPER11_M0_NO_DARK_STATEMENT_ARGUMENT_SIGNATURE_V13_BUILT")


if __name__ == "__main__":
    main()
