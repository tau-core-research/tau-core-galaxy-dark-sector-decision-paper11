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
    acceptance_rows = read_csv(DERIVED / "frontier_provenance_evidence_acceptance_v26.csv")
    priority_summary = read_csv(DERIVED / "post_writer_scoring_unblock_priority_recheck_summary_v41.csv")[0]
    out: list[dict[str, object]] = []
    for index, row in enumerate(acceptance_rows, start=1):
        blockers = []
        if priority_summary["first_frontier_dependency_after_recheck"] != "SCD24_PROVENANCE_EVIDENCE":
            blockers.append("post_writer_frontier_not_provenance_evidence")
        if row["evidence_input_present"] != "true":
            blockers.append("frontier_evidence_input_missing")
        if row["accepted_for_promotion_review"] != "true":
            blockers.append("v26_acceptance_not_passed")
        out.append(
            {
                "recheck_id": f"PWFPEA42_{index:03d}",
                "acceptance_id": row["acceptance_id"],
                "galaxy_id": row["galaxy_id"],
                "v41_frontier_dependency": priority_summary["first_frontier_dependency_after_recheck"],
                "v41_frontier_artifact": priority_summary["first_frontier_artifact_after_recheck"],
                "v26_acceptance_status": row["acceptance_status"],
                "v26_evidence_input_present": row["evidence_input_present"],
                "v26_accepted_for_promotion_review": row["accepted_for_promotion_review"],
                "acceptance_recheck_blockers": ";".join(blockers),
                "accepted_for_promotion_review_after_recheck": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "post_writer_frontier_evidence_acceptance_recheck_only_no_scores",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    accepted = sum(row["accepted_for_promotion_review_after_recheck"] == "true" for row in rows)
    present = sum(row["v26_evidence_input_present"] == "true" for row in rows)
    return [
        {
            "summary_id": "POST_WRITER_FRONTIER_EVIDENCE_ACCEPTANCE_RECHECK_V42",
            "acceptance_recheck_rows": len(rows),
            "evidence_input_rows_present_after_recheck": present,
            "accepted_for_promotion_review_rows_after_recheck": accepted,
            "blocked_rows_after_recheck": len(rows) - accepted,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_FRONTIER_EVIDENCE_ACCEPTANCE_RECHECK_BLOCKED"
            if accepted == 0
            else "POST_WRITER_FRONTIER_EVIDENCE_ACCEPTANCE_RECHECK_READY",
            "claim_boundary": "post_writer_frontier_evidence_acceptance_recheck_only_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = recheck_rows()
    write_csv(
        DERIVED / "post_writer_frontier_evidence_acceptance_recheck_v42.csv",
        rows,
        [
            "recheck_id",
            "acceptance_id",
            "galaxy_id",
            "v41_frontier_dependency",
            "v41_frontier_artifact",
            "v26_acceptance_status",
            "v26_evidence_input_present",
            "v26_accepted_for_promotion_review",
            "acceptance_recheck_blockers",
            "accepted_for_promotion_review_after_recheck",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "post_writer_frontier_evidence_acceptance_recheck_summary_v42.csv",
        summary(rows),
        [
            "summary_id",
            "acceptance_recheck_rows",
            "evidence_input_rows_present_after_recheck",
            "accepted_for_promotion_review_rows_after_recheck",
            "blocked_rows_after_recheck",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_POST_WRITER_FRONTIER_EVIDENCE_ACCEPTANCE_RECHECK_V42_BUILT")


if __name__ == "__main__":
    main()
