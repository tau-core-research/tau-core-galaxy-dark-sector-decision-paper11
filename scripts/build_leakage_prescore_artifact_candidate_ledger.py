#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
INPUT = ROOT / "data/input"
SOURCE_MANIFEST = ROOT / "data/source_manifest"


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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def first_by(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row[key]: row for row in rows}


def count_rows(path: Path) -> int:
    return len(read_csv(path))


def candidate_for(row: dict[str, str], provenance: dict[str, dict[str, str]], galaxy_roles: dict[str, dict[str, str]]) -> dict[str, object]:
    galaxy_id = row["galaxy_id"]
    evidence_id = row["evidence_id"]
    if evidence_id == "LEC10_SOURCE_ROUTE":
        source = provenance[galaxy_id]
        return {
            "candidate_artifact_uri_or_id": "data/input/source_import_provenance_evidence_v21.csv",
            "candidate_artifact_hash_or_accession": source["sha256_or_external_accession"],
            "candidate_row_selector": source["row_id"],
            "candidate_support_detail": source["source_route"],
            "candidate_review_status": "CANDIDATE_ARTIFACT_IDENTIFIED_REVIEW_REQUIRED",
            "candidate_limitation": "requires reviewer confirmation before leakage-evidence ingestion",
        }
    if evidence_id == "LEC10_OBSERVED_INPUTS":
        target = INPUT / "source_import_real_values_v12.csv"
        imported_rows = count_rows(target)
        return {
            "candidate_artifact_uri_or_id": "data/input/source_import_real_values_v12.csv",
            "candidate_artifact_hash_or_accession": sha256(target),
            "candidate_row_selector": f"galaxy_id == {galaxy_id}; imported numeric rows in v12",
            "candidate_support_detail": f"v12 imported source values; total imported rows={imported_rows}",
            "candidate_review_status": "CANDIDATE_ARTIFACT_IDENTIFIED_REVIEW_REQUIRED",
            "candidate_limitation": "requires reviewer confirmation of import route, units, and non-endpoint use",
        }
    if evidence_id == "LEC10_MORPH_LABELS":
        source = galaxy_roles[galaxy_id]
        target = SOURCE_MANIFEST / "galaxy_list_freeze_v02.csv"
        return {
            "candidate_artifact_uri_or_id": "data/source_manifest/galaxy_list_freeze_v02.csv",
            "candidate_artifact_hash_or_accession": sha256(target),
            "candidate_row_selector": source["row_id"],
            "candidate_support_detail": f"decision_role={source['decision_role']}; source_route={source['source_route']}",
            "candidate_review_status": "PARTIAL_CANDIDATE_ARTIFACT_IDENTIFIED_REVIEW_REQUIRED",
            "candidate_limitation": "role freeze is present, but reviewer must confirm it is sufficient as morphology/readout label evidence",
        }
    if evidence_id == "LEC10_BENCHMARK_INPUTS":
        target = SOURCE_MANIFEST / "scoring_formula_freeze_v02.csv"
        return {
            "candidate_artifact_uri_or_id": "data/source_manifest/scoring_formula_freeze_v02.csv;data/source_manifest/control_implementation_freeze_v03.csv;data/source_manifest/control_manifest_v01.csv",
            "candidate_artifact_hash_or_accession": sha256(target),
            "candidate_row_selector": "global benchmark and control policy rows; applies to all frozen galaxies",
            "candidate_support_detail": "scoring formula, benchmark/control policy, and forbidden-input rules are frozen before endpoint scoring",
            "candidate_review_status": "PARTIAL_CANDIDATE_ARTIFACT_IDENTIFIED_REVIEW_REQUIRED",
            "candidate_limitation": "global policy candidate still needs reviewer confirmation and may need bundle-level hash/accession support",
        }
    raise ValueError(f"unexpected evidence_id: {evidence_id}")


def ledger_rows() -> list[dict[str, object]]:
    requests = read_csv(DERIVED / "leakage_prescore_artifact_request_ledger_v64.csv")
    provenance = first_by(read_csv(INPUT / "source_import_provenance_evidence_v21.csv"), "galaxy_id")
    galaxy_roles = first_by(read_csv(SOURCE_MANIFEST / "galaxy_list_freeze_v02.csv"), "galaxy_id")
    out: list[dict[str, object]] = []
    for index, row in enumerate(requests, start=1):
        candidate = candidate_for(row, provenance, galaxy_roles)
        out.append(
            {
                "candidate_id": f"LPAC67_{index:03d}",
                "request_id": row["request_id"],
                "work_order_id": row["work_order_id"],
                "leakage_evidence_row_id": row["leakage_evidence_row_id"],
                "galaxy_id": row["galaxy_id"],
                "proposed_split": row["proposed_split"],
                "evidence_id": row["evidence_id"],
                "request_family": row["request_family"],
                "candidate_artifact_uri_or_id": candidate["candidate_artifact_uri_or_id"],
                "candidate_artifact_hash_or_accession": candidate["candidate_artifact_hash_or_accession"],
                "candidate_row_selector": candidate["candidate_row_selector"],
                "candidate_support_detail": candidate["candidate_support_detail"],
                "candidate_review_status": candidate["candidate_review_status"],
                "candidate_limitation": candidate["candidate_limitation"],
                "may_promote_to_leakage_evidence_without_review": "false",
                "may_activate_row_from_candidate": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "leakage_prescore_artifact_candidate_ledger_only_no_evidence_no_scores",
            }
        )
    return out


def coverage_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for evidence_id in sorted({str(row["evidence_id"]) for row in rows}):
        subset = [row for row in rows if row["evidence_id"] == evidence_id]
        full = sum(row["candidate_review_status"] == "CANDIDATE_ARTIFACT_IDENTIFIED_REVIEW_REQUIRED" for row in subset)
        partial = sum(row["candidate_review_status"] == "PARTIAL_CANDIDATE_ARTIFACT_IDENTIFIED_REVIEW_REQUIRED" for row in subset)
        out.append(
            {
                "coverage_id": f"LPAC67_{evidence_id}",
                "evidence_id": evidence_id,
                "candidate_rows": len(subset),
                "full_candidate_rows": full,
                "partial_candidate_rows": partial,
                "review_required_rows": len(subset),
                "ready_for_leakage_evidence_rows": 0,
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "leakage_prescore_artifact_candidate_coverage_only_no_scores",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    full = sum(row["candidate_review_status"] == "CANDIDATE_ARTIFACT_IDENTIFIED_REVIEW_REQUIRED" for row in rows)
    partial = sum(row["candidate_review_status"] == "PARTIAL_CANDIDATE_ARTIFACT_IDENTIFIED_REVIEW_REQUIRED" for row in rows)
    return [
        {
            "summary_id": "LEAKAGE_PRESCORE_ARTIFACT_CANDIDATE_LEDGER_V67",
            "candidate_rows": len(rows),
            "galaxies_covered": len({row["galaxy_id"] for row in rows}),
            "evidence_checks_per_galaxy": 4,
            "full_candidate_rows": full,
            "partial_candidate_rows": partial,
            "review_required_rows": len(rows),
            "ready_for_leakage_evidence_rows": 0,
            "leakage_evidence_rows_created": 0,
            "activation_rows_authorized": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PRESCORE_ARTIFACT_CANDIDATES_IDENTIFIED_REVIEW_REQUIRED",
            "next_required_artifact": "completed_candidate_review_response_authorizing_prescore_artifacts",
            "claim_boundary": "leakage_prescore_artifact_candidate_ledger_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = ledger_rows()
    coverage = coverage_rows(rows)
    write_csv(
        DERIVED / "leakage_prescore_artifact_candidate_ledger_v67.csv",
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
            "candidate_support_detail",
            "candidate_review_status",
            "candidate_limitation",
            "may_promote_to_leakage_evidence_without_review",
            "may_activate_row_from_candidate",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "leakage_prescore_artifact_candidate_coverage_v67.csv",
        coverage,
        [
            "coverage_id",
            "evidence_id",
            "candidate_rows",
            "full_candidate_rows",
            "partial_candidate_rows",
            "review_required_rows",
            "ready_for_leakage_evidence_rows",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "leakage_prescore_artifact_candidate_summary_v67.csv",
        summary(rows),
        [
            "summary_id",
            "candidate_rows",
            "galaxies_covered",
            "evidence_checks_per_galaxy",
            "full_candidate_rows",
            "partial_candidate_rows",
            "review_required_rows",
            "ready_for_leakage_evidence_rows",
            "leakage_evidence_rows_created",
            "activation_rows_authorized",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_LEAKAGE_PRESCORE_ARTIFACT_CANDIDATE_LEDGER_V67_BUILT")


if __name__ == "__main__":
    main()
