#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDNAMES = [
    "prediction_row_value_id",
    "scoring_row_id",
    "galaxy_id",
    "family_id",
    "radial_index",
    "radius_kpc",
    "frozen_formula_body",
    "source_anchor_value_id",
    "v_anchor_km_s",
    "frozen_prediction_value_km_s",
    "source_route",
    "leakage_evidence_id",
    "prediction_value_decision",
    "next_required_artifact",
    "forbidden_inputs",
    "prediction_row_values_frozen",
    "family_prediction_rows_written",
    "endpoint_scoring_allowed",
    "claim_boundary",
]


SUMMARY_FIELDNAMES = [
    "summary_id",
    "prediction_row_value_freeze_artifact",
    "source_formula_body_artifact",
    "source_anchor_value_artifact",
    "source_rows_evaluated",
    "galaxies_with_frozen_values",
    "family_id",
    "frozen_formula_body",
    "prediction_row_values_frozen",
    "family_prediction_rows_written",
    "families_with_numeric_predictions",
    "endpoint_scoring_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]


FORMULA_BODY = "v_body_km_s(R) := v_anchor_km_s(R)"
NEXT_ARTIFACT = "m0_no_dark_family_prediction_row_emission_v08"


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


def scoring_row_ids() -> dict[str, str]:
    rows = read_csv(DERIVED / "activated_scoring_rows_v10.csv")
    return {row["galaxy_id"]: row["scoring_row_id"] for row in rows}


def prediction_rows() -> list[dict[str, object]]:
    formula_body = summary_row("m0_no_dark_velocity_readout_formula_body_freeze_summary_v08.csv")
    if formula_body["overall_status"] != (
        "M0_NO_DARK_VELOCITY_FORMULA_BODY_FROZEN_BLOCKED_PREDICTION_ROW_VALUE_FREEZE_MISSING"
    ):
        raise ValueError("velocity formula body freeze is not in the expected handoff state")
    if formula_body["frozen_formula_body"] != FORMULA_BODY:
        raise ValueError("unexpected M0 no-dark formula body")

    activated = scoring_row_ids()
    anchors = read_csv(DERIVED / "m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08.csv")
    forbidden = (
        "v_obs_km_s;endpoint_residual;heldout_score;family_winner;best_fit_curve;"
        "posthoc_formula_switch;posthoc_prediction_rescale;posthoc_weight_fit;"
        "posthoc_sign_choice;posthoc_normalization;numeric_score_value"
    )
    rows: list[dict[str, object]] = []
    for index, row in enumerate(anchors, start=1):
        galaxy_id = row["galaxy_id"]
        if galaxy_id not in activated:
            raise ValueError(f"anchor row has no activated scoring row: {galaxy_id}")
        rows.append(
            {
                "prediction_row_value_id": f"M0NDPRVF08_{index:04d}",
                "scoring_row_id": activated[galaxy_id],
                "galaxy_id": galaxy_id,
                "family_id": "M0",
                "radial_index": row["radial_index"],
                "radius_kpc": row["radius_kpc"],
                "frozen_formula_body": FORMULA_BODY,
                "source_anchor_value_id": row["combined_anchor_value_id"],
                "v_anchor_km_s": row["v_anchor_km_s"],
                "frozen_prediction_value_km_s": row["v_anchor_km_s"],
                "source_route": row["source_route"],
                "leakage_evidence_id": row["leakage_evidence_id"],
                "prediction_value_decision": "M0_NO_DARK_PREDICTION_VALUE_FROZEN_FROM_ANCHOR",
                "next_required_artifact": NEXT_ARTIFACT,
                "forbidden_inputs": forbidden,
                "prediction_row_values_frozen": "true",
                "family_prediction_rows_written": 0,
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "m0_no_dark_prediction_row_value_freeze_only_no_family_table_rows_no_scores",
            }
        )
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "M0_NO_DARK_PREDICTION_ROW_VALUE_FREEZE_V08",
            "prediction_row_value_freeze_artifact": "m0_no_dark_prediction_row_value_freeze_v08",
            "source_formula_body_artifact": "m0_no_dark_velocity_readout_formula_body_freeze_v08",
            "source_anchor_value_artifact": "m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08",
            "source_rows_evaluated": len(rows),
            "galaxies_with_frozen_values": len({row["galaxy_id"] for row in rows}),
            "family_id": "M0",
            "frozen_formula_body": FORMULA_BODY,
            "prediction_row_values_frozen": len(rows),
            "family_prediction_rows_written": 0,
            "families_with_numeric_predictions": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_PREDICTION_ROW_VALUES_FROZEN_BLOCKED_FAMILY_ROW_EMISSION_MISSING",
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": "m0_no_dark_prediction_row_value_freeze_only_no_family_table_rows_no_scores_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_prediction_row_value_freeze_v08.md").write_text(
        f"""# M0 No-Dark Prediction Row Value Freeze v08

**Doc class:** prediction-row value-freeze gate
**Status:** M0 no-dark row values frozen; family table row emission missing; no scoring

Script:

```text
scripts/build_m0_no_dark_prediction_row_value_freeze.py
```

Derived outputs:

```text
data/derived/m0_no_dark_prediction_row_value_freeze_v08.csv
data/derived/m0_no_dark_prediction_row_value_freeze_summary_v08.csv
```

This artifact closes the `m0_no_dark_prediction_row_value_freeze_v08` blocker
by freezing M0 no-dark numeric row values from the already frozen formula body:

```text
{FORMULA_BODY}
```

For each source-side anchor row, the frozen row value is:

```text
frozen_prediction_value_km_s := v_anchor_km_s
```

The artifact deliberately does not write rows into
`family_prediction_tables_v08.csv`. It freezes values for a later row-emission
gate only.

## Current Result

The expected status is:

```text
M0_NO_DARK_PREDICTION_ROW_VALUES_FROZEN_BLOCKED_FAMILY_ROW_EMISSION_MISSING
```

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This gate freezes M0 no-dark row values only. It does not write family
prediction table rows, does not compute endpoint scores, does not compare
M0/M1/M2, and does not decide whether a dark-sector component is required.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = prediction_rows()
    write_csv(DERIVED / "m0_no_dark_prediction_row_value_freeze_v08.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_prediction_row_value_freeze_summary_v08.csv",
        summary(rows),
        SUMMARY_FIELDNAMES,
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_PREDICTION_ROW_VALUE_FREEZE_V08_BUILT")


if __name__ == "__main__":
    main()
