#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

NEXT_ARTIFACT = "m1_response_parameter_adjustable_slot_resolution_v13.csv"
STATUS = "M1_RESPONSE_PARAMETER_COUNT_VALUE_LEDGER_V12_PARTIAL_VALUES_READY_ADJUSTABLE_SLOT_RESOLUTION_PENDING"
CLAIM_BOUNDARY = "m1_response_parameter_count_value_ledger_only_no_final_k_no_response_values_no_scores"

FIELDS = [
    "ledger_row_id",
    "classification_row_id",
    "readiness_id",
    "family_id",
    "response_component",
    "countability_class",
    "count_value_status",
    "slot_count_value",
    "count_value_rule",
    "resolution_needed",
    "resolution_reason",
    "final_m1_global_count_input_allowed",
    "response_value_input_allowed",
    "parsimony_input_allowed",
    "next_required_artifact",
    "forbidden_inputs",
    "endpoint_scoring_allowed",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "ledger_artifact",
    "classification_status",
    "ledger_rows",
    "resolved_zero_rows",
    "conditional_pending_rows",
    "numeric_slot_count_values_written",
    "final_m1_global_count_written",
    "numeric_response_values_written",
    "parsimony_scores_written",
    "endpoint_scoring_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]

VALUE_RULES = {
    "activation_rule": {
        "count_value_status": "RESOLVED_ZERO_ADMISSIBILITY_GUARD",
        "slot_count_value": "0",
        "count_value_rule": "pre-scoring M1 activation policy contributes zero direct parameters when it remains an admissibility guard",
        "resolution_needed": "false",
        "resolution_reason": "activation is represented as a source-side admissibility guard, not a numeric response value",
    },
    "carrier": {
        "count_value_status": "CONDITIONAL_COUNT_VALUE_PENDING",
        "slot_count_value": "VALUE_PENDING_RESPONSE_SLOT_RESOLUTION",
        "count_value_rule": "0 if the carrier remains a protocol placeholder; otherwise count each declared carrier amplitude, density, scale, kernel, or shape parameter",
        "resolution_needed": "true",
        "resolution_reason": "requires later evidence that no physical carrier parameter has been introduced",
    },
    "amplitude_law": {
        "count_value_status": "CONDITIONAL_COUNT_VALUE_PENDING",
        "slot_count_value": "VALUE_PENDING_RESPONSE_SLOT_RESOLUTION",
        "count_value_rule": "0 if no response amplitude is active; otherwise count each adjustable response amplitude, normalization, or strength parameter",
        "resolution_needed": "true",
        "resolution_reason": "requires later response-slot resolution before any M1 count or response value can be frozen",
    },
    "scale_law": {
        "count_value_status": "CONDITIONAL_COUNT_VALUE_PENDING",
        "slot_count_value": "VALUE_PENDING_RESPONSE_SLOT_RESOLUTION",
        "count_value_rule": "0 if no response scale is active; otherwise count each adjustable radial, mass, morphology, or transition scale",
        "resolution_needed": "true",
        "resolution_reason": "requires later evidence that no adjustable response scale is active",
    },
    "channel_handoff": {
        "count_value_status": "RESOLVED_ZERO_PROTOCOL_HANDOFF_CONTAINER",
        "slot_count_value": "0",
        "count_value_rule": "handoff contributes zero direct parameters when it only records protocol order and dependencies",
        "resolution_needed": "false",
        "resolution_reason": "protocol container without direct numeric response degree of freedom",
    },
    "zero_response_policy": {
        "count_value_status": "RESOLVED_ZERO_NULL_ROUTE_GUARD",
        "slot_count_value": "0",
        "count_value_rule": "explicit zero-response routes contribute zero parameters unless a numeric rescue or exception term is later introduced",
        "resolution_needed": "false",
        "resolution_reason": "null, inactive, missing, and inadmissible routes are explicit zero-response cases",
    },
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


def classification_status() -> str:
    rows = read_csv(DERIVED / "m1_response_parameter_count_classification_summary_v11.csv")
    return rows[0]["overall_status"]


def ledger_rows() -> list[dict[str, object]]:
    classified = read_csv(DERIVED / "m1_response_parameter_count_classification_v11.csv")
    out: list[dict[str, object]] = []
    for index, row in enumerate(classified, start=1):
        rule = VALUE_RULES[row["response_component"]]
        pending = rule["resolution_needed"] == "true"
        out.append(
            {
                "ledger_row_id": f"M1RPCVL12_{index:03d}",
                "classification_row_id": row["classification_row_id"],
                "readiness_id": row["readiness_id"],
                "family_id": row["family_id"],
                "response_component": row["response_component"],
                "countability_class": row["countability_class"],
                "count_value_status": rule["count_value_status"],
                "slot_count_value": rule["slot_count_value"],
                "count_value_rule": rule["count_value_rule"],
                "resolution_needed": rule["resolution_needed"],
                "resolution_reason": rule["resolution_reason"],
                "final_m1_global_count_input_allowed": "false",
                "response_value_input_allowed": "false",
                "parsimony_input_allowed": "false",
                "next_required_artifact": NEXT_ARTIFACT if pending else "none_until_response_slot_resolution",
                "forbidden_inputs": row["forbidden_inputs"],
                "endpoint_scoring_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    resolved_zero = sum(str(row["slot_count_value"]) == "0" for row in rows)
    conditional = sum(str(row["resolution_needed"]) == "true" for row in rows)
    return [
        {
            "summary_id": "M1_RESPONSE_PARAMETER_COUNT_VALUE_LEDGER_V12",
            "ledger_artifact": "m1_response_parameter_count_value_ledger_v12",
            "classification_status": classification_status(),
            "ledger_rows": len(rows),
            "resolved_zero_rows": resolved_zero,
            "conditional_pending_rows": conditional,
            "numeric_slot_count_values_written": resolved_zero,
            "final_m1_global_count_written": "false",
            "numeric_response_values_written": 0,
            "parsimony_scores_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": STATUS,
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m1_response_parameter_count_value_ledger_v12.md").write_text(
        f"""# M1 Response Parameter Count Value Ledger v12

**Doc class:** M1 response-parameter count-value ledger
**Reader role:** scoring-frontier parameter-count reviewer
**Status:** partial slot values ready; response-slot resolution pending
**Canonical parent:** M1 response parameter count classification v11

Script:

```text
scripts/build_m1_response_parameter_count_value_ledger.py
```

Derived outputs:

```text
data/derived/m1_response_parameter_count_value_ledger_v12.csv
data/derived/m1_response_parameter_count_value_ledger_summary_v12.csv
```

## Current Result

The v12 ledger converts the v11 M1 response-slot countability classes into
slot-level count-value rows. Pure admissibility, handoff, and zero-response
guards receive zero slot values. Carrier, amplitude, and scale slots remain
conditional until a later response-slot resolution proves whether a physical or
adjustable response degree of freedom is absent or active.

The expected status is:

```text
{STATUS}
```

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This artifact writes no final M1 global parameter count, no response value, no
Response_tau formula, no per-galaxy response privilege count, no parsimony
penalty, no endpoint scores, and no dark-sector verdict. It only records
slot-level count-value rules and the remaining response-slot evidence needed
before a final M1 global count can be formed.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = ledger_rows()
    write_csv(DERIVED / "m1_response_parameter_count_value_ledger_v12.csv", rows, FIELDS)
    write_csv(DERIVED / "m1_response_parameter_count_value_ledger_summary_v12.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER11_M1_RESPONSE_PARAMETER_COUNT_VALUE_LEDGER_V12_BUILT")


if __name__ == "__main__":
    main()
