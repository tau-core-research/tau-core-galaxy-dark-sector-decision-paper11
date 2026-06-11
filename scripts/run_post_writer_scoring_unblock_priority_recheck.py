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
    priorities = read_csv(DERIVED / "scoring_unblock_priority_v25.csv")
    dependency_summary = read_csv(DERIVED / "post_writer_scoring_dependency_closure_recheck_summary_v40.csv")[0]
    out: list[dict[str, object]] = []
    for row in priorities:
        blockers = []
        if row["dependency_decision"] != "READY":
            blockers.append("v25_priority_dependency_blocked")
        if dependency_summary["ready_dependencies_after_recheck"] == "0":
            blockers.append("post_writer_dependency_recheck_zero_ready_dependencies")
        if dependency_summary["endpoint_scoring_allowed_anywhere"] != "true":
            blockers.append("post_writer_dependency_recheck_scoring_not_allowed")
        out.append(
            {
                "recheck_id": f"PWSUP41_{int(row['priority_rank']):03d}",
                "priority_rank": row["priority_rank"],
                "dependency_id": row["dependency_id"],
                "dependency_class": row["dependency_class"],
                "unblock_mode": row["unblock_mode"],
                "v25_frontier_now": row["frontier_now"],
                "v40_ready_dependencies_after_recheck": dependency_summary["ready_dependencies_after_recheck"],
                "next_required_artifact": row["next_required_artifact"],
                "priority_recheck_blockers": ";".join(blockers),
                "frontier_now_after_recheck": "true" if row["priority_rank"] == "1" and blockers else "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "post_writer_scoring_unblock_priority_recheck_only_no_scores",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked = sum(row["priority_recheck_blockers"] != "" for row in rows)
    frontier = [row for row in rows if row["frontier_now_after_recheck"] == "true"]
    return [
        {
            "summary_id": "POST_WRITER_SCORING_UNBLOCK_PRIORITY_RECHECK_V41",
            "priority_rows_rechecked": len(rows),
            "blocked_priority_rows_after_recheck": blocked,
            "frontier_now_rows_after_recheck": len(frontier),
            "first_frontier_dependency_after_recheck": frontier[0]["dependency_id"] if frontier else "none",
            "first_frontier_artifact_after_recheck": frontier[0]["next_required_artifact"] if frontier else "none",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_SCORING_UNBLOCK_FRONTIER_CONFIRMED"
            if frontier
            else "POST_WRITER_SCORING_UNBLOCK_FRONTIER_CLEAR",
            "claim_boundary": "post_writer_scoring_unblock_priority_recheck_only_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = recheck_rows()
    write_csv(
        DERIVED / "post_writer_scoring_unblock_priority_recheck_v41.csv",
        rows,
        [
            "recheck_id",
            "priority_rank",
            "dependency_id",
            "dependency_class",
            "unblock_mode",
            "v25_frontier_now",
            "v40_ready_dependencies_after_recheck",
            "next_required_artifact",
            "priority_recheck_blockers",
            "frontier_now_after_recheck",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "post_writer_scoring_unblock_priority_recheck_summary_v41.csv",
        summary(rows),
        [
            "summary_id",
            "priority_rows_rechecked",
            "blocked_priority_rows_after_recheck",
            "frontier_now_rows_after_recheck",
            "first_frontier_dependency_after_recheck",
            "first_frontier_artifact_after_recheck",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_POST_WRITER_SCORING_UNBLOCK_PRIORITY_RECHECK_V41_BUILT")


if __name__ == "__main__":
    main()
