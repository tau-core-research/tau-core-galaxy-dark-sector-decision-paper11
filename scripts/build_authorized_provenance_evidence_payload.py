#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
ACTIVE_TARGET = ROOT / "data/input/source_import_provenance_evidence_v21.csv"


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


def payload_rows() -> list[dict[str, object]]:
    draft_rows = read_csv(DERIVED / "frontier_provenance_evidence_payload_draft_v46.csv")
    auth_rows = read_csv(DERIVED / "post_hash_review_promotion_response_intake_v53.csv")
    auth_by_galaxy = {row["galaxy_id"]: row for row in auth_rows}
    out: list[dict[str, object]] = []
    for draft in draft_rows:
        auth = auth_by_galaxy[draft["galaxy_id"]]
        authorized = (
            auth["primary_table1_hash_recomputed_matched"] == "true"
            and auth["reviewer_promotion_decision"] == "PROMOTE_TO_COMPLETE_V21_EVIDENCE"
            and auth["may_copy_to_v21_after_authorization"] == "true"
            and auth["may_mark_provenance_complete_after_authorization"] == "true"
            and auth["endpoint_scoring_allowed"] == "false"
        )
        out.append(
            {
                "galaxy_id": draft["galaxy_id"],
                "catalog": draft["catalog"],
                "table_or_file": draft["table_or_file"],
                "version_or_date": draft["version_or_date"],
                "row_id": draft["row_id"],
                "sha256_or_external_accession": draft["sha256_or_external_accession"],
                "source_route": draft["source_route"],
                "leakage_evidence_id": draft["leakage_evidence_id"],
                "provenance_evidence_status": "PROVENANCE_EVIDENCE_COMPLETE" if authorized else "AUTHORIZATION_BLOCKED",
                "authorization_review_id": auth["review_id"],
                "payload_write_status": "READY_FOR_SEPARATE_ACTIVE_V21_WRITE_GATE" if authorized else "NOT_READY_FOR_ACTIVE_V21_WRITE",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "authorized_provenance_evidence_payload_only_not_active_input_no_scores",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["payload_write_status"] == "READY_FOR_SEPARATE_ACTIVE_V21_WRITE_GATE" for row in rows)
    complete = sum(row["provenance_evidence_status"] == "PROVENANCE_EVIDENCE_COMPLETE" for row in rows)
    return [
        {
            "summary_id": "AUTHORIZED_PROVENANCE_EVIDENCE_PAYLOAD_V54",
            "payload_rows": len(rows),
            "complete_provenance_payload_rows": complete,
            "ready_for_active_v21_write_rows": ready,
            "active_v21_target": "data/input/source_import_provenance_evidence_v21.csv",
            "active_v21_target_present": str(ACTIVE_TARGET.exists()).lower(),
            "active_v21_rows_written_by_this_step": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "AUTHORIZED_PROVENANCE_EVIDENCE_PAYLOAD_READY_NOT_ACTIVE_INPUT"
            if ready == len(rows)
            else "AUTHORIZED_PROVENANCE_EVIDENCE_PAYLOAD_BLOCKED",
            "next_required_action": "run_separate_active_v21_write_gate_then_recompute_source_import_provenance_gates",
            "claim_boundary": "authorized_provenance_evidence_payload_only_no_active_input_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = payload_rows()
    write_csv(
        DERIVED / "authorized_provenance_evidence_payload_v54.csv",
        rows,
        [
            "galaxy_id",
            "catalog",
            "table_or_file",
            "version_or_date",
            "row_id",
            "sha256_or_external_accession",
            "source_route",
            "leakage_evidence_id",
            "provenance_evidence_status",
            "authorization_review_id",
            "payload_write_status",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "authorized_provenance_evidence_payload_summary_v54.csv",
        summary(rows),
        [
            "summary_id",
            "payload_rows",
            "complete_provenance_payload_rows",
            "ready_for_active_v21_write_rows",
            "active_v21_target",
            "active_v21_target_present",
            "active_v21_rows_written_by_this_step",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_action",
            "claim_boundary",
        ],
    )
    print("PAPER11_AUTHORIZED_PROVENANCE_EVIDENCE_PAYLOAD_V54_BUILT")


if __name__ == "__main__":
    main()
