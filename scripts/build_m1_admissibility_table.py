#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDS = [
    "admissibility_id",
    "family_id",
    "formula_slot",
    "response_component",
    "admissibility_class",
    "admissibility_rule",
    "admissible_handoff",
    "zero_response_condition",
    "exception_policy",
    "forbidden_inputs",
    "admissibility_status",
    "response_tau_formula_claim_allowed",
    "numeric_response_values_allowed",
    "family_prediction_rows_written",
    "endpoint_scoring_allowed",
    "next_required_artifact",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "admissibility_artifact",
    "response_formula_table_status",
    "family_id",
    "formula_slot",
    "admissibility_rows",
    "ready_admissibility_rows",
    "blocked_admissibility_rows",
    "response_tau_formula_claim_allowed",
    "numeric_response_values_allowed",
    "family_prediction_rows_written",
    "endpoint_scoring_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]

NEXT_ARTIFACT = "m2_benchmark_profile_table_v06"
FORBIDDEN_INPUTS = (
    "endpoint_residual;heldout_score;family_winner;best_fit_curve;"
    "posthoc_admissibility;posthoc_response_activation;posthoc_response_amplitude"
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def response_table_ready() -> bool:
    path = DERIVED / "m1_tau_response_formula_table_summary_v06.csv"
    if not path.exists():
        return False
    rows = read_csv(path)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M1_TAU_RESPONSE_FORMULA_TABLE_READY_ADMISSIBILITY_BLOCKED"
        and rows[0]["response_tau_formula_claimed"] == "false"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def admissibility_rows() -> list[dict[str, object]]:
    base = {
        "family_id": "M1",
        "formula_slot": "response_admissibility_rule",
        "forbidden_inputs": FORBIDDEN_INPUTS,
        "admissibility_status": "READY",
        "response_tau_formula_claim_allowed": "false",
        "numeric_response_values_allowed": "false",
        "family_prediction_rows_written": "0",
        "endpoint_scoring_allowed": "false",
        "next_required_artifact": NEXT_ARTIFACT,
        "claim_boundary": "m1_admissibility_table_only_no_response_tau_formula_no_values_no_predictions_no_scores",
    }
    return [
        {
            **base,
            "admissibility_id": "M1ADM06_SOURCE_FREEZE",
            "response_component": "activation_rule",
            "admissibility_class": "source_freeze_admissibility",
            "admissibility_rule": "M1 response activation may depend only on pre-scoring source-side response-candidate records.",
            "admissible_handoff": "activation_candidate_admissible_if_source_frozen",
            "zero_response_condition": "missing_or_unreviewed_source_candidate",
            "exception_policy": "record_exception_as_zero_response_candidate_without_row_drop",
        },
        {
            **base,
            "admissibility_id": "M1ADM06_NON_CIRCULARITY",
            "response_component": "carrier",
            "admissibility_class": "non_circularity_guard",
            "admissibility_rule": "The carrier placeholder may not be selected or retyped from endpoint residuals, held-out scores, or the family winner.",
            "admissible_handoff": "carrier_slot_admissible_only_as_predeclared_placeholder",
            "zero_response_condition": "carrier_selected_from_endpoint_information",
            "exception_policy": "mark carrier route inadmissible and force zero response",
        },
        {
            **base,
            "admissibility_id": "M1ADM06_NO_POSTHOC_RESCUE",
            "response_component": "amplitude_law",
            "admissibility_class": "no_posthoc_rescue_guard",
            "admissibility_rule": "Amplitude policy may not introduce a compensating fitted rescue term before a lawful value-freeze gate exists.",
            "admissible_handoff": "amplitude_policy_pending_value_freeze",
            "zero_response_condition": "amplitude_chosen_from_residual_or_best_fit_curve",
            "exception_policy": "reject amplitude route and preserve no-score state",
        },
        {
            **base,
            "admissibility_id": "M1ADM06_SCALE_GUARD",
            "response_component": "scale_law",
            "admissibility_class": "scale_readout_guard",
            "admissibility_rule": "Scale policy must remain source-side and cannot be tuned by radial-zone score improvement.",
            "admissible_handoff": "scale_policy_pending_source_side_freeze",
            "zero_response_condition": "scale_selected_from_inner_or_outer_zone_score",
            "exception_policy": "route to zero response and require new frozen scale artifact",
        },
        {
            **base,
            "admissibility_id": "M1ADM06_ZERO_RESPONSE",
            "response_component": "zero_response_policy",
            "admissibility_class": "zero_response_guard",
            "admissibility_rule": "Inactive, missing, or inadmissible M1 response cases must be represented as explicit zero-response routes.",
            "admissible_handoff": "zero_response_cases_preserved_for_parameter_count",
            "zero_response_condition": "inactive_missing_or_inadmissible_response",
            "exception_policy": "zero route cannot be replaced by a fitted weak response",
        },
        {
            **base,
            "admissibility_id": "M1ADM06_HANDOFF",
            "response_component": "channel_handoff",
            "admissibility_class": "prediction_handoff_guard",
            "admissibility_rule": "M1 may not write prediction rows until later response-value, parameter-count, and benchmark-comparison gates are closed.",
            "admissible_handoff": "admissibility_contract_ready_no_prediction_rows",
            "zero_response_condition": "downstream_value_or_count_gate_missing",
            "exception_policy": "keep family prediction table blocked for M1",
        },
    ]


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["admissibility_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    upstream_ready = response_table_ready()
    return [
        {
            "summary_id": "M1_ADMISSIBILITY_TABLE_V06",
            "admissibility_artifact": "m1_admissibility_table_v06",
            "response_formula_table_status": "READY" if upstream_ready else "BLOCKED",
            "family_id": "M1",
            "formula_slot": "response_admissibility_rule",
            "admissibility_rows": len(rows),
            "ready_admissibility_rows": ready if upstream_ready else 0,
            "blocked_admissibility_rows": blocked if upstream_ready else len(rows),
            "response_tau_formula_claim_allowed": "false",
            "numeric_response_values_allowed": "false",
            "family_prediction_rows_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M1_ADMISSIBILITY_TABLE_READY_M2_BENCHMARK_BLOCKED"
            if upstream_ready and blocked == 0
            else "M1_ADMISSIBILITY_TABLE_BLOCKED",
            "next_required_artifact": NEXT_ARTIFACT if upstream_ready and blocked == 0 else "m1_tau_response_formula_table_v06",
            "claim_boundary": "m1_admissibility_table_only_no_response_tau_formula_no_values_no_predictions_no_scores",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m1_admissibility_table_v06.md").write_text(
        f"""# M1 Admissibility Table v06

**Doc class:** M1 response-admissibility rule table
**Status:** admissibility table ready; benchmark profile blocked; no response values

Script:

```text
scripts/build_m1_admissibility_table.py
```

Derived outputs:

```text
data/derived/m1_admissibility_table_v06.csv
data/derived/m1_admissibility_table_summary_v06.csv
```

This artifact fills the M1 `response_admissibility_rule` slot as a pre-scoring
contract. It checks source-freeze admissibility, non-circularity, no posthoc
rescue, scale/readout guarding, explicit zero-response cases, and channel
handoff discipline.

## Current Result

The expected status is:

```text
M1_ADMISSIBILITY_TABLE_READY_M2_BENCHMARK_BLOCKED
```

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This table does not claim a `Response_tau` formula, does not prove a physical
Tau response field, writes no numeric response values, writes no M1 prediction
rows, computes no endpoint scores, and makes no dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = admissibility_rows()
    write_csv(DERIVED / "m1_admissibility_table_v06.csv", rows, FIELDS)
    write_csv(DERIVED / "m1_admissibility_table_summary_v06.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER11_M1_ADMISSIBILITY_TABLE_V06_BUILT")


if __name__ == "__main__":
    main()
