#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDNAMES = [
    "scale_policy_id",
    "policy_class",
    "scale_scope",
    "allowed_policy",
    "blocked_policy",
    "shape_readout_guard",
    "counting_rule",
    "forbidden_inputs",
    "policy_status",
    "numeric_scale_values_written",
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


def coefficient_policy_ready() -> bool:
    path = DERIVED / "m0_no_dark_coefficient_policy_summary_v07.csv"
    if not path.exists():
        return False
    rows = read_csv(path)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_COEFFICIENT_POLICY_READY"
        and rows[0]["numeric_values_written"] == "0"
        and rows[0]["prediction_rows_written"] == "0"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def policy_rows() -> list[dict[str, object]]:
    common_forbidden = (
        "endpoint_residual;heldout_score;family_winner;best_fit_curve;"
        "posthoc_scale_selection;posthoc_radial_window;per_galaxy_rescue_scale"
    )
    rows = [
        {
            "scale_policy_id": "M0NDSP07_RADIAL_DOMAIN",
            "policy_class": "radial_domain_policy",
            "scale_scope": "shared_radial_grid_and_admissible_radial_domain",
            "allowed_policy": "radial-domain use must follow the imported shared grid and predeclared admissibility route",
            "blocked_policy": "choosing a galaxy-specific radial window after observing endpoint residual shape",
            "shape_readout_guard": "radial-domain failures must remain visible as blocked or fallback states, not hidden by window selection",
            "counting_rule": "any later adjustable radial-domain privilege counts before endpoint scoring",
        },
        {
            "scale_policy_id": "M0NDSP07_NORMALIZATION_SCALE",
            "policy_class": "normalization_policy",
            "scale_scope": "baryonic_and_readout_normalization_scales",
            "allowed_policy": "normalization scales must be source-side, globally declared, or explicitly counted before predictions",
            "blocked_policy": "using a hidden normalization scale to convert a weak shape route into a fitted level route",
            "shape_readout_guard": "normalization cannot collapse level/amplitude support into shape/readout support",
            "counting_rule": "each adjustable normalization scale counts at the declared family level or per galaxy if private",
        },
        {
            "scale_policy_id": "M0NDSP07_TRANSITION_SCALE",
            "policy_class": "transition_policy",
            "scale_scope": "inner_outer_or_low_acceleration_transition_scales",
            "allowed_policy": "transition scales may be symbolic or source-rule derived only if frozen before prediction rows",
            "blocked_policy": "placing transition radii at residual features or family-winner-favorable breakpoints",
            "shape_readout_guard": "transition behavior must be audited separately from endpoint residual improvement",
            "counting_rule": "each adjustable transition scale counts unless frozen as a non-numeric source-side rule",
        },
        {
            "scale_policy_id": "M0NDSP07_SCALE_INVARIANCE_LIMITS",
            "policy_class": "known_limit_policy",
            "scale_scope": "zero_source_large_radius_small_radius_and_inactive_limits",
            "allowed_policy": "known-limit behavior must be stated as constraints before any executable formula is admitted",
            "blocked_policy": "allowing the formula to change scale behavior silently outside the tested radial range",
            "shape_readout_guard": "limit failures cannot be repaired by endpoint-specific scale exceptions",
            "counting_rule": "limit exceptions count as explicit fallback or family privileges",
        },
        {
            "scale_policy_id": "M0NDSP07_ROW_SHARED_POLICY",
            "policy_class": "row_shared_policy",
            "scale_scope": "row_family_and_population_level_scale_reuse",
            "allowed_policy": "scale rules must be reusable across rows unless a predeclared counted privilege says otherwise",
            "blocked_policy": "private per-row scale rules selected after inspecting row sensitivity or controls",
            "shape_readout_guard": "row sensitivity is a diagnostic/control signal, not authorization for a private rescue scale",
            "counting_rule": "private row scales count per row and block no-dark simplicity claims",
        },
        {
            "scale_policy_id": "M0NDSP07_FALLBACK_HANDOFF",
            "policy_class": "fallback_handoff_policy",
            "scale_scope": "scale_missing_null_or_inadmissible_routes",
            "allowed_policy": "missing, null, or inadmissible scale routes hand off to the declared fallback policy",
            "blocked_policy": "creating a silent scale exception that writes predictions before fallback authorization",
            "shape_readout_guard": "scale failure must remain distinguishable from formula failure and source-label failure",
            "counting_rule": "fallback handoff writes no numeric prediction until the fallback policy is closed",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["policy_status"] = "READY" if coefficient_policy_ready() else "BLOCKED_UPSTREAM_COEFFICIENT_POLICY"
        row["numeric_scale_values_written"] = 0
        row["prediction_rows_written"] = 0
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_scale_policy_only_no_values_no_predictions_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["policy_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    return [
        {
            "summary_id": "M0_NO_DARK_SCALE_POLICY_V07",
            "source_artifact": "m0_no_dark_coefficient_policy_v07",
            "policy_rows": len(rows),
            "ready_policy_rows": ready,
            "blocked_policy_rows": blocked,
            "numeric_scale_values_written": 0,
            "prediction_rows_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_SCALE_POLICY_READY"
            if blocked == 0
            else "M0_NO_DARK_SCALE_POLICY_BLOCKED",
            "next_required_artifact": "m0_no_dark_fallback_policy_v07"
            if blocked == 0
            else "m0_no_dark_coefficient_policy_v07",
            "claim_boundary": "m0_no_dark_scale_policy_only_no_values_no_predictions_no_scores_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_scale_policy_v07.md").write_text(
        """# M0 No-Dark Scale Policy v07

**Doc class:** no-dark M0 formula-table scale policy
**Status:** scale policy ready; no numeric scale values; no predictions; no scoring

Script:

```text
scripts/build_m0_no_dark_scale_policy.py
```

Derived outputs:

```text
data/derived/m0_no_dark_scale_policy_v07.csv
data/derived/m0_no_dark_scale_policy_summary_v07.csv
```

This artifact fills the fixed-scale policy slot of the M0 no-dark formula
table. It imports the coefficient-policy discipline from
`m0_no_dark_coefficient_policy_v07` and projects it to scale use: radial-domain
scope, normalization scales, transition scales, known-limit behavior, row-level
scale reuse, and fallback handoff.

## Current Result

The expected status is:

```text
M0_NO_DARK_SCALE_POLICY_READY
```

The policy is shape-aware after the Paper 10 update:

```text
scale choice != residual-window rescue
level/amplitude support != shape/readout support
```

It forbids post-hoc radial windows, hidden normalization scales, private
per-galaxy rescue scales, and endpoint-selected transition radii. Any later
adjustable scale, threshold, radial window, transition rule, or private row
privilege must be declared and counted before endpoint scoring.

The next formula-table policy blocker is:

```text
m0_no_dark_fallback_policy_v07
```

## Claim Boundary

This policy does not assign numeric scale values, write prediction rows,
compute velocities, compare M0/M1/M2, or decide the dark-sector question. It
only closes the fixed-scale policy slot of the M0 no-dark formula table.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = policy_rows()
    write_csv(DERIVED / "m0_no_dark_scale_policy_v07.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_scale_policy_summary_v07.csv",
        summary(rows),
        [
            "summary_id",
            "source_artifact",
            "policy_rows",
            "ready_policy_rows",
            "blocked_policy_rows",
            "numeric_scale_values_written",
            "prediction_rows_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_SCALE_POLICY_V07_BUILT")


if __name__ == "__main__":
    main()
