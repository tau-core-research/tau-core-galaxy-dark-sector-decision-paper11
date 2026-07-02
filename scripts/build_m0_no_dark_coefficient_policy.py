#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDNAMES = [
    "policy_id",
    "policy_class",
    "coefficient_scope",
    "allowed_policy",
    "blocked_policy",
    "shape_readout_guard",
    "counting_rule",
    "forbidden_inputs",
    "policy_status",
    "numeric_values_written",
    "prediction_rows_written",
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


def upstream_policy_ready() -> bool:
    path = DERIVED / "m0_no_dark_expression_coefficient_freeze_summary_v12.csv"
    if not path.exists():
        return False
    rows = read_csv(path)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_EXPRESSION_COEFFICIENT_FREEZE_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def policy_rows() -> list[dict[str, object]]:
    common_forbidden = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_parameter_discount;posthoc_shape_selection"
    rows = [
        {
            "policy_id": "M0NDCP07_NO_DARK_EXCLUSION",
            "policy_class": "family_boundary",
            "coefficient_scope": "no_dark_constraint",
            "allowed_policy": "M0 carries no hidden dark-sector response coefficient; any explicit response coefficient disqualifies the row from M0",
            "blocked_policy": "using a hidden halo, acceleration, potential, density, or response amplitude as an M0 rescue",
            "shape_readout_guard": "shape/readout terms must remain source-side morphology/readout terms, not dark-response substitutes",
            "counting_rule": "no numeric coefficient is assigned here; later adjustable response-like coefficients are non-M0 privileges",
        },
        {
            "policy_id": "M0NDCP07_GLOBAL_COEFFICIENT_EXPOSURE",
            "policy_class": "global_coefficient_policy",
            "coefficient_scope": "global_or_family_level_coefficients",
            "allowed_policy": "global coefficients may be fixed, symbolic, or explicitly counted before prediction rows",
            "blocked_policy": "discounting global coefficients after inspecting endpoint scores or family winner",
            "shape_readout_guard": "a global coefficient cannot collapse shape/readout evidence into a single tuned level",
            "counting_rule": "each adjustable global coefficient counts at full declared family cost in later numeric-count tables",
        },
        {
            "policy_id": "M0NDCP07_PER_GALAXY_PRIVILEGE",
            "policy_class": "per_galaxy_policy",
            "coefficient_scope": "per_galaxy_coefficients_or_switches",
            "allowed_policy": "per-galaxy coefficients are forbidden unless predeclared as counted privileges before scoring",
            "blocked_policy": "choosing per-galaxy amplitudes, switches, or rescue constants from residual shape",
            "shape_readout_guard": "row/galaxy sensitivity must be audited as a control signal, not repaired by a private coefficient",
            "counting_rule": "any permitted per-galaxy privilege counts per galaxy and blocks no-dark simplicity claims",
        },
        {
            "policy_id": "M0NDCP07_BARYONIC_NORMALIZATION",
            "policy_class": "source_input_policy",
            "coefficient_scope": "baryonic_mass_or_unit_normalization",
            "allowed_policy": "baryonic normalizations must be source-side, fixed by the imported mass model, or explicitly counted",
            "blocked_policy": "using best-fit baryonic rescaling as an undeclared no-dark coefficient",
            "shape_readout_guard": "baryonic normalization cannot be selected to mimic Paper 10-style shape/readout support",
            "counting_rule": "adjustable baryonic normalization counts as a declared parameter in later numeric-count tables",
        },
        {
            "policy_id": "M0NDCP07_READOUT_OPERATOR_SHAPE",
            "policy_class": "shape_readout_policy",
            "coefficient_scope": "readout_operator_amplitudes_scales_thresholds",
            "allowed_policy": "readout operator amplitudes, radial scales, thresholds, and kernel-shape roles must be exposed before predictions",
            "blocked_policy": "choosing operator parameters from held-out residuals, family winner, or post-score curve shape",
            "shape_readout_guard": "level/amplitude and shape/readout support must remain separate columns in later prediction contracts",
            "counting_rule": "every adjustable readout operator coefficient or scale counts unless frozen as a non-numeric source rule",
        },
        {
            "policy_id": "M0NDCP07_FAILURE_AND_NULL_ROUTE",
            "policy_class": "failure_route_policy",
            "coefficient_scope": "null_fallback_or_missing_label_routes",
            "allowed_policy": "missing labels, inadmissible terms, or null routes may only route to declared fallback states",
            "blocked_policy": "creating a silent exception coefficient or residual-specific rescue term in a failure route",
            "shape_readout_guard": "shape failure cannot be converted into a fitted level rescue",
            "counting_rule": "fallback routes write no numeric prediction unless a later explicit fallback policy authorizes it",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["policy_status"] = "READY" if upstream_policy_ready() else "BLOCKED_UPSTREAM_COEFFICIENT_FREEZE"
        row["numeric_values_written"] = 0
        row["prediction_rows_written"] = 0
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_coefficient_policy_only_no_values_no_predictions_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["policy_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    return [
        {
            "summary_id": "M0_NO_DARK_COEFFICIENT_POLICY_V07",
            "source_artifact": "m0_no_dark_expression_coefficient_freeze_v12",
            "policy_rows": len(rows),
            "ready_policy_rows": ready,
            "blocked_policy_rows": blocked,
            "numeric_values_written": 0,
            "prediction_rows_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_COEFFICIENT_POLICY_READY"
            if blocked == 0
            else "M0_NO_DARK_COEFFICIENT_POLICY_BLOCKED",
            "next_required_artifact": "m0_no_dark_scale_policy_v07"
            if blocked == 0
            else "m0_no_dark_expression_coefficient_freeze_v12",
            "claim_boundary": "m0_no_dark_coefficient_policy_only_no_values_no_predictions_no_scores_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_coefficient_policy_v07.md").write_text(
        """# M0 No-Dark Coefficient Policy v07

**Doc class:** no-dark M0 formula-table coefficient policy
**Status:** coefficient policy ready; no numeric values; no predictions; no scoring

Script:

```text
scripts/build_m0_no_dark_coefficient_policy.py
```

Derived outputs:

```text
data/derived/m0_no_dark_coefficient_policy_v07.csv
data/derived/m0_no_dark_coefficient_policy_summary_v07.csv
```

This artifact fills the first concrete formula-table policy blocker identified
by the v81/v82 scoring frontier. It imports the expression-side coefficient
freeze discipline from `m0_no_dark_expression_coefficient_freeze_v12` and
projects it to the M0 formula-table level.

## Current Result

The expected status is:

```text
M0_NO_DARK_COEFFICIENT_POLICY_READY
```

The policy is shape-aware after the Paper 10 update:

```text
level/amplitude support != shape/readout support
```

It forbids hidden dark-sector compensation inside M0 and requires any future
adjustable coefficient, scale, switch, threshold, or per-galaxy privilege to be
declared and counted before endpoint scoring.

The next formula-table policy blocker is:

```text
m0_no_dark_scale_policy_v07
```

## Claim Boundary

This policy does not assign numeric coefficient values, write prediction rows,
compute velocities, compare M0/M1/M2, or decide the dark-sector question. It
only closes the coefficient-policy slot of the M0 no-dark formula table.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = policy_rows()
    write_csv(DERIVED / "m0_no_dark_coefficient_policy_v07.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_coefficient_policy_summary_v07.csv",
        summary(rows),
        [
            "summary_id",
            "source_artifact",
            "policy_rows",
            "ready_policy_rows",
            "blocked_policy_rows",
            "numeric_values_written",
            "prediction_rows_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_COEFFICIENT_POLICY_V07_BUILT")


if __name__ == "__main__":
    main()
