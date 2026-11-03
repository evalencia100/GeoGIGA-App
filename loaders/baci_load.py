"""
loaders/baci_load.py
---------------------------------------------------------------------------
Turns one downloaded BACI release (CSV files) into Parquet files that the
atlas and the question template can query in seconds.

Input   data/raw/baci/<snapshot>/BACI_HS92_Y1995_V202601.csv ... (unchanged)
Output  data/baci/hs_rev=92/t=2024/data_0.parquet   one folder per revision-year
        data/baci_meta/products_hs92.parquet         product names per revision

Run from the repository root:
    python loaders/baci_load.py data/raw/baci/2026-01-22

Countries are NOT written here: the one country table for the whole atlas is
reference/countries.csv. This script only checks that every country code in
the new release is in that table, and stops if one is missing.

Needs: duckdb   (pip install -r requirements.txt)
"""

import csv
import re
import shutil
import sys
from pathlib import Path

import duckdb

OUT_DIR = Path("data/baci")
META_DIR = Path("data/baci_meta")
COUNTRIES = Path("reference/countries.csv")
FILE_PATTERN = re.compile(r"^BACI_HS(\d{2})_Y(\d{4})_V(\d{6}[a-z]?)\.csv$")


def main(snapshot):
    snapshot = Path(snapshot)
    files = [f for f in sorted(snapshot.glob("BACI_HS*_Y*_V*.csv"))
             if FILE_PATTERN.match(f.name)]
    if not files:
        sys.exit(f"No BACI trade files found in {snapshot}")

    # Revision, year and version come from the FILE NAME, never from list position.
    parsed = [FILE_PATTERN.match(f.name).groups() for f in files]
    versions = {v for _, _, v in parsed}
    if len(versions) > 1:
        sys.exit(f"More than one BACI version in {snapshot}: {versions}. "
                 "CEPII advises never mixing versions.")
    version = versions.pop()
    revisions = sorted({rev for rev, _, _ in parsed})
    print(f"BACI {version}: {len(files)} files, revisions {', '.join(revisions)}")

    check_countries(snapshot, version)

    con = duckdb.connect()
    for rev in revisions:
        target = OUT_DIR / f"hs_rev={rev}"
        if target.exists():
            shutil.rmtree(target)          # replace this revision completely
        OUT_DIR.mkdir(parents=True, exist_ok=True)

        glob = str(snapshot / f"BACI_HS{rev}_Y*_V{version}.csv")
        # Every column is read as text first, then converted on purpose:
        #  - k stays text, so "010111" keeps its leading zero
        #  - v and q may contain padded "NA"; trim() + TRY_CAST makes them missing
        con.execute(f"""
            CREATE OR REPLACE TABLE flows AS
            SELECT
                CAST(t AS INTEGER)                      AS t,
                CAST(i AS INTEGER)                      AS i,
                CAST(j AS INTEGER)                      AS j,
                trim(k)                                 AS k,
                TRY_CAST(trim(v) AS DOUBLE)             AS v,
                TRY_CAST(trim(q) AS DOUBLE)             AS q,
                trim(q)                                 AS q_raw,
                CAST(regexp_extract(filename, '_Y(\\d{{4}})_', 1) AS INTEGER) AS year_in_name,
                '{version}'                             AS version,
                {int(rev)}                              AS hs_rev
            FROM read_csv('{glob}', header = true, all_varchar = true,
                          filename = true)
        """)

        # Safety checks: stop rather than write something wrong.
        problems = con.execute("""
            SELECT
              count(*) FILTER (WHERE t <> year_in_name)                    AS wrong_year,
              count(*) FILTER (WHERE length(k) <> 6)                       AS bad_code,
              count(*) FILTER (WHERE v IS NULL)                            AS missing_value,
              count(*) FILTER (WHERE q IS NULL AND q_raw NOT IN ('NA', '')) AS unreadable_q
            FROM flows
        """).fetchone()
        if any(problems):
            sys.exit(f"HS{rev}: checks failed (wrong_year, bad_code, missing_value, "
                     f"unreadable_q) = {problems}. Nothing written.")

        con.execute(f"""
            COPY (SELECT t, i, j, k, v, q, version, hs_rev FROM flows)
            TO '{OUT_DIR}' (FORMAT parquet, PARTITION_BY (hs_rev, t),
                            OVERWRITE_OR_IGNORE true)
        """)
        rows, years = con.execute(
            "SELECT count(*), string_agg(DISTINCT t::VARCHAR, ', ' ORDER BY t::VARCHAR) FROM flows"
        ).fetchone()
        print(f"  HS{rev}: {rows:,} rows written, years {years}")

        # Product names for this revision
        product_file = snapshot / f"product_codes_HS{rev}_V{version}.csv"
        if product_file.exists():
            META_DIR.mkdir(parents=True, exist_ok=True)
            con.execute(f"""
                COPY (SELECT * FROM read_csv('{product_file}', all_varchar = true))
                TO '{META_DIR / f"products_hs{rev}.parquet"}' (FORMAT parquet)
            """)

    print(f"Done. Parquet is in {OUT_DIR}/")


def check_countries(snapshot, version):
    """Stop if the release has a country code that reference/countries.csv lacks."""
    raw = snapshot / f"country_codes_V{version}.csv"
    if not raw.exists():
        print(f"  (no {raw.name} in snapshot; skipping country check)")
        return
    with open(COUNTRIES, encoding="utf-8") as f:
        known = {row["country_code"] for row in csv.DictReader(f)}
    with open(raw, encoding="utf-8") as f:
        new = {row["country_code"] for row in csv.DictReader(f)} - known
    if new:
        sys.exit(f"Country codes in this release but not in {COUNTRIES}: "
                 f"{sorted(new, key=int)}. Add them to the reference table first.")
    print(f"  country codes: all {len(known)} known codes match {COUNTRIES}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python loaders/baci_load.py data/raw/baci/<snapshot-date>")
    main(sys.argv[1])
