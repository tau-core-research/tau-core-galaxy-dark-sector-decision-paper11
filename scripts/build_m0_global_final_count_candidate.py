#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

NEXT_ARTIFACT = "m0_global_final_count_freeze_v15.csv"
STATUS = "M0_GLOBAL_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE"
CLAIM_BOUNDARY = "m0_global_final_count_candidate_only_no_freeze_no_parsimony_no_scores"

FIELDS = [
    "candidate_row_id",
    "family_id",
    "count_domain",
    "input_artifacts",
    "slot_count_rows_used",
    "resolved_zero_slot_rows",
    "unresolved_slot_rows",
    "adjustable_privileges_found",
    "candidate_k_m0_global",
    "candidate_status",
    "freeze_input_allowed",
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
    "adjustable_privileges_found",
    "candidate_k_m0_global",
    "final_count_frozen",
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
    ledger = read_csv(DERIVED / "m0_global_parameter_count_value_ledger_v12.csv")
    resolution = read_csv(DERIVED / "m0_global_adjustable_slot_resolution_v13.csv")
    fixed_zero = [row for row in ledger if row["resolution_needed"] == "false" and row["slot_count_value"] == "0"]
    resolved_zero = [row for row in resolution if row["slot_count_value"] == "0"]
    resolved_slots = {row["global_slot_name"] for row in resolution}
    unresolved_ledger_slots = [
        row for row in ledger if row["resolution_needed"] == "true" and row["global_slot_name"] not in resolved_slots
    ]
    unresolved_resolution_slots = [
        row for row in resolution if row["slot_resolution_status"] != "RESOLVED_ZERO_FIXED_SOURCE_SIDE_OR_GUARD"
    ]
    unresolved = unresolved_ledger_slots + unresolved_resolution_slots
    adjustable = [row for row in resolution if row["adjustable_privilege_found"] == "true"]
    slot_count_rows_used = len(fixed_zero) + len(resolved_zero)
    candidate = sum(int(row["slot_count_value"]) for row in fixed_zero + resolved_zero)
    status = STATUS if not unresolved and not adjustable and slot_count_rows_used == 6 else "M0_GLOBAL_FINAL_COUNT_CANDIDATE_V14_BLOCKED"
    return [
        {
            "candidate_row_id": "M0GFC14_001",
            "family_id": "M0",
            "count_domain": "global_formula_parameters",
            "input_artifacts": "m0_global_parameter_count_value_ledger_v12.csv;m0_global_adjustable_slot_resolution_v13.csv",
            "slot_count_rows_used": slot_count_rows_used,
            "resolved_zero_slot_rows": len(fixed_zero) + len(resolved_zero),
            "unresolved_slot_rows": len(unresolved),
            "adjustable_privileges_found": len(adjustable),
            "candidate_k_m0_global": candidate if status == STATUS else "CANDIDATE_BLOCKED",
            "candidate_status": status,
            "freeze_input_allowed": "true" if status == STATUS else "false",
            "parsimony_input_allowed": "false",
            "next_required_artifact": NEXT_ARTIFACT,
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_parameter_discount",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    row = rows[0]
    return [
        {
            "summary_id": "M0_GLOBAL_FINAL_COUNT_CANDIDATE_V14",
            "candidate_artifact": "m0_global_final_count_candidate_v14",
            "v12_ledger_status": summary_row("m0_global_parameter_count_value_ledger_summary_v12.csv")["overall_status"],
            "v13_resolution_status": summary_row("m0_global_adjustable_slot_resolution_summary_v13.csv")["overall_status"],
            "slot_count_rows_used": row["slot_count_rows_used"],
            "resolved_zero_slot_rows": row["resolved_zero_slot_rows"],
            "unresolved_slot_rows": row["unresolved_slot_rows"],
            "adjustable_privileges_found": row["adjustable_privileges_found"],
            "candidate_k_m0_global": row["candidate_k_m0_global"],
            "final_count_frozen": "false",
            "parsimony_scores_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": row["candidate_status"],
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_global_final_count_candidate_v14.md").write_text(
        f"""# M0 Global Final Count Candidate v14

**Doc class:** M0 global final-count candidate
**Reader role:** scoring-frontier parameter-count reviewer
**Status:** M0 global count candidate ready for freeze; no scoring
**Canonical parent:** M0 global adjustable-slot resolution v13

Script:

```text
scripts/build_m0_global_final_count_candidate.py
```

Derived outputs:

```text
data/derived/m0_global_final_count_candidate_v14.csv
data/derived/m0_global_final_count_candidate_summary_v14.csv
```

## Current Result

The v14 candidate combines the two zero-valued rows from the v12 count-value
ledger with the four conditional rows resolved by the v13 adjustable-slot
resolution. The resulting candidate M0 global count is recorded only as a
freeze input candidate.

The expected status is:

```text
{STATUS}
```

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This artifact does not freeze the final M0 global count, does not compute
parsimony, does not authorize endpoint scoring, and does not decide the
dark-sector question. It only creates a source-side candidate count for the
next freeze/audit gate.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = candidate_rows()
    write_csv(DERIVED / "m0_global_final_count_candidate_v14.csv", rows, FIELDS)
    write_csv(DERIVED / "m0_global_final_count_candidate_summary_v14.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER11_M0_GLOBAL_FINAL_COUNT_CANDIDATE_V14_BUILT")


if __name__ == "__main__":
    main()
