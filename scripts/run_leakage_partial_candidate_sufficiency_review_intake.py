#!/usr/bin/env python3
from __future__ import annotations

import csv
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
PACKAGE_ROOT = ROOT / "review_packages/leakage_partial_candidate_sufficiency_v71_review_package"
RESPONSE_DIR = ROOT / "review_packages/leakage_partial_candidate_sufficiency_v71_completed_review_response"
RESPONSE_ZIP = ROOT / "review_packages/leakage_partial_candidate_sufficiency_v71_completed_review_response.zip"
RESPONSE_CSV = "leakage_partial_candidate_sufficiency_v71_review_response.csv"
REQUIRED_RESPONSE_FILES = {
    RESPONSE_CSV,
    "leakage_partial_candidate_sufficiency_v71_review_completed_summary.csv",
    "leakage_partial_candidate_sufficiency_v71_review_notes.md",
    "leakage_partial_candidate_sufficiency_v71_review_validation_log.txt",
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


def source_rows() -> tuple[list[dict[str, str]], str]:
    response_path = RESPONSE_DIR / RESPONSE_CSV
    if response_path.exists():
        return read_csv(response_path), "completed_response"
    return (
        read_csv(PACKAGE_ROOT / "templates/leakage_partial_candidate_sufficiency_v71_review_response_TEMPLATE.csv"),
        "template_absent_completed_response",
    )


def accepted_sufficiency(row: dict[str, str], source_mode: str) -> bool:
    if source_mode != "completed_response":
        return False
    return all(
        [
            row["sufficiency_review_decision"] == "ACCEPT_PARTIAL_CANDIDATE_SUFFICIENT_FOR_LATER_INGESTION_GATE",
            row["partial_candidate_sufficient_for_later_ingestion"] == "true",
            row["minimal_required_fields_covered"] == "true",
            row["artifact_is_prescore"] == "true",
            row["artifact_uses_forbidden_inputs"] == "false",
            row["may_promote_to_leakage_evidence_after_ingestion"] == "true",
            row["may_activate_row_after_ingestion"] == "false",
            row["endpoint_scoring_allowed"] == "false",
        ]
    )


def intake_decision(row: dict[str, str], source_mode: str) -> tuple[str, str]:
    if accepted_sufficiency(row, source_mode):
        return (
            "ACCEPT_PARTIAL_SUFFICIENCY_FOR_LATER_LEAKAGE_EVIDENCE_GATE_NOT_EVIDENCE",
            "SUFFICIENCY_ACCEPTED_FOR_LATER_LEAKAGE_EVIDENCE_INGESTION",
        )
    if source_mode != "completed_response":
        return (
            "BLOCKED_COMPLETED_V71_SUFFICIENCY_RESPONSE_ABSENT",
            "NOT_ACCEPTED_COMPLETED_RESPONSE_ABSENT",
        )
    return (
        "BLOCKED_PARTIAL_SUFFICIENCY_REVIEW_INCOMPLETE_OR_UNSAFE",
        "NOT_ACCEPTED_REVIEW_INCOMPLETE_OR_UNSAFE",
    )


def intake_rows() -> list[dict[str, object]]:
    rows, source_mode = source_rows()
    out: list[dict[str, object]] = []
    for row in rows:
        decision, status = intake_decision(row, source_mode)
        out.append(
            {
                "ingestion_gate_id": row["ingestion_gate_id"],
                "candidate_id": row["candidate_id"],
                "leakage_evidence_row_id": row["leakage_evidence_row_id"],
                "galaxy_id": row["galaxy_id"],
                "proposed_split": row["proposed_split"],
                "evidence_id": row["evidence_id"],
                "request_family": row["request_family"],
                "candidate_artifact_uri_or_id": row["candidate_artifact_uri_or_id"],
                "candidate_artifact_hash_or_accession": row["candidate_artifact_hash_or_accession"],
                "candidate_row_selector": row["candidate_row_selector"],
                "sufficiency_review_decision": row["sufficiency_review_decision"],
                "partial_candidate_sufficient_for_later_ingestion": row[
                    "partial_candidate_sufficient_for_later_ingestion"
                ],
                "minimal_required_fields_covered": row["minimal_required_fields_covered"],
                "artifact_is_prescore": row["artifact_is_prescore"],
                "artifact_uses_forbidden_inputs": row["artifact_uses_forbidden_inputs"],
                "may_promote_to_leakage_evidence_after_ingestion": row[
                    "may_promote_to_leakage_evidence_after_ingestion"
                ],
                "may_activate_row_after_ingestion": row["may_activate_row_after_ingestion"],
                "endpoint_scoring_allowed": row["endpoint_scoring_allowed"],
                "source_mode": source_mode,
                "intake_decision": decision,
                "sufficiency_candidate_status": status,
                "claim_boundary": "leakage_partial_candidate_sufficiency_review_intake_only_no_evidence_no_scores_no_dark_sector_verdict",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    accepted = sum(
        row["sufficiency_candidate_status"] == "SUFFICIENCY_ACCEPTED_FOR_LATER_LEAKAGE_EVIDENCE_INGESTION"
        for row in rows
    )
    blocked = len(rows) - accepted
    response_files = response_files_present()
    response_present = response_files == len(REQUIRED_RESPONSE_FILES)
    all_accepted = response_present and accepted == len(rows)
    return [
        {
            "summary_id": "LEAKAGE_PARTIAL_CANDIDATE_SUFFICIENCY_REVIEW_INTAKE_V73",
            "response_zip": "review_packages/leakage_partial_candidate_sufficiency_v71_completed_review_response.zip",
            "response_files_present": response_files,
            "intake_rows": len(rows),
            "galaxies_covered": len({row["galaxy_id"] for row in rows}),
            "partial_evidence_components": 2,
            "completed_response_present": str(response_present).lower(),
            "accepted_sufficiency_rows": accepted,
            "blocked_or_missing_rows": blocked,
            "target_evidence_rows_created": 0,
            "leakage_pass_authorized": 0,
            "activation_rows_authorized": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PARTIAL_SUFFICIENCY_REVIEW_READY_FOR_LATER_LEAKAGE_EVIDENCE_GATE"
            if all_accepted
            else "PARTIAL_SUFFICIENCY_REVIEW_RESPONSE_PRESENT_BUT_BLOCKED"
            if response_present
            else "PARTIAL_SUFFICIENCY_REVIEW_RESPONSE_BLOCKED_OR_ABSENT",
            "next_required_artifact": "full_leakage_evidence_ingestion_gate_after_accepted_v71_response"
            if all_accepted
            else "completed_leakage_partial_candidate_sufficiency_v71_review_response.zip",
            "claim_boundary": "leakage_partial_candidate_sufficiency_review_intake_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = intake_rows()
    write_csv(
        DERIVED / "leakage_partial_candidate_sufficiency_review_intake_v73.csv",
        rows,
        [
            "ingestion_gate_id",
            "candidate_id",
            "leakage_evidence_row_id",
            "galaxy_id",
            "proposed_split",
            "evidence_id",
            "request_family",
            "candidate_artifact_uri_or_id",
            "candidate_artifact_hash_or_accession",
            "candidate_row_selector",
            "sufficiency_review_decision",
            "partial_candidate_sufficient_for_later_ingestion",
            "minimal_required_fields_covered",
            "artifact_is_prescore",
            "artifact_uses_forbidden_inputs",
            "may_promote_to_leakage_evidence_after_ingestion",
            "may_activate_row_after_ingestion",
            "endpoint_scoring_allowed",
            "source_mode",
            "intake_decision",
            "sufficiency_candidate_status",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "leakage_partial_candidate_sufficiency_review_intake_summary_v73.csv",
        summary(rows),
        [
            "summary_id",
            "response_zip",
            "response_files_present",
            "intake_rows",
            "galaxies_covered",
            "partial_evidence_components",
            "completed_response_present",
            "accepted_sufficiency_rows",
            "blocked_or_missing_rows",
            "target_evidence_rows_created",
            "leakage_pass_authorized",
            "activation_rows_authorized",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_LEAKAGE_PARTIAL_CANDIDATE_SUFFICIENCY_REVIEW_INTAKE_V73_BUILT")


if __name__ == "__main__":
    main()
