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


def frontier_rows() -> list[dict[str, object]]:
    v70 = read_csv(DERIVED / "leakage_evidence_candidate_ingestion_summary_v70.csv")[0]
    v73 = read_csv(DERIVED / "leakage_partial_candidate_sufficiency_review_intake_summary_v73.csv")[0]
    v74 = read_csv(DERIVED / "leakage_partial_candidate_sufficiency_preaudit_summary_v74.csv")[0]
    v76_path = DERIVED / "full_leakage_evidence_ingestion_summary_v76.csv"
    v76 = read_csv(v76_path)[0] if v76_path.exists() else {}
    v77_path = DERIVED / "leakage_audit_evidence_v10_writer_summary_v77.csv"
    v77 = read_csv(v77_path)[0] if v77_path.exists() else {}
    partial_blocked = int(v73["blocked_or_missing_rows"])
    v76_ready = v76.get("overall_status") == "FULL_LEAKAGE_EVIDENCE_INGESTION_READY_FOR_TARGET_EVIDENCE_WRITE"
    v77_written = v77.get("overall_status") == "LEAKAGE_AUDIT_EVIDENCE_WRITTEN_REVIEW_PENDING"
    if v77_written:
        rank2_status = str(v77["overall_status"])
        rank2_blocked = "target leakage evidence rows are written, but leakage pass review is still pending"
        rank2_next = str(v77["next_required_artifact"])
        rank3_status = "WAITING_ON_LEAKAGE_PASS_REVIEW"
    elif v76_ready:
        rank2_status = str(v76["overall_status"])
        rank2_blocked = "full leakage evidence components are ready, but target evidence rows are not written yet"
        rank2_next = str(v76["next_required_artifact"])
        rank3_status = "WAITING_ON_LEAKAGE_AUDIT_EVIDENCE_V10_WRITE"
    elif partial_blocked == 0:
        rank2_status = "READY_FOR_FULL_LEAKAGE_EVIDENCE_INGESTION_AFTER_ACCEPTED_V71_RESPONSE"
        rank2_blocked = "full leakage evidence has not yet been ingested even though the partial sufficiency response is accepted"
        rank2_next = "run_full_leakage_evidence_ingestion_gate_v76"
        rank3_status = "WAITING_ON_FULL_LEAKAGE_EVIDENCE_INGESTION"
    else:
        rank2_status = "WAITING_ON_RANK_1_SUFFICIENCY_RESPONSE"
        rank2_blocked = "full leakage evidence cannot be created until the two partial components pass sufficiency review"
        rank2_next = "accepted_v71_sufficiency_response_then_full_leakage_evidence_ingestion_gate"
        rank3_status = "WAITING_ON_FULL_LEAKAGE_EVIDENCE_INGESTION"
    rank1_blocked = (
        "partial sufficiency blocker cleared; accepted sufficiency rows still do not create evidence"
        if partial_blocked == 0
        else (
            f"{v73['blocked_or_missing_rows']} morphology-label/benchmark-policy partial rows "
            "remain blocked or missing completed sufficiency response"
        )
    )
    return [
        {
            "frontier_id": "SFS72_LEAKAGE_PARTIAL_SUFFICIENCY_RESPONSE",
            "frontier_rank": 1,
            "frontier_class": "source_blindness_leakage_component_sufficiency",
            "current_status": v73["overall_status"],
            "ready_detail": (
                f"{v70['galaxies_with_source_and_observed_candidates']} galaxies have source-route and observed-input "
                f"draft candidates; {v74['preaudit_review_ready_rows']} partial rows are preaudit review-ready"
            ),
            "blocked_detail": rank1_blocked,
            "required_before_scoring": "true",
            "next_required_artifact": v73["next_required_artifact"],
            "next_gate_after_artifact": "leakage_evidence_ingestion_gate_recheck_after_v71_response",
            "target_evidence_rows_created": "0",
            "leakage_pass_authorized": "false",
            "activation_rows_authorized": "0",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "scoring_frontier_status_only_no_evidence_no_scores_no_dark_sector_verdict",
        },
        {
            "frontier_id": "SFS72_FULL_LEAKAGE_EVIDENCE_INGESTION",
            "frontier_rank": 2,
            "frontier_class": "full_four_component_leakage_evidence_ingestion",
            "current_status": rank2_status,
            "ready_detail": "source-route and observed-input draft candidates are available for all 18 galaxies",
            "blocked_detail": rank2_blocked,
            "required_before_scoring": "true",
            "next_required_artifact": rank2_next,
            "next_gate_after_artifact": "source_import_leakage_audit_recheck",
            "target_evidence_rows_created": "0",
            "leakage_pass_authorized": "false",
            "activation_rows_authorized": "0",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "scoring_frontier_status_only_no_evidence_no_scores_no_dark_sector_verdict",
        },
        {
            "frontier_id": "SFS72_SCORING_ACTIVATION_RECHECK",
            "frontier_rank": 3,
            "frontier_class": "row_activation_after_leakage_pass",
            "current_status": rank3_status,
            "ready_detail": "real source values are already present but validation remains leakage-gated",
            "blocked_detail": "row activation is forbidden until leakage pass exists for every scoring row",
            "required_before_scoring": "true",
            "next_required_artifact": "scoring_activation_gate_recheck_after_leakage_pass",
            "next_gate_after_artifact": "scoring_dependency_closure_recheck",
            "target_evidence_rows_created": "0",
            "leakage_pass_authorized": "false",
            "activation_rows_authorized": "0",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "scoring_frontier_status_only_no_evidence_no_scores_no_dark_sector_verdict",
        },
    ]


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked = [row for row in rows if row["endpoint_scoring_allowed"] == "false"]
    v73 = read_csv(DERIVED / "leakage_partial_candidate_sufficiency_review_intake_summary_v73.csv")[0]
    v76_path = DERIVED / "full_leakage_evidence_ingestion_summary_v76.csv"
    v76 = read_csv(v76_path)[0] if v76_path.exists() else {}
    v77_path = DERIVED / "leakage_audit_evidence_v10_writer_summary_v77.csv"
    v77 = read_csv(v77_path)[0] if v77_path.exists() else {}
    partial_blocked = v73["blocked_or_missing_rows"]
    v76_ready = v76.get("overall_status") == "FULL_LEAKAGE_EVIDENCE_INGESTION_READY_FOR_TARGET_EVIDENCE_WRITE"
    v77_written = v77.get("overall_status") == "LEAKAGE_AUDIT_EVIDENCE_WRITTEN_REVIEW_PENDING"
    if v77_written:
        overall_status = "SCORING_FRONTIER_BLOCKED_ON_LEAKAGE_PASS_REVIEW"
        first_artifact = str(v77["next_required_artifact"])
    elif v76_ready:
        overall_status = "SCORING_FRONTIER_BLOCKED_ON_LEAKAGE_AUDIT_EVIDENCE_V10_WRITE"
        first_artifact = str(v76["next_required_artifact"])
    elif partial_blocked == "0":
        overall_status = "SCORING_FRONTIER_BLOCKED_ON_FULL_LEAKAGE_EVIDENCE_INGESTION_GATE"
        first_artifact = rows[0]["next_required_artifact"]
    else:
        overall_status = "SCORING_FRONTIER_BLOCKED_ON_COMPLETED_V71_SUFFICIENCY_RESPONSE"
        first_artifact = rows[0]["next_required_artifact"]
    return [
        {
            "summary_id": "SCORING_FRONTIER_STATUS_V72",
            "frontier_rows": len(rows),
            "blocked_frontier_rows": len(blocked),
            "first_frontier_id": rows[0]["frontier_id"],
            "first_frontier_artifact": first_artifact,
            "required_components_for_full_scoring_leakage_pass": 4,
            "partial_candidate_rows_requiring_review": partial_blocked,
            "target_evidence_rows_created": 0,
            "leakage_pass_authorized": 0,
            "activation_rows_authorized": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": overall_status,
            "claim_boundary": "scoring_frontier_status_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = frontier_rows()
    write_csv(
        DERIVED / "scoring_frontier_status_v72.csv",
        rows,
        [
            "frontier_id",
            "frontier_rank",
            "frontier_class",
            "current_status",
            "ready_detail",
            "blocked_detail",
            "required_before_scoring",
            "next_required_artifact",
            "next_gate_after_artifact",
            "target_evidence_rows_created",
            "leakage_pass_authorized",
            "activation_rows_authorized",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "scoring_frontier_status_summary_v72.csv",
        summary(rows),
        [
            "summary_id",
            "frontier_rows",
            "blocked_frontier_rows",
            "first_frontier_id",
            "first_frontier_artifact",
            "required_components_for_full_scoring_leakage_pass",
            "partial_candidate_rows_requiring_review",
            "target_evidence_rows_created",
            "leakage_pass_authorized",
            "activation_rows_authorized",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_SCORING_FRONTIER_STATUS_V72_BUILT")


if __name__ == "__main__":
    main()
