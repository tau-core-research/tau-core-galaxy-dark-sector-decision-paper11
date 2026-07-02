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


EMISSION_FIELDS = [
    "emission_row_id",
    *TABLE_FIELDS,
    "source_prediction_row_value_id",
    "source_formula_body",
    "source_route",
    "leakage_evidence_id",
    "emission_decision",
    "next_required_artifact",
    "forbidden_inputs",
    "family_prediction_row_written",
    "endpoint_scoring_allowed",
    "claim_boundary",
]


SUMMARY_FIELDS = [
    "summary_id",
    "family_row_emission_artifact",
    "target_prediction_table_artifact",
    "source_prediction_row_value_artifact",
    "family_id",
    "emitted_prediction_rows",
    "galaxies_with_emitted_rows",
    "families_with_numeric_predictions",
    "endpoint_scoring_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]


NEXT_ARTIFACT = "m0_label_rule_table_v06"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def summary_row(path: str) -> dict[str, str]:
    rows = read_csv(DERIVED / path)
    if len(rows) != 1:
        raise ValueError(f"expected one summary row in {path}")
    return rows[0]


def emitted_rows() -> list[dict[str, object]]:
    value_summary = summary_row("m0_no_dark_prediction_row_value_freeze_summary_v08.csv")
    if value_summary["overall_status"] != (
        "M0_NO_DARK_PREDICTION_ROW_VALUES_FROZEN_BLOCKED_FAMILY_ROW_EMISSION_MISSING"
    ):
        raise ValueError("prediction row value freeze is not in the expected handoff state")
    value_rows = read_csv(DERIVED / "m0_no_dark_prediction_row_value_freeze_v08.csv")
    forbidden = (
        "v_obs_km_s;endpoint_residual;heldout_score;family_winner;best_fit_curve;"
        "posthoc_formula_switch;posthoc_prediction_rescale;posthoc_row_drop;"
        "posthoc_family_selection;numeric_score_value"
    )
    rows: list[dict[str, object]] = []
    for index, row in enumerate(value_rows, start=1):
        table_row = {
            "scoring_row_id": row["scoring_row_id"],
            "galaxy_id": row["galaxy_id"],
            "family_id": row["family_id"],
            "radial_index": row["radial_index"],
            "radius_kpc": row["radius_kpc"],
            "v_pred_km_s": row["frozen_prediction_value_km_s"],
            "prediction_source_slot": "M0:no_dark_readout_formula",
            "formula_table_status": "M0_NO_DARK_ROW_VALUE_FROZEN",
            "prediction_status": "PREDICTION_ROW_EMITTED_NOT_SCORED",
        }
        rows.append(
            {
                "emission_row_id": f"M0NDFPRE08_{index:04d}",
                **table_row,
                "source_prediction_row_value_id": row["prediction_row_value_id"],
                "source_formula_body": row["frozen_formula_body"],
                "source_route": row["source_route"],
                "leakage_evidence_id": row["leakage_evidence_id"],
                "emission_decision": "M0_NO_DARK_FAMILY_PREDICTION_ROW_EMITTED",
                "next_required_artifact": NEXT_ARTIFACT,
                "forbidden_inputs": forbidden,
                "family_prediction_row_written": "true",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "m0_no_dark_family_prediction_row_emission_only_no_scores_no_family_comparison",
            }
        )
    return rows


def table_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [{field: row[field] for field in TABLE_FIELDS} for row in rows]


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "M0_NO_DARK_FAMILY_PREDICTION_ROW_EMISSION_V08",
            "family_row_emission_artifact": "m0_no_dark_family_prediction_row_emission_v08",
            "target_prediction_table_artifact": "family_prediction_tables_v08.csv",
            "source_prediction_row_value_artifact": "m0_no_dark_prediction_row_value_freeze_v08",
            "family_id": "M0",
            "emitted_prediction_rows": len(rows),
            "galaxies_with_emitted_rows": len({row["galaxy_id"] for row in rows}),
            "families_with_numeric_predictions": 1 if rows else 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_FAMILY_PREDICTION_ROWS_EMITTED_SCORING_BLOCKED",
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": "m0_no_dark_family_prediction_row_emission_only_no_scores_no_dark_sector_verdict",
        }
    ]


def table_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "FAMILY_PREDICTION_TABLES_V08",
            "prediction_table_artifact": "family_prediction_tables_v08.csv",
            "table_header_written": "true",
            "numeric_prediction_rows_written": len(rows),
            "families_with_numeric_predictions": 1 if rows else 0,
            "m0_no_dark_formula_table_status": "M0_NO_DARK_ROWS_EMITTED",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FAMILY_PREDICTION_TABLES_M0_NO_DARK_ROWS_EMITTED_SCORING_BLOCKED",
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": "family_prediction_tables_m0_no_dark_rows_only_no_scores_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_family_prediction_row_emission_v08.md").write_text(
        f"""# M0 No-Dark Family Prediction Row Emission v08

**Doc class:** family-prediction row emission gate
**Status:** M0 no-dark rows emitted; scoring blocked

Script:

```text
scripts/build_m0_no_dark_family_prediction_row_emission.py
```

Derived outputs:

```text
data/derived/m0_no_dark_family_prediction_row_emission_v08.csv
data/derived/m0_no_dark_family_prediction_row_emission_summary_v08.csv
data/derived/family_prediction_tables_v08.csv
data/derived/family_prediction_tables_summary_v08.csv
```

This artifact materializes the frozen M0 no-dark row values into the family
prediction table shape. It writes `v_pred_km_s` rows for the M0 no-dark
readout slot only.

## Current Result

The expected status is:

```text
M0_NO_DARK_FAMILY_PREDICTION_ROWS_EMITTED_SCORING_BLOCKED
```

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This gate writes M0 no-dark family-prediction rows only. It does not compute endpoint scores,
does not compare M0/M1/M2, does not validate the no-dark
model, and does not decide whether a dark-sector component is required.
""",
        encoding="utf-8",
    )
    (DOCS / "family_prediction_tables_v08.md").write_text(
        f"""# Family Prediction Tables v08

**Doc class:** prediction-table artifact
**Status:** M0 no-dark rows emitted; scoring blocked

Script:

```text
scripts/build_m0_no_dark_family_prediction_row_emission.py
```

Derived outputs:

```text
data/derived/family_prediction_tables_v08.csv
data/derived/family_prediction_tables_summary_v08.csv
```

This artifact closes the broad `family_prediction_tables_v08.csv` presence
blocker by writing the M0 no-dark family-prediction rows created from the
frozen source-side row values. It contains only the M0 no-dark prediction slot.

## Current Result

The expected status is:

```text
FAMILY_PREDICTION_TABLES_M0_NO_DARK_ROWS_EMITTED_SCORING_BLOCKED
```

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This table contains M0 no-dark prediction rows only. It does not compute endpoint scores,
does not compare M0/M1/M2, does not validate the no-dark
model, and does not decide whether a dark-sector component is required.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = emitted_rows()
    write_csv(DERIVED / "m0_no_dark_family_prediction_row_emission_v08.csv", rows, EMISSION_FIELDS)
    write_csv(
        DERIVED / "m0_no_dark_family_prediction_row_emission_summary_v08.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_csv(DERIVED / "family_prediction_tables_v08.csv", table_rows(rows), TABLE_FIELDS)
    write_csv(
        DERIVED / "family_prediction_tables_summary_v08.csv",
        table_summary(rows),
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
    print("PAPER11_M0_NO_DARK_FAMILY_PREDICTION_ROW_EMISSION_V08_BUILT")


if __name__ == "__main__":
    main()
