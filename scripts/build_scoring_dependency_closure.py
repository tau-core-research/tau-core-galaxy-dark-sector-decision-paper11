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


def summary_row(name: str) -> dict[str, str]:
    return read_csv(DERIVED / name)[0]


def dependency_row(
    dependency_id: str,
    scoring_stage: str,
    required_artifact: str,
    upstream_status: str,
    next_required_artifact: str,
    blocking_detail: str,
    claim_boundary: str,
) -> dict[str, object]:
    blocked = upstream_status not in {
        "READY",
        "PROVENANCE_EVIDENCE_READY_FOR_PROMOTION",
        "PROVENANCE_PROMOTION_READY_NOT_IMPORTED",
        "RAW_IMPORT_READY_BY_PROVENANCE",
        "SOURCE_IMPORT_AND_LEAKAGE_READY",
        "SCORING_ACTIVATION_READY",
    }
    return {
        "dependency_id": dependency_id,
        "scoring_stage": scoring_stage,
        "required_artifact": required_artifact,
        "upstream_status": upstream_status,
        "dependency_decision": "BLOCKED" if blocked else "READY",
        "blocking_detail": blocking_detail if blocked else "none",
        "next_required_artifact": next_required_artifact,
        "endpoint_scoring_allowed": "false",
        "claim_boundary": claim_boundary,
    }


def dependency_rows() -> list[dict[str, object]]:
    rows = [
        dependency_row(
            "SCD24_PROVENANCE_EVIDENCE",
            "source_provenance",
            "data/input/source_import_provenance_evidence_v21.csv",
            summary_row("source_import_provenance_evidence_gate_summary_v22.csv")["overall_status"],
            "data/input/source_import_provenance_evidence_v21.csv",
            "external provenance evidence input is absent",
            "dependency_closure_only_no_evidence_claim",
        ),
        dependency_row(
            "SCD24_PROVENANCE_PROMOTION",
            "source_provenance",
            "data/derived/source_import_provenance_promotion_gate_v23.csv",
            summary_row("source_import_provenance_promotion_summary_v23.csv")["overall_status"],
            "data/input/source_import_provenance_evidence_v21.csv",
            "provenance evidence gate does not allow promotion",
            "dependency_closure_only_no_provenance_promotion",
        ),
        dependency_row(
            "SCD24_PROVENANCE_AUDIT",
            "source_import",
            "data/derived/source_import_provenance_audit_v20.csv",
            summary_row("source_import_provenance_audit_summary_v20.csv")["overall_status"],
            "data/input/source_import_provenance_evidence_v21.csv",
            "raw import is blocked by incomplete provenance",
            "dependency_closure_only_no_source_import",
        ),
        dependency_row(
            "SCD24_RAW_ADAPTER_INPUT",
            "source_import",
            "data/input/source_import_raw_sparc_like_v15.csv",
            summary_row("source_import_raw_adapter_summary_v15.csv")["overall_status"],
            "data/input/source_import_raw_sparc_like_v15.csv",
            "SPARC-like raw input file is absent",
            "dependency_closure_only_no_raw_adapter_claim",
        ),
        dependency_row(
            "SCD24_WRITE_AUTHORIZATION",
            "source_import",
            "data/derived/source_import_write_authorization_v16.csv",
            summary_row("source_import_write_authorization_summary_v16.csv")["overall_status"],
            "data/input/source_import_raw_sparc_like_v15.csv",
            "write authorization remains blocked",
            "dependency_closure_only_no_write_authorization",
        ),
        dependency_row(
            "SCD24_AUTHORIZED_WRITER",
            "source_import",
            "data/derived/source_import_authorized_writer_v17.csv",
            summary_row("source_import_authorized_writer_summary_v17.csv")["overall_status"],
            "data/input/source_import_raw_sparc_like_v15.csv",
            "authorized writer writes zero rows",
            "dependency_closure_only_no_source_import",
        ),
        dependency_row(
            "SCD24_REAL_VALUES",
            "observed_inputs",
            "data/input/source_import_real_values_v12.csv",
            summary_row("source_import_real_values_summary_v12.csv")["overall_status"],
            "data/input/source_import_real_values_v12.csv",
            "real observed input values are absent",
            "dependency_closure_only_no_observed_value_claim",
        ),
        dependency_row(
            "SCD24_LEAKAGE_AUDIT",
            "source_blindness",
            "data/derived/source_import_leakage_summary_v09.csv",
            summary_row("source_import_leakage_summary_v09.csv")["overall_status"],
            "data/input/source_import_real_values_v12.csv",
            "source import and leakage audit are not passed",
            "dependency_closure_only_no_leakage_pass_claim",
        ),
        dependency_row(
            "SCD24_ROW_ACTIVATION",
            "scoring_activation",
            "data/derived/scoring_activation_gate_v13.csv",
            summary_row("scoring_activation_summary_v13.csv")["overall_status"],
            "data/input/source_import_real_values_v12.csv",
            "zero rows are activated for scoring",
            "dependency_closure_only_no_scoring_activation",
        ),
    ]
    for blocker in read_csv(DERIVED / "scoring_activation_global_blockers_v13.csv"):
        rows.append(
            dependency_row(
                blocker["blocker_id"].replace("SAG13", "SCD24"),
                "global_scoring_prerequisite",
                blocker["required_artifact"],
                blocker["current_status"],
                blocker["required_artifact"],
                blocker["blocking_detail"],
                "dependency_closure_only_no_global_scoring_claim",
            )
        )
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked_rows = sum(row["dependency_decision"] == "BLOCKED" for row in rows)
    ready_rows = len(rows) - blocked_rows
    next_required = next(
        (row["next_required_artifact"] for row in rows if row["dependency_decision"] == "BLOCKED"),
        "none",
    )
    return [
        {
            "summary_id": "SCORING_DEPENDENCY_CLOSURE_V24",
            "dependencies_checked": len(rows),
            "ready_dependencies": ready_rows,
            "blocked_dependencies": blocked_rows,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SCORING_DEPENDENCY_CLOSURE_BLOCKED"
            if blocked_rows
            else "SCORING_DEPENDENCY_CLOSURE_READY",
            "next_required_artifact": next_required,
            "claim_boundary": "scoring_dependency_closure_only_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = dependency_rows()
    summary_rows = summary(rows)
    write_csv(
        DERIVED / "scoring_dependency_closure_v24.csv",
        rows,
        [
            "dependency_id",
            "scoring_stage",
            "required_artifact",
            "upstream_status",
            "dependency_decision",
            "blocking_detail",
            "next_required_artifact",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "scoring_dependency_closure_summary_v24.csv",
        summary_rows,
        [
            "summary_id",
            "dependencies_checked",
            "ready_dependencies",
            "blocked_dependencies",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_SCORING_DEPENDENCY_CLOSURE_V24_BUILT")


if __name__ == "__main__":
    main()
