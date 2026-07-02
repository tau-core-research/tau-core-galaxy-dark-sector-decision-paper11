#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
KERNEL_EXPRESSION_INTERFACE_SUMMARY = DERIVED / "m0_no_dark_kernel_expression_interface_summary_v10.csv"
SOURCE_SIDE_STATEMENT_SUMMARY = DERIVED / "m0_no_dark_source_side_expression_statement_summary_v13.csv"
TERM_LIST_SUMMARY = DERIVED / "m0_no_dark_statement_term_list_summary_v13.csv"
ARGUMENT_SIGNATURE_SUMMARY = DERIVED / "m0_no_dark_statement_argument_signature_summary_v13.csv"
CONSTRAINT_GUARDS_SUMMARY = DERIVED / "m0_no_dark_statement_constraint_guards_summary_v13.csv"
PRE_DIMENSIONAL_PROOF_SUMMARY = DERIVED / "m0_no_dark_statement_pre_dimensional_proof_summary_v13.csv"
FREEZE_PROVENANCE_SUMMARY = DERIVED / "m0_no_dark_statement_freeze_provenance_summary_v13.csv"


FIELDNAMES = [
    "statement_slot_id",
    "statement_slot_class",
    "required_specification",
    "completion_status",
    "next_required_artifact",
    "forbidden_inputs",
    "statement_claim_allowed",
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


def kernel_expression_interface_ready() -> bool:
    if not KERNEL_EXPRESSION_INTERFACE_SUMMARY.exists():
        return False
    rows = read_csv(KERNEL_EXPRESSION_INTERFACE_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_KERNEL_EXPRESSION_INTERFACE_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def source_side_statement_ready() -> bool:
    if not SOURCE_SIDE_STATEMENT_SUMMARY.exists():
        return False
    rows = read_csv(SOURCE_SIDE_STATEMENT_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_SOURCE_SIDE_EXPRESSION_STATEMENT_READY_FOR_TERM_LIST"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
        and rows[0]["formula_claim_allowed"] == "false"
    )


def term_list_ready() -> bool:
    if not TERM_LIST_SUMMARY.exists():
        return False
    rows = read_csv(TERM_LIST_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_STATEMENT_TERM_LIST_READY_FOR_ARGUMENT_SIGNATURE"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
        and rows[0]["formula_claim_allowed"] == "false"
    )


def argument_signature_ready() -> bool:
    if not ARGUMENT_SIGNATURE_SUMMARY.exists():
        return False
    rows = read_csv(ARGUMENT_SIGNATURE_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_STATEMENT_ARGUMENT_SIGNATURE_READY_FOR_CONSTRAINT_GUARDS"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
        and rows[0]["formula_claim_allowed"] == "false"
    )


def constraint_guards_ready() -> bool:
    if not CONSTRAINT_GUARDS_SUMMARY.exists():
        return False
    rows = read_csv(CONSTRAINT_GUARDS_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_STATEMENT_CONSTRAINT_GUARDS_READY_FOR_PRE_DIMENSIONAL_PROOF"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
        and rows[0]["formula_claim_allowed"] == "false"
    )


def pre_dimensional_proof_ready() -> bool:
    if not PRE_DIMENSIONAL_PROOF_SUMMARY.exists():
        return False
    rows = read_csv(PRE_DIMENSIONAL_PROOF_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_STATEMENT_PRE_DIMENSIONAL_PROOF_READY_FOR_FREEZE_PROVENANCE"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
        and rows[0]["formula_claim_allowed"] == "false"
    )


def freeze_provenance_ready() -> bool:
    if not FREEZE_PROVENANCE_SUMMARY.exists():
        return False
    rows = read_csv(FREEZE_PROVENANCE_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_STATEMENT_FREEZE_PROVENANCE_READY_FOR_PAYLOAD"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
        and rows[0]["formula_claim_allowed"] == "false"
    )


def contract_rows() -> list[dict[str, object]]:
    statement_ready = source_side_statement_ready()
    terms_ready = term_list_ready()
    signature_ready = argument_signature_ready()
    guards_ready = constraint_guards_ready()
    pre_dimensional_ready = pre_dimensional_proof_ready()
    freeze_ready = freeze_provenance_ready()
    rows = [
        {
            "statement_slot_id": "M0NDFES12_SOURCE_SIDE_STATEMENT",
            "statement_slot_class": "source_side_expression_statement",
            "required_specification": "single frozen source-side expression statement, symbolic or algorithmic, before endpoint residuals are used",
            "completion_status": "READY" if statement_ready else "SOURCE_SIDE_EXPRESSION_STATEMENT_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_source_side_expression_statement_v13",
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_expression_switch",
        },
        {
            "statement_slot_id": "M0NDFES12_TERM_LIST",
            "statement_slot_class": "term_list",
            "required_specification": "complete list of admissible terms and operators used by the statement",
            "completion_status": "READY" if terms_ready else "TERM_LIST_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_statement_term_list_v13",
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;posthoc_term_addition",
        },
        {
            "statement_slot_id": "M0NDFES12_ARGUMENT_SIGNATURE",
            "statement_slot_class": "argument_signature",
            "required_specification": "ordered source-side argument signature with no endpoint-selected arguments",
            "completion_status": "READY" if signature_ready else "ARGUMENT_SIGNATURE_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_statement_argument_signature_v13",
            "forbidden_inputs": "endpoint_residual;posthoc_label_switch;family_winner",
        },
        {
            "statement_slot_id": "M0NDFES12_CONSTRAINT_GUARDS",
            "statement_slot_class": "constraint_guards",
            "required_specification": "domain, null/gauge, no-dark, and fallback guards attached to the statement",
            "completion_status": "READY" if guards_ready else "CONSTRAINT_GUARDS_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_statement_constraint_guards_v13",
            "forbidden_inputs": "endpoint_residual;best_fit_curve;posthoc_exception",
        },
        {
            "statement_slot_id": "M0NDFES12_PRE_DIMENSIONAL_PROOF",
            "statement_slot_class": "pre_dimensional_proof",
            "required_specification": "pre-score dimensional proof route for the statement output class",
            "completion_status": "READY" if pre_dimensional_ready else "PRE_DIMENSIONAL_PROOF_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_statement_pre_dimensional_proof_v13",
            "forbidden_inputs": "endpoint_residual;heldout_score;posthoc_unit_rescale",
        },
        {
            "statement_slot_id": "M0NDFES12_FREEZE_PROVENANCE",
            "statement_slot_class": "freeze_provenance",
            "required_specification": "timestamped/source-frozen provenance that the statement was fixed before scoring comparisons",
            "completion_status": "READY" if freeze_ready else "FREEZE_PROVENANCE_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_statement_freeze_provenance_v13",
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve",
        },
    ]
    for row in rows:
        row["statement_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_frozen_expression_statement_contract_only_no_statement_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["completion_status"] == "READY" for row in rows)
    blocked = [row for row in rows if row["completion_status"] != "READY"]
    upstream_ready = kernel_expression_interface_ready()
    return [
        {
            "summary_id": "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_V12",
            "statement_artifact": "m0_no_dark_frozen_expression_statement_v12",
            "kernel_expression_interface_status": "READY" if upstream_ready else "BLOCKED",
            "required_statement_slots": len(rows),
            "ready_statement_slots": ready,
            "blocked_statement_slots": len(blocked),
            "source_side_expression_statement_written": "true" if source_side_statement_ready() else "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": (
                f"M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_{blocked[0]['statement_slot_class'].upper()}_BLOCKED"
                if upstream_ready and blocked
                else "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_FOR_PAYLOAD"
                if upstream_ready
                else "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_BLOCKED"
            ),
            "next_required_artifact": blocked[0]["next_required_artifact"] if blocked else "m0_no_dark_frozen_expression_payload_v11",
            "claim_boundary": "m0_no_dark_frozen_expression_statement_contract_only_no_statement_no_scores_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    rows = contract_rows()
    summary_row = summary(rows)[0]
    (DOCS / "m0_no_dark_frozen_expression_statement_v12.md").write_text(
        f"""# M0 No-Dark Frozen Expression Statement v12

**Doc class:** no-dark M0 frozen-expression statement contract
**Status:** statement contract ready; no formula; no scoring

Script:

```text
scripts/build_m0_no_dark_frozen_expression_statement_contract.py
```

Derived outputs:

```text
data/derived/m0_no_dark_frozen_expression_statement_v12.csv
data/derived/m0_no_dark_frozen_expression_statement_summary_v12.csv
```

This artifact expands the first formula-bearing statement blocker into the
minimum acceptance slots required before a source-side no-dark expression can
be treated as frozen.

## Current Result

The expected status is:

```text
{summary_row["overall_status"]}
```

The first concrete missing artifact is:

```text
{summary_row["next_required_artifact"]}
```

## Claim Boundary

This contract does not define a velocity formula, does not assign coefficients,
does not compute predictions, does not score galaxies, and does not decide the
dark-sector question. It only tracks the statement-side slots required before
the payload can be accepted.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = contract_rows()
    write_csv(DERIVED / "m0_no_dark_frozen_expression_statement_v12.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_frozen_expression_statement_summary_v12.csv",
        summary(rows),
        [
            "summary_id",
            "statement_artifact",
            "kernel_expression_interface_status",
            "required_statement_slots",
            "ready_statement_slots",
            "blocked_statement_slots",
            "source_side_expression_statement_written",
            "formula_claim_allowed",
            "numeric_predictions_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_V12_BUILT")


if __name__ == "__main__":
    main()
