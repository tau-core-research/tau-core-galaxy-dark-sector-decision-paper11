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
    work_orders = read_csv(DERIVED / "frontier_provenance_evidence_work_order_v27.csv")
    acceptance_by_galaxy = {
        row["galaxy_id"]: row for row in read_csv(DERIVED / "post_writer_frontier_evidence_acceptance_recheck_v42.csv")
    }
    out: list[dict[str, object]] = []
    for index, row in enumerate(work_orders, start=1):
        acceptance = acceptance_by_galaxy[row["galaxy_id"]]
        blockers = []
        if acceptance["accepted_for_promotion_review_after_recheck"] != "true":
            blockers.append("post_writer_frontier_acceptance_not_passed")
        if row["work_order_status"] != "CLOSED_EVIDENCE_READY":
            blockers.append("v27_work_order_not_closed")
        if row["may_write_evidence_input"] != "true":
            blockers.append("v27_evidence_write_not_allowed")
        out.append(
            {
                "recheck_id": f"PWFWO43_{index:03d}",
                "work_order_id": row["work_order_id"],
                "galaxy_id": row["galaxy_id"],
                "target_evidence_artifact": row["target_evidence_artifact"],
                "v42_accepted_for_promotion_review_after_recheck": acceptance[
                    "accepted_for_promotion_review_after_recheck"
                ],
                "v27_work_order_status": row["work_order_status"],
                "v27_may_write_evidence_input": row["may_write_evidence_input"],
                "work_order_recheck_blockers": ";".join(blockers),
                "work_order_status_after_recheck": "OPEN_EVIDENCE_COLLECTION_REQUIRED"
                if blockers
                else "CLOSED_EVIDENCE_READY",
                "may_write_evidence_input_after_recheck": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "post_writer_frontier_work_order_recheck_only_no_evidence_no_scores",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    closed = sum(row["work_order_status_after_recheck"] == "CLOSED_EVIDENCE_READY" for row in rows)
    writable = sum(row["may_write_evidence_input_after_recheck"] == "true" for row in rows)
    return [
        {
            "summary_id": "POST_WRITER_FRONTIER_WORK_ORDER_RECHECK_V43",
            "work_order_recheck_rows": len(rows),
            "open_work_order_rows_after_recheck": len(rows) - closed,
            "closed_work_order_rows_after_recheck": closed,
            "may_write_evidence_input_rows_after_recheck": writable,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_FRONTIER_WORK_ORDER_RECHECK_BLOCKED"
            if closed == 0
            else "POST_WRITER_FRONTIER_WORK_ORDER_RECHECK_READY",
            "claim_boundary": "post_writer_frontier_work_order_recheck_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = recheck_rows()
    write_csv(
        DERIVED / "post_writer_frontier_work_order_recheck_v43.csv",
        rows,
        [
            "recheck_id",
            "work_order_id",
            "galaxy_id",
            "target_evidence_artifact",
            "v42_accepted_for_promotion_review_after_recheck",
            "v27_work_order_status",
            "v27_may_write_evidence_input",
            "work_order_recheck_blockers",
            "work_order_status_after_recheck",
            "may_write_evidence_input_after_recheck",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "post_writer_frontier_work_order_recheck_summary_v43.csv",
        summary(rows),
        [
            "summary_id",
            "work_order_recheck_rows",
            "open_work_order_rows_after_recheck",
            "closed_work_order_rows_after_recheck",
            "may_write_evidence_input_rows_after_recheck",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_POST_WRITER_FRONTIER_WORK_ORDER_RECHECK_V43_BUILT")


if __name__ == "__main__":
    main()
