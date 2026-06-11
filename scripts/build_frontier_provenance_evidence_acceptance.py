#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
INPUT = ROOT / "data/input/source_import_provenance_evidence_v21.csv"

REQUIRED_FIELDS = [
    "catalog",
    "table_or_file",
    "version_or_date",
    "row_id",
    "sha256_or_external_accession",
    "source_route",
    "leakage_evidence_id",
    "provenance_evidence_status",
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


def evidence_by_galaxy() -> dict[str, dict[str, str]]:
    if not INPUT.exists():
        return {}
    return {row.get("galaxy_id", ""): row for row in read_csv(INPUT)}


def acceptance_rows() -> list[dict[str, object]]:
    priority = read_csv(DERIVED / "scoring_unblock_priority_summary_v25.csv")[0]
    manifest = read_csv(DERIVED / "source_import_provenance_manifest_v19.csv")
    evidence = evidence_by_galaxy()
    out: list[dict[str, object]] = []
    for index, row in enumerate(manifest, start=1):
        galaxy_id = row["galaxy_id"]
        evidence_row = evidence.get(galaxy_id)
        if evidence_row is None:
            missing_fields = "input_row_missing"
            complete = False
            status = "PENDING_INPUT"
        else:
            missing = [
                field
                for field in REQUIRED_FIELDS
                if evidence_row.get(field, "") == "" or evidence_row.get(field, "").startswith("FILL_")
            ]
            status_ok = evidence_row.get("provenance_evidence_status") == "PROVENANCE_EVIDENCE_COMPLETE"
            missing_fields = ";".join(missing) if missing else "none"
            complete = not missing and status_ok
            status = "ACCEPTED_FOR_REVIEW" if complete else "PRESENT_BUT_INCOMPLETE"
        out.append(
            {
                "acceptance_id": f"FPEA26_{index:03d}",
                "galaxy_id": galaxy_id,
                "frontier_dependency": priority["first_frontier_dependency"],
                "frontier_artifact": priority["first_frontier_artifact"],
                "required_fields": ";".join(REQUIRED_FIELDS),
                "evidence_input_present": str(evidence_row is not None).lower(),
                "missing_or_placeholder_fields": missing_fields,
                "acceptance_status": status,
                "accepted_for_promotion_review": str(complete).lower(),
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "frontier_evidence_acceptance_only_no_source_import_no_scores",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    accepted = sum(row["accepted_for_promotion_review"] == "true" for row in rows)
    present = sum(row["evidence_input_present"] == "true" for row in rows)
    return [
        {
            "summary_id": "FRONTIER_PROVENANCE_EVIDENCE_ACCEPTANCE_V26",
            "frontier_dependency": "SCD24_PROVENANCE_EVIDENCE",
            "frontier_artifact": "data/input/source_import_provenance_evidence_v21.csv",
            "candidate_rows": len(rows),
            "evidence_input_rows_present": present,
            "accepted_for_promotion_review_rows": accepted,
            "blocked_rows": len(rows) - accepted,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FRONTIER_EVIDENCE_ACCEPTANCE_PENDING_INPUT"
            if accepted == 0
            else "FRONTIER_EVIDENCE_ACCEPTANCE_REVIEW_READY",
            "claim_boundary": "frontier_evidence_acceptance_only_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = acceptance_rows()
    summary_rows = summary(rows)
    write_csv(
        DERIVED / "frontier_provenance_evidence_acceptance_v26.csv",
        rows,
        [
            "acceptance_id",
            "galaxy_id",
            "frontier_dependency",
            "frontier_artifact",
            "required_fields",
            "evidence_input_present",
            "missing_or_placeholder_fields",
            "acceptance_status",
            "accepted_for_promotion_review",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "frontier_provenance_evidence_acceptance_summary_v26.csv",
        summary_rows,
        [
            "summary_id",
            "frontier_dependency",
            "frontier_artifact",
            "candidate_rows",
            "evidence_input_rows_present",
            "accepted_for_promotion_review_rows",
            "blocked_rows",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_FRONTIER_PROVENANCE_EVIDENCE_ACCEPTANCE_V26_BUILT")


if __name__ == "__main__":
    main()
