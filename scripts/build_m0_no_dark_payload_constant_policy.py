#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
SYMBOL_BINDING_SUMMARY = DERIVED / "m0_no_dark_payload_symbol_binding_table_summary_v12.csv"
PAYLOAD_SUMMARY = DERIVED / "m0_no_dark_frozen_expression_payload_summary_v11.csv"


FIELDNAMES = [
    "policy_id",
    "constant_policy_class",
    "policy_role",
    "allowed_policy",
    "blocked_policy",
    "completion_status",
    "next_required_artifact",
    "forbidden_inputs",
    "policy_claim_allowed",
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


def symbol_binding_ready() -> bool:
    if not SYMBOL_BINDING_SUMMARY.exists() or not PAYLOAD_SUMMARY.exists():
        return False
    bindings = read_csv(SYMBOL_BINDING_SUMMARY)
    payload = read_csv(PAYLOAD_SUMMARY)
    return (
        len(bindings) == 1
        and bindings[0]["overall_status"] == "M0_NO_DARK_PAYLOAD_SYMBOL_BINDING_TABLE_READY_FOR_CONSTANT_POLICY"
        and bindings[0]["endpoint_scoring_allowed_anywhere"] == "false"
        and len(payload) == 1
        and payload[0]["overall_status"]
        in {
            "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_READY_CONSTANT_POLICY_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_READY_DIMENSIONAL_TRACE_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_READY_MACHINE_PAYLOAD_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_READY_PAYLOAD_LEAKAGE_CERTIFICATE_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_READY_FOR_KERNEL_EXPRESSION",
        }
        and payload[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def policy_rows() -> list[dict[str, object]]:
    rows = [
        {
            "policy_id": "M0NDPCP12_FIXED_SOURCE_CONSTANTS",
            "constant_policy_class": "fixed_source_constants",
            "policy_role": "declare source-side constants that may appear only if already fixed upstream",
            "allowed_policy": "constant names may be referenced only from source-side records or physical unit declarations",
            "blocked_policy": "introduce a constant after inspecting endpoint residuals",
        },
        {
            "policy_id": "M0NDPCP12_FREE_PARAMETER_DECLARATION",
            "constant_policy_class": "free_parameter_declaration",
            "policy_role": "separate declared free parameters from fixed source constants before scoring",
            "allowed_policy": "free parameter labels are allowed only as labels without values, bounds, or fitted choices",
            "blocked_policy": "choosing parameter values, ranges, or priors from heldout performance",
        },
        {
            "policy_id": "M0NDPCP12_SCALE_POLICY",
            "constant_policy_class": "scale_policy",
            "policy_role": "declare whether scale-like symbols are fixed, derived, or still blocked",
            "allowed_policy": "scale status must be source-side or explicitly blocked until dimensional trace",
            "blocked_policy": "posthoc unit or scale normalization from best-fit curve shape",
        },
        {
            "policy_id": "M0NDPCP12_BRANCH_SWITCH_POLICY",
            "constant_policy_class": "branch_switch_policy",
            "policy_role": "declare whether branch and switch symbols are allowed before formula construction",
            "allowed_policy": "branches and switches must be predeclared and non-endpoint-selected",
            "blocked_policy": "choosing a branch after comparing no-dark and dark-sector family outcomes",
        },
        {
            "policy_id": "M0NDPCP12_NULL_FALLBACK_CONSTANT_POLICY",
            "constant_policy_class": "null_fallback_constant_policy",
            "policy_role": "prevent null and fallback routes from introducing hidden numerical constants",
            "allowed_policy": "null and fallback paths may block or route rows but may not inject fitted constants",
            "blocked_policy": "using fallback constants to repair failed predictions",
        },
        {
            "policy_id": "M0NDPCP12_HANDOFF_TO_DIMENSIONAL_TRACE",
            "constant_policy_class": "dimensional_trace_handoff",
            "policy_role": "handoff constant policy to the dimensional trace gate before formula body work",
            "allowed_policy": "the next artifact must audit dimensions before machine payload or scoring work",
            "blocked_policy": "moving from constant labels directly to formula or endpoint scoring",
        },
    ]
    for row in rows:
        row["completion_status"] = "READY"
        row["next_required_artifact"] = "m0_no_dark_payload_dimensional_trace_v12"
        row["forbidden_inputs"] = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_parameter_discount"
        row["policy_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_payload_constant_policy_only_policy_no_values_no_formula_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["completion_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    upstream_ready = symbol_binding_ready()
    return [
        {
            "summary_id": "M0_NO_DARK_PAYLOAD_CONSTANT_POLICY_V12",
            "constant_policy_artifact": "m0_no_dark_payload_constant_policy_v12",
            "symbol_binding_status": "READY" if upstream_ready else "BLOCKED",
            "policy_rows": len(rows),
            "ready_policy_rows": ready,
            "blocked_policy_rows": blocked,
            "constant_policy_written": "true" if upstream_ready and blocked == 0 else "false",
            "formula_body_written": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_PAYLOAD_CONSTANT_POLICY_READY_FOR_DIMENSIONAL_TRACE"
            if upstream_ready and blocked == 0
            else "M0_NO_DARK_PAYLOAD_CONSTANT_POLICY_BLOCKED",
            "next_required_artifact": "m0_no_dark_payload_dimensional_trace_v12",
            "claim_boundary": "m0_no_dark_payload_constant_policy_only_policy_no_values_no_formula_no_scores_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_payload_constant_policy_v12.md").write_text(
        """# M0 No-Dark Payload Constant Policy v12

**Doc class:** no-dark M0 payload constant-policy contract
**Status:** constant policy ready; dimensional trace blocked; no values; no formula; no scoring

Script:

```text
scripts/build_m0_no_dark_payload_constant_policy.py
```

Derived outputs:

```text
data/derived/m0_no_dark_payload_constant_policy_v12.csv
data/derived/m0_no_dark_payload_constant_policy_summary_v12.csv
```

This artifact declares the allowed constant, scale, branch, switch, and free
parameter policy classes before any formula body is written.

## Current Result

The expected status is:

```text
M0_NO_DARK_PAYLOAD_CONSTANT_POLICY_READY_FOR_DIMENSIONAL_TRACE
```

The next missing artifact is:

```text
m0_no_dark_payload_dimensional_trace_v12
```

## Claim Boundary

This constant-policy artifact does not assign numerical values, does not define
a velocity formula, does not compute predictions, does not score galaxies, and
does not decide the dark-sector question. It only fixes which constant and
switch policy classes are admissible before dimensional tracing.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = policy_rows()
    write_csv(DERIVED / "m0_no_dark_payload_constant_policy_v12.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_payload_constant_policy_summary_v12.csv",
        summary(rows),
        [
            "summary_id",
            "constant_policy_artifact",
            "symbol_binding_status",
            "policy_rows",
            "ready_policy_rows",
            "blocked_policy_rows",
            "constant_policy_written",
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
    print("PAPER11_M0_NO_DARK_PAYLOAD_CONSTANT_POLICY_V12_BUILT")


if __name__ == "__main__":
    main()
