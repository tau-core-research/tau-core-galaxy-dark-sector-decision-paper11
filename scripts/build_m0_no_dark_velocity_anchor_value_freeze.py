#!/usr/bin/env python3
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
INPUT = ROOT / "data/input"


FIELDNAMES = [
    "anchor_value_freeze_id",
    "galaxy_id",
    "selected_anchor_class",
    "frozen_source_catalog",
    "frozen_source_table",
    "frozen_source_columns",
    "imported_source_rows",
    "source_route_count",
    "value_freeze_decision",
    "next_required_artifact",
    "forbidden_inputs",
    "anchor_value_source_frozen",
    "anchor_numeric_value_rows_written",
    "velocity_formula_written",
    "numeric_prediction_rows_written",
    "endpoint_scoring_allowed",
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


def summary_row(path: str) -> dict[str, str]:
    rows = read_csv(DERIVED / path)
    if len(rows) != 1:
        raise ValueError(f"expected one summary row in {path}")
    return rows[0]


def value_freeze_rows() -> list[dict[str, object]]:
    selection_rule = summary_row("m0_no_dark_velocity_anchor_selection_rule_summary_v08.csv")
    real_value_gate = summary_row("source_import_real_values_summary_v12.csv")
    provenance_audit = summary_row("source_import_provenance_audit_summary_v20.csv")
    leakage_pass = summary_row("leakage_audit_pass_review_summary_v78.csv")
    source_rows = read_csv(INPUT / "source_import_real_values_v12.csv")
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in source_rows:
        grouped[row["galaxy_id"]].append(row)
    common_forbidden = (
        "v_obs_km_s;endpoint_residual;heldout_score;family_winner;"
        "best_fit_curve;posthoc_unit_rescale;posthoc_coefficient_fit;"
        "posthoc_anchor_value"
    )
    rows: list[dict[str, object]] = [
        {
            "anchor_value_freeze_id": "M0NDVAVF08_GATE_HANDOFF",
            "galaxy_id": "ALL",
            "selected_anchor_class": "source_side_baryonic_gravity_velocity_carrier",
            "frozen_source_catalog": "SPARC",
            "frozen_source_table": "MassModels_Lelli2016c.mrt",
            "frozen_source_columns": "v_gas_km_s;v_disk_km_s;v_bulge_km_s",
            "imported_source_rows": real_value_gate["imported_numeric_rows"],
            "source_route_count": provenance_audit["provenance_complete_rows"],
            "value_freeze_decision": "READY_FOR_ANCHOR_VALUE_FREEZE_REVIEW",
            "next_required_artifact": "m0_no_dark_velocity_anchor_unit_normalization_v08",
        },
        {
            "anchor_value_freeze_id": "M0NDVAVF08_SELECTION_RULE_HANDOFF",
            "galaxy_id": "ALL",
            "selected_anchor_class": "source_side_baryonic_gravity_velocity_carrier",
            "frozen_source_catalog": "SPARC",
            "frozen_source_table": "MassModels_Lelli2016c.mrt",
            "frozen_source_columns": "v_gas_km_s;v_disk_km_s;v_bulge_km_s",
            "imported_source_rows": real_value_gate["imported_numeric_rows"],
            "source_route_count": provenance_audit["provenance_complete_rows"],
            "value_freeze_decision": "ANCHOR_VALUE_SOURCE_CLASS_FROZEN",
            "next_required_artifact": "m0_no_dark_velocity_anchor_unit_normalization_v08",
        },
        {
            "anchor_value_freeze_id": "M0NDVAVF08_LEAKAGE_GUARD",
            "galaxy_id": "ALL",
            "selected_anchor_class": "source_side_baryonic_gravity_velocity_carrier",
            "frozen_source_catalog": "SPARC",
            "frozen_source_table": "MassModels_Lelli2016c.mrt",
            "frozen_source_columns": "v_gas_km_s;v_disk_km_s;v_bulge_km_s",
            "imported_source_rows": real_value_gate["imported_numeric_rows"],
            "source_route_count": provenance_audit["provenance_complete_rows"],
            "value_freeze_decision": "ANCHOR_VALUE_LEAKAGE_GUARD_INHERITED",
            "next_required_artifact": "m0_no_dark_velocity_anchor_unit_normalization_v08",
        },
        {
            "anchor_value_freeze_id": "M0NDVAVF08_UNIT_NORMALIZATION",
            "galaxy_id": "ALL",
            "selected_anchor_class": "source_side_baryonic_gravity_velocity_carrier",
            "frozen_source_catalog": "SPARC",
            "frozen_source_table": "MassModels_Lelli2016c.mrt",
            "frozen_source_columns": "v_gas_km_s;v_disk_km_s;v_bulge_km_s",
            "imported_source_rows": real_value_gate["imported_numeric_rows"],
            "source_route_count": provenance_audit["provenance_complete_rows"],
            "value_freeze_decision": "BLOCKED_ANCHOR_UNIT_NORMALIZATION_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_unit_normalization_v08",
        },
    ]
    catalogs = Counter(row["catalog"] for row in source_rows)
    tables = Counter(row["table_or_file"] for row in source_rows)
    for index, galaxy_id in enumerate(sorted(grouped), start=1):
        galaxy_rows = grouped[galaxy_id]
        source_route_count = len({row["source_route"] for row in galaxy_rows})
        rows.append(
            {
                "anchor_value_freeze_id": f"M0NDVAVF08_GALAXY_{index:03d}",
                "galaxy_id": galaxy_id,
                "selected_anchor_class": "source_side_baryonic_gravity_velocity_carrier",
                "frozen_source_catalog": next(iter(catalogs)),
                "frozen_source_table": next(iter(tables)),
                "frozen_source_columns": "v_gas_km_s;v_disk_km_s;v_bulge_km_s",
                "imported_source_rows": len(galaxy_rows),
                "source_route_count": source_route_count,
                "value_freeze_decision": "ANCHOR_VALUE_SOURCE_COLUMNS_FROZEN_NO_FORMULA",
                "next_required_artifact": "m0_no_dark_velocity_anchor_unit_normalization_v08",
            }
        )
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["anchor_value_source_frozen"] = "true"
        row["anchor_numeric_value_rows_written"] = 0
        row["velocity_formula_written"] = "false"
        row["numeric_prediction_rows_written"] = 0
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_velocity_anchor_value_freeze_source_columns_only_no_formula_no_predictions"
    rows[0]["observed_status"] = selection_rule["overall_status"]
    rows[1]["observed_status"] = real_value_gate["overall_status"]
    rows[2]["observed_status"] = leakage_pass["overall_status"]
    rows[3]["observed_status"] = "NO_ANCHOR_UNIT_NORMALIZATION_PRESENT"
    for row in rows[4:]:
        row["observed_status"] = "IMPORTED_SOURCE_VALUE_COLUMNS_PRESENT"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    galaxy_rows = [row for row in rows if str(row["galaxy_id"]) != "ALL"]
    blocked = sum(str(row["value_freeze_decision"]).startswith("BLOCKED") for row in rows)
    imported_rows = sum(int(row["imported_source_rows"]) for row in galaxy_rows)
    return [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_ANCHOR_VALUE_FREEZE_V08",
            "anchor_value_freeze_artifact": "m0_no_dark_velocity_anchor_value_freeze_v08",
            "value_freeze_rows": len(rows),
            "galaxy_value_freeze_rows": len(galaxy_rows),
            "imported_source_rows_referenced": imported_rows,
            "blocked_value_freeze_checks": blocked,
            "anchor_value_source_frozen": "true",
            "anchor_numeric_value_rows_written": 0,
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": 0,
            "families_with_numeric_predictions": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_ANCHOR_VALUE_FREEZE_PRESENT_BLOCKED_UNIT_NORMALIZATION_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_unit_normalization_v08",
            "claim_boundary": "m0_no_dark_velocity_anchor_value_freeze_source_columns_only_no_unit_normalization_no_velocity_formula_no_predictions_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_velocity_anchor_value_freeze_v08.md").write_text(
        """# M0 No-Dark Velocity-Anchor Value Freeze v08

**Doc class:** velocity-anchor value-freeze gate
**Status:** source-value columns frozen; unit normalization missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_anchor_value_freeze.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_anchor_value_freeze_v08.csv
data/derived/m0_no_dark_velocity_anchor_value_freeze_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_anchor_value_freeze_v08`
presence blocker by freezing the source-side value columns allowed for the M0
no-dark velocity anchor. The frozen source is the SPARC
`MassModels_Lelli2016c.mrt` baryonic velocity-component lane:

```text
v_gas_km_s;v_disk_km_s;v_bulge_km_s
```

The gate does not read or use `v_obs_km_s`, endpoint residuals, heldout scores,
family winners, best-fit curves, posthoc rescaling, or fitted coefficient
quality. It does not combine the frozen source columns into a formula. It only
freezes the source columns and per-galaxy source-row coverage before any later
unit-normalization or velocity-formula step.

## Current Result

The expected status is:

```text
M0_NO_DARK_ANCHOR_VALUE_FREEZE_PRESENT_BLOCKED_UNIT_NORMALIZATION_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_anchor_unit_normalization_v08
```

## Claim Boundary

This gate freezes only source-side anchor value columns and provenance coverage. It does not compute a combined anchor value, does not normalize units into a formula-ready carrier, does not assign coupling normalization, does not write a velocity formula, does not write prediction rows, does not run endpoint scoring, and does not decide whether a dark-sector component is required.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = value_freeze_rows()
    write_csv(DERIVED / "m0_no_dark_velocity_anchor_value_freeze_v08.csv", rows, FIELDNAMES + ["observed_status"])
    write_csv(
        DERIVED / "m0_no_dark_velocity_anchor_value_freeze_summary_v08.csv",
        summary(rows),
        [
            "summary_id",
            "anchor_value_freeze_artifact",
            "value_freeze_rows",
            "galaxy_value_freeze_rows",
            "imported_source_rows_referenced",
            "blocked_value_freeze_checks",
            "anchor_value_source_frozen",
            "anchor_numeric_value_rows_written",
            "velocity_formula_written",
            "numeric_prediction_rows_written",
            "families_with_numeric_predictions",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_VELOCITY_ANCHOR_VALUE_FREEZE_V08_BUILT")


if __name__ == "__main__":
    main()
