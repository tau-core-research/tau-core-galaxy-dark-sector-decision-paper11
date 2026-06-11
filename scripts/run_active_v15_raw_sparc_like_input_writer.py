#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
EXTERNAL = ROOT / "data/external/sparc_hash_audit_v50"
TARGET = ROOT / "data/input/source_import_raw_sparc_like_v15.csv"
MASS_MODELS = EXTERNAL / "MassModels_Lelli2016c.mrt"

RAW_COLUMNS = [
    "galaxy_id",
    "radial_index",
    "radius_kpc",
    "v_obs_km_s",
    "sigma_v_km_s",
    "v_gas_km_s",
    "v_disk_km_s",
    "v_bulge_km_s",
    "catalog",
    "table_or_file",
    "version_or_date",
    "row_id",
    "sha256_or_external_accession",
    "source_route",
    "leakage_evidence_id",
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


def massmodels_source_metadata() -> dict[str, str]:
    rows = read_csv(DERIVED / "frontier_provenance_source_candidate_ledger_v45.csv")
    for row in rows:
        if row["table_or_file"] == "MassModels_Lelli2016c.mrt":
            return row
    raise RuntimeError("MassModels source candidate is missing from v45 ledger")


def provenance_by_galaxy() -> dict[str, dict[str, str]]:
    return {
        row["galaxy_id"]: row
        for row in read_csv(ROOT / "data/input/source_import_provenance_evidence_v21.csv")
        if row["provenance_evidence_status"] == "PROVENANCE_EVIDENCE_COMPLETE"
    }


def expected_galaxies() -> list[str]:
    return [row["galaxy_id"] for row in read_csv(DERIVED / "activated_scoring_rows_v08.csv")]


def data_lines() -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    for line_number, line in enumerate(MASS_MODELS.read_text().splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        parts = stripped.split()
        if len(parts) != 10:
            continue
        try:
            float(parts[1])
            float(parts[2])
            float(parts[3])
            float(parts[4])
            float(parts[5])
            float(parts[6])
            float(parts[7])
        except ValueError:
            continue
        out.append((line_number, stripped))
    return out


def raw_rows() -> list[dict[str, object]]:
    source = massmodels_source_metadata()
    provenance = provenance_by_galaxy()
    expected = set(expected_galaxies())
    radial_index_by_galaxy = {galaxy_id: 0 for galaxy_id in expected}
    rows: list[dict[str, object]] = []
    for line_number, line in data_lines():
        parts = line.split()
        galaxy_id = parts[0]
        if galaxy_id not in expected:
            continue
        radial_index_by_galaxy[galaxy_id] += 1
        provenance_row = provenance[galaxy_id]
        rows.append(
            {
                "galaxy_id": galaxy_id,
                "radial_index": radial_index_by_galaxy[galaxy_id],
                "radius_kpc": parts[2],
                "v_obs_km_s": parts[3],
                "sigma_v_km_s": parts[4],
                "v_gas_km_s": parts[5],
                "v_disk_km_s": parts[6],
                "v_bulge_km_s": parts[7],
                "catalog": "SPARC",
                "table_or_file": "MassModels_Lelli2016c.mrt",
                "version_or_date": source["version_or_date"],
                "row_id": f"MassModels_Lelli2016c.mrt:line:{line_number}:radial_index:{radial_index_by_galaxy[galaxy_id]}",
                "sha256_or_external_accession": source["sha256_or_external_accession"],
                "source_route": provenance_row["source_route"].replace(
                    "SPARC_Lelli2016c.mrt", "MassModels_Lelli2016c.mrt"
                ),
                "leakage_evidence_id": provenance_row["leakage_evidence_id"],
            }
        )
    missing = expected - {row["galaxy_id"] for row in rows}
    if missing:
        raise RuntimeError(f"MassModels rows missing for galaxies: {sorted(missing)}")
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "ACTIVE_V15_RAW_SPARC_LIKE_INPUT_WRITER_V56",
            "source_file": "data/external/sparc_hash_audit_v50/MassModels_Lelli2016c.mrt",
            "target_raw_input": "data/input/source_import_raw_sparc_like_v15.csv",
            "raw_rows_written": len(rows),
            "galaxies_written": len({row["galaxy_id"] for row in rows}),
            "target_file_written": "true",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "ACTIVE_V15_RAW_SPARC_LIKE_INPUT_WRITTEN",
            "claim_boundary": "active_v15_raw_input_writer_only_no_v12_write_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = raw_rows()
    write_csv(TARGET, rows, RAW_COLUMNS)
    write_csv(
        DERIVED / "active_v15_raw_sparc_like_input_writer_summary_v56.csv",
        summary(rows),
        [
            "summary_id",
            "source_file",
            "target_raw_input",
            "raw_rows_written",
            "galaxies_written",
            "target_file_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_ACTIVE_V15_RAW_SPARC_LIKE_INPUT_WRITER_V56_BUILT")


if __name__ == "__main__":
    main()
