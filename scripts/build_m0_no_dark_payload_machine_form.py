#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
DIMENSIONAL_TRACE_SUMMARY = DERIVED / "m0_no_dark_payload_dimensional_trace_summary_v12.csv"
PAYLOAD_SUMMARY = DERIVED / "m0_no_dark_frozen_expression_payload_summary_v11.csv"


FIELDNAMES = [
    "machine_payload_id",
    "serialization_class",
    "payload_role",
    "required_payload_fields",
    "blocked_runtime_behavior",
    "completion_status",
    "next_required_artifact",
    "forbidden_inputs",
    "machine_payload_claim_allowed",
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


def dimensional_trace_ready() -> bool:
    if not DIMENSIONAL_TRACE_SUMMARY.exists() or not PAYLOAD_SUMMARY.exists():
        return False
    trace = read_csv(DIMENSIONAL_TRACE_SUMMARY)
    payload = read_csv(PAYLOAD_SUMMARY)
    return (
        len(trace) == 1
        and trace[0]["overall_status"] == "M0_NO_DARK_PAYLOAD_DIMENSIONAL_TRACE_READY_FOR_MACHINE_PAYLOAD"
        and trace[0]["endpoint_scoring_allowed_anywhere"] == "false"
        and len(payload) == 1
        and payload[0]["overall_status"]
        in {
            "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_READY_MACHINE_PAYLOAD_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_READY_PAYLOAD_LEAKAGE_CERTIFICATE_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_READY_FOR_KERNEL_EXPRESSION",
        }
        and payload[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def machine_payload_rows() -> list[dict[str, object]]:
    rows = [
        {
            "machine_payload_id": "M0NDPMF12_SOURCE_STATE_PAYLOAD",
            "serialization_class": "source_state_payload",
            "payload_role": "serialize source-state and morphology/readout handles as typed payload inputs",
            "required_payload_fields": "source_state_id;source_route_id;morphology_handle;readout_handle;unit_guard_id",
            "blocked_runtime_behavior": "derive_source_state_or_morphology_handle_from_endpoint_residual",
        },
        {
            "machine_payload_id": "M0NDPMF12_BARYONIC_RADIAL_PAYLOAD",
            "serialization_class": "baryonic_radial_payload",
            "payload_role": "serialize imported baryonic and radial-grid handles without resampling or fitted scaling",
            "required_payload_fields": "baryonic_input_id;radius_grid_id;radius_unit_class;source_provenance_guard",
            "blocked_runtime_behavior": "choose_baryonic_proxy_or_radial_sampling_from_best_fit_curve",
        },
        {
            "machine_payload_id": "M0NDPMF12_OPERATOR_GUARD_PAYLOAD",
            "serialization_class": "operator_guard_payload",
            "payload_role": "serialize readout operators, guards, null routes, and fallback stop states",
            "required_payload_fields": "operator_slot_id;guard_id;null_route_id;fallback_policy_id;stop_condition",
            "blocked_runtime_behavior": "select_operator_or_guard_after_family_winner_is_known",
        },
        {
            "machine_payload_id": "M0NDPMF12_CONSTANT_POLICY_PAYLOAD",
            "serialization_class": "constant_policy_payload",
            "payload_role": "serialize fixed/free/scale/branch policy classes without assigning numerical values",
            "required_payload_fields": "constant_policy_id;unit_role;free_or_fixed_status;branch_policy_id;scale_policy_id",
            "blocked_runtime_behavior": "inject_value_prior_bound_or_conversion_factor_from_heldout_score",
        },
        {
            "machine_payload_id": "M0NDPMF12_DIMENSION_TRACE_PAYLOAD",
            "serialization_class": "dimension_trace_payload",
            "payload_role": "serialize the dimensional path and output-unit target inspected by the previous trace gate",
            "required_payload_fields": "input_dimension_class;operator_dimension_effect;output_unit_target;dimension_stop_guard",
            "blocked_runtime_behavior": "repair_dimension_failure_with_posthoc_unit_rescale",
        },
        {
            "machine_payload_id": "M0NDPMF12_HANDOFF_TO_LEAKAGE_CERTIFICATE",
            "serialization_class": "leakage_certificate_handoff",
            "payload_role": "handoff the machine-inspectable payload to a payload-level leakage certificate",
            "required_payload_fields": "payload_manifest_id;serialization_hash_policy;forbidden_input_manifest;leakage_certificate_blocker_id",
            "blocked_runtime_behavior": "execute_prediction_callable_or_emit_v_pred_km_s_rows",
        },
    ]
    for row in rows:
        row["completion_status"] = "READY"
        row["next_required_artifact"] = "m0_no_dark_payload_leakage_certificate_v12"
        row["forbidden_inputs"] = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_callable_switch"
        row["machine_payload_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_payload_machine_form_only_serialized_payload_contract_no_formula_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["completion_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    upstream_ready = dimensional_trace_ready()
    return [
        {
            "summary_id": "M0_NO_DARK_PAYLOAD_MACHINE_FORM_V12",
            "machine_payload_artifact": "m0_no_dark_payload_machine_form_v12",
            "dimensional_trace_status": "READY" if upstream_ready else "BLOCKED",
            "machine_payload_rows": len(rows),
            "ready_machine_payload_rows": ready,
            "blocked_machine_payload_rows": blocked,
            "machine_payload_written": "true" if upstream_ready and blocked == 0 else "false",
            "prediction_callable_written": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_PAYLOAD_MACHINE_FORM_READY_FOR_LEAKAGE_CERTIFICATE"
            if upstream_ready and blocked == 0
            else "M0_NO_DARK_PAYLOAD_MACHINE_FORM_BLOCKED",
            "next_required_artifact": "m0_no_dark_payload_leakage_certificate_v12",
            "claim_boundary": "m0_no_dark_payload_machine_form_only_serialization_no_formula_no_values_no_scores_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_payload_machine_form_v12.md").write_text(
        """# M0 No-Dark Payload Machine Form v12

**Doc class:** no-dark M0 payload machine-form contract
**Status:** machine payload ready; leakage certificate blocked; no formula; no scoring

Script:

```text
scripts/build_m0_no_dark_payload_machine_form.py
```

Derived outputs:

```text
data/derived/m0_no_dark_payload_machine_form_v12.csv
data/derived/m0_no_dark_payload_machine_form_summary_v12.csv
```

This artifact serializes the payload contract into inspectable machine-readable
slots. It records source-state, baryonic/radial, operator/guard,
constant-policy, dimensional-trace, and leakage-certificate handoff records.

## Current Result

The expected status is:

```text
M0_NO_DARK_PAYLOAD_MACHINE_FORM_READY_FOR_LEAKAGE_CERTIFICATE
```

The next missing artifact is:

```text
m0_no_dark_payload_leakage_certificate_v12
```

## Claim Boundary

This machine-form artifact does not assign numerical values, does not define a
velocity formula, does not expose a prediction callable, does not compute
predictions, does not score galaxies, and does not decide the dark-sector
question. It only serializes the already-gated payload so that a later leakage
certificate can verify that no endpoint information entered it.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = machine_payload_rows()
    write_csv(DERIVED / "m0_no_dark_payload_machine_form_v12.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_payload_machine_form_summary_v12.csv",
        summary(rows),
        [
            "summary_id",
            "machine_payload_artifact",
            "dimensional_trace_status",
            "machine_payload_rows",
            "ready_machine_payload_rows",
            "blocked_machine_payload_rows",
            "machine_payload_written",
            "prediction_callable_written",
            "formula_claim_allowed",
            "numeric_predictions_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_PAYLOAD_MACHINE_FORM_V12_BUILT")


if __name__ == "__main__":
    main()
