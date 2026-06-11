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
    review_rows = read_csv(DERIVED / "frontier_provenance_review_response_intake_v48.csv")
    review_summary = read_csv(DERIVED / "frontier_provenance_review_response_intake_summary_v48.csv")[0]
    hash_summary = read_csv(DERIVED / "frontier_external_hash_recompute_audit_summary_v50.csv")[0]
    primary_hash_matched = hash_summary["primary_table1_hash_recomputed_matched"] == "true"
    rows: list[dict[str, object]] = []
    for index, row in enumerate(review_rows, start=1):
        blockers: list[str] = []
        if not primary_hash_matched:
            blockers.append("primary_table1_hash_not_recomputed_matched")
        if row["reviewer_decision"] != "PROMOTE_TO_COMPLETE_V21_EVIDENCE":
            blockers.append("reviewer_decision_keeps_review_required_not_complete")
        if row["may_copy_to_v21_after_review"] != "true":
            blockers.append("row_copy_to_v21_not_authorized")
        if row["may_mark_provenance_complete"] != "true":
            blockers.append("row_provenance_complete_not_authorized")
        if review_summary["may_copy_to_v21_without_separate_promotion"] != "true":
            blockers.append("explicit_promotion_authorization_missing")
        allowed = not blockers
        rows.append(
            {
                "post_hash_recheck_id": f"PHFRPR51_{index:03d}",
                "review_id": row["review_id"],
                "galaxy_id": row["galaxy_id"],
                "primary_table1_hash_recomputed_matched": str(primary_hash_matched).lower(),
                "v48_reviewer_decision": row["reviewer_decision"],
                "promotion_recheck_blockers": ";".join(blockers) if blockers else "none",
                "promotion_recheck_decision": "PROMOTE_TO_V21_EVIDENCE" if allowed else "DO_NOT_PROMOTE_TO_V21_EVIDENCE",
                "may_write_v21_evidence_input_after_recheck": str(allowed).lower(),
                "may_mark_provenance_complete_after_recheck": str(allowed).lower(),
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "post_hash_frontier_review_promotion_recheck_only_no_v21_write_no_scores",
            }
        )
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    row_count = len(rows)
    hash_matched_rows = sum(row["primary_table1_hash_recomputed_matched"] == "true" for row in rows)
    allowed = sum(row["may_write_v21_evidence_input_after_recheck"] == "true" for row in rows)
    return [
        {
            "summary_id": "POST_HASH_FRONTIER_REVIEW_PROMOTION_RECHECK_V51",
            "review_rows": row_count,
            "primary_hash_matched_review_rows": hash_matched_rows,
            "promotion_allowed_rows_after_hash": allowed,
            "promotion_blocked_rows_after_hash": row_count - allowed,
            "v21_evidence_rows_created": 0,
            "provenance_complete_rows_marked": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_HASH_FRONTIER_REVIEW_PROMOTION_RECHECK_BLOCKED"
            if allowed != row_count
            else "POST_HASH_FRONTIER_REVIEW_PROMOTION_READY_NOT_WRITTEN",
            "next_required_action": "issue_explicit_review_promotion_authorization_for_v21_copy_and_provenance_completion",
            "claim_boundary": "post_hash_frontier_review_promotion_recheck_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = recheck_rows()
    summary_rows = summary(rows)
    write_csv(
        DERIVED / "post_hash_frontier_review_promotion_recheck_v51.csv",
        rows,
        [
            "post_hash_recheck_id",
            "review_id",
            "galaxy_id",
            "primary_table1_hash_recomputed_matched",
            "v48_reviewer_decision",
            "promotion_recheck_blockers",
            "promotion_recheck_decision",
            "may_write_v21_evidence_input_after_recheck",
            "may_mark_provenance_complete_after_recheck",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "post_hash_frontier_review_promotion_recheck_summary_v51.csv",
        summary_rows,
        [
            "summary_id",
            "review_rows",
            "primary_hash_matched_review_rows",
            "promotion_allowed_rows_after_hash",
            "promotion_blocked_rows_after_hash",
            "v21_evidence_rows_created",
            "provenance_complete_rows_marked",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_action",
            "claim_boundary",
        ],
    )
    print("PAPER11_POST_HASH_FRONTIER_REVIEW_PROMOTION_RECHECK_V51_BUILT")


if __name__ == "__main__":
    main()
