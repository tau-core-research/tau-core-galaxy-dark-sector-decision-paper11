#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
MACHINE_PAYLOAD_SUMMARY = DERIVED / "m0_no_dark_payload_machine_form_summary_v12.csv"
PAYLOAD_SUMMARY = DERIVED / "m0_no_dark_frozen_expression_payload_summary_v11.csv"


FIELDNAMES = [
    "certificate_id",
    "certificate_class",
    "certificate_role",
    "accepted_evidence",
    "blocked_leakage_route",
    "completion_status",
    "next_required_artifact",
    "forbidden_inputs",
    "certificate_claim_allowed",
    "formula_claim_allowed",
    "numeric_prediction_allowed",
    "endpoint_scoring_allowed",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def machine_payload_ready() -> bool:
    if not MACHINE_PAYLOAD_SUMMARY.exists() or not PAYLOAD_SUMMARY.exists():
        return False
    machine = read_csv(MACHINE_PAYLOAD_SUMMARY)
    payload = read_csv(PAYLOAD_SUMMARY)
    return (
        len(machine) == 1
        and machine[0]["overall_status"] == "M0_NO_DARK_PAYLOAD_MACHINE_FORM_READY_FOR_LEAKAGE_CERTIFICATE"
        and machine[0]["endpoint_scoring_allowed_anywhere"] == "false"
        and len(payload) == 1
        and payload[0]["overall_status"]
        in {
            "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_READY_PAYLOAD_LEAKAGE_CERTIFICATE_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_READY_FOR_KERNEL_EXPRESSION",
        }
        and payload[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def certificate_rows() -> list[dict[str, object]]:
    rows = [
        {
            "certificate_id": "M0NDPLC12_FORBIDDEN_INPUT_MANIFEST",
            "certificate_class": "forbidden_input_manifest",
            "certificate_role": "certify that endpoint residuals, heldout scores, family winners, and best-fit curves are forbidden payload inputs",
            "accepted_evidence": "machine-form rows expose a forbidden-input manifest before any prediction writer exists",
            "blocked_leakage_route": "payload field sourced from endpoint_residual or heldout_score",
        },
        {
            "certificate_id": "M0NDPLC12_FREEZE_ORDER_CERTIFICATE",
            "certificate_class": "freeze_order_certificate",
            "certificate_role": "certify that statement, symbol binding, constant policy, dimensional trace, and machine form precede prediction rows",
            "accepted_evidence": "payload gates are ordered before family prediction table construction",
            "blocked_leakage_route": "post-score rewrite of payload symbols, constants, or unit path",
        },
        {
            "certificate_id": "M0NDPLC12_SERIALIZATION_HASH_POLICY",
            "certificate_class": "serialization_hash_policy",
            "certificate_role": "certify that serialized payload fields are inspectable and hashable before later execution",
            "accepted_evidence": "payload manifest contains deterministic serialization fields and no prediction callable",
            "blocked_leakage_route": "silent callable switch or untracked payload mutation",
        },
        {
            "certificate_id": "M0NDPLC12_SOURCE_PROVENANCE_GUARDS",
            "certificate_class": "source_provenance_guards",
            "certificate_role": "certify that source-state, baryonic/radial, operator, guard, and dimension records remain source-side",
            "accepted_evidence": "each machine-form row points to source-side or pre-score guard classes",
            "blocked_leakage_route": "source proxy chosen from best-fit curve quality",
        },
        {
            "certificate_id": "M0NDPLC12_NULL_FALLBACK_STOP_CERTIFICATE",
            "certificate_class": "null_fallback_stop_certificate",
            "certificate_role": "certify that null, fallback, and blocked routes stop rows instead of repairing endpoint failures",
            "accepted_evidence": "fallback and null paths are serialized as stop states, not rescue terms",
            "blocked_leakage_route": "fallback term introduced after failed prediction performance",
        },
        {
            "certificate_id": "M0NDPLC12_HANDOFF_TO_FORMULA_TABLES",
            "certificate_class": "formula_table_handoff",
            "certificate_role": "handoff the leakage-certified payload boundary to later formula and prediction-table contracts",
            "accepted_evidence": "payload leakage certificate closes without formula, callable, prediction rows, or scoring",
            "blocked_leakage_route": "direct endpoint scoring after payload certification",
        },
    ]
    for row in rows:
        row["completion_status"] = "READY"
        row["next_required_artifact"] = "family_prediction_tables_v08.csv"
        row["forbidden_inputs"] = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_callable_switch"
        row["certificate_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_payload_leakage_certificate_only_no_formula_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["completion_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    upstream_ready = machine_payload_ready()
    return [
        {
            "summary_id": "M0_NO_DARK_PAYLOAD_LEAKAGE_CERTIFICATE_V12",
            "payload_leakage_certificate_artifact": "m0_no_dark_payload_leakage_certificate_v12",
            "machine_payload_status": "READY" if upstream_ready else "BLOCKED",
            "certificate_rows": len(rows),
            "ready_certificate_rows": ready,
            "blocked_certificate_rows": blocked,
            "payload_leakage_certificate_written": "true" if upstream_ready and blocked == 0 else "false",
            "prediction_callable_written": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_PAYLOAD_LEAKAGE_CERTIFICATE_READY_FOR_FORMULA_TABLES"
            if upstream_ready and blocked == 0
            else "M0_NO_DARK_PAYLOAD_LEAKAGE_CERTIFICATE_BLOCKED",
            "next_required_artifact": "family_prediction_tables_v08.csv",
            "claim_boundary": "m0_no_dark_payload_leakage_certificate_only_no_formula_no_values_no_scores_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_payload_leakage_certificate_v12.md").write_text(
        """# M0 No-Dark Payload Leakage Certificate v12

**Doc class:** no-dark M0 payload leakage certificate
**Status:** payload leakage certificate ready; formula tables still blocked; no formula; no scoring

Script:

```text
scripts/build_m0_no_dark_payload_leakage_certificate.py
```

Derived outputs:

```text
data/derived/m0_no_dark_payload_leakage_certificate_v12.csv
data/derived/m0_no_dark_payload_leakage_certificate_summary_v12.csv
```

This artifact certifies that the machine-readable M0 no-dark payload remains
pre-endpoint. It records forbidden input manifests, freeze ordering,
serialization/hash policy, source-provenance guards, null/fallback stop
behavior, and the handoff to later formula-table contracts.

## Current Result

The expected status is:

```text
M0_NO_DARK_PAYLOAD_LEAKAGE_CERTIFICATE_READY_FOR_FORMULA_TABLES
```

The next required artifact is:

```text
family_prediction_tables_v08.csv
```

## Claim Boundary

This leakage certificate does not assign numerical values, does not define a
velocity formula, does not expose a prediction callable, does not compute
predictions, does not score galaxies, and does not decide the dark-sector
question. It only certifies that the serialized payload boundary excludes
endpoint-derived information before later formula-table work.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = certificate_rows()
    write_csv(DERIVED / "m0_no_dark_payload_leakage_certificate_v12.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_payload_leakage_certificate_summary_v12.csv",
        summary(rows),
        [
            "summary_id",
            "payload_leakage_certificate_artifact",
            "machine_payload_status",
            "certificate_rows",
            "ready_certificate_rows",
            "blocked_certificate_rows",
            "payload_leakage_certificate_written",
            "prediction_callable_written",
            "formula_claim_allowed",
            "numeric_predictions_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_PAYLOAD_LEAKAGE_CERTIFICATE_V12_BUILT")


if __name__ == "__main__":
    main()
