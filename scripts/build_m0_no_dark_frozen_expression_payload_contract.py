#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
KERNEL_EXPRESSION_INTERFACE_SUMMARY = DERIVED / "m0_no_dark_kernel_expression_interface_summary_v10.csv"
STATEMENT_SUMMARY = DERIVED / "m0_no_dark_frozen_expression_statement_summary_v12.csv"
SYMBOL_BINDING_SUMMARY = DERIVED / "m0_no_dark_payload_symbol_binding_table_summary_v12.csv"
CONSTANT_POLICY_SUMMARY = DERIVED / "m0_no_dark_payload_constant_policy_summary_v12.csv"
DIMENSIONAL_TRACE_SUMMARY = DERIVED / "m0_no_dark_payload_dimensional_trace_summary_v12.csv"
MACHINE_PAYLOAD_SUMMARY = DERIVED / "m0_no_dark_payload_machine_form_summary_v12.csv"
PAYLOAD_LEAKAGE_CERTIFICATE_SUMMARY = DERIVED / "m0_no_dark_payload_leakage_certificate_summary_v12.csv"


FIELDNAMES = [
    "payload_slot_id",
    "payload_slot_class",
    "required_specification",
    "completion_status",
    "next_required_artifact",
    "forbidden_inputs",
    "payload_claim_allowed",
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


def statement_next() -> str:
    if STATEMENT_SUMMARY.exists():
        rows = read_csv(STATEMENT_SUMMARY)
        if len(rows) == 1:
            return rows[0]["next_required_artifact"]
    return "m0_no_dark_frozen_expression_statement_v12"


def statement_ready_for_payload() -> bool:
    if not STATEMENT_SUMMARY.exists():
        return False
    rows = read_csv(STATEMENT_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_FOR_PAYLOAD"
        and rows[0]["next_required_artifact"] == "m0_no_dark_frozen_expression_payload_v11"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
        and rows[0]["formula_claim_allowed"] == "false"
    )


def symbol_binding_ready() -> bool:
    if not SYMBOL_BINDING_SUMMARY.exists():
        return False
    rows = read_csv(SYMBOL_BINDING_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_PAYLOAD_SYMBOL_BINDING_TABLE_READY_FOR_CONSTANT_POLICY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
        and rows[0]["formula_claim_allowed"] == "false"
    )


def constant_policy_ready() -> bool:
    if not CONSTANT_POLICY_SUMMARY.exists():
        return False
    rows = read_csv(CONSTANT_POLICY_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_PAYLOAD_CONSTANT_POLICY_READY_FOR_DIMENSIONAL_TRACE"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
        and rows[0]["formula_claim_allowed"] == "false"
    )


def dimensional_trace_ready() -> bool:
    if not DIMENSIONAL_TRACE_SUMMARY.exists():
        return False
    rows = read_csv(DIMENSIONAL_TRACE_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_PAYLOAD_DIMENSIONAL_TRACE_READY_FOR_MACHINE_PAYLOAD"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
        and rows[0]["formula_claim_allowed"] == "false"
    )


def machine_payload_ready() -> bool:
    if not MACHINE_PAYLOAD_SUMMARY.exists():
        return False
    rows = read_csv(MACHINE_PAYLOAD_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_PAYLOAD_MACHINE_FORM_READY_FOR_LEAKAGE_CERTIFICATE"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
        and rows[0]["formula_claim_allowed"] == "false"
    )


def payload_leakage_certificate_ready() -> bool:
    if not PAYLOAD_LEAKAGE_CERTIFICATE_SUMMARY.exists():
        return False
    rows = read_csv(PAYLOAD_LEAKAGE_CERTIFICATE_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_PAYLOAD_LEAKAGE_CERTIFICATE_READY_FOR_FORMULA_TABLES"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
        and rows[0]["formula_claim_allowed"] == "false"
    )


def contract_rows() -> list[dict[str, object]]:
    next_statement = statement_next()
    statement_ready = statement_ready_for_payload()
    binding_ready = symbol_binding_ready()
    constant_ready = constant_policy_ready()
    trace_ready = dimensional_trace_ready()
    machine_ready = machine_payload_ready()
    leakage_ready = payload_leakage_certificate_ready()
    rows = [
        {
            "payload_slot_id": "M0NDFEP11_EXPRESSION_STATEMENT",
            "payload_slot_class": "frozen_expression_statement",
            "required_specification": "single source-side symbolic or algorithmic expression statement with no endpoint-selected terms",
            "completion_status": "READY" if statement_ready else "FROZEN_EXPRESSION_STATEMENT_REQUIRED_NOT_FILLED",
            "next_required_artifact": next_statement,
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_expression_switch",
        },
        {
            "payload_slot_id": "M0NDFEP11_SYMBOL_BINDING_TABLE",
            "payload_slot_class": "symbol_binding_table",
            "required_specification": "one-to-one binding from every expression symbol to approved source-side inputs and guards",
            "completion_status": "READY" if binding_ready else "SYMBOL_BINDING_TABLE_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_payload_symbol_binding_table_v12",
            "forbidden_inputs": "endpoint_residual;posthoc_label_switch;family_winner",
        },
        {
            "payload_slot_id": "M0NDFEP11_CONSTANT_POLICY",
            "payload_slot_class": "constant_policy",
            "required_specification": "all constants, switches, branches, and scale parameters declared with fixed/free status before scoring",
            "completion_status": "READY" if constant_ready else "CONSTANT_POLICY_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_payload_constant_policy_v12",
            "forbidden_inputs": "endpoint_residual;family_winner;posthoc_parameter_discount",
        },
        {
            "payload_slot_id": "M0NDFEP11_DIMENSIONAL_TRACE",
            "payload_slot_class": "dimensional_trace",
            "required_specification": "complete dimensional trace from payload inputs to km/s output without posthoc rescaling",
            "completion_status": "READY" if trace_ready else "DIMENSIONAL_TRACE_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_payload_dimensional_trace_v12",
            "forbidden_inputs": "endpoint_residual;heldout_score;posthoc_unit_rescale",
        },
        {
            "payload_slot_id": "M0NDFEP11_MACHINE_PAYLOAD",
            "payload_slot_class": "machine_payload",
            "required_specification": "machine-readable expression payload that can be inspected before any prediction writer executes",
            "completion_status": "READY" if machine_ready else "MACHINE_PAYLOAD_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_payload_machine_form_v12",
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;posthoc_callable_switch",
        },
        {
            "payload_slot_id": "M0NDFEP11_LEAKAGE_CERTIFICATE",
            "payload_slot_class": "payload_leakage_certificate",
            "required_specification": "payload-level certificate that expression terms were fixed before endpoint residuals or family winners were available",
            "completion_status": "READY" if leakage_ready else "PAYLOAD_LEAKAGE_CERTIFICATE_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_payload_leakage_certificate_v12",
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve",
        },
    ]
    for row in rows:
        row["payload_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_frozen_expression_payload_contract_only_no_payload_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["completion_status"] == "READY" for row in rows)
    blocked = [row for row in rows if row["completion_status"] != "READY"]
    upstream_ready = kernel_expression_interface_ready()
    return [
        {
            "summary_id": "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_V11",
            "payload_artifact": "m0_no_dark_frozen_expression_payload_v11",
            "kernel_expression_interface_status": "READY" if upstream_ready else "BLOCKED",
            "required_payload_slots": len(rows),
            "ready_payload_slots": ready,
            "blocked_payload_slots": len(blocked),
            "frozen_expression_payload_written": "true" if statement_ready_for_payload() else "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": (
                f"M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_READY_{blocked[0]['payload_slot_class'].upper()}_BLOCKED"
                if upstream_ready and blocked
                else "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_READY_FOR_KERNEL_EXPRESSION"
                if upstream_ready
                else "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_BLOCKED"
            ),
            "next_required_artifact": blocked[0]["next_required_artifact"] if blocked else "family_prediction_tables_v08.csv",
            "claim_boundary": "m0_no_dark_frozen_expression_payload_contract_only_no_payload_no_scores_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    rows = contract_rows()
    summary_row = summary(rows)[0]
    (DOCS / "m0_no_dark_frozen_expression_payload_v11.md").write_text(
        f"""# M0 No-Dark Frozen Expression Payload v11

**Doc class:** no-dark M0 frozen-expression payload contract
**Status:** payload contract ready; payload slot work blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_frozen_expression_payload_contract.py
```

Derived outputs:

```text
data/derived/m0_no_dark_frozen_expression_payload_v11.csv
data/derived/m0_no_dark_frozen_expression_payload_summary_v11.csv
```

This artifact expands the formula-bearing frozen-expression payload into the
minimum payload slots required before any prediction rows can be written.

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

This contract does not write the frozen expression payload, does not define a
velocity formula, does not assign coefficients, does not compute predictions,
does not score galaxies, and does not decide the dark-sector question. It only
identifies the first formula-bearing payload component that must be supplied
before the M0 no-dark family can produce prediction rows.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = contract_rows()
    write_csv(DERIVED / "m0_no_dark_frozen_expression_payload_v11.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_frozen_expression_payload_summary_v11.csv",
        summary(rows),
        [
            "summary_id",
            "payload_artifact",
            "kernel_expression_interface_status",
            "required_payload_slots",
            "ready_payload_slots",
            "blocked_payload_slots",
            "frozen_expression_payload_written",
            "formula_claim_allowed",
            "numeric_predictions_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_V11_BUILT")


if __name__ == "__main__":
    main()
