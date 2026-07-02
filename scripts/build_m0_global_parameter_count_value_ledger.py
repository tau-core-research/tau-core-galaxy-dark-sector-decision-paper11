#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

NEXT_ARTIFACT = "m0_global_adjustable_slot_resolution_v13.csv"
STATUS = "M0_GLOBAL_PARAMETER_COUNT_VALUE_LEDGER_V12_PARTIAL_VALUES_READY_ADJUSTABLE_SLOT_RESOLUTION_PENDING"
CLAIM_BOUNDARY = "m0_global_parameter_count_value_ledger_only_no_final_k_no_parsimony_no_scores"

FIELDS = [
    "ledger_row_id",
    "classification_row_id",
    "readiness_id",
    "family_id",
    "global_slot_name",
    "countability_class",
    "count_value_status",
    "slot_count_value",
    "count_value_rule",
    "resolution_needed",
    "resolution_reason",
    "final_m0_global_count_input_allowed",
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
    "disqualifying_guard_rows",
    "numeric_slot_count_values_written",
    "final_m0_global_count_written",
    "parsimony_scores_written",
    "endpoint_scoring_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]

VALUE_RULES = {
    "source_state": {
        "count_value_status": "CONDITIONAL_COUNT_VALUE_PENDING",
        "slot_count_value": "VALUE_PENDING_ADJUSTABLE_SLOT_RESOLUTION",
        "count_value_rule": "0 if source-state binding is fixed source-side; otherwise count each adjustable source-state coefficient or post-freeze morphology switch",
        "resolution_needed": "true",
        "resolution_reason": "requires evidence that no adjustable source-state coefficient or post-freeze switch is active",
    },
    "no_dark_constraint": {
        "count_value_status": "RESOLVED_ZERO_OR_DISQUALIFYING_GUARD",
        "slot_count_value": "0",
        "count_value_rule": "fixed no-dark family guard contributes zero M0 parameters; a hidden compensator disqualifies M0 instead of counting as an M0 parameter",
        "resolution_needed": "false",
        "resolution_reason": "fixed family eligibility guard with explicit disqualification route",
    },
    "baryonic_input": {
        "count_value_status": "CONDITIONAL_COUNT_VALUE_PENDING",
        "slot_count_value": "VALUE_PENDING_ADJUSTABLE_SLOT_RESOLUTION",
        "count_value_rule": "0 if baryonic inputs are shared source-side records; otherwise count adjustable normalization, scale, or mass-model privileges",
        "resolution_needed": "true",
        "resolution_reason": "requires evidence that baryonic normalization, scale, and mass-model choices are fixed or shared",
    },
    "readout_operator": {
        "count_value_status": "CONDITIONAL_COUNT_VALUE_PENDING",
        "slot_count_value": "VALUE_PENDING_ADJUSTABLE_SLOT_RESOLUTION",
        "count_value_rule": "0 if the readout operator is fixed symbolically; otherwise count each adjustable amplitude, radial scale, threshold, or kernel-shape parameter",
        "resolution_needed": "true",
        "resolution_reason": "requires evidence that no adjustable readout amplitude, scale, threshold, or kernel-shape parameter is active",
    },
    "failure_route": {
        "count_value_status": "CONDITIONAL_COUNT_VALUE_PENDING",
        "slot_count_value": "VALUE_PENDING_ADJUSTABLE_SLOT_RESOLUTION",
        "count_value_rule": "0 for pure null/blocked/fallback guards; otherwise count rescue coefficients and per-galaxy exceptions at full weight",
        "resolution_needed": "true",
        "resolution_reason": "requires explicit zero/nonzero evidence for rescue coefficients and exception routes",
    },
    "assembly": {
        "count_value_status": "RESOLVED_ZERO_AGGREGATE_CONTAINER",
        "slot_count_value": "0",
        "count_value_rule": "assembly row contributes zero direct parameters when it only aggregates child slots; child adjustable slots are counted in their own rows",
        "resolution_needed": "false",
        "resolution_reason": "aggregate audit container without direct numeric degree of freedom",
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
    rows = read_csv(DERIVED / "m0_global_parameter_count_classification_summary_v11.csv")
    return rows[0]["overall_status"]


def ledger_rows() -> list[dict[str, object]]:
    classified = read_csv(DERIVED / "m0_global_parameter_count_classification_v11.csv")
    out: list[dict[str, object]] = []
    for index, row in enumerate(classified, start=1):
        rule = VALUE_RULES[row["global_slot_name"]]
        pending = rule["resolution_needed"] == "true"
        out.append(
            {
                "ledger_row_id": f"M0GPCVL12_{index:03d}",
                "classification_row_id": row["classification_row_id"],
                "readiness_id": row["readiness_id"],
                "family_id": row["family_id"],
                "global_slot_name": row["global_slot_name"],
                "countability_class": row["countability_class"],
                "count_value_status": rule["count_value_status"],
                "slot_count_value": rule["slot_count_value"],
                "count_value_rule": rule["count_value_rule"],
                "resolution_needed": rule["resolution_needed"],
                "resolution_reason": rule["resolution_reason"],
                "final_m0_global_count_input_allowed": "false",
                "parsimony_input_allowed": "false",
                "next_required_artifact": NEXT_ARTIFACT if pending else "none_until_aggregate_resolution",
                "forbidden_inputs": row["forbidden_inputs"],
                "endpoint_scoring_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    resolved_zero = sum(str(row["slot_count_value"]) == "0" for row in rows)
    conditional = sum(str(row["resolution_needed"]) == "true" for row in rows)
    disqualifying = sum("DISQUALIF" in str(row["countability_class"]) for row in rows)
    return [
        {
            "summary_id": "M0_GLOBAL_PARAMETER_COUNT_VALUE_LEDGER_V12",
            "ledger_artifact": "m0_global_parameter_count_value_ledger_v12",
            "classification_status": classification_status(),
            "ledger_rows": len(rows),
            "resolved_zero_rows": resolved_zero,
            "conditional_pending_rows": conditional,
            "disqualifying_guard_rows": disqualifying,
            "numeric_slot_count_values_written": resolved_zero,
            "final_m0_global_count_written": "false",
            "parsimony_scores_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": STATUS,
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_global_parameter_count_value_ledger_v12.md").write_text(
        f"""# M0 Global Parameter Count Value Ledger v12

**Doc class:** M0 global parameter count-value ledger
**Reader role:** scoring-frontier parameter-count reviewer
**Status:** partial slot values ready; adjustable-slot resolution pending
**Canonical parent:** M0 global parameter count classification v11

Script:

```text
scripts/build_m0_global_parameter_count_value_ledger.py
```

Derived outputs:

```text
data/derived/m0_global_parameter_count_value_ledger_v12.csv
data/derived/m0_global_parameter_count_value_ledger_summary_v12.csv
```

## Current Result

The v12 ledger converts the v11 countability classes into count-value rows.
Fixed guards and aggregate containers can receive zero slot values. Conditional
rows remain pending until an explicit source-side adjustable-slot resolution
shows whether a coefficient, scale, switch, threshold, rescue route, or
privilege is active.

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
dark-sector question. It only records slot-level count-value rules and the
remaining adjustable-slot evidence needed before a final M0 global count can be
formed.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = ledger_rows()
    write_csv(DERIVED / "m0_global_parameter_count_value_ledger_v12.csv", rows, FIELDS)
    write_csv(DERIVED / "m0_global_parameter_count_value_ledger_summary_v12.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER11_M0_GLOBAL_PARAMETER_COUNT_VALUE_LEDGER_V12_BUILT")


if __name__ == "__main__":
    main()
