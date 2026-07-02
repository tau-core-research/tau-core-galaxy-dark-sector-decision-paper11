#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
PAYLOAD_SUMMARY = DERIVED / "m0_no_dark_frozen_expression_payload_summary_v11.csv"


FIELDNAMES = [
    "binding_id",
    "symbol_class",
    "binding_role",
    "allowed_source",
    "blocked_binding",
    "completion_status",
    "next_required_artifact",
    "forbidden_inputs",
    "binding_claim_allowed",
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


def payload_ready_for_symbol_binding() -> bool:
    if not PAYLOAD_SUMMARY.exists():
        return False
    rows = read_csv(PAYLOAD_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"]
        in {
            "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_READY_SYMBOL_BINDING_TABLE_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_READY_CONSTANT_POLICY_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_READY_DIMENSIONAL_TRACE_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_READY_MACHINE_PAYLOAD_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_READY_PAYLOAD_LEAKAGE_CERTIFICATE_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_READY_FOR_KERNEL_EXPRESSION",
        }
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
        and rows[0]["formula_claim_allowed"] == "false"
    )


def binding_rows() -> list[dict[str, object]]:
    rows = [
        {
            "binding_id": "M0NDPSBT12_SOURCE_STATE_SYMBOL",
            "symbol_class": "source_state_symbol",
            "binding_role": "bind morphology/readout source-state symbols to approved source-side records",
            "allowed_source": "pre-score source-basis, source-route, and statement argument records",
            "blocked_binding": "source state inferred from endpoint residuals or family winner",
        },
        {
            "binding_id": "M0NDPSBT12_BARYONIC_INPUT_SYMBOL",
            "symbol_class": "baryonic_input_symbol",
            "binding_role": "bind baryonic input symbols to imported observed-input columns",
            "allowed_source": "source-import values and leakage-reviewed observed-input records",
            "blocked_binding": "baryonic proxy chosen after best-fit curve quality is known",
        },
        {
            "binding_id": "M0NDPSBT12_RADIUS_GRID_SYMBOL",
            "symbol_class": "radius_grid_symbol",
            "binding_role": "bind radial-grid symbols to the frozen galaxy row domain",
            "allowed_source": "declared row-level radial grid or imported radius column only",
            "blocked_binding": "radial resampling selected from heldout score behavior",
        },
        {
            "binding_id": "M0NDPSBT12_READOUT_OPERATOR_SYMBOL",
            "symbol_class": "readout_operator_symbol",
            "binding_role": "bind readout operator symbols to approved source-side readout metadata",
            "allowed_source": "argument-signature readout operator slot and pre-dimensional route obligations",
            "blocked_binding": "operator selected by comparing no-dark and dark-sector residuals",
        },
        {
            "binding_id": "M0NDPSBT12_GUARD_SYMBOL",
            "symbol_class": "guard_symbol",
            "binding_role": "bind guard symbols to declared domain, null, gauge, no-dark, fallback, and leakage guards",
            "allowed_source": "constraint-guard rows and freeze-provenance records",
            "blocked_binding": "guard introduced to repair a failed endpoint prediction",
        },
        {
            "binding_id": "M0NDPSBT12_ASSEMBLY_SYMBOL",
            "symbol_class": "assembly_symbol",
            "binding_role": "bind assembly/order symbols to non-numeric statement assembly metadata",
            "allowed_source": "argument-signature assembly slot and payload contract order metadata",
            "blocked_binding": "assembly reordered after residual inspection",
        },
    ]
    for row in rows:
        row["completion_status"] = "READY"
        row["next_required_artifact"] = "m0_no_dark_payload_constant_policy_v12"
        row["forbidden_inputs"] = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_symbol_switch"
        row["binding_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_payload_symbol_binding_table_only_bindings_no_formula_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["completion_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    upstream_ready = payload_ready_for_symbol_binding()
    return [
        {
            "summary_id": "M0_NO_DARK_PAYLOAD_SYMBOL_BINDING_TABLE_V12",
            "symbol_binding_artifact": "m0_no_dark_payload_symbol_binding_table_v12",
            "payload_contract_status": "READY" if upstream_ready else "BLOCKED",
            "binding_rows": len(rows),
            "ready_binding_rows": ready,
            "blocked_binding_rows": blocked,
            "symbol_binding_table_written": "true" if upstream_ready and blocked == 0 else "false",
            "formula_body_written": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_PAYLOAD_SYMBOL_BINDING_TABLE_READY_FOR_CONSTANT_POLICY"
            if upstream_ready and blocked == 0
            else "M0_NO_DARK_PAYLOAD_SYMBOL_BINDING_TABLE_BLOCKED",
            "next_required_artifact": "m0_no_dark_payload_constant_policy_v12",
            "claim_boundary": "m0_no_dark_payload_symbol_binding_table_only_bindings_no_formula_no_scores_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_payload_symbol_binding_table_v12.md").write_text(
        """# M0 No-Dark Payload Symbol Binding Table v12

**Doc class:** no-dark M0 payload symbol-binding contract
**Status:** symbol bindings ready; constant policy blocked; no formula; no scoring

Script:

```text
scripts/build_m0_no_dark_payload_symbol_binding_table.py
```

Derived outputs:

```text
data/derived/m0_no_dark_payload_symbol_binding_table_v12.csv
data/derived/m0_no_dark_payload_symbol_binding_table_summary_v12.csv
```

This artifact binds payload symbol classes to approved source-side inputs,
operator metadata, guards, and assembly metadata before any formula body is
written.

## Current Result

The expected status is:

```text
M0_NO_DARK_PAYLOAD_SYMBOL_BINDING_TABLE_READY_FOR_CONSTANT_POLICY
```

The next missing artifact is:

```text
m0_no_dark_payload_constant_policy_v12
```

## Claim Boundary

This symbol-binding table does not define a velocity formula, does not assign
coefficients, does not compute predictions, does not score galaxies, and does
not decide the dark-sector question. It only fixes which approved source-side
objects later payload symbols may refer to.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = binding_rows()
    write_csv(DERIVED / "m0_no_dark_payload_symbol_binding_table_v12.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_payload_symbol_binding_table_summary_v12.csv",
        summary(rows),
        [
            "summary_id",
            "symbol_binding_artifact",
            "payload_contract_status",
            "binding_rows",
            "ready_binding_rows",
            "blocked_binding_rows",
            "symbol_binding_table_written",
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
    print("PAPER11_M0_NO_DARK_PAYLOAD_SYMBOL_BINDING_TABLE_V12_BUILT")


if __name__ == "__main__":
    main()
