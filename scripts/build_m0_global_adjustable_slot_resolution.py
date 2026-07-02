#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

NEXT_ARTIFACT = "m0_global_final_count_candidate_v14.csv"
STATUS = "M0_GLOBAL_ADJUSTABLE_SLOT_RESOLUTION_V13_READY_FOR_FINAL_COUNT_CANDIDATE"
CLAIM_BOUNDARY = "m0_global_adjustable_slot_resolution_only_no_final_k_no_parsimony_no_scores"

FIELDS = [
    "resolution_row_id",
    "ledger_row_id",
    "readiness_id",
    "family_id",
    "global_slot_name",
    "prior_count_value_status",
    "slot_resolution_status",
    "slot_count_value",
    "resolution_evidence",
    "adjustable_privilege_found",
    "final_count_candidate_input_allowed",
    "parsimony_input_allowed",
    "next_required_artifact",
    "forbidden_inputs",
    "endpoint_scoring_allowed",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "resolution_artifact",
    "ledger_status",
    "conditional_rows_checked",
    "resolved_zero_rows",
    "unresolved_rows",
    "adjustable_privileges_found",
    "final_m0_global_count_candidate_ready",
    "final_m0_global_count_written",
    "parsimony_scores_written",
    "endpoint_scoring_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]

EVIDENCE_REQUIREMENTS = {
    "source_state": [
        (
            "m0_no_dark_expression_source_basis_v13.csv",
            "basis_id",
            "M0NDESB13_SOURCE_FREEZE_BASIS",
            "basis_status",
            "READY",
        ),
        (
            "m0_no_dark_payload_symbol_binding_table_v12.csv",
            "binding_id",
            "M0NDPSBT12_SOURCE_STATE_SYMBOL",
            "completion_status",
            "READY",
        ),
    ],
    "baryonic_input": [
        (
            "m0_no_dark_expression_source_basis_v13.csv",
            "basis_id",
            "M0NDESB13_BARYONIC_BINDING_BASIS",
            "basis_status",
            "READY",
        ),
        (
            "m0_no_dark_payload_symbol_binding_table_v12.csv",
            "binding_id",
            "M0NDPSBT12_BARYONIC_INPUT_SYMBOL",
            "completion_status",
            "READY",
        ),
        (
            "shared_scoring_input_table_v06.csv",
            "shared_input_id",
            "SSIT06_BARYONIC_COMPONENTS",
            "shared_input_status",
            "READY",
        ),
    ],
    "readout_operator": [
        (
            "m0_no_dark_readout_equation_contract_v08.csv",
            "equation_slot_id",
            "M0NDRE08_PARAMETERS",
            "completion_status",
            "READY",
        ),
        (
            "m0_no_dark_readout_equation_contract_v08.csv",
            "equation_slot_id",
            "M0NDRE08_SERIALIZATION",
            "completion_status",
            "READY",
        ),
        (
            "m0_no_dark_payload_symbol_binding_table_v12.csv",
            "binding_id",
            "M0NDPSBT12_READOUT_OPERATOR_SYMBOL",
            "completion_status",
            "READY",
        ),
    ],
    "failure_route": [
        (
            "m0_no_dark_fallback_policy_v07.csv",
            "fallback_policy_id",
            "M0NDFP07_FAILURE_REPORTING_ROUTE",
            "policy_status",
            "READY",
        ),
        (
            "m0_no_dark_expression_null_fallback_policy_v13.csv",
            "policy_id",
            "M0NDNFB13_FAILURE_ROUTE_POLICY",
            "policy_status",
            "READY",
        ),
        (
            "m0_no_dark_payload_symbol_binding_table_v12.csv",
            "binding_id",
            "M0NDPSBT12_GUARD_SYMBOL",
            "completion_status",
            "READY",
        ),
    ],
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def require_ready(filename: str, id_field: str, row_id: str, status_field: str, ready_value: str) -> str:
    rows = read_csv(DERIVED / filename)
    matches = [row for row in rows if row[id_field] == row_id]
    if len(matches) != 1:
        raise ValueError(f"expected one {row_id} row in {filename}")
    status = matches[0][status_field]
    if status != ready_value:
        raise ValueError(f"{row_id} in {filename} has {status_field}={status}, expected {ready_value}")
    return f"{filename}:{row_id}:{status_field}={ready_value}"


def ledger_status() -> str:
    rows = read_csv(DERIVED / "m0_global_parameter_count_value_ledger_summary_v12.csv")
    return rows[0]["overall_status"]


def resolution_rows() -> list[dict[str, object]]:
    ledger = read_csv(DERIVED / "m0_global_parameter_count_value_ledger_v12.csv")
    conditional = [row for row in ledger if row["resolution_needed"] == "true"]
    out: list[dict[str, object]] = []
    for index, row in enumerate(conditional, start=1):
        slot = row["global_slot_name"]
        evidence = [
            require_ready(filename, id_field, row_id, status_field, ready_value)
            for filename, id_field, row_id, status_field, ready_value in EVIDENCE_REQUIREMENTS[slot]
        ]
        out.append(
            {
                "resolution_row_id": f"M0GASR13_{index:03d}",
                "ledger_row_id": row["ledger_row_id"],
                "readiness_id": row["readiness_id"],
                "family_id": row["family_id"],
                "global_slot_name": slot,
                "prior_count_value_status": row["count_value_status"],
                "slot_resolution_status": "RESOLVED_ZERO_FIXED_SOURCE_SIDE_OR_GUARD",
                "slot_count_value": "0",
                "resolution_evidence": ";".join(evidence),
                "adjustable_privilege_found": "false",
                "final_count_candidate_input_allowed": "true",
                "parsimony_input_allowed": "false",
                "next_required_artifact": NEXT_ARTIFACT,
                "forbidden_inputs": row["forbidden_inputs"],
                "endpoint_scoring_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    unresolved = sum(row["slot_resolution_status"] != "RESOLVED_ZERO_FIXED_SOURCE_SIDE_OR_GUARD" for row in rows)
    privileges = sum(row["adjustable_privilege_found"] == "true" for row in rows)
    return [
        {
            "summary_id": "M0_GLOBAL_ADJUSTABLE_SLOT_RESOLUTION_V13",
            "resolution_artifact": "m0_global_adjustable_slot_resolution_v13",
            "ledger_status": ledger_status(),
            "conditional_rows_checked": len(rows),
            "resolved_zero_rows": sum(row["slot_count_value"] == "0" for row in rows),
            "unresolved_rows": unresolved,
            "adjustable_privileges_found": privileges,
            "final_m0_global_count_candidate_ready": "true" if unresolved == 0 and privileges == 0 else "false",
            "final_m0_global_count_written": "false",
            "parsimony_scores_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": STATUS if unresolved == 0 and privileges == 0 else "M0_GLOBAL_ADJUSTABLE_SLOT_RESOLUTION_V13_UNRESOLVED",
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_global_adjustable_slot_resolution_v13.md").write_text(
        f"""# M0 Global Adjustable Slot Resolution v13

**Doc class:** M0 global adjustable-slot resolution ledger
**Reader role:** scoring-frontier parameter-count reviewer
**Status:** conditional M0 global slots resolved for final-count candidate
**Canonical parent:** M0 global parameter count-value ledger v12

Script:

```text
scripts/build_m0_global_adjustable_slot_resolution.py
```

Derived outputs:

```text
data/derived/m0_global_adjustable_slot_resolution_v13.csv
data/derived/m0_global_adjustable_slot_resolution_summary_v13.csv
```

## Current Result

The v13 resolution checks the four conditional M0 global slots left open by the
v12 count-value ledger: source state, baryonic input, readout operator, and
failure route. Each slot is resolved as a zero-count slot only when pre-score
source-basis, symbol-binding, shared-input, readout-contract, or fallback-policy
evidence is already `READY`.

The expected status is:

```text
{STATUS}
```

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This artifact does not write the final M0 global parameter count, does not
compute parsimony, does not authorize endpoint scoring, and does not decide the
dark-sector question. It only records that the conditional M0 global slots have
source-side or guard evidence sufficient for a later final-count candidate.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = resolution_rows()
    write_csv(DERIVED / "m0_global_adjustable_slot_resolution_v13.csv", rows, FIELDS)
    write_csv(DERIVED / "m0_global_adjustable_slot_resolution_summary_v13.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER11_M0_GLOBAL_ADJUSTABLE_SLOT_RESOLUTION_V13_BUILT")


if __name__ == "__main__":
    main()
