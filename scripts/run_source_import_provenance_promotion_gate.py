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


def promotion_rows() -> list[dict[str, object]]:
    manifest = read_csv(DERIVED / "source_import_provenance_manifest_v19.csv")
    evidence_gate = read_csv(DERIVED / "source_import_provenance_evidence_gate_v22.csv")[0]
    evidence_allows = evidence_gate["provenance_promotion_allowed"] == "true"
    blocker = (
        "none"
        if evidence_allows
        else "provenance_evidence_gate_not_allowed;provenance_evidence_input_missing"
    )
    decision = "PROMOTE_PROVENANCE" if evidence_allows else "DO_NOT_PROMOTE_PROVENANCE"
    promotion_allowed = "true" if evidence_allows else "false"

    rows: list[dict[str, object]] = []
    for index, row in enumerate(manifest, start=1):
        rows.append(
            {
                "promotion_gate_id": f"SIPPG23_{index:03d}",
                "source_provenance_id": row["provenance_id"],
                "galaxy_id": row["galaxy_id"],
                "evidence_gate_id": evidence_gate["evidence_gate_id"],
                "evidence_input_status": evidence_gate["evidence_input_status"],
                "v22_provenance_promotion_allowed": evidence_gate["provenance_promotion_allowed"],
                "promotion_allowed": promotion_allowed,
                "promotion_decision": decision,
                "promotion_blockers": blocker,
                "provenance_rows_promoted": 1 if evidence_allows else 0,
                "raw_import_allowed_after_promotion": "true" if evidence_allows else "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "provenance_promotion_gate_only_no_manifest_mutation_no_scores",
            }
        )
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    candidate_rows = len(rows)
    allowed_rows = sum(row["promotion_allowed"] == "true" for row in rows)
    blocked_rows = candidate_rows - allowed_rows
    promoted_rows = sum(int(row["provenance_rows_promoted"]) for row in rows)
    return [
        {
            "summary_id": "SOURCE_IMPORT_PROVENANCE_PROMOTION_GATE_V23",
            "candidate_rows": candidate_rows,
            "promotion_allowed_rows": allowed_rows,
            "promotion_blocked_rows": blocked_rows,
            "provenance_rows_promoted": promoted_rows,
            "raw_import_allowed_rows_after_promotion": promoted_rows,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PROVENANCE_PROMOTION_BLOCKED"
            if blocked_rows
            else "PROVENANCE_PROMOTION_READY_NOT_IMPORTED",
            "next_required_artifact": "data/input/source_import_provenance_evidence_v21.csv",
            "claim_boundary": "provenance_promotion_gate_only_no_source_import_no_scores",
        }
    ]


def main() -> None:
    rows = promotion_rows()
    summary_rows = summary(rows)
    write_csv(
        DERIVED / "source_import_provenance_promotion_gate_v23.csv",
        rows,
        [
            "promotion_gate_id",
            "source_provenance_id",
            "galaxy_id",
            "evidence_gate_id",
            "evidence_input_status",
            "v22_provenance_promotion_allowed",
            "promotion_allowed",
            "promotion_decision",
            "promotion_blockers",
            "provenance_rows_promoted",
            "raw_import_allowed_after_promotion",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "source_import_provenance_promotion_summary_v23.csv",
        summary_rows,
        [
            "summary_id",
            "candidate_rows",
            "promotion_allowed_rows",
            "promotion_blocked_rows",
            "provenance_rows_promoted",
            "raw_import_allowed_rows_after_promotion",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_SOURCE_IMPORT_PROVENANCE_PROMOTION_GATE_V23_BUILT")


if __name__ == "__main__":
    main()
