#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


TABLE_FIELDS = [
    "scoring_row_id",
    "galaxy_id",
    "family_id",
    "radial_index",
    "radius_kpc",
    "v_pred_km_s",
    "prediction_source_slot",
    "formula_table_status",
    "prediction_status",
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


def m0_formula_table_ready() -> bool:
    path = DERIVED / "m0_no_dark_formula_table_contract_summary_v06.csv"
    if not path.exists():
        return False
    rows = read_csv(path)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_FORMULA_TABLE_READY_FOR_PREDICTION_ROWS"
        and rows[0]["numeric_predictions_written"] == "0"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def summary_rows() -> list[dict[str, object]]:
    m0_ready = m0_formula_table_ready()
    return [
        {
            "summary_id": "FAMILY_PREDICTION_TABLES_V08",
            "prediction_table_artifact": "family_prediction_tables_v08.csv",
            "table_header_written": "true",
            "numeric_prediction_rows_written": 0,
            "families_with_numeric_predictions": 0,
            "m0_no_dark_formula_table_status": "READY_FOR_PREDICTION_ROWS"
            if m0_ready
            else "BLOCKED_BEFORE_PREDICTION_ROWS",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FAMILY_PREDICTION_TABLES_PRESENT_NO_NUMERIC_ROWS",
            "next_required_artifact": "m0_no_dark_prediction_row_writer_v08"
            if m0_ready
            else "m0_no_dark_formula_table_v06",
            "claim_boundary": "family_prediction_tables_header_only_no_predictions_no_scores_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "family_prediction_tables_v08.md").write_text(
        """# Family Prediction Tables v08

**Doc class:** family prediction table artifact, header-only
**Status:** table present; zero numeric prediction rows; no scoring

Script:

```text
scripts/build_family_prediction_tables.py
```

Derived outputs:

```text
data/derived/family_prediction_tables_v08.csv
data/derived/family_prediction_tables_summary_v08.csv
```

This artifact closes the broad `family_prediction_tables_v08.csv` presence
blocker without writing any velocity predictions. The table header is present
and matches the v80 schema, but there are no `v_pred_km_s` rows.

## Current Result

The expected status is:

```text
FAMILY_PREDICTION_TABLES_PRESENT_NO_NUMERIC_ROWS
```

The next concrete blocker is:

```text
m0_no_dark_prediction_row_writer_v08
```

## Claim Boundary

This artifact does not compute predictions, write velocity rows, compare
families, activate endpoint scoring, or decide the dark-sector question. It
only records that the prediction-table artifact exists and that the next
required work is a source-side prediction-row writer.
""",
        encoding="utf-8",
    )


def main() -> None:
    write_csv(DERIVED / "family_prediction_tables_v08.csv", [], TABLE_FIELDS)
    write_csv(
        DERIVED / "family_prediction_tables_summary_v08.csv",
        summary_rows(),
        [
            "summary_id",
            "prediction_table_artifact",
            "table_header_written",
            "numeric_prediction_rows_written",
            "families_with_numeric_predictions",
            "m0_no_dark_formula_table_status",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    write_doc()
    print("PAPER11_FAMILY_PREDICTION_TABLES_V08_BUILT")


if __name__ == "__main__":
    main()
