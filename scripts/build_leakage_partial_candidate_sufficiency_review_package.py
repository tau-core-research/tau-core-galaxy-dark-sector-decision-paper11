#!/usr/bin/env python3
from __future__ import annotations

import csv
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
PACKAGE_ROOT = ROOT / "review_packages/leakage_partial_candidate_sufficiency_v71_review_package"
ZIP_PATH = ROOT / "review_packages/leakage_partial_candidate_sufficiency_v71_review_package.zip"
CLAIM_BOUNDARY = "leakage_partial_candidate_sufficiency_review_package_only_no_evidence_no_scores"


README = """# Leakage Partial Candidate Sufficiency v71 Review Package

**Status:** partial-candidate sufficiency review package only; not leakage
evidence; no activation; no endpoint scoring.

The v70 ingestion gate found draft source-route and observed-input candidates
for all 18 galaxies, but the morphology-label and benchmark-policy components
remain blocked. This package asks reviewers whether those 36 partial candidate
rows are sufficient for a later leakage-evidence ingestion gate.

## Reviewer Tasks

1. Review each partial morphology-label or benchmark-policy candidate.
2. Decide whether it is sufficient as prescore leakage-evidence support.
3. Confirm that the candidate uses no endpoint residuals, best-fit curves,
   family winners, held-out scores, or post-score selections.
4. Keep activation and endpoint scoring disabled. A later ingestion gate must
   decide whether accepted rows become active leakage evidence.

## Hard Stops

- Do not treat this package as active leakage evidence.
- Do not copy rows into `data/input/leakage_audit_evidence_v10.csv`.
- Do not authorize leakage pass from this package.
- Do not activate scoring rows or compute endpoint scores.
"""


DO_NOT_COPY = """# Do Not Copy Without Completed Sufficiency Review

This package is a review handoff for the 36 partial rows blocked by v70.

Rows may be considered by a later leakage-evidence ingestion gate only after a
completed sufficiency review accepts them. This package itself creates no
evidence rows, no activation rows, and no endpoint scores.
"""


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def policy_rows() -> list[dict[str, object]]:
    coverage = read_csv(DERIVED / "leakage_evidence_candidate_ingestion_coverage_v70.csv")
    roles = {
        "LEC10_SOURCE_ROUTE": "required_source_route_blindness_component",
        "LEC10_OBSERVED_INPUTS": "required_observed_input_blindness_component",
        "LEC10_MORPH_LABELS": "required_morphology_label_blindness_component",
        "LEC10_BENCHMARK_INPUTS": "required_benchmark_policy_blindness_component",
    }
    decisions = {
        "LEC10_SOURCE_ROUTE": "DRAFT_AVAILABLE_NOT_EVIDENCE_NO_SCORING",
        "LEC10_OBSERVED_INPUTS": "DRAFT_AVAILABLE_NOT_EVIDENCE_NO_SCORING",
        "LEC10_MORPH_LABELS": "REQUIRED_FOR_FULL_LEAKAGE_PASS_PARTIAL_SUFFICIENCY_REVIEW_REQUIRED",
        "LEC10_BENCHMARK_INPUTS": "REQUIRED_FOR_FULL_LEAKAGE_PASS_PARTIAL_SUFFICIENCY_REVIEW_REQUIRED",
    }
    out: list[dict[str, object]] = []
    for index, row in enumerate(coverage, start=1):
        out.append(
            {
                "policy_id": f"LPCS71_{index:03d}",
                "evidence_id": row["evidence_id"],
                "scoring_role": roles[row["evidence_id"]],
                "v70_candidate_rows": row["candidate_rows"],
                "v70_draft_available_rows": row["draft_available_rows"],
                "v70_blocked_rows": row["blocked_rows"],
                "minimum_policy_decision": decisions[row["evidence_id"]],
                "required_for_full_leakage_pass": "true",
                "may_use_minimum_two_component_gate_for_endpoint_scoring": "false",
                "requires_completed_sufficiency_review": str(row["blocked_rows"] != "0").lower(),
                "target_evidence_rows_created": "0",
                "leakage_pass_authorized": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "leakage_partial_candidate_sufficiency_policy_only_no_evidence_no_scores",
            }
        )
    return out


def summary_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked_components = [row for row in rows if row["requires_completed_sufficiency_review"] == "true"]
    draft_components = [row for row in rows if row["v70_draft_available_rows"] == "18"]
    partial_review_rows = sum(int(str(row["v70_blocked_rows"])) for row in rows)
    return [
        {
            "summary_id": "LEAKAGE_PARTIAL_CANDIDATE_SUFFICIENCY_POLICY_V71",
            "policy_rows": len(rows),
            "required_components_for_full_scoring_leakage_pass": 4,
            "components_with_full_draft_available": len(draft_components),
            "components_requiring_sufficiency_review": len(blocked_components),
            "partial_candidate_rows_requiring_review": partial_review_rows,
            "minimum_scoring_policy": "FULL_FOUR_COMPONENT_LEAKAGE_REQUIRED_BEFORE_ENDPOINT_SCORING",
            "target_evidence_rows_created": 0,
            "leakage_pass_authorized": 0,
            "activation_rows_authorized": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PARTIAL_SUFFICIENCY_REVIEW_PACKAGE_REQUIRED_BEFORE_LEAKAGE_PASS",
            "next_required_artifact": "completed_leakage_partial_candidate_sufficiency_v71_review_response",
            "claim_boundary": "leakage_partial_candidate_sufficiency_policy_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def response_template_rows() -> list[dict[str, object]]:
    rows = read_csv(DERIVED / "leakage_evidence_candidate_ingestion_gate_v70.csv")
    out: list[dict[str, object]] = []
    for row in rows:
        if row["draft_evidence_candidate_status"] != "NOT_AVAILABLE_FOR_LEAKAGE_EVIDENCE_ROW":
            continue
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
                "sufficiency_review_decision": "KEEP_BLOCKED_PARTIAL_REVIEW_REQUIRED_NOT_AUTHORIZED",
                "partial_candidate_sufficient_for_later_ingestion": "false",
                "minimal_required_fields_covered": "false",
                "artifact_is_prescore": "true",
                "artifact_uses_forbidden_inputs": "UNKNOWN_REVIEW_REQUIRED",
                "may_promote_to_leakage_evidence_after_ingestion": "false",
                "may_activate_row_after_ingestion": "false",
                "endpoint_scoring_allowed": "false",
                "reviewer_notes": "",
            }
        )
    return out


def build_package() -> None:
    policy = policy_rows()
    summary = summary_rows(policy)
    write_csv(
        DERIVED / "leakage_partial_candidate_sufficiency_policy_v71.csv",
        policy,
        [
            "policy_id",
            "evidence_id",
            "scoring_role",
            "v70_candidate_rows",
            "v70_draft_available_rows",
            "v70_blocked_rows",
            "minimum_policy_decision",
            "required_for_full_leakage_pass",
            "may_use_minimum_two_component_gate_for_endpoint_scoring",
            "requires_completed_sufficiency_review",
            "target_evidence_rows_created",
            "leakage_pass_authorized",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "leakage_partial_candidate_sufficiency_policy_summary_v71.csv",
        summary,
        [
            "summary_id",
            "policy_rows",
            "required_components_for_full_scoring_leakage_pass",
            "components_with_full_draft_available",
            "components_requiring_sufficiency_review",
            "partial_candidate_rows_requiring_review",
            "minimum_scoring_policy",
            "target_evidence_rows_created",
            "leakage_pass_authorized",
            "activation_rows_authorized",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )

    if PACKAGE_ROOT.exists():
        shutil.rmtree(PACKAGE_ROOT)
    PACKAGE_ROOT.mkdir(parents=True, exist_ok=True)
    write_text(PACKAGE_ROOT / "README.md", README)
    write_text(PACKAGE_ROOT / "DO_NOT_COPY_WITHOUT_COMPLETED_SUFFICIENCY_REVIEW.md", DO_NOT_COPY)

    package_files = [
        {
            "source": DERIVED / "leakage_evidence_candidate_ingestion_gate_v70.csv",
            "target": "data/leakage_evidence_candidate_ingestion_gate_v70.csv",
            "role": "72-row v70 ingestion gate output",
        },
        {
            "source": DERIVED / "leakage_evidence_candidate_ingestion_coverage_v70.csv",
            "target": "data/leakage_evidence_candidate_ingestion_coverage_v70.csv",
            "role": "v70 leakage component coverage",
        },
        {
            "source": DERIVED / "leakage_evidence_candidate_ingestion_summary_v70.csv",
            "target": "data/leakage_evidence_candidate_ingestion_summary_v70.csv",
            "role": "v70 gate summary and claim boundary",
        },
        {
            "source": DERIVED / "leakage_partial_candidate_sufficiency_policy_v71.csv",
            "target": "data/leakage_partial_candidate_sufficiency_policy_v71.csv",
            "role": "full-four-component minimum leakage policy",
        },
        {
            "source": DERIVED / "leakage_partial_candidate_sufficiency_policy_summary_v71.csv",
            "target": "data/leakage_partial_candidate_sufficiency_policy_summary_v71.csv",
            "role": "v71 policy summary and next required artifact",
        },
    ]
    manifest_rows: list[dict[str, str]] = [
        {
            "package_path": "README.md",
            "source_path": "generated_by_leakage_partial_candidate_sufficiency_review_package_builder",
            "role": "review instructions",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "package_path": "DO_NOT_COPY_WITHOUT_COMPLETED_SUFFICIENCY_REVIEW.md",
            "source_path": "generated_by_leakage_partial_candidate_sufficiency_review_package_builder",
            "role": "hard-stop notice",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    for item in package_files:
        target = PACKAGE_ROOT / item["target"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(item["source"], target)
        manifest_rows.append(
            {
                "package_path": item["target"],
                "source_path": str(item["source"].relative_to(ROOT)),
                "role": item["role"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    response_target = PACKAGE_ROOT / "templates/leakage_partial_candidate_sufficiency_v71_review_response_TEMPLATE.csv"
    write_csv(
        response_target,
        response_template_rows(),
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
            "reviewer_notes",
        ],
    )
    manifest_rows.append(
        {
            "package_path": "templates/leakage_partial_candidate_sufficiency_v71_review_response_TEMPLATE.csv",
            "source_path": "generated_from_leakage_evidence_candidate_ingestion_gate_v70_blocked_rows",
            "role": "fillable partial candidate sufficiency review response template",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    write_csv(
        PACKAGE_ROOT / "REVIEW_MANIFEST.csv",
        manifest_rows,
        ["package_path", "source_path", "role", "claim_boundary"],
    )

    ZIP_PATH.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PACKAGE_ROOT.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(PACKAGE_ROOT.parent))


def main() -> None:
    build_package()
    print(f"PAPER11_LEAKAGE_PARTIAL_CANDIDATE_SUFFICIENCY_REVIEW_PACKAGE_V71_BUILT {ZIP_PATH}")


if __name__ == "__main__":
    main()
