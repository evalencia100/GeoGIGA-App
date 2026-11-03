"""
templates/baci_question.py
---------------------------------------------------------------------------
Template: answer ONE question with BACI and save ONE small table for a chart.

How to use
  1. Copy this file into src/working/ (or anywhere) and give it the chart id
     as its name, e.g.  01-cobalt-supplier-concentration.py
  2. Change only the four blocks marked CHANGE.
  3. Run it from the repository root:   python path/to/your_copy.py

It reads the Parquet written by loaders/baci_load.py, never the raw CSVs,
so it takes seconds, not minutes.
Needs: duckdb   (pip install -r requirements.txt)
"""

from pathlib import Path

import duckdb

# ── CHANGE 1: the question, in one sentence (goes into the output header) ───
QUESTION = "Who trades with whom, North and South, 2000-2024?"

# ── CHANGE 2: HS revision and years ────────────────────────────────────────
HS = 92              # 92 for long series (1995-), 22 for modern products (2022-)
YEARS = (2023, 2024)

# ── CHANGE 3: products (HS6 codes, as text, in the SAME revision as HS) ────
# None means all products. Look codes up in reference/hs/, don't guess them.
PRODUCTS = ["260500"]

# ── CHANGE 4: how to group countries ───────────────────────────────────────
# Either a column of reference/countries.csv ("global_south") ...
GROUP_BY = None
# ... or your own groups, by ISO3 (set GROUP_BY = None to use these).
# Everyone not listed becomes "Others".
GROUPS = {
    "China": ["CHN"],
    "United States": ["USA"],
    "European Union": ["AUT", "BEL", "BGR", "HRV", "CYP", "CZE", "DNK", "EST",
                       "FIN", "FRA", "DEU", "GRC", "HUN", "IRL", "ITA", "LVA",
                       "LTU", "LUX", "MLT", "NLD", "POL", "PRT", "ROU", "SVK",
                       "SVN", "ESP", "SWE"],
}

OUTPUT = Path("data/working/north-south-trade.csv")   # name it after the chart id

# ───────────────────────────────────────────────────────────────────────────
# Nothing below needs changing.

con = duckdb.connect()

# Country -> group lookup, keyed on the BACI code. Groups are defined by ISO3
# (atlas_iso3), never by numeric code: BACI's numbers differ from ISO for
# France, the USA, India, Norway and Switzerland, and Sudan changed code in 2012.
con.execute("""
    CREATE TABLE countries AS
    SELECT * FROM read_csv('reference/countries.csv', all_varchar = true)
""")
if GROUP_BY == "global_south":
    con.execute("""
        CREATE TABLE code_group AS
        SELECT CAST(country_code AS INTEGER) AS code,
               CASE global_south WHEN 'yes' THEN 'Global South'
                                 WHEN 'no'  THEN 'Global North'
                                 ELSE 'Unassigned' END AS grp
        FROM countries
    """)
elif GROUP_BY:
    con.execute(f"""
        CREATE TABLE code_group AS
        SELECT CAST(country_code AS INTEGER) AS code,
               coalesce({GROUP_BY}, 'Unassigned') AS grp
        FROM countries
    """)
else:
    pairs = [(iso, name) for name, isos in GROUPS.items() for iso in isos]
    con.execute("CREATE TABLE groups (atlas_iso3 VARCHAR, grp VARCHAR)")
    con.executemany("INSERT INTO groups VALUES (?, ?)", pairs)
    con.execute("""
        CREATE TABLE code_group AS
        SELECT CAST(c.country_code AS INTEGER) AS code,
               coalesce(g.grp, 'Others') AS grp
        FROM countries c LEFT JOIN groups g USING (atlas_iso3)
    """)

product_filter = ""
if PRODUCTS:
    codes = ", ".join(f"'{p}'" for p in PRODUCTS)
    product_filter = f"AND f.k IN ({codes})"

# Tonnes are only meaningful for a single product.
tonnes = "sum(f.q)" if PRODUCTS and len(PRODUCTS) == 1 else "NULL"

result = con.execute(f"""
    SELECT f.t                                AS year,
           coalesce(ge.grp, 'Unmatched')      AS exporter,
           coalesce(gi.grp, 'Unmatched')      AS importer,
           round(sum(f.v) / 1e6, 3)           AS value_usd_bn,  -- v is thousands of USD
           {tonnes}                           AS tonnes
    FROM read_parquet('data/baci/*/*/*.parquet', hive_partitioning = true) f
    LEFT JOIN code_group ge ON f.i = ge.code
    LEFT JOIN code_group gi ON f.j = gi.code
    WHERE f.hs_rev = {HS} AND f.t BETWEEN {YEARS[0]} AND {YEARS[1]} {product_filter}
    GROUP BY ALL
    ORDER BY ALL
""").df()

# Checks before saving
if (result[["exporter", "importer"]] == "Unmatched").any().any():
    raise SystemExit("Some BACI codes are missing from reference/countries.csv.")
latest = result["year"].max()
print(f"{QUESTION}\nHS{HS}, {YEARS[0]}-{YEARS[1]}. Note: {latest} is provisional "
      f"if it is the latest BACI year (asterisk it).")
print(result.head(12).to_string(index=False))

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
result.to_csv(OUTPUT, index=False)
print(f"Saved {len(result)} rows to {OUTPUT}")
