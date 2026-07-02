#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
INPUT = ROOT / "data/input"


VALUE_FIELDNAMES = [
    "combined_anchor_value_id",
    "galaxy_id",
    "radial_index",
    "radius_kpc",
    "v_gas_km_s",
    "v_disk_km_s",
    "v_bulge_km_s",
    "s_gas",
    "s_disk",
    "s_bulge",
    "w_gas",
    "w_disk",
    "w_bulge",
    "n_anchor",
    "v_anchor_sq_km2_s2",
    "v_anchor_km_s",
    "source_route",
    "leakage_evidence_id",
    "anchor_value_decision",
    "next_required_artifact",
    "forbidden_inputs",
    "combined_anchor_values_written",
    "velocity_formula_written",
    "numeric_prediction_rows_written",
    "endpoint_scoring_allowed",
    "claim_boundary",
]


SUMMARY_FIELDNAMES = [
    "summary_id",
    "anchor_combined_anchor_value_artifact",
    "source_rows_evaluated",
    "galaxies_with_anchor_values",
    "identity_weight_rows",
    "negative_anchor_sq_rows",
    "combined_anchor_values_written",
    "velocity_formula_written",
    "numeric_prediction_rows_written",
    "families_with_numeric_predictions",
    "endpoint_scoring_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]


FROZEN_EXPRESSION = (
    "v_anchor_sq_km2_s2 = "
    "(s_gas*w_gas*v_gas_km_s^2 + "
    "s_disk*w_disk*v_disk_km_s^2 + "
    "s_bulge*w_bulge*v_bulge_km_s^2) / n_anchor"
)

NEXT_ARTIFACT = "m0_no_dark_velocity_readout_formula_body_freeze_v08"


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


def combined_anchor_value_rows() -> list[dict[str, object]]:
    expression_freeze = summary_row("m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_summary_v08.csv")
    leakage_pass = summary_row("leakage_audit_pass_review_summary_v78.csv")
    if expression_freeze["overall_status"] != (
        "M0_NO_DARK_ANCHOR_COMBINED_ANCHOR_EXPRESSION_FROZEN_BLOCKED_VALUE_FREEZE_MISSING"
    ):
        raise ValueError("combined-anchor expression freeze is not in the expected handoff state")
    if leakage_pass["overall_status"] != "LEAKAGE_AUDIT_PASS_REVIEWED_ACTIVATION_PENDING":
        raise ValueError("leakage pass review is not in the expected state")

    source_rows = read_csv(INPUT / "source_import_real_values_v12.csv")
    forbidden = (
        "v_obs_km_s;endpoint_residual;heldout_score;family_winner;best_fit_curve;"
        "posthoc_combined_anchor_value;posthoc_formula_switch;posthoc_weight_fit;"
        "posthoc_sign_choice;posthoc_normalization;numeric_prediction_value"
    )
    rows: list[dict[str, object]] = []
    for index, source in enumerate(source_rows, start=1):
        v_gas = float(source["v_gas_km_s"])
        v_disk = float(source["v_disk_km_s"])
        v_bulge = float(source["v_bulge_km_s"])
        s_gas = s_disk = s_bulge = 1
        w_gas = w_disk = w_bulge = 1
        n_anchor = 1
        anchor_sq = (
            s_gas * w_gas * v_gas * v_gas
            + s_disk * w_disk * v_disk * v_disk
            + s_bulge * w_bulge * v_bulge * v_bulge
        ) / n_anchor
        rows.append(
            {
                "combined_anchor_value_id": f"M0NDVACAVF08_{index:04d}",
                "galaxy_id": source["galaxy_id"],
                "radial_index": source["radial_index"],
                "radius_kpc": source["radius_kpc"],
                "v_gas_km_s": source["v_gas_km_s"],
                "v_disk_km_s": source["v_disk_km_s"],
                "v_bulge_km_s": source["v_bulge_km_s"],
                "s_gas": s_gas,
                "s_disk": s_disk,
                "s_bulge": s_bulge,
                "w_gas": w_gas,
                "w_disk": w_disk,
                "w_bulge": w_bulge,
                "n_anchor": n_anchor,
                "v_anchor_sq_km2_s2": f"{anchor_sq:.6f}",
                "v_anchor_km_s": f"{math.sqrt(anchor_sq):.6f}",
                "source_route": source["source_route"],
                "leakage_evidence_id": source["leakage_evidence_id"],
                "anchor_value_decision": "COMBINED_ANCHOR_VALUE_FROZEN_IDENTITY_BARYONIC_CARRIER",
                "next_required_artifact": NEXT_ARTIFACT,
                "forbidden_inputs": forbidden,
                "combined_anchor_values_written": "true",
                "velocity_formula_written": "false",
                "numeric_prediction_rows_written": 0,
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "m0_no_dark_velocity_anchor_combined_anchor_value_freeze_only_no_velocity_formula_no_predictions",
            }
        )
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    galaxies = {str(row["galaxy_id"]) for row in rows}
    identity_rows = sum(
        str(row["s_gas"]) == "1"
        and str(row["s_disk"]) == "1"
        and str(row["s_bulge"]) == "1"
        and str(row["w_gas"]) == "1"
        and str(row["w_disk"]) == "1"
        and str(row["w_bulge"]) == "1"
        and str(row["n_anchor"]) == "1"
        for row in rows
    )
    negative_anchor_sq_rows = sum(float(row["v_anchor_sq_km2_s2"]) < 0.0 for row in rows)
    return [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_ANCHOR_COMBINED_ANCHOR_VALUE_FREEZE_V08",
            "anchor_combined_anchor_value_artifact": "m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08",
            "source_rows_evaluated": len(rows),
            "galaxies_with_anchor_values": len(galaxies),
            "identity_weight_rows": identity_rows,
            "negative_anchor_sq_rows": negative_anchor_sq_rows,
            "combined_anchor_values_written": len(rows),
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": 0,
            "families_with_numeric_predictions": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_ANCHOR_COMBINED_ANCHOR_VALUES_FROZEN_BLOCKED_VELOCITY_FORMULA_BODY_FREEZE_MISSING",
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": "m0_no_dark_velocity_anchor_combined_anchor_value_freeze_only_no_velocity_formula_no_predictions_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08.md").write_text(
        f"""# M0 No-Dark Velocity-Anchor Combined Anchor Value Freeze v08

**Doc class:** velocity-anchor combined-anchor value-freeze gate
**Status:** combined-anchor values frozen; velocity formula body missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_anchor_combined_anchor_value_freeze.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08.csv
data/derived/m0_no_dark_velocity_anchor_combined_anchor_value_freeze_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08`
presence blocker by evaluating the frozen source-side combined-anchor expression
on the imported SPARC baryonic velocity components:

```text
{FROZEN_EXPRESSION}
```

The value freeze uses the canonical no-dark identity carrier:

```text
s_gas = s_disk = s_bulge = +1
w_gas = w_disk = w_bulge = 1
n_anchor = 1
```

This gives:

```text
v_anchor_sq_km2_s2 = v_gas_km_s^2 + v_disk_km_s^2 + v_bulge_km_s^2
v_anchor_km_s = sqrt(v_anchor_sq_km2_s2)
```

These are frozen anchor values, not `v_pred_km_s` family-prediction rows. The
route does not use observed velocities, endpoint residuals, heldout scores,
family winners, best-fit curves, posthoc fit quality, or any score-derived
normalization.

## Current Result

The expected status is:

```text
M0_NO_DARK_ANCHOR_COMBINED_ANCHOR_VALUES_FROZEN_BLOCKED_VELOCITY_FORMULA_BODY_FREEZE_MISSING
```

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This gate freezes source-side combined-anchor values only. It does not write a
velocity formula, does not emit `v_pred_km_s` rows, does not run endpoint
scoring, and does not decide whether a dark-sector component is required.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = combined_anchor_value_rows()
    write_csv(DERIVED / "m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08.csv", rows, VALUE_FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_velocity_anchor_combined_anchor_value_freeze_summary_v08.csv",
        summary(rows),
        SUMMARY_FIELDNAMES,
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_VELOCITY_ANCHOR_COMBINED_ANCHOR_VALUE_FREEZE_V08_BUILT")


if __name__ == "__main__":
    main()
