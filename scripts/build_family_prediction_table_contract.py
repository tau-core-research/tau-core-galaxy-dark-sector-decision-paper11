#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/source_manifest"
DERIVED = ROOT / "data/derived"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def schema_rows() -> list[dict[str, object]]:
    fields = [
        ("scoring_row_id", "string", "Activated scoring row id from activated_scoring_rows_v10.csv"),
        ("galaxy_id", "string", "Galaxy identifier matching the activated row"),
        ("family_id", "enum", "One of M0, M1, or M2"),
        ("radial_index", "integer", "Radial grid index shared with the observed-input table"),
        ("radius_kpc", "float", "Radius in kpc on the frozen shared radial grid"),
        ("v_pred_km_s", "float", "Frozen family prediction at this radial point"),
        ("prediction_source_slot", "string", "Formula slot used to produce the prediction"),
        ("formula_table_status", "string", "Formula-slot readiness status before scoring"),
        ("prediction_status", "string", "Prediction-row readiness status"),
    ]
    return [
        {
            "field_name": name,
            "field_type": field_type,
            "definition": definition,
            "required_before_scoring": "true",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "family_prediction_table_schema_only_no_predictions",
        }
        for name, field_type, definition in fields
    ]


def slot_rows() -> list[dict[str, object]]:
    formula_rows = read_csv(SOURCE / "family_formula_table_v05.csv")
    out: list[dict[str, object]] = []
    for index, row in enumerate(formula_rows, start=1):
        ready = row["formula_table_status"] == "FORMULA_TABLE_READY"
        out.append(
            {
                "slot_requirement_id": f"FPT80_{index:03d}",
                "family_id": row["family_id"],
                "formula_slot": row["formula_slot"],
                "required_formula_artifact": row["next_required_artifact"],
                "minimum_required_entries": row["minimum_required_entries"],
                "formula_table_status": row["formula_table_status"],
                "prediction_slot_status": "PREDICTION_SLOT_READY" if ready else "PREDICTION_SLOT_BLOCKED_FORMULA_TABLE_MISSING",
                "forbidden_inputs": row["forbidden_inputs"],
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "family_prediction_slot_requirement_only_no_formula_claim",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["prediction_slot_status"] == "PREDICTION_SLOT_READY" for row in rows)
    blocked = len(rows) - ready
    next_required = next(
        (row["required_formula_artifact"] for row in rows if row["prediction_slot_status"] != "PREDICTION_SLOT_READY"),
        "family_prediction_tables_v08.csv",
    )
    return [
        {
            "summary_id": "FAMILY_PREDICTION_TABLE_CONTRACT_V80",
            "required_formula_slots": len(rows),
            "ready_formula_slots": ready,
            "blocked_formula_slots": blocked,
            "numeric_prediction_rows_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FAMILY_PREDICTION_TABLE_CONTRACT_READY_FORMULA_SLOTS_BLOCKED"
            if blocked
            else "FAMILY_PREDICTION_TABLE_CONTRACT_READY_FOR_NUMERIC_PREDICTIONS",
            "next_required_artifact": next_required,
            "claim_boundary": "family_prediction_table_contract_only_no_predictions_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    schema = schema_rows()
    slots = slot_rows()
    summary_rows = summary(slots)
    write_csv(
        DERIVED / "family_prediction_table_schema_v80.csv",
        schema,
        [
            "field_name",
            "field_type",
            "definition",
            "required_before_scoring",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "family_prediction_table_slot_requirements_v80.csv",
        slots,
        [
            "slot_requirement_id",
            "family_id",
            "formula_slot",
            "required_formula_artifact",
            "minimum_required_entries",
            "formula_table_status",
            "prediction_slot_status",
            "forbidden_inputs",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "family_prediction_table_contract_summary_v80.csv",
        summary_rows,
        [
            "summary_id",
            "required_formula_slots",
            "ready_formula_slots",
            "blocked_formula_slots",
            "numeric_prediction_rows_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_FAMILY_PREDICTION_TABLE_CONTRACT_V80_BUILT")


if __name__ == "__main__":
    main()
