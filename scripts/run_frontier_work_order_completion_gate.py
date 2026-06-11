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


def completion_rows() -> list[dict[str, object]]:
    work_orders = read_csv(DERIVED / "frontier_provenance_evidence_work_order_v27.csv")
    acceptance_by_galaxy = {
        row["galaxy_id"]: row for row in read_csv(DERIVED / "frontier_provenance_evidence_acceptance_v26.csv")
    }
    rows: list[dict[str, object]] = []
    for index, row in enumerate(work_orders, start=1):
        acceptance = acceptance_by_galaxy[row["galaxy_id"]]
        accepted = acceptance["accepted_for_promotion_review"] == "true"
        open_required = row["work_order_status"] == "OPEN_EVIDENCE_COLLECTION_REQUIRED"
        blockers = []
        if open_required:
            blockers.append("work_order_open")
        if not accepted:
            blockers.append("not_accepted_for_promotion_review")
        rows.append(
            {
                "completion_gate_id": f"FWOC28_{index:03d}",
                "work_order_id": row["work_order_id"],
                "galaxy_id": row["galaxy_id"],
                "acceptance_source": "data/derived/frontier_provenance_evidence_acceptance_v26.csv",
                "work_order_source": "data/derived/frontier_provenance_evidence_work_order_v27.csv",
                "accepted_for_promotion_review": acceptance["accepted_for_promotion_review"],
                "work_order_status": row["work_order_status"],
                "completion_blockers": ";".join(blockers) if blockers else "none",
                "completion_decision": "CLOSE_WORK_ORDER" if not blockers else "DO_NOT_CLOSE_WORK_ORDER",
                "may_write_evidence_input_after_completion": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "frontier_work_order_completion_gate_only_no_evidence_no_scores",
            }
        )
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    closed = sum(row["completion_decision"] == "CLOSE_WORK_ORDER" for row in rows)
    return [
        {
            "summary_id": "FRONTIER_WORK_ORDER_COMPLETION_GATE_V28",
            "completion_gate_rows": len(rows),
            "work_orders_closed": closed,
            "work_orders_blocked": len(rows) - closed,
            "may_write_evidence_input_anywhere": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FRONTIER_WORK_ORDER_COMPLETION_BLOCKED"
            if closed < len(rows)
            else "FRONTIER_WORK_ORDER_COMPLETION_READY",
            "claim_boundary": "frontier_work_order_completion_gate_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = completion_rows()
    summary_rows = summary(rows)
    write_csv(
        DERIVED / "frontier_work_order_completion_gate_v28.csv",
        rows,
        [
            "completion_gate_id",
            "work_order_id",
            "galaxy_id",
            "acceptance_source",
            "work_order_source",
            "accepted_for_promotion_review",
            "work_order_status",
            "completion_blockers",
            "completion_decision",
            "may_write_evidence_input_after_completion",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "frontier_work_order_completion_gate_summary_v28.csv",
        summary_rows,
        [
            "summary_id",
            "completion_gate_rows",
            "work_orders_closed",
            "work_orders_blocked",
            "may_write_evidence_input_anywhere",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_FRONTIER_WORK_ORDER_COMPLETION_GATE_V28_BUILT")


if __name__ == "__main__":
    main()
