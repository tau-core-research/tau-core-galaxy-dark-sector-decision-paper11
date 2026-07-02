#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
CONSTANT_POLICY_SUMMARY = DERIVED / "m0_no_dark_payload_constant_policy_summary_v12.csv"
PAYLOAD_SUMMARY = DERIVED / "m0_no_dark_frozen_expression_payload_summary_v11.csv"


FIELDNAMES = [
    "trace_id",
    "trace_class",
    "dimensional_role",
    "required_trace",
    "blocked_trace",
    "completion_status",
    "next_required_artifact",
    "forbidden_inputs",
    "trace_claim_allowed",
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


def constant_policy_ready() -> bool:
    if not CONSTANT_POLICY_SUMMARY.exists() or not PAYLOAD_SUMMARY.exists():
        return False
    constants = read_csv(CONSTANT_POLICY_SUMMARY)
    payload = read_csv(PAYLOAD_SUMMARY)
    return (
        len(constants) == 1
        and constants[0]["overall_status"] == "M0_NO_DARK_PAYLOAD_CONSTANT_POLICY_READY_FOR_DIMENSIONAL_TRACE"
        and constants[0]["endpoint_scoring_allowed_anywhere"] == "false"
        and len(payload) == 1
        and payload[0]["overall_status"]
        in {
            "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_READY_DIMENSIONAL_TRACE_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_READY_MACHINE_PAYLOAD_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_READY_PAYLOAD_LEAKAGE_CERTIFICATE_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_READY_FOR_KERNEL_EXPRESSION",
        }
        and payload[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def trace_rows() -> list[dict[str, object]]:
    rows = [
        {
            "trace_id": "M0NDPDT12_INPUT_DIMENSION_CLASSES",
            "trace_class": "input_dimension_classes",
            "dimensional_role": "classify source-state, baryonic, radial, readout, guard, and assembly symbols by unit role",
            "required_trace": "every bound payload symbol must have a declared dimension class or an explicit dimensionless guard role",
            "blocked_trace": "using an unclassified symbol in a later formula body",
        },
        {
            "trace_id": "M0NDPDT12_OPERATOR_DIMENSION_EFFECTS",
            "trace_class": "operator_dimension_effects",
            "dimensional_role": "declare how readout and assembly operations transform dimension classes",
            "required_trace": "operators may transform only declared input classes and must preserve a traceable output class",
            "blocked_trace": "operator effects chosen from endpoint residual shape or curve-fit convenience",
        },
        {
            "trace_id": "M0NDPDT12_CONSTANT_UNIT_COMPATIBILITY",
            "trace_class": "constant_unit_compatibility",
            "dimensional_role": "link constant-policy classes to unit compatibility without assigning values",
            "required_trace": "fixed, free, scale, branch, and fallback policy classes must expose their unit role before formula writing",
            "blocked_trace": "hidden numerical rescaling, posthoc unit normalization, or fitted conversion constants",
        },
        {
            "trace_id": "M0NDPDT12_OUTPUT_UNIT_TARGET",
            "trace_class": "output_unit_target",
            "dimensional_role": "declare the later velocity-readout target unit class",
            "required_trace": "the payload path must be capable of reaching velocity units before any v_pred_km_s rows are emitted",
            "blocked_trace": "claiming a velocity formula before the machine payload and leakage certificate exist",
        },
        {
            "trace_id": "M0NDPDT12_NULL_FALLBACK_DIMENSION_POLICY",
            "trace_class": "null_fallback_dimension_policy",
            "dimensional_role": "prevent null or fallback routes from repairing dimensional failures",
            "required_trace": "null and fallback routes may block invalid rows but cannot introduce compensating units or values",
            "blocked_trace": "dimension repair after seeing endpoint performance",
        },
        {
            "trace_id": "M0NDPDT12_HANDOFF_TO_MACHINE_PAYLOAD",
            "trace_class": "machine_payload_handoff",
            "dimensional_role": "handoff the dimensionally traced payload requirements to a later machine-readable payload",
            "required_trace": "the next artifact must serialize the inspected payload before predictions or scoring",
            "blocked_trace": "moving from dimensional trace directly to numeric prediction rows",
        },
    ]
    for row in rows:
        row["completion_status"] = "READY"
        row["next_required_artifact"] = "m0_no_dark_payload_machine_form_v12"
        row["forbidden_inputs"] = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_unit_rescale"
        row["trace_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_payload_dimensional_trace_only_unit_trace_no_formula_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["completion_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    upstream_ready = constant_policy_ready()
    return [
        {
            "summary_id": "M0_NO_DARK_PAYLOAD_DIMENSIONAL_TRACE_V12",
            "dimensional_trace_artifact": "m0_no_dark_payload_dimensional_trace_v12",
            "constant_policy_status": "READY" if upstream_ready else "BLOCKED",
            "trace_rows": len(rows),
            "ready_trace_rows": ready,
            "blocked_trace_rows": blocked,
            "dimensional_trace_written": "true" if upstream_ready and blocked == 0 else "false",
            "formula_body_written": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_PAYLOAD_DIMENSIONAL_TRACE_READY_FOR_MACHINE_PAYLOAD"
            if upstream_ready and blocked == 0
            else "M0_NO_DARK_PAYLOAD_DIMENSIONAL_TRACE_BLOCKED",
            "next_required_artifact": "m0_no_dark_payload_machine_form_v12",
            "claim_boundary": "m0_no_dark_payload_dimensional_trace_only_units_no_formula_no_values_no_scores_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_payload_dimensional_trace_v12.md").write_text(
        """# M0 No-Dark Payload Dimensional Trace v12

**Doc class:** no-dark M0 payload dimensional-trace contract
**Status:** dimensional trace ready; machine payload blocked; no formula; no scoring

Script:

```text
scripts/build_m0_no_dark_payload_dimensional_trace.py
```

Derived outputs:

```text
data/derived/m0_no_dark_payload_dimensional_trace_v12.csv
data/derived/m0_no_dark_payload_dimensional_trace_summary_v12.csv
```

This artifact records the required dimensional path from bound payload symbols
and constant-policy classes toward a later velocity-readout payload. It is a
unit-trace gate, not a velocity formula.

## Current Result

The expected status is:

```text
M0_NO_DARK_PAYLOAD_DIMENSIONAL_TRACE_READY_FOR_MACHINE_PAYLOAD
```

The next missing artifact is:

```text
m0_no_dark_payload_machine_form_v12
```

## Claim Boundary

This dimensional-trace artifact does not assign numerical values, does not
define a velocity formula, does not compute predictions, does not score
galaxies, and does not decide the dark-sector question. It only declares the
unit and dimensional admissibility path that the later machine-readable payload
must satisfy.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = trace_rows()
    write_csv(DERIVED / "m0_no_dark_payload_dimensional_trace_v12.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_payload_dimensional_trace_summary_v12.csv",
        summary(rows),
        [
            "summary_id",
            "dimensional_trace_artifact",
            "constant_policy_status",
            "trace_rows",
            "ready_trace_rows",
            "blocked_trace_rows",
            "dimensional_trace_written",
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
    print("PAPER11_M0_NO_DARK_PAYLOAD_DIMENSIONAL_TRACE_V12_BUILT")


if __name__ == "__main__":
    main()
