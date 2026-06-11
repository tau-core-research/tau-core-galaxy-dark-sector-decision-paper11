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


def row_blockers(row: dict[str, str], summary: dict[str, str]) -> list[str]:
    blockers: list[str] = []
    if row["row_route_internal_consistency"] != "pass":
        blockers.append("route_internal_consistency_not_passed")
    if row["leakage_evidence_status"] != "pass_prescore_source_route_review_id":
        blockers.append("prescore_source_route_review_id_not_passed")
    if row["source_hash_route_status"] != "source_hash_independently_recomputed_and_matched":
        blockers.append("external_source_hash_not_independently_recomputed")
    if row["reviewer_decision"] != "PROMOTE_TO_COMPLETE_V21_EVIDENCE":
        blockers.append("reviewer_decision_keeps_review_required_not_complete")
    if row["may_copy_to_v21_after_review"] != "true":
        blockers.append("row_copy_to_v21_not_authorized")
    if row["may_mark_provenance_complete"] != "true":
        blockers.append("row_provenance_complete_not_authorized")
    if summary["may_copy_to_v21_without_separate_promotion"] != "true":
        blockers.append("separate_promotion_gate_not_authorized_by_response")
    if summary["external_hash_recomputed"] != "true":
        blockers.append("summary_external_hash_recomputed_false")
    if summary["complete_evidence_rows_authorized"] != summary["review_rows"]:
        blockers.append("summary_complete_evidence_rows_not_authorized")
    return blockers


def gate_rows() -> list[dict[str, object]]:
    rows = read_csv(DERIVED / "frontier_provenance_review_response_intake_v48.csv")
    summary = read_csv(DERIVED / "frontier_provenance_review_response_intake_summary_v48.csv")[0]
    out: list[dict[str, object]] = []
    for index, row in enumerate(rows, start=1):
        blockers = row_blockers(row, summary)
        promotion_allowed = not blockers
        out.append(
            {
                "promotion_review_gate_id": f"FPRPG49_{index:03d}",
                "review_id": row["review_id"],
                "galaxy_id": row["galaxy_id"],
                "v48_route_consistency": row["row_route_internal_consistency"],
                "v48_source_hash_route_status": row["source_hash_route_status"],
                "v48_leakage_evidence_status": row["leakage_evidence_status"],
                "v48_reviewer_decision": row["reviewer_decision"],
                "v48_completion_status": summary["completion_status"],
                "external_hash_recomputed": summary["external_hash_recomputed"],
                "promotion_gate_blockers": ";".join(blockers) if blockers else "none",
                "promotion_gate_decision": "PROMOTE_TO_V21_EVIDENCE" if promotion_allowed else "DO_NOT_PROMOTE_TO_V21_EVIDENCE",
                "may_write_v21_evidence_input_after_gate": str(promotion_allowed).lower(),
                "may_mark_provenance_complete_after_gate": str(promotion_allowed).lower(),
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "frontier_review_promotion_gate_only_no_v21_write_no_scores",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    row_count = len(rows)
    promoted = sum(row["may_write_v21_evidence_input_after_gate"] == "true" for row in rows)
    blocked = row_count - promoted
    return [
        {
            "summary_id": "FRONTIER_REVIEW_PROMOTION_GATE_V49",
            "review_rows": row_count,
            "promotion_allowed_rows": promoted,
            "promotion_blocked_rows": blocked,
            "v21_evidence_rows_created": 0,
            "provenance_complete_rows_marked": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FRONTIER_REVIEW_PROMOTION_BLOCKED" if blocked else "FRONTIER_REVIEW_PROMOTION_READY_NOT_WRITTEN",
            "next_required_action": "independently_recompute_external_sparc_hash_and_issue_explicit_promotion_authorization",
            "claim_boundary": "frontier_review_promotion_gate_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = gate_rows()
    summary_rows = summary(rows)
    write_csv(
        DERIVED / "frontier_review_promotion_gate_v49.csv",
        rows,
        [
            "promotion_review_gate_id",
            "review_id",
            "galaxy_id",
            "v48_route_consistency",
            "v48_source_hash_route_status",
            "v48_leakage_evidence_status",
            "v48_reviewer_decision",
            "v48_completion_status",
            "external_hash_recomputed",
            "promotion_gate_blockers",
            "promotion_gate_decision",
            "may_write_v21_evidence_input_after_gate",
            "may_mark_provenance_complete_after_gate",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "frontier_review_promotion_gate_summary_v49.csv",
        summary_rows,
        [
            "summary_id",
            "review_rows",
            "promotion_allowed_rows",
            "promotion_blocked_rows",
            "v21_evidence_rows_created",
            "provenance_complete_rows_marked",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_action",
            "claim_boundary",
        ],
    )
    print("PAPER11_FRONTIER_REVIEW_PROMOTION_GATE_V49_BUILT")


if __name__ == "__main__":
    main()
