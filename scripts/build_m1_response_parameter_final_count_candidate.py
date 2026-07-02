#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

NEXT_ARTIFACT = "m1_response_parameter_final_count_freeze_v15.csv"
STATUS = "M1_RESPONSE_PARAMETER_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE"
CLAIM_BOUNDARY = "m1_response_parameter_final_count_candidate_only_no_freeze_no_response_values_no_scores"

FIELDS = [
    "candidate_row_id",
    "family_id",
    "count_domain",
    "input_artifacts",
    "slot_count_rows_used",
    "resolved_zero_slot_rows",
    "unresolved_slot_rows",
    "adjustable_response_parameters_found",
    "candidate_k_m1_global",
    "candidate_status",
    "freeze_input_allowed",
    "response_value_input_allowed",
    "parsimony_input_allowed",
    "next_required_artifact",
    "forbidden_inputs",
    "endpoint_scoring_allowed",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "candidate_artifact",
    "v12_ledger_status",
    "v13_resolution_status",
    "slot_count_rows_used",
    "resolved_zero_slot_rows",
    "unresolved_slot_rows",
    "adjustable_response_parameters_found",
    "candidate_k_m1_global",
    "final_count_frozen",
    "numeric_response_values_written",
    "parsimony_scores_written",
    "endpoint_scoring_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
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


def summary_row(filename: str) -> dict[str, str]:
    rows = read_csv(DERIVED / filename)
    if len(rows) != 1:
        raise ValueError(f"expected one summary row in {filename}")
    return rows[0]


def candidate_rows() -> list[dict[str, object]]:
    ledger = read_csv(DERIVED / "m1_response_parameter_count_value_ledger_v12.csv")
    resolution = read_csv(DERIVED / "m1_response_parameter_adjustable_slot_resolution_v13.csv")

    fixed_zero = [row for row in ledger if row["resolution_needed"] == "false" and row["slot_count_value"] == "0"]
    resolved_zero = [row for row in resolution if row["slot_count_value"] == "0"]
    resolved_components = {row["response_component"] for row in resolution}
    unresolved_ledger_slots = [
        row for row in ledger if row["resolution_needed"] == "true" and row["response_component"] not in resolved_components
    ]
    unresolved_resolution_slots = [
        row
        for row in resolution
        if row["slot_resolution_status"] != "RESOLVED_ZERO_INACTIVE_OR_PLACEHOLDER_RESPONSE_SLOT"
    ]
    unresolved = unresolved_ledger_slots + unresolved_resolution_slots
    adjustable = [row for row in resolution if row["adjustable_response_parameter_found"] == "true"]
    slot_count_rows_used = len(fixed_zero) + len(resolved_zero)
    candidate = sum(int(row["slot_count_value"]) for row in fixed_zero + resolved_zero)
    status = (
        STATUS
        if not unresolved and not adjustable and slot_count_rows_used == 6
        else "M1_RESPONSE_PARAMETER_FINAL_COUNT_CANDIDATE_V14_BLOCKED"
    )

    return [
        {
            "candidate_row_id": "M1RPFC14_001",
            "family_id": "M1",
            "count_domain": "global_response_parameters",
            "input_artifacts": "m1_response_parameter_count_value_ledger_v12.csv;m1_response_parameter_adjustable_slot_resolution_v13.csv",
            "slot_count_rows_used": slot_count_rows_used,
            "resolved_zero_slot_rows": len(fixed_zero) + len(resolved_zero),
            "unresolved_slot_rows": len(unresolved),
            "adjustable_response_parameters_found": len(adjustable),
            "candidate_k_m1_global": candidate if status == STATUS else "CANDIDATE_BLOCKED",
            "candidate_status": status,
            "freeze_input_allowed": "true" if status == STATUS else "false",
            "response_value_input_allowed": "false",
            "parsimony_input_allowed": "false",
            "next_required_artifact": NEXT_ARTIFACT,
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_response_activation;posthoc_response_amplitude;numeric_score_value",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    row = rows[0]
    return [
        {
            "summary_id": "M1_RESPONSE_PARAMETER_FINAL_COUNT_CANDIDATE_V14",
            "candidate_artifact": "m1_response_parameter_final_count_candidate_v14",
            "v12_ledger_status": summary_row("m1_response_parameter_count_value_ledger_summary_v12.csv")["overall_status"],
            "v13_resolution_status": summary_row("m1_response_parameter_adjustable_slot_resolution_summary_v13.csv")[
                "overall_status"
            ],
            "slot_count_rows_used": row["slot_count_rows_used"],
            "resolved_zero_slot_rows": row["resolved_zero_slot_rows"],
            "unresolved_slot_rows": row["unresolved_slot_rows"],
            "adjustable_response_parameters_found": row["adjustable_response_parameters_found"],
            "candidate_k_m1_global": row["candidate_k_m1_global"],
            "final_count_frozen": "false",
            "numeric_response_values_written": 0,
            "parsimony_scores_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": row["candidate_status"],
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m1_response_parameter_final_count_candidate_v14.md").write_text(
        f"""# M1 Response Parameter Final Count Candidate v14

**Doc class:** M1 response-parameter final-count candidate
**Reader role:** scoring-frontier parameter-count reviewer
**Status:** M1 global response-parameter count candidate ready for freeze; no response values; no scoring
**Canonical parent:** M1 response-parameter adjustable-slot resolution v13

Script:

```text
scripts/build_m1_response_parameter_final_count_candidate.py
```

Derived outputs:

```text
data/derived/m1_response_parameter_final_count_candidate_v14.csv
data/derived/m1_response_parameter_final_count_candidate_summary_v14.csv
```

## Current Result

The v14 candidate combines the three zero-valued guard rows from the v12
count-value ledger with the three conditional rows resolved by the v13
adjustable-slot resolution. The resulting candidate M1 global count is recorded
only as a freeze input candidate.

The expected status is:

```text
{STATUS}
```

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This artifact does not freeze the final M1 global count, does not write
`Response_tau`, does not write numeric response values, does not compute
parsimony, does not authorize endpoint scoring, and does not decide whether a
Tau response or dark-sector layer is physically absent or necessary. It only
creates a protocol-local candidate count for the next freeze/audit gate.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = candidate_rows()
    write_csv(DERIVED / "m1_response_parameter_final_count_candidate_v14.csv", rows, FIELDS)
    write_csv(DERIVED / "m1_response_parameter_final_count_candidate_summary_v14.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER11_M1_RESPONSE_PARAMETER_FINAL_COUNT_CANDIDATE_V14_BUILT")


if __name__ == "__main__":
    main()
