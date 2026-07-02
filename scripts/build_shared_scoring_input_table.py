#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDS = [
    "shared_input_id",
    "family_scope",
    "formula_slot",
    "input_component",
    "component_scope",
    "frozen_statement",
    "allowed_values",
    "counting_policy",
    "forbidden_inputs",
    "shared_input_status",
    "numeric_input_values_written",
    "family_prediction_rows_written",
    "endpoint_scoring_allowed",
    "next_required_artifact",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "shared_input_artifact",
    "m2_nuisance_status",
    "family_scope",
    "formula_slot",
    "shared_input_components",
    "numeric_input_values_written",
    "family_prediction_rows_written",
    "endpoint_scoring_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]

NEXT_ARTIFACT = "numeric_parameter_count_table_v06"
READY_STATUS = "SHARED_SCORING_INPUT_TABLE_READY_PARAMETER_COUNTS_BLOCKED"
FORBIDDEN_INPUTS = (
    "endpoint_residual;heldout_score;family_winner;posthoc_radial_mask;"
    "posthoc_component_drop;posthoc_uncertainty_policy;posthoc_grid_change"
)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def m2_nuisance_status() -> str:
    rows = read_csv(DERIVED / "m2_nuisance_policy_table_summary_v06.csv")
    if not rows:
        return "M2_NUISANCE_POLICY_TABLE_MISSING"
    return rows[0]["overall_status"]


def input_rows() -> list[dict[str, object]]:
    base = {
        "family_scope": "ALL",
        "formula_slot": "shared_scoring_inputs",
        "forbidden_inputs": FORBIDDEN_INPUTS,
        "shared_input_status": "READY",
        "numeric_input_values_written": "0",
        "family_prediction_rows_written": "0",
        "endpoint_scoring_allowed": "false",
        "next_required_artifact": NEXT_ARTIFACT,
        "claim_boundary": "shared_scoring_input_table_only_no_numeric_inputs_no_predictions_no_scores_no_validation",
    }
    return [
        {
            **base,
            "shared_input_id": "SSIT06_DATA_LOADER",
            "input_component": "data_loader_policy",
            "component_scope": "family_independent_input_loading_before_scoring",
            "frozen_statement": "All families must use the same source-side input loader contract before endpoint scoring.",
            "allowed_values": "authorized_real_value_input;frozen_source_import_schema;no_family_specific_loader",
            "counting_policy": "family-specific loader exceptions must be counted or block endpoint eligibility",
        },
        {
            **base,
            "shared_input_id": "SSIT06_RADIAL_GRID",
            "input_component": "radial_grid_policy",
            "component_scope": "shared_radius_grid_and_row_alignment",
            "frozen_statement": "The scored radial grid and row alignment must be shared across families and cannot be changed from residuals.",
            "allowed_values": "activated_rows_only;source_import_radius_grid;no_posthoc_grid_change",
            "counting_policy": "post-freeze grid changes invalidate scoring eligibility",
        },
        {
            **base,
            "shared_input_id": "SSIT06_RADIAL_MASK",
            "input_component": "radial_mask_policy",
            "component_scope": "shared_masking_and_exclusion_policy",
            "frozen_statement": "Radial masks and exclusions must be declared before endpoint family comparison.",
            "allowed_values": "public_quality_mask;predeclared_common_mask;no_posthoc_radial_mask",
            "counting_policy": "family-specific masks count as tuning privileges unless source-side and predeclared",
        },
        {
            **base,
            "shared_input_id": "SSIT06_UNCERTAINTY",
            "input_component": "uncertainty_handling_policy",
            "component_scope": "shared_weighting_error_floor_and_covariance_policy",
            "frozen_statement": "Uncertainty handling and row weights must be common across families before scoring.",
            "allowed_values": "published_uncertainties;predeclared_error_floor;predeclared_covariance_policy",
            "counting_policy": "post-freeze uncertainty changes block endpoint verdict eligibility",
        },
        {
            **base,
            "shared_input_id": "SSIT06_BARYONIC_COMPONENTS",
            "input_component": "baryonic_component_policy",
            "component_scope": "shared_gas_disk_bulge_component_availability",
            "frozen_statement": "Baryonic component availability and missing-component handling must be common before scoring.",
            "allowed_values": "source_catalog_components;predeclared_missing_component_rule;no_posthoc_component_drop",
            "counting_policy": "family-specific component dropping is forbidden unless predeclared and counted",
        },
        {
            **base,
            "shared_input_id": "SSIT06_PREDICTION_HANDOFF",
            "input_component": "parameter_count_handoff",
            "component_scope": "numeric_parameter_count_handoff",
            "frozen_statement": "Endpoint scoring remains blocked until all family adjustable privileges are counted before scoring.",
            "allowed_values": "NO_ENDPOINT_SCORING;HANDOFF_BLOCKED_PENDING_PARAMETER_COUNTS",
            "counting_policy": "all later scoring runs must consume the frozen count table before any score is computed",
        },
    ]


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "SHARED_SCORING_INPUT_TABLE_V06",
            "shared_input_artifact": "shared_scoring_input_table_v06",
            "m2_nuisance_status": m2_nuisance_status(),
            "family_scope": "ALL",
            "formula_slot": "shared_scoring_inputs",
            "shared_input_components": len(rows),
            "numeric_input_values_written": "0",
            "family_prediction_rows_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": READY_STATUS,
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": "shared_scoring_input_table_only_no_numeric_inputs_no_predictions_no_scores_no_validation",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "shared_scoring_input_table_v06.md").write_text(
        f"""# Shared Scoring Input Table v06

**Doc class:** shared scoring-input contract
**Status:** shared input policy ready; parameter counts blocked; no scoring

Script:

```text
scripts/build_shared_scoring_input_table.py
```

Derived outputs:

```text
data/derived/shared_scoring_input_table_v06.csv
data/derived/shared_scoring_input_table_summary_v06.csv
```

This artifact fills the `shared_scoring_inputs` slot as a family-independent
pre-scoring contract. It freezes the data-loader policy, radial-grid policy,
radial-mask policy, uncertainty-handling policy, baryonic-component policy, and
parameter-count handoff before any endpoint score can be computed.

## Current Result

The expected status is:

```text
{READY_STATUS}
```

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This table writes no numeric input values, writes no family prediction rows,
computes no endpoint scores, compares no families, and makes no dark-sector
verdict. It only freezes the shared input policy required before parameter
counts can be reviewed.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = input_rows()
    write_csv(DERIVED / "shared_scoring_input_table_v06.csv", rows, FIELDS)
    write_csv(DERIVED / "shared_scoring_input_table_summary_v06.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER11_SHARED_SCORING_INPUT_TABLE_V06_BUILT")


if __name__ == "__main__":
    main()
