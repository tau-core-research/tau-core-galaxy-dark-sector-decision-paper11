#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

NEXT_ARTIFACT = "m1_response_parameter_final_count_candidate_v14.csv"
STATUS = "M1_RESPONSE_PARAMETER_ADJUSTABLE_SLOT_RESOLUTION_V13_READY_FOR_FINAL_COUNT_CANDIDATE"
CLAIM_BOUNDARY = "m1_response_parameter_adjustable_slot_resolution_only_no_final_k_no_response_values_no_scores"

FIELDS = [
    "resolution_row_id",
    "ledger_row_id",
    "readiness_id",
    "family_id",
    "response_component",
    "prior_count_value_status",
    "slot_resolution_status",
    "slot_count_value",
    "resolution_evidence",
    "adjustable_response_parameter_found",
    "final_count_candidate_input_allowed",
    "response_value_input_allowed",
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
    "adjustable_response_parameters_found",
    "final_m1_global_count_candidate_ready",
    "final_m1_global_count_written",
    "numeric_response_values_written",
    "parsimony_scores_written",
    "endpoint_scoring_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]

EVIDENCE_REQUIREMENTS = {
    "carrier": [
        ("m1_tau_response_formula_table_v06.csv", "response_table_id", "M1TRFT06_CARRIER", "numeric_response_values_written", "0"),
        ("m1_tau_response_formula_table_v06.csv", "response_table_id", "M1TRFT06_CARRIER", "response_tau_formula_claimed", "false"),
        ("m1_admissibility_table_v06.csv", "admissibility_id", "M1ADM06_NON_CIRCULARITY", "admissibility_status", "READY"),
        ("m1_admissibility_table_v06.csv", "admissibility_id", "M1ADM06_NON_CIRCULARITY", "numeric_response_values_allowed", "false"),
    ],
    "amplitude_law": [
        ("m1_tau_response_formula_table_v06.csv", "response_table_id", "M1TRFT06_AMPLITUDE", "numeric_response_values_written", "0"),
        ("m1_tau_response_formula_table_v06.csv", "response_table_id", "M1TRFT06_AMPLITUDE", "response_tau_formula_claimed", "false"),
        ("m1_admissibility_table_v06.csv", "admissibility_id", "M1ADM06_NO_POSTHOC_RESCUE", "admissibility_status", "READY"),
        ("m1_admissibility_table_v06.csv", "admissibility_id", "M1ADM06_NO_POSTHOC_RESCUE", "numeric_response_values_allowed", "false"),
    ],
    "scale_law": [
        ("m1_tau_response_formula_table_v06.csv", "response_table_id", "M1TRFT06_SCALE", "numeric_response_values_written", "0"),
        ("m1_tau_response_formula_table_v06.csv", "response_table_id", "M1TRFT06_SCALE", "response_tau_formula_claimed", "false"),
        ("m1_admissibility_table_v06.csv", "admissibility_id", "M1ADM06_SCALE_GUARD", "admissibility_status", "READY"),
        ("m1_admissibility_table_v06.csv", "admissibility_id", "M1ADM06_SCALE_GUARD", "numeric_response_values_allowed", "false"),
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


def require_value(filename: str, id_field: str, row_id: str, status_field: str, ready_value: str) -> str:
    rows = read_csv(DERIVED / filename)
    matches = [row for row in rows if row[id_field] == row_id]
    if len(matches) != 1:
        raise ValueError(f"expected one {row_id} row in {filename}")
    status = matches[0][status_field]
    if status != ready_value:
        raise ValueError(f"{row_id} in {filename} has {status_field}={status}, expected {ready_value}")
    return f"{filename}:{row_id}:{status_field}={ready_value}"


def ledger_status() -> str:
    rows = read_csv(DERIVED / "m1_response_parameter_count_value_ledger_summary_v12.csv")
    return rows[0]["overall_status"]


def resolution_rows() -> list[dict[str, object]]:
    ledger = read_csv(DERIVED / "m1_response_parameter_count_value_ledger_v12.csv")
    conditional = [row for row in ledger if row["resolution_needed"] == "true"]
    out: list[dict[str, object]] = []
    for index, row in enumerate(conditional, start=1):
        component = row["response_component"]
        evidence = [
            require_value(filename, id_field, row_id, status_field, ready_value)
            for filename, id_field, row_id, status_field, ready_value in EVIDENCE_REQUIREMENTS[component]
        ]
        out.append(
            {
                "resolution_row_id": f"M1RPASR13_{index:03d}",
                "ledger_row_id": row["ledger_row_id"],
                "readiness_id": row["readiness_id"],
                "family_id": row["family_id"],
                "response_component": component,
                "prior_count_value_status": row["count_value_status"],
                "slot_resolution_status": "RESOLVED_ZERO_INACTIVE_OR_PLACEHOLDER_RESPONSE_SLOT",
                "slot_count_value": "0",
                "resolution_evidence": ";".join(evidence),
                "adjustable_response_parameter_found": "false",
                "final_count_candidate_input_allowed": "true",
                "response_value_input_allowed": "false",
                "parsimony_input_allowed": "false",
                "next_required_artifact": NEXT_ARTIFACT,
                "forbidden_inputs": row["forbidden_inputs"],
                "endpoint_scoring_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    unresolved = sum(row["slot_resolution_status"] != "RESOLVED_ZERO_INACTIVE_OR_PLACEHOLDER_RESPONSE_SLOT" for row in rows)
    adjustable = sum(row["adjustable_response_parameter_found"] == "true" for row in rows)
    return [
        {
            "summary_id": "M1_RESPONSE_PARAMETER_ADJUSTABLE_SLOT_RESOLUTION_V13",
            "resolution_artifact": "m1_response_parameter_adjustable_slot_resolution_v13",
            "ledger_status": ledger_status(),
            "conditional_rows_checked": len(rows),
            "resolved_zero_rows": sum(row["slot_count_value"] == "0" for row in rows),
            "unresolved_rows": unresolved,
            "adjustable_response_parameters_found": adjustable,
            "final_m1_global_count_candidate_ready": "true" if unresolved == 0 and adjustable == 0 else "false",
            "final_m1_global_count_written": "false",
            "numeric_response_values_written": 0,
            "parsimony_scores_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": STATUS if unresolved == 0 and adjustable == 0 else "M1_RESPONSE_PARAMETER_ADJUSTABLE_SLOT_RESOLUTION_V13_UNRESOLVED",
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m1_response_parameter_adjustable_slot_resolution_v13.md").write_text(
        f"""# M1 Response Parameter Adjustable Slot Resolution v13

**Doc class:** M1 response-parameter adjustable-slot resolution ledger
**Reader role:** scoring-frontier parameter-count reviewer
**Status:** conditional M1 response slots resolved for final-count candidate
**Canonical parent:** M1 response parameter count-value ledger v12

Script:

```text
scripts/build_m1_response_parameter_adjustable_slot_resolution.py
```

Derived outputs:

```text
data/derived/m1_response_parameter_adjustable_slot_resolution_v13.csv
data/derived/m1_response_parameter_adjustable_slot_resolution_summary_v13.csv
```

## Current Result

The v13 resolution checks the three conditional M1 response slots left open by
the v12 count-value ledger: carrier, amplitude, and scale. Each slot is
resolved as a zero-count slot only for the present protocol state, where the M1
formula table and admissibility table still write no `Response_tau` formula, no
numeric response values, no M1 prediction rows, and no endpoint scores.

The expected status is:

```text
{STATUS}
```

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This artifact does not prove that an M1 response layer is physically absent,
does not write a final M1 global parameter count, does not write response
values, does not construct `Response_tau`, does not compute parsimony, does not
authorize endpoint scoring, and does not decide the dark-sector question. It
only records that the present M1 scaffold has no active adjustable response
slot before a later final-count candidate.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = resolution_rows()
    write_csv(DERIVED / "m1_response_parameter_adjustable_slot_resolution_v13.csv", rows, FIELDS)
    write_csv(
        DERIVED / "m1_response_parameter_adjustable_slot_resolution_summary_v13.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER11_M1_RESPONSE_PARAMETER_ADJUSTABLE_SLOT_RESOLUTION_V13_BUILT")


if __name__ == "__main__":
    main()
