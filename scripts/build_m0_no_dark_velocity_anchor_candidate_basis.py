#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDNAMES = [
    "anchor_candidate_check_id",
    "anchor_candidate_component",
    "candidate_class",
    "required_condition",
    "observed_status",
    "candidate_basis_decision",
    "next_required_artifact",
    "forbidden_inputs",
    "candidate_basis_written",
    "anchor_selection_rule_written",
    "anchor_value_written",
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


def candidate_basis_rows() -> list[dict[str, object]]:
    source_law = summary_row("m0_no_dark_velocity_anchor_source_law_summary_v08.csv")
    dimensional_trace = summary_row("m0_no_dark_payload_dimensional_trace_summary_v12.csv")
    readout_interface = summary_row("m0_no_dark_readout_equation_interface_summary_v08.csv")
    leakage_certificate = summary_row("m0_no_dark_payload_leakage_certificate_summary_v12.csv")
    common_forbidden = (
        "vobs;endpoint_residual;heldout_score;family_winner;best_fit_curve;"
        "posthoc_unit_rescale;posthoc_coefficient_fit;posthoc_anchor_choice;"
        "posthoc_candidate_pruning"
    )
    rows = [
        {
            "anchor_candidate_check_id": "M0NDVACB08_SOURCE_LAW_HANDOFF",
            "anchor_candidate_component": "source_law_handoff",
            "candidate_class": "none_handoff",
            "required_condition": "anchor-source-law gate is present and identifies candidate basis as the next blocker",
            "observed_status": source_law["overall_status"],
            "candidate_basis_decision": "READY_FOR_ANCHOR_CANDIDATE_BASIS_REVIEW",
            "next_required_artifact": "m0_no_dark_velocity_anchor_selection_rule_v08",
        },
        {
            "anchor_candidate_check_id": "M0NDVACB08_BARYONIC_GRAVITY_CARRIER",
            "anchor_candidate_component": "admissible_candidate_class",
            "candidate_class": "source_side_baryonic_gravity_velocity_carrier",
            "required_condition": "candidate may be a source-side baryonic gravitational velocity or acceleration carrier derived before scoring",
            "observed_status": dimensional_trace["overall_status"],
            "candidate_basis_decision": "ADMISSIBLE_CANDIDATE_CLASS_DECLARED",
            "next_required_artifact": "m0_no_dark_velocity_anchor_selection_rule_v08",
        },
        {
            "anchor_candidate_check_id": "M0NDVACB08_SOURCE_FIELD_DIMENSIONED_CARRIER",
            "anchor_candidate_component": "admissible_candidate_class",
            "candidate_class": "source_side_dimensioned_field_carrier",
            "required_condition": "candidate may be a predeclared source-side field carrier with velocity or acceleration dimension and no endpoint tuning",
            "observed_status": readout_interface["overall_status"],
            "candidate_basis_decision": "ADMISSIBLE_CANDIDATE_CLASS_DECLARED",
            "next_required_artifact": "m0_no_dark_velocity_anchor_selection_rule_v08",
        },
        {
            "anchor_candidate_check_id": "M0NDVACB08_IMPORTED_SOURCE_SCALE_CARRIER",
            "anchor_candidate_component": "conditional_candidate_class",
            "candidate_class": "independent_imported_source_scale_carrier",
            "required_condition": "candidate may be an independently imported source scale only if provenance and leakage gates mark it pre-scoring and non-rotation-fitted",
            "observed_status": leakage_certificate["overall_status"],
            "candidate_basis_decision": "CONDITIONAL_CANDIDATE_CLASS_DECLARED",
            "next_required_artifact": "m0_no_dark_velocity_anchor_selection_rule_v08",
        },
        {
            "anchor_candidate_check_id": "M0NDVACB08_FORBIDDEN_ROTATION_FIT_CARRIER",
            "anchor_candidate_component": "rejected_candidate_class",
            "candidate_class": "observed_rotation_or_residual_fit_carrier",
            "required_condition": "observed rotation, residual quality, family winner, and posthoc fitted scale cannot be candidate anchors",
            "observed_status": "FORBIDDEN_BY_SOURCE_LAW_AND_LEAKAGE_GUARD",
            "candidate_basis_decision": "REJECTED_CANDIDATE_CLASS_DECLARED",
            "next_required_artifact": "m0_no_dark_velocity_anchor_selection_rule_v08",
        },
        {
            "anchor_candidate_check_id": "M0NDVACB08_SELECTION_RULE",
            "anchor_candidate_component": "anchor_selection_rule",
            "candidate_class": "none_selection_rule",
            "required_condition": "a pre-scoring rule must choose among admissible candidate classes before any formula or numeric row exists",
            "observed_status": "NO_VELOCITY_ANCHOR_SELECTION_RULE_PRESENT",
            "candidate_basis_decision": "BLOCKED_ANCHOR_SELECTION_RULE_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_selection_rule_v08",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["candidate_basis_written"] = "true"
        row["anchor_selection_rule_written"] = "false"
        row["anchor_value_written"] = "false"
        row["velocity_formula_written"] = "false"
        row["numeric_prediction_rows_written"] = 0
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_velocity_anchor_candidate_basis_gate_only_no_selection_rule_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked = sum(str(row["candidate_basis_decision"]).startswith("BLOCKED") for row in rows)
    admissible = sum(
        str(row["candidate_basis_decision"])
        in {"ADMISSIBLE_CANDIDATE_CLASS_DECLARED", "CONDITIONAL_CANDIDATE_CLASS_DECLARED"}
        for row in rows
    )
    rejected = sum(str(row["candidate_basis_decision"]) == "REJECTED_CANDIDATE_CLASS_DECLARED" for row in rows)
    return [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_ANCHOR_CANDIDATE_BASIS_V08",
            "anchor_candidate_basis_artifact": "m0_no_dark_velocity_anchor_candidate_basis_v08",
            "candidate_basis_checks": len(rows),
            "admissible_candidate_classes": admissible,
            "rejected_candidate_classes": rejected,
            "blocked_candidate_basis_checks": blocked,
            "candidate_basis_written": "true",
            "anchor_selection_rule_written": "false",
            "anchor_value_written": "false",
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": 0,
            "families_with_numeric_predictions": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_ANCHOR_CANDIDATE_BASIS_PRESENT_BLOCKED_ANCHOR_SELECTION_RULE_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_selection_rule_v08",
            "claim_boundary": "m0_no_dark_velocity_anchor_candidate_basis_gate_only_no_selection_rule_no_anchor_value_no_predictions_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_velocity_anchor_candidate_basis_v08.md").write_text(
        """# M0 No-Dark Velocity-Anchor Candidate Basis v08

**Doc class:** velocity-anchor candidate-basis gate
**Status:** candidate basis present; anchor selection rule missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_anchor_candidate_basis.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_anchor_candidate_basis_v08.csv
data/derived/m0_no_dark_velocity_anchor_candidate_basis_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_anchor_candidate_basis_v08`
presence blocker by listing only admissible classes of velocity-anchor carriers.
The candidate basis is source-side and pre-scoring. It permits only candidate
classes that can carry velocity or acceleration dimension without using
observed rotation residuals, heldout scores, family winners, best-fit curves,
posthoc rescaling, or fitted coefficient quality.

The basis does not choose among candidates. That narrower choice remains the
next required gate.

## Current Result

The expected status is:

```text
M0_NO_DARK_ANCHOR_CANDIDATE_BASIS_PRESENT_BLOCKED_ANCHOR_SELECTION_RULE_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_anchor_selection_rule_v08
```

## Claim Boundary

This gate declares only admissible and rejected candidate classes. It does not choose an anchor candidate, does not choose an anchor value, does not assign coupling normalization, does not write a velocity formula, does not write prediction rows, does not run endpoint scoring, and does not decide whether a dark-sector component is required.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = candidate_basis_rows()
    write_csv(DERIVED / "m0_no_dark_velocity_anchor_candidate_basis_v08.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_velocity_anchor_candidate_basis_summary_v08.csv",
        summary(rows),
        [
            "summary_id",
            "anchor_candidate_basis_artifact",
            "candidate_basis_checks",
            "admissible_candidate_classes",
            "rejected_candidate_classes",
            "blocked_candidate_basis_checks",
            "candidate_basis_written",
            "anchor_selection_rule_written",
            "anchor_value_written",
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
    print("PAPER11_M0_NO_DARK_VELOCITY_ANCHOR_CANDIDATE_BASIS_V08_BUILT")


if __name__ == "__main__":
    main()
