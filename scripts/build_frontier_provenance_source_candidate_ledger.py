#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"

SPARC_SOURCES = [
    {
        "source_candidate_id": "FPSC45_SPARC_TABLE1",
        "catalog": "SPARC",
        "table_or_file": "SPARC_Lelli2016c.mrt",
        "version_or_date": "SPARC webpage last update 2020-05-29; local source-candidate audit 2026-06-11",
        "source_url": "https://astroweb.case.edu/SPARC/SPARC_Lelli2016c.mrt",
        "landing_page_url": "https://astroweb.case.edu/SPARC/",
        "paper_reference": "Lelli, McGaugh, Schombert 2016 AJ 152 157",
        "sha256_or_external_accession": "sha256:5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243",
        "source_role": "galaxy_sample_row_identity_and_original_rotation_curve_reference_provenance",
    },
    {
        "source_candidate_id": "FPSC45_SPARC_MASSMODELS",
        "catalog": "SPARC",
        "table_or_file": "MassModels_Lelli2016c.mrt",
        "version_or_date": "SPARC webpage last update 2020-05-29; local source-candidate audit 2026-06-11",
        "source_url": "https://astroweb.case.edu/SPARC/MassModels_Lelli2016c.mrt",
        "landing_page_url": "https://astroweb.case.edu/SPARC/",
        "paper_reference": "Lelli, McGaugh, Schombert 2016 AJ 152 157",
        "sha256_or_external_accession": "sha256:9108994b12cc401b94a1768beca61c53ec354779385c9c9cc571049f3043244c",
        "source_role": "future_raw_mass_model_source_route_candidate_not_imported",
    },
]


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


def source_rows() -> list[dict[str, object]]:
    return [
        {
            **source,
            "review_status": "SOURCE_CANDIDATE_READY_FOR_HUMAN_REVIEW",
            "may_write_v21_evidence_input": "false",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "frontier_provenance_source_candidate_only_no_evidence_no_scores",
        }
        for source in SPARC_SOURCES
    ]


def coverage_rows() -> list[dict[str, object]]:
    checklist = read_csv(DERIVED / "frontier_provenance_evidence_intake_checklist_v44.csv")
    rows: list[dict[str, object]] = []
    for index, row in enumerate(checklist, start=1):
        galaxy_id = row["galaxy_id"]
        rows.append(
            {
                "coverage_id": f"FPSC45_COVERAGE_{index:03d}",
                "galaxy_id": galaxy_id,
                "primary_source_candidate_id": "FPSC45_SPARC_TABLE1",
                "candidate_row_id_rule": f"Galaxy == {galaxy_id} in SPARC_Lelli2016c.mrt",
                "candidate_source_route": f"SPARC landing page -> SPARC_Lelli2016c.mrt -> Galaxy == {galaxy_id}",
                "candidate_leakage_evidence_id": f"PRE_SCORE_SOURCE_ROUTE_REVIEW_{galaxy_id}",
                "coverage_status": "CANDIDATE_ROW_IDENTIFIED_NOT_V21_EVIDENCE",
                "may_mark_provenance_complete": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "frontier_provenance_source_candidate_coverage_only_no_evidence_no_scores",
            }
        )
    return rows


def summary(sources: list[dict[str, object]], coverage: list[dict[str, object]]) -> list[dict[str, object]]:
    ready_sources = sum(row["review_status"] == "SOURCE_CANDIDATE_READY_FOR_HUMAN_REVIEW" for row in sources)
    covered = sum(row["coverage_status"] == "CANDIDATE_ROW_IDENTIFIED_NOT_V21_EVIDENCE" for row in coverage)
    return [
        {
            "summary_id": "FRONTIER_PROVENANCE_SOURCE_CANDIDATE_LEDGER_V45",
            "source_candidate_rows": len(sources),
            "ready_for_human_review_source_rows": ready_sources,
            "coverage_rows": len(coverage),
            "candidate_rows_identified": covered,
            "v21_evidence_rows_created": "0",
            "may_write_v21_evidence_input_anywhere": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FRONTIER_PROVENANCE_SOURCE_CANDIDATES_READY_NOT_EVIDENCE",
            "claim_boundary": "frontier_provenance_source_candidate_ledger_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    sources = source_rows()
    coverage = coverage_rows()
    write_csv(
        DERIVED / "frontier_provenance_source_candidate_ledger_v45.csv",
        sources,
        [
            "source_candidate_id",
            "catalog",
            "table_or_file",
            "version_or_date",
            "source_url",
            "landing_page_url",
            "paper_reference",
            "sha256_or_external_accession",
            "source_role",
            "review_status",
            "may_write_v21_evidence_input",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "frontier_provenance_source_candidate_coverage_v45.csv",
        coverage,
        [
            "coverage_id",
            "galaxy_id",
            "primary_source_candidate_id",
            "candidate_row_id_rule",
            "candidate_source_route",
            "candidate_leakage_evidence_id",
            "coverage_status",
            "may_mark_provenance_complete",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "frontier_provenance_source_candidate_ledger_summary_v45.csv",
        summary(sources, coverage),
        [
            "summary_id",
            "source_candidate_rows",
            "ready_for_human_review_source_rows",
            "coverage_rows",
            "candidate_rows_identified",
            "v21_evidence_rows_created",
            "may_write_v21_evidence_input_anywhere",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_FRONTIER_PROVENANCE_SOURCE_CANDIDATE_LEDGER_V45_BUILT")


if __name__ == "__main__":
    main()
