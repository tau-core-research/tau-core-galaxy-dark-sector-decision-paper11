#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"

PRIORITY_PLAN = {
    "SCD24_PROVENANCE_EVIDENCE": {
        "rank": 1,
        "dependency_class": "root_source_evidence",
        "unblock_mode": "serial_first",
        "why_next": "first missing source-side evidence artifact; downstream provenance promotion and audit depend on it",
        "actionable_next_step": "create reviewed data/input/source_import_provenance_evidence_v21.csv from external source provenance",
    },
    "SCD24_PROVENANCE_PROMOTION": {
        "rank": 2,
        "dependency_class": "source_provenance_downstream",
        "unblock_mode": "after_rank_1",
        "why_next": "promotion can only be reconsidered after the evidence gate allows it",
        "actionable_next_step": "rerun v22 and v23 after reviewed provenance evidence exists",
    },
    "SCD24_PROVENANCE_AUDIT": {
        "rank": 3,
        "dependency_class": "source_provenance_downstream",
        "unblock_mode": "after_rank_2",
        "why_next": "raw import must remain blocked until provenance completeness passes",
        "actionable_next_step": "rerun provenance audit after provenance promotion is allowed",
    },
    "SCD24_RAW_ADAPTER_INPUT": {
        "rank": 4,
        "dependency_class": "raw_source_input",
        "unblock_mode": "serial_source_import",
        "why_next": "raw source values are present and validation-pending; this gate must remain separate from v12 writes",
        "actionable_next_step": "keep v15 validation reproducible and proceed only through explicit v12 write authorization",
    },
    "SCD24_WRITE_AUTHORIZATION": {
        "rank": 5,
        "dependency_class": "source_import_authorization",
        "unblock_mode": "after_rank_4",
        "why_next": "the writer must remain disabled until explicit v12 source-import authorization is present",
        "actionable_next_step": "set PAPER11_ALLOW_REAL_SOURCE_IMPORT_WRITE=1 only after accepting the v15 raw input review boundary",
    },
    "SCD24_AUTHORIZED_WRITER": {
        "rank": 6,
        "dependency_class": "source_import_authorization",
        "unblock_mode": "after_rank_5",
        "why_next": "real v12 input should only be written by an authorized writer path",
        "actionable_next_step": "rerun authorized writer to produce data/input/source_import_real_values_v12.csv",
    },
    "SCD24_REAL_VALUES": {
        "rank": 7,
        "dependency_class": "observed_input_gate",
        "unblock_mode": "after_rank_6",
        "why_next": "row activation requires real observed input values to pass the value gate",
        "actionable_next_step": "rerun v12 real value gate after the authorized writer creates the target input",
    },
    "SCD24_LEAKAGE_AUDIT": {
        "rank": 8,
        "dependency_class": "source_blindness_gate",
        "unblock_mode": "after_rank_7",
        "why_next": "observed inputs must pass the leakage audit before scoring activation",
        "actionable_next_step": "rerun leakage audit after real values are present",
    },
    "SCD24_ROW_ACTIVATION": {
        "rank": 9,
        "dependency_class": "row_activation_gate",
        "unblock_mode": "after_rank_8",
        "why_next": "no galaxy row may enter endpoint scoring until value and leakage gates pass",
        "actionable_next_step": "rerun scoring activation gate after source-side gates pass",
    },
    "SCD24_FAMILY_FORMULA_TABLES": {
        "rank": 10,
        "dependency_class": "parallel_global_scoring_prerequisite",
        "unblock_mode": "parallel_with_source_import",
        "why_next": "family prediction tables can be prepared independently but cannot be scored yet",
        "actionable_next_step": "fill frozen family prediction table contract without using endpoint residuals",
    },
    "SCD24_PARAMETER_COUNTS": {
        "rank": 11,
        "dependency_class": "parallel_global_scoring_prerequisite",
        "unblock_mode": "parallel_with_source_import",
        "why_next": "parsimony scoring needs frozen numeric parameter counts before verdicts",
        "actionable_next_step": "fill numeric parameter count table under the frozen count policy",
    },
    "SCD24_CONTROL_RUNNERS": {
        "rank": 12,
        "dependency_class": "parallel_global_scoring_prerequisite",
        "unblock_mode": "parallel_with_source_import",
        "why_next": "controls must exist before any family comparison can be interpreted",
        "actionable_next_step": "implement control runner outputs without selecting a model winner",
    },
    "SCD24_DECISION_THRESHOLDS": {
        "rank": 13,
        "dependency_class": "parallel_global_scoring_prerequisite",
        "unblock_mode": "parallel_with_source_import",
        "why_next": "numeric thresholds must be frozen before any scoring verdict",
        "actionable_next_step": "freeze numeric decision thresholds before endpoint scores are computed",
    },
}


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


def priority_rows() -> list[dict[str, object]]:
    closure = read_csv(DERIVED / "scoring_dependency_closure_v24.csv")
    rows: list[dict[str, object]] = []
    for row in closure:
        plan = PRIORITY_PLAN[row["dependency_id"]]
        blocked = row["dependency_decision"] == "BLOCKED"
        rows.append(
            {
                "priority_rank": plan["rank"],
                "dependency_id": row["dependency_id"],
                "dependency_class": plan["dependency_class"],
                "unblock_mode": plan["unblock_mode"],
                "upstream_status": row["upstream_status"],
                "dependency_decision": row["dependency_decision"],
                "required_artifact": row["required_artifact"],
                "next_required_artifact": row["next_required_artifact"],
                "why_next": plan["why_next"],
                "actionable_next_step": plan["actionable_next_step"],
                "frontier_now": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "scoring_unblock_priority_only_no_scores_no_dark_sector_verdict",
            }
        )
    rows = sorted(rows, key=lambda item: int(item["priority_rank"]))
    for row in rows:
        if row["dependency_decision"] == "BLOCKED":
            row["frontier_now"] = "true"
            break
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    frontier = [row for row in rows if row["frontier_now"] == "true"]
    blocked = sum(row["dependency_decision"] == "BLOCKED" for row in rows)
    return [
        {
            "summary_id": "SCORING_UNBLOCK_PRIORITY_V25",
            "priority_rows": len(rows),
            "blocked_priority_rows": blocked,
            "frontier_now_rows": len(frontier),
            "first_frontier_dependency": frontier[0]["dependency_id"] if frontier else "none",
            "first_frontier_artifact": frontier[0]["next_required_artifact"] if frontier else "none",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SCORING_UNBLOCK_FRONTIER_IDENTIFIED" if frontier else "SCORING_UNBLOCK_FRONTIER_CLEAR",
            "claim_boundary": "scoring_unblock_priority_only_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = priority_rows()
    summary_rows = summary(rows)
    write_csv(
        DERIVED / "scoring_unblock_priority_v25.csv",
        rows,
        [
            "priority_rank",
            "dependency_id",
            "dependency_class",
            "unblock_mode",
            "upstream_status",
            "dependency_decision",
            "required_artifact",
            "next_required_artifact",
            "why_next",
            "actionable_next_step",
            "frontier_now",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "scoring_unblock_priority_summary_v25.csv",
        summary_rows,
        [
            "summary_id",
            "priority_rows",
            "blocked_priority_rows",
            "frontier_now_rows",
            "first_frontier_dependency",
            "first_frontier_artifact",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_SCORING_UNBLOCK_PRIORITY_V25_BUILT")


if __name__ == "__main__":
    main()
