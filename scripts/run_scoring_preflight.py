#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/source_manifest"
DERIVED = ROOT / "data/derived"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def input_requirements() -> list[dict[str, object]]:
    return [
        {
            "requirement_id": "SPR07_ACTIVE_ROWS",
            "required_artifact": "activated_scoring_rows_v08.csv",
            "purpose": "Declare exactly which galaxy rows enter train, heldout, challenge, and control scoring",
            "current_status": "BLOCKED_BY_SOURCE_ROW_AUDIT",
            "endpoint_scoring_allowed": "false",
            "blocking_source": "data/derived/activation_blockers_v06.csv",
            "claim_boundary": "preflight_only_no_scores",
        },
        {
            "requirement_id": "SPR07_OBSERVED_INPUTS",
            "required_artifact": "scoring_observed_inputs_v08.csv",
            "purpose": "Provide radial grid, observed velocity, uncertainty, and baryonic component inputs",
            "current_status": "BLOCKED_BY_SOURCE_IMPORT",
            "endpoint_scoring_allowed": "false",
            "blocking_source": "data/source_manifest/source_row_audit_v05.csv",
            "claim_boundary": "preflight_only_no_scores",
        },
        {
            "requirement_id": "SPR07_FAMILY_PREDICTIONS",
            "required_artifact": "family_prediction_tables_v08.csv",
            "purpose": "Provide frozen predicted velocity/readout arrays for M0, M1, and M2 before score aggregation",
            "current_status": "BLOCKED_BY_FORMULA_TABLES",
            "endpoint_scoring_allowed": "false",
            "blocking_source": "data/source_manifest/family_formula_table_v05.csv",
            "claim_boundary": "preflight_only_no_family_comparison",
        },
        {
            "requirement_id": "SPR07_PARAMETER_COUNTS",
            "required_artifact": "numeric_parameter_count_table_v08.csv",
            "purpose": "Provide numeric parameter and per-galaxy privilege counts for parsimony penalty",
            "current_status": "BLOCKED_BY_NUMERIC_COUNT_READINESS",
            "endpoint_scoring_allowed": "false",
            "blocking_source": "data/source_manifest/numeric_count_readiness_v05.csv",
            "claim_boundary": "preflight_only_no_parsimony_claim",
        },
        {
            "requirement_id": "SPR07_CONTROL_OUTPUTS",
            "required_artifact": "control_runner_outputs_v08.csv",
            "purpose": "Provide shuffle, wrong-family, null-source, leakage, radial, and parity control outputs",
            "current_status": "BLOCKED_BY_UNIMPLEMENTED_RUNNERS",
            "endpoint_scoring_allowed": "false",
            "blocking_source": "data/derived/control_runner_blockers_v06.csv",
            "claim_boundary": "preflight_only_no_control_result",
        },
        {
            "requirement_id": "SPR07_DECISION_THRESHOLDS",
            "required_artifact": "numeric_decision_thresholds_v08.csv",
            "purpose": "Provide numeric adequacy, improvement, stability, and unresolved thresholds before verdict",
            "current_status": "BLOCKED_BY_THRESHOLD_PENDING",
            "endpoint_scoring_allowed": "false",
            "blocking_source": "data/source_manifest/decision_threshold_v01.csv",
            "claim_boundary": "preflight_only_no_verdict",
        },
    ]


def formula_components() -> list[dict[str, object]]:
    rows = read_csv(SOURCE / "scoring_formula_freeze_v02.csv")
    out: list[dict[str, object]] = []
    for row in rows:
        out.append(
            {
                "formula_id": row["formula_id"],
                "score_component": row["score_component"],
                "formula_policy_status": "READY_AS_POLICY_NOT_RUN",
                "requires_input_artifacts": "activated_scoring_rows_v08.csv;scoring_observed_inputs_v08.csv;family_prediction_tables_v08.csv",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "scoring_formula_policy_only_no_score",
            }
        )
    return out


def summary(requirements: list[dict[str, object]], components: list[dict[str, object]]) -> list[dict[str, object]]:
    readiness = read_csv(DERIVED / "readiness_summary_v06.csv")[0]
    blocked_requirements = sum(1 for row in requirements if str(row["current_status"]).startswith("BLOCKED"))
    formula_policy_ready = len(components)
    endpoint_allowed = any(row["endpoint_scoring_allowed"] == "true" for row in requirements + components)
    return [
        {
            "summary_id": "SCORING_PREFLIGHT_V07",
            "readiness_dependency": readiness["overall_status"],
            "blocked_scoring_requirements": blocked_requirements,
            "formula_policy_components_ready": formula_policy_ready,
            "endpoint_scoring_allowed_anywhere": str(endpoint_allowed).lower(),
            "overall_status": "SCORING_NOT_READY",
            "next_required_artifact": "activated_scoring_rows_v08.csv",
            "claim_boundary": "scoring_preflight_only_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    requirements = input_requirements()
    components = formula_components()
    summary_rows = summary(requirements, components)
    write_csv(
        DERIVED / "scoring_input_requirements_v07.csv",
        requirements,
        [
            "requirement_id",
            "required_artifact",
            "purpose",
            "current_status",
            "endpoint_scoring_allowed",
            "blocking_source",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "scoring_formula_components_v07.csv",
        components,
        [
            "formula_id",
            "score_component",
            "formula_policy_status",
            "requires_input_artifacts",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "scoring_preflight_summary_v07.csv",
        summary_rows,
        [
            "summary_id",
            "readiness_dependency",
            "blocked_scoring_requirements",
            "formula_policy_components_ready",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_SCORING_PREFLIGHT_V07_BUILT")


if __name__ == "__main__":
    main()
