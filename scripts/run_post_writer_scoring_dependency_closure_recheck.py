#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
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


def recheck_rows() -> list[dict[str, object]]:
    dependencies = read_csv(DERIVED / "scoring_dependency_closure_v24.csv")
    preflight_summary = read_csv(DERIVED / "post_writer_scoring_preflight_recheck_summary_v39.csv")[0]
    out: list[dict[str, object]] = []
    for index, row in enumerate(dependencies, start=1):
        blockers = []
        if row["dependency_decision"] != "READY":
            blockers.append("v24_dependency_not_ready")
        if preflight_summary["ready_requirements_after_recheck"] == "0":
            blockers.append("post_writer_preflight_recheck_zero_ready_requirements")
        if preflight_summary["endpoint_scoring_allowed_anywhere"] != "true":
            blockers.append("post_writer_preflight_recheck_scoring_not_allowed")
        out.append(
            {
                "recheck_id": f"PWSCD40_{index:03d}",
                "dependency_id": row["dependency_id"],
                "scoring_stage": row["scoring_stage"],
                "required_artifact": row["required_artifact"],
                "v24_dependency_decision": row["dependency_decision"],
                "v24_upstream_status": row["upstream_status"],
                "v39_ready_requirements_after_recheck": preflight_summary["ready_requirements_after_recheck"],
                "dependency_recheck_blockers": ";".join(blockers),
                "dependency_decision_after_recheck": "BLOCKED" if blockers else "READY",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "post_writer_scoring_dependency_closure_recheck_only_no_scores",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked = sum(row["dependency_decision_after_recheck"] == "BLOCKED" for row in rows)
    return [
        {
            "summary_id": "POST_WRITER_SCORING_DEPENDENCY_CLOSURE_RECHECK_V40",
            "dependencies_rechecked": len(rows),
            "ready_dependencies_after_recheck": len(rows) - blocked,
            "blocked_dependencies_after_recheck": blocked,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_SCORING_DEPENDENCY_CLOSURE_RECHECK_BLOCKED"
            if blocked
            else "POST_WRITER_SCORING_DEPENDENCY_CLOSURE_RECHECK_READY",
            "claim_boundary": "post_writer_scoring_dependency_closure_recheck_only_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = recheck_rows()
    write_csv(
        DERIVED / "post_writer_scoring_dependency_closure_recheck_v40.csv",
        rows,
        [
            "recheck_id",
            "dependency_id",
            "scoring_stage",
            "required_artifact",
            "v24_dependency_decision",
            "v24_upstream_status",
            "v39_ready_requirements_after_recheck",
            "dependency_recheck_blockers",
            "dependency_decision_after_recheck",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "post_writer_scoring_dependency_closure_recheck_summary_v40.csv",
        summary(rows),
        [
            "summary_id",
            "dependencies_rechecked",
            "ready_dependencies_after_recheck",
            "blocked_dependencies_after_recheck",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_POST_WRITER_SCORING_DEPENDENCY_CLOSURE_RECHECK_V40_BUILT")


if __name__ == "__main__":
    main()
