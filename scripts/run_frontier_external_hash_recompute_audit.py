#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
CACHE = ROOT / "data/external/sparc_hash_audit_v50"


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
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def audit_rows() -> list[dict[str, object]]:
    sources = read_csv(DERIVED / "frontier_provenance_source_candidate_ledger_v45.csv")
    rows: list[dict[str, object]] = []
    for source in sources:
        cache_path = CACHE / source["table_or_file"]
        expected = source["sha256_or_external_accession"].removeprefix("sha256:")
        present = cache_path.exists()
        recomputed = sha256(cache_path) if present else ""
        matched = present and recomputed == expected
        rows.append(
            {
                "hash_audit_id": f"FEHRA50_{source['source_candidate_id']}",
                "source_candidate_id": source["source_candidate_id"],
                "catalog": source["catalog"],
                "table_or_file": source["table_or_file"],
                "source_url": source["source_url"],
                "cache_path": str(cache_path.relative_to(ROOT)),
                "expected_sha256": expected,
                "recomputed_sha256": recomputed,
                "file_size_bytes": cache_path.stat().st_size if present else 0,
                "source_access_status": "LIVE_DOWNLOAD_CACHED_FOR_HASH_AUDIT" if present else "CACHE_FILE_MISSING",
                "hash_recompute_status": "EXTERNAL_HASH_RECOMPUTED_MATCHED" if matched else "EXTERNAL_HASH_RECOMPUTE_BLOCKED_OR_MISMATCHED",
                "may_promote_v21_by_hash_alone": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "frontier_external_hash_recompute_audit_only_no_evidence_no_scores",
            }
        )
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    matched = sum(row["hash_recompute_status"] == "EXTERNAL_HASH_RECOMPUTED_MATCHED" for row in rows)
    table1_matched = any(
        row["source_candidate_id"] == "FPSC45_SPARC_TABLE1"
        and row["hash_recompute_status"] == "EXTERNAL_HASH_RECOMPUTED_MATCHED"
        for row in rows
    )
    return [
        {
            "summary_id": "FRONTIER_EXTERNAL_HASH_RECOMPUTE_AUDIT_V50",
            "source_candidate_rows": len(rows),
            "hash_recomputed_matched_rows": matched,
            "primary_table1_hash_recomputed_matched": str(table1_matched).lower(),
            "v21_evidence_rows_created": 0,
            "provenance_complete_rows_marked": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FRONTIER_EXTERNAL_HASH_RECOMPUTED_MATCHED" if matched == len(rows) else "FRONTIER_EXTERNAL_HASH_RECOMPUTE_INCOMPLETE",
            "claim_boundary": "frontier_external_hash_recompute_audit_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = audit_rows()
    summary_rows = summary(rows)
    write_csv(
        DERIVED / "frontier_external_hash_recompute_audit_v50.csv",
        rows,
        [
            "hash_audit_id",
            "source_candidate_id",
            "catalog",
            "table_or_file",
            "source_url",
            "cache_path",
            "expected_sha256",
            "recomputed_sha256",
            "file_size_bytes",
            "source_access_status",
            "hash_recompute_status",
            "may_promote_v21_by_hash_alone",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "frontier_external_hash_recompute_audit_summary_v50.csv",
        summary_rows,
        [
            "summary_id",
            "source_candidate_rows",
            "hash_recomputed_matched_rows",
            "primary_table1_hash_recomputed_matched",
            "v21_evidence_rows_created",
            "provenance_complete_rows_marked",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_FRONTIER_EXTERNAL_HASH_RECOMPUTE_AUDIT_V50_BUILT")


if __name__ == "__main__":
    main()
