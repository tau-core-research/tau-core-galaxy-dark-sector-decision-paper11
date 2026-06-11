#!/usr/bin/env python3
from __future__ import annotations

import csv
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
RESPONSE_DIR = ROOT / "review_packages/leakage_prescore_artifact_candidate_v67_completed_review_response"
RESPONSE_ZIP = ROOT / "review_packages/leakage_prescore_artifact_candidate_v67_completed_review_response.zip"
RESPONSE_CSV = "leakage_prescore_artifact_candidate_v67_review_response.csv"
REQUIRED_RESPONSE_FILES = {
    RESPONSE_CSV,
    "leakage_prescore_artifact_candidate_v67_review_completed_summary.csv",
    "leakage_prescore_artifact_candidate_v67_review_notes.md",
    "leakage_prescore_artifact_candidate_v67_review_validation_log.txt",
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


def response_files_present() -> int:
    present = sum((RESPONSE_DIR / name).exists() for name in REQUIRED_RESPONSE_FILES)
    if RESPONSE_ZIP.exists():
        with zipfile.ZipFile(RESPONSE_ZIP) as archive:
            names = {Path(name).name for name in archive.namelist() if not name.endswith("/")}
        present = max(present, len(names & REQUIRED_RESPONSE_FILES))
    return present


def accepted_candidate(row: dict[str, str]) -> bool:
    return all(
        [
            row["candidate_review_decision"] == "ACCEPT_AS_PRESCORE_ARTIFACT_CANDIDATE_FOR_LATER_INGESTION_GATE",
            row["candidate_artifact_accepted"] == "true",
            row["minimal_required_fields_covered"] == "true",
            row["artifact_is_prescore"] == "true",
            row["artifact_uses_forbidden_inputs"] == "false",
            row["may_promote_to_leakage_evidence_after_ingestion"] == "true",
            row["may_activate_row_after_ingestion"] == "false",
            row["endpoint_scoring_allowed"] == "false",
        ]
    )


def intake_decision(row: dict[str, str]) -> tuple[str, str]:
    if accepted_candidate(row):
        return (
            "ACCEPT_AS_PRESCORE_CANDIDATE_FOR_LATER_LEAKAGE_EVIDENCE_GATE_NOT_EVIDENCE",
            "CANDIDATE_FOR_LATER_LEAKAGE_EVIDENCE_INGESTION",
        )
    return (
        "BLOCKED_PARTIAL_CANDIDATE_REVIEW_INCOMPLETE_OR_UNSAFE",
        "NOT_CANDIDATE_PARTIAL_REVIEW_REQUIRED",
    )


def intake_rows() -> list[dict[str, object]]:
    rows = read_csv(RESPONSE_DIR / RESPONSE_CSV)
    out: list[dict[str, object]] = []
    for row in rows:
        decision, status = intake_decision(row)
        out.append(
            {
                "candidate_id": row["candidate_id"],
                "request_id": row["request_id"],
                "work_order_id": row["work_order_id"],
                "leakage_evidence_row_id": row["leakage_evidence_row_id"],
                "galaxy_id": row["galaxy_id"],
                "proposed_split": row["proposed_split"],
                "evidence_id": row["evidence_id"],
                "request_family": row["request_family"],
                "candidate_artifact_uri_or_id": row["candidate_artifact_uri_or_id"],
                "candidate_artifact_hash_or_accession": row["candidate_artifact_hash_or_accession"],
                "candidate_row_selector": row["candidate_row_selector"],
                "candidate_review_decision": row["candidate_review_decision"],
                "candidate_artifact_accepted": row["candidate_artifact_accepted"],
                "minimal_required_fields_covered": row["minimal_required_fields_covered"],
                "artifact_is_prescore": row["artifact_is_prescore"],
                "artifact_uses_forbidden_inputs": row["artifact_uses_forbidden_inputs"],
                "may_promote_to_leakage_evidence_after_ingestion": row[
                    "may_promote_to_leakage_evidence_after_ingestion"
                ],
                "may_activate_row_after_ingestion": row["may_activate_row_after_ingestion"],
                "endpoint_scoring_allowed": row["endpoint_scoring_allowed"],
                "source_mode": "completed_response",
                "intake_decision": decision,
                "leakage_evidence_candidate_status": status,
                "claim_boundary": "leakage_prescore_artifact_candidate_review_intake_only_no_evidence_no_scores_no_dark_sector_verdict",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    accepted_rows = sum(
        row["leakage_evidence_candidate_status"] == "CANDIDATE_FOR_LATER_LEAKAGE_EVIDENCE_INGESTION"
        for row in rows
    )
    blocked_rows = len(rows) - accepted_rows
    return [
        {
            "summary_id": "LEAKAGE_PRESCORE_ARTIFACT_CANDIDATE_REVIEW_INTAKE_V69",
            "response_zip": "review_packages/leakage_prescore_artifact_candidate_v67_completed_review_response.zip",
            "response_files_present": response_files_present(),
            "intake_rows": len(rows),
            "galaxies_covered": len({row["galaxy_id"] for row in rows}),
            "evidence_checks_per_galaxy": 4,
            "completed_response_present": "true",
            "accepted_candidate_rows": accepted_rows,
            "blocked_partial_rows": blocked_rows,
            "candidate_rows_for_later_leakage_evidence": accepted_rows,
            "leakage_evidence_rows_created": 0,
            "activation_rows_authorized": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PRESCORE_CANDIDATE_REVIEW_PARTIAL_ACCEPTANCE_NEEDS_LEAKAGE_EVIDENCE_GATE",
            "next_required_artifact": "leakage_evidence_candidate_ingestion_gate_for_36_accepted_candidates",
            "claim_boundary": "leakage_prescore_artifact_candidate_review_intake_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = intake_rows()
    write_csv(
        DERIVED / "leakage_prescore_artifact_candidate_review_intake_v69.csv",
        rows,
        [
            "candidate_id",
            "request_id",
            "work_order_id",
            "leakage_evidence_row_id",
            "galaxy_id",
            "proposed_split",
            "evidence_id",
            "request_family",
            "candidate_artifact_uri_or_id",
            "candidate_artifact_hash_or_accession",
            "candidate_row_selector",
            "candidate_review_decision",
            "candidate_artifact_accepted",
            "minimal_required_fields_covered",
            "artifact_is_prescore",
            "artifact_uses_forbidden_inputs",
            "may_promote_to_leakage_evidence_after_ingestion",
            "may_activate_row_after_ingestion",
            "endpoint_scoring_allowed",
            "source_mode",
            "intake_decision",
            "leakage_evidence_candidate_status",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "leakage_prescore_artifact_candidate_review_intake_summary_v69.csv",
        summary(rows),
        [
            "summary_id",
            "response_zip",
            "response_files_present",
            "intake_rows",
            "galaxies_covered",
            "evidence_checks_per_galaxy",
            "completed_response_present",
            "accepted_candidate_rows",
            "blocked_partial_rows",
            "candidate_rows_for_later_leakage_evidence",
            "leakage_evidence_rows_created",
            "activation_rows_authorized",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_LEAKAGE_PRESCORE_ARTIFACT_CANDIDATE_REVIEW_INTAKE_V69_BUILT")


if __name__ == "__main__":
    main()
