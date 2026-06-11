#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "paper11_submission_source"


def run(cmd: list[str], cwd: Path = ROOT) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def main() -> None:
    env = os.environ.copy()
    env.setdefault("SOURCE_DATE_EPOCH", "1781136000")
    run(["python", "scripts/run_readiness_audit.py"])
    run(["python", "scripts/build_scoring_input_scaffold.py"])
    run(["python", "scripts/build_source_import_contract.py"])
    run(["python", "scripts/build_source_import_values.py"])
    run(["python", "scripts/build_source_import_real_values_template.py"])
    run(["python", "scripts/build_source_import_provenance_manifest.py"])
    run(["python", "scripts/build_source_import_provenance_template.py"])
    run(["python", "scripts/run_source_import_provenance_evidence_gate.py"])
    run(["python", "scripts/run_source_import_provenance_promotion_gate.py"])
    run(["python", "scripts/run_source_import_provenance_audit.py"])
    run(["python", "scripts/build_source_import_raw_template.py"])
    run(["python", "scripts/run_active_v15_raw_sparc_like_input_writer.py"])
    run(["python", "scripts/run_source_import_raw_adapter.py"])
    run(["python", "scripts/run_source_import_write_authorization.py"])
    run(["python", "scripts/run_source_import_authorized_writer.py"])
    run(["python", "scripts/run_source_import_real_values_gate.py"])
    run(["python", "scripts/run_source_import_leakage_audit.py"])
    run(["python", "scripts/run_scoring_activation_gate.py"])
    run(["python", "scripts/build_scoring_dependency_closure.py"])
    run(["python", "scripts/build_scoring_unblock_priority.py"])
    run(["python", "scripts/build_frontier_provenance_evidence_acceptance.py"])
    run(["python", "scripts/build_frontier_provenance_evidence_work_order.py"])
    run(["python", "scripts/run_frontier_work_order_completion_gate.py"])
    run(["python", "scripts/run_frontier_evidence_write_authorization.py"])
    run(["python", "scripts/run_frontier_authorized_evidence_writer.py"])
    run(["python", "scripts/run_frontier_post_writer_evidence_absence_audit.py"])
    run(["python", "scripts/run_post_writer_evidence_gate_recheck.py"])
    run(["python", "scripts/run_post_writer_provenance_promotion_recheck.py"])
    run(["python", "scripts/run_post_writer_raw_import_recheck.py"])
    run(["python", "scripts/run_post_writer_raw_adapter_recheck.py"])
    run(["python", "scripts/run_post_writer_real_values_gate_recheck.py"])
    run(["python", "scripts/run_post_writer_leakage_audit_recheck.py"])
    run(["python", "scripts/run_post_writer_scoring_activation_recheck.py"])
    run(["python", "scripts/run_scoring_preflight.py"])
    run(["python", "scripts/run_post_writer_scoring_preflight_recheck.py"])
    run(["python", "scripts/run_post_writer_scoring_dependency_closure_recheck.py"])
    run(["python", "scripts/run_post_writer_scoring_unblock_priority_recheck.py"])
    run(["python", "scripts/run_post_writer_frontier_evidence_acceptance_recheck.py"])
    run(["python", "scripts/run_post_writer_frontier_work_order_recheck.py"])
    run(["python", "scripts/build_frontier_provenance_evidence_intake_contract.py"])
    run(["python", "scripts/build_frontier_provenance_source_candidate_ledger.py"])
    run(["python", "scripts/build_frontier_provenance_evidence_payload_draft.py"])
    run(["python", "scripts/build_frontier_provenance_review_package.py"])
    run(["python", "scripts/ingest_frontier_provenance_review_response.py"])
    run(["python", "scripts/run_frontier_review_promotion_gate.py"])
    run(["python", "scripts/run_frontier_external_hash_recompute_audit.py"])
    run(["python", "scripts/run_post_hash_frontier_review_promotion_recheck.py"])
    run(["python", "scripts/build_post_hash_review_promotion_package.py"])
    run(["python", "scripts/ingest_post_hash_review_promotion_response.py"])
    run(["python", "scripts/build_authorized_provenance_evidence_payload.py"])
    run(["python", "scripts/run_active_v21_provenance_evidence_writer.py"])
    run(["python", "scripts/validate_protocol_manifests.py"])
    run(["tectonic", "main.tex"], cwd=SOURCE)
    run(["python", "scripts/build_arxiv_source.py"])
    run(["pytest", "-q"])
    print("PAPER11_REPRODUCTION_COMPLETE")


if __name__ == "__main__":
    main()
