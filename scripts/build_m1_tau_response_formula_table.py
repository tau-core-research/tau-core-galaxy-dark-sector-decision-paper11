#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDS = [
    "response_table_id",
    "family_id",
    "formula_slot",
    "response_component",
    "component_scope",
    "frozen_statement",
    "allowed_values",
    "blocked_until",
    "response_tau_formula_claimed",
    "numeric_response_values_written",
    "family_prediction_rows_written",
    "endpoint_scoring_allowed",
    "forbidden_inputs",
    "next_required_artifact",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "response_formula_table_artifact",
    "family_id",
    "formula_slot",
    "response_components",
    "response_tau_formula_claimed",
    "numeric_response_values_written",
    "family_prediction_rows_written",
    "endpoint_scoring_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]

NEXT_ARTIFACT = "m1_admissibility_table_v06"
FORBIDDEN_INPUTS = (
    "endpoint_residual;heldout_score;family_winner;best_fit_curve;"
    "posthoc_response_activation;posthoc_response_amplitude;numeric_score_value"
)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def response_rows() -> list[dict[str, object]]:
    base = {
        "family_id": "M1",
        "formula_slot": "tau_response_formula",
        "response_tau_formula_claimed": "false",
        "numeric_response_values_written": "0",
        "family_prediction_rows_written": "0",
        "endpoint_scoring_allowed": "false",
        "forbidden_inputs": FORBIDDEN_INPUTS,
        "next_required_artifact": NEXT_ARTIFACT,
        "claim_boundary": "m1_tau_response_formula_table_only_no_response_tau_formula_no_predictions_no_scores",
    }
    return [
        {
            **base,
            "response_table_id": "M1TRFT06_ACTIVATION",
            "response_component": "activation_rule",
            "component_scope": "source_side_response_candidate_activation",
            "frozen_statement": "M1 response activation must be decided by a later admissibility table before endpoint scoring.",
            "allowed_values": "RESPONSE_INACTIVE;RESPONSE_ADMISSIBILITY_PENDING;RESPONSE_ACTIVE_ONLY_IF_ADMISSIBLE",
            "blocked_until": "m1_admissibility_table_v06",
        },
        {
            **base,
            "response_table_id": "M1TRFT06_CARRIER",
            "response_component": "carrier",
            "component_scope": "tau_base_substrate_response_carrier_placeholder",
            "frozen_statement": "The response carrier slot is declared as a protocol placeholder, not a physical field theorem.",
            "allowed_values": "TAU_RESPONSE_CARRIER_UNSPECIFIED;TAU_RESPONSE_CARRIER_ADMISSIBILITY_PENDING",
            "blocked_until": "m1_admissibility_table_v06",
        },
        {
            **base,
            "response_table_id": "M1TRFT06_AMPLITUDE",
            "response_component": "amplitude_law",
            "component_scope": "response_amplitude_placeholder",
            "frozen_statement": "No numeric response amplitude is written before admissibility and parameter-count gates.",
            "allowed_values": "NO_NUMERIC_AMPLITUDE;AMPLITUDE_POLICY_PENDING",
            "blocked_until": "m1_admissibility_table_v06",
        },
        {
            **base,
            "response_table_id": "M1TRFT06_SCALE",
            "response_component": "scale_law",
            "component_scope": "response_scale_placeholder",
            "frozen_statement": "No response scale is selected from endpoint residuals or held-out scores.",
            "allowed_values": "NO_NUMERIC_SCALE;SCALE_POLICY_PENDING",
            "blocked_until": "m1_admissibility_table_v06",
        },
        {
            **base,
            "response_table_id": "M1TRFT06_HANDOFF",
            "response_component": "channel_handoff",
            "component_scope": "family_prediction_table_handoff",
            "frozen_statement": "M1 cannot write family prediction rows until admissibility, parameter count, and response value gates are closed.",
            "allowed_values": "NO_M1_PREDICTION_ROWS;HANDOFF_BLOCKED_PENDING_ADMISSIBILITY",
            "blocked_until": "m1_admissibility_table_v06",
        },
        {
            **base,
            "response_table_id": "M1TRFT06_ZERO_RESPONSE",
            "response_component": "zero_response_policy",
            "component_scope": "inactive_or_inadmissible_response_cases",
            "frozen_statement": "Inactive or inadmissible M1 response routes must remain explicit zero-response cases, not fitted rescue terms.",
            "allowed_values": "ZERO_RESPONSE_IF_INACTIVE;ZERO_RESPONSE_IF_INADMISSIBLE;NO_POSTHOC_RESCUE",
            "blocked_until": "m1_admissibility_table_v06",
        },
    ]


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "M1_TAU_RESPONSE_FORMULA_TABLE_V06",
            "response_formula_table_artifact": "m1_tau_response_formula_table_v06",
            "family_id": "M1",
            "formula_slot": "tau_response_formula",
            "response_components": len(rows),
            "response_tau_formula_claimed": "false",
            "numeric_response_values_written": "0",
            "family_prediction_rows_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M1_TAU_RESPONSE_FORMULA_TABLE_READY_ADMISSIBILITY_BLOCKED",
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": "m1_tau_response_formula_table_only_no_response_tau_formula_no_predictions_no_scores",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m1_tau_response_formula_table_v06.md").write_text(
        f"""# M1 Tau Response Formula Table v06

**Doc class:** M1 response-formula table contract
**Status:** response slot table ready; admissibility blocked; no Response_tau formula

Script:

```text
scripts/build_m1_tau_response_formula_table.py
```

Derived outputs:

```text
data/derived/m1_tau_response_formula_table_v06.csv
data/derived/m1_tau_response_formula_table_summary_v06.csv
```

This artifact fills the M1 `tau_response_formula` formula-table slot as a
pre-scoring contract. It freezes the required response components: activation
rule, carrier slot, amplitude policy, scale policy, channel handoff, and
zero-response policy.

## Current Result

The expected status is:

```text
M1_TAU_RESPONSE_FORMULA_TABLE_READY_ADMISSIBILITY_BLOCKED
```

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This table does not claim a `Response_tau` formula, does not claim a physical
Tau response field, writes no numeric response values, writes no M1 prediction
rows, computes no endpoint scores, and makes no dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = response_rows()
    write_csv(DERIVED / "m1_tau_response_formula_table_v06.csv", rows, FIELDS)
    write_csv(DERIVED / "m1_tau_response_formula_table_summary_v06.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER11_M1_TAU_RESPONSE_FORMULA_TABLE_V06_BUILT")


if __name__ == "__main__":
    main()
