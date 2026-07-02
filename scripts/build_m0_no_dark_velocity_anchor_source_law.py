#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDNAMES = [
    "anchor_source_law_check_id",
    "anchor_source_law_component",
    "required_condition",
    "observed_status",
    "anchor_source_law_decision",
    "next_required_artifact",
    "forbidden_inputs",
    "anchor_source_law_written",
    "anchor_candidate_basis_written",
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


def anchor_source_law_rows() -> list[dict[str, object]]:
    dimension_anchor = summary_row("m0_no_dark_velocity_dimension_anchor_rule_summary_v08.csv")
    dimensional_trace = summary_row("m0_no_dark_payload_dimensional_trace_summary_v12.csv")
    readout_interface = summary_row("m0_no_dark_readout_equation_interface_summary_v08.csv")
    coefficient_policy = summary_row("m0_no_dark_coefficient_policy_summary_v07.csv")
    scale_policy = summary_row("m0_no_dark_scale_policy_summary_v07.csv")
    leakage_certificate = summary_row("m0_no_dark_payload_leakage_certificate_summary_v12.csv")
    common_forbidden = (
        "endpoint_residual;heldout_score;family_winner;best_fit_curve;"
        "posthoc_unit_rescale;posthoc_coefficient_fit;posthoc_anchor_choice;"
        "posthoc_anchor_candidate_selection"
    )
    rows = [
        {
            "anchor_source_law_check_id": "M0NDVASL08_DIMENSION_ANCHOR_HANDOFF",
            "anchor_source_law_component": "dimension_anchor_handoff",
            "required_condition": "dimension-anchor gate is present and identifies the missing source-law layer",
            "observed_status": dimension_anchor["overall_status"],
            "anchor_source_law_decision": "READY_FOR_ANCHOR_SOURCE_LAW_REVIEW",
            "next_required_artifact": "m0_no_dark_velocity_anchor_candidate_basis_v08",
        },
        {
            "anchor_source_law_check_id": "M0NDVASL08_SOURCE_LAW_SCOPE",
            "anchor_source_law_component": "source_law_scope",
            "required_condition": "velocity dimension must be sourced by a source-side law before any formula or numeric row exists",
            "observed_status": readout_interface["overall_status"],
            "anchor_source_law_decision": "ANCHOR_SOURCE_LAW_SCOPE_DECLARED",
            "next_required_artifact": "m0_no_dark_velocity_anchor_candidate_basis_v08",
        },
        {
            "anchor_source_law_check_id": "M0NDVASL08_DIMENSIONED_CARRIER_GUARD",
            "anchor_source_law_component": "dimensioned_carrier_guard",
            "required_condition": "candidate anchors must be source-side dimensioned carriers rather than fitted velocity residuals",
            "observed_status": dimensional_trace["overall_status"],
            "anchor_source_law_decision": "ANCHOR_SOURCE_LAW_CARRIER_GUARD_DECLARED",
            "next_required_artifact": "m0_no_dark_velocity_anchor_candidate_basis_v08",
        },
        {
            "anchor_source_law_check_id": "M0NDVASL08_NORMALIZATION_SEPARATION",
            "anchor_source_law_component": "normalization_separation_guard",
            "required_condition": "coefficient and scale policies remain separate from the anchor-source choice",
            "observed_status": f"{coefficient_policy['overall_status']}+{scale_policy['overall_status']}",
            "anchor_source_law_decision": "ANCHOR_SOURCE_LAW_NORMALIZATION_SEPARATION_DECLARED",
            "next_required_artifact": "m0_no_dark_velocity_anchor_candidate_basis_v08",
        },
        {
            "anchor_source_law_check_id": "M0NDVASL08_CANDIDATE_BASIS",
            "anchor_source_law_component": "anchor_candidate_basis",
            "required_condition": "a pre-scoring basis must list admissible anchor candidates and rejection rules",
            "observed_status": "NO_VELOCITY_ANCHOR_CANDIDATE_BASIS_PRESENT",
            "anchor_source_law_decision": "BLOCKED_ANCHOR_CANDIDATE_BASIS_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_candidate_basis_v08",
        },
        {
            "anchor_source_law_check_id": "M0NDVASL08_LEAKAGE_GUARD",
            "anchor_source_law_component": "leakage_guard",
            "required_condition": "candidate basis and later anchor choice cannot be selected from endpoint scores or residual fit quality",
            "observed_status": leakage_certificate["overall_status"],
            "anchor_source_law_decision": "READY_LEAKAGE_GUARD_ONLY",
            "next_required_artifact": "m0_no_dark_velocity_anchor_candidate_basis_v08",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["anchor_source_law_written"] = "true"
        row["anchor_candidate_basis_written"] = "false"
        row["velocity_formula_written"] = "false"
        row["numeric_prediction_rows_written"] = 0
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_velocity_anchor_source_law_gate_only_no_candidate_basis_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked = sum(str(row["anchor_source_law_decision"]).startswith("BLOCKED") for row in rows)
    return [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_ANCHOR_SOURCE_LAW_V08",
            "anchor_source_law_artifact": "m0_no_dark_velocity_anchor_source_law_v08",
            "anchor_source_law_checks": len(rows),
            "blocked_anchor_source_law_checks": blocked,
            "anchor_source_law_written": "true",
            "anchor_candidate_basis_written": "false",
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": 0,
            "families_with_numeric_predictions": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_ANCHOR_SOURCE_LAW_PRESENT_BLOCKED_ANCHOR_CANDIDATE_BASIS_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_candidate_basis_v08",
            "claim_boundary": "m0_no_dark_velocity_anchor_source_law_gate_only_no_candidate_basis_no_predictions_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_velocity_anchor_source_law_v08.md").write_text(
        """# M0 No-Dark Velocity-Anchor Source Law v08

**Doc class:** velocity-anchor source-law gate
**Status:** source-law gate present; anchor candidate basis missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_anchor_source_law.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_anchor_source_law_v08.csv
data/derived/m0_no_dark_velocity_anchor_source_law_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_anchor_source_law_v08` presence
blocker by declaring the rule class for a lawful velocity anchor. The no-dark
M0 route may only obtain velocity dimension from a source-side, pre-scoring,
dimensioned carrier. The anchor cannot be chosen from endpoint residuals,
heldout scores, family winners, best-fit curves, posthoc rescaling, or fitted
coefficient quality.

The artifact intentionally does not list the admissible candidate carriers.
That narrower basis remains the next required gate.

## Current Result

The expected status is:

```text
M0_NO_DARK_ANCHOR_SOURCE_LAW_PRESENT_BLOCKED_ANCHOR_CANDIDATE_BASIS_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_anchor_candidate_basis_v08
```

## Claim Boundary

This gate declares only the source-law admissibility layer. It does not choose an anchor candidate, does not choose an anchor value, does not assign coupling normalization, does not write a velocity formula, does not write prediction rows, does not run endpoint scoring, and does not decide whether a dark-sector component is required.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = anchor_source_law_rows()
    write_csv(DERIVED / "m0_no_dark_velocity_anchor_source_law_v08.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_velocity_anchor_source_law_summary_v08.csv",
        summary(rows),
        [
            "summary_id",
            "anchor_source_law_artifact",
            "anchor_source_law_checks",
            "blocked_anchor_source_law_checks",
            "anchor_source_law_written",
            "anchor_candidate_basis_written",
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
    print("PAPER11_M0_NO_DARK_VELOCITY_ANCHOR_SOURCE_LAW_V08_BUILT")


if __name__ == "__main__":
    main()
