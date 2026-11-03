# Data card: BACI (CEPII)

> **Status:** **v1.0, concluded** 2026-11-03 · describes release **V202601** (22 Jan 2026), revisions **HS92** and **HS22**. From here on it improves through use: add to §11 whenever a chart teaches us something.
> **Purpose:** a self-contained reference, so nobody has to reopen the CEPII pages or the zip readme. It describes the dataset *in general*, not any one chart.
> **Atlas status:** not promoted. Promotion to `registry/sources.yaml` is Eduardo's call.
> **Related files:** `reference/country-codes.md` (all 238 codes) · `reference/hs-products.md` (HS structure, HS92 compared with HS22, concordance) · `source-update-calendar.md` · `_relationships.md` (BACI ↔ Comtrade and other sources)
> **In the repository:** `loaders/baci_download.py` (download + unzip) · `loaders/baci_load.py` (CSV → Parquet) · `templates/baci_question.py` (one question → one table) · `reference/countries.csv` (the country table) · `reference/hs/` (code lists, concordances) · `reference/geo/` (world map, grid map)

---

## 1. At a glance

| Attribute | Value |
|---|---|
| Full name | BACI: Base pour l'Analyse du Commerce International |
| Publisher | CEPII (Paris). Contact: baci@cepii.fr. Report issues with the version and HS revision. |
| Homepage | http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37 |
| What it measures | Annual bilateral **merchandise (goods)** trade, by product |
| Unit of observation | One row = year × exporter × importer × product (HS 6-digit) |
| Source kind (atlas) | **aggregate**: it harmonises UN Comtrade and does not observe trade itself |
| Upstream | UN Comtrade (see `_relationships.md`) |
| Countries | ~200 (238 codes including historical and "n.e.s." entities) |
| Products | HS92: 5,022 codes · HS22: 5,609 codes |
| Revisions held | **HS92 (1995–2024)** for long series · **HS22 (2022–2024)** for modern product detail |
| Frequency | Annual only |
| Update cadence | Once a year, in **January**. Next: V202701, late January 2027 (see calendar). |
| Publication lag | About 13 months (the January 2026 release ends at 2024) |
| Latest year | **Provisional**, and can be revised substantially, which earns the atlas asterisk |
| Free? | **Yes.** No registration and no fee. |
| Licence | Etalab Open Licence 2.0. Any use is allowed if "BACI, CEPII" is credited, ideally with a link. |
| Public API? | **No.** Bulk zip per HS revision, at a predictable address (`https://www.cepii.fr/DATA_DOWNLOAD/baci/data/BACI_HS{rev}_V{version}.zip`), so download is scripted: `python loaders/baci_download.py --load`. |
| Geocoded? | **No.** Country level only (§6). |
| Format | CSV (comma, dot decimal), one file per year, plus country and product metadata CSVs and a readme |
| Size | On the order of 10 million rows per year file and several GB per revision. **Too big for Excel.** |
| Citation | Gaulier, G. and Zignago, S. (2010). *BACI: International Trade Database at the Product-Level. The 1994-2007 Version.* CEPII Working Paper N°2010-23. |
| Proposed fetch class | `manual` |
| Proposed change check | Version string (`V2027xx`) on the CEPII download page |

### Files in a release
`BACI_HS{rev}_Y{year}_V{version}.csv` (one per year) · `country_codes_V{version}.csv` · `product_codes_HS{rev}_V{version}.csv` · `Readme.txt`.
The version is `YYYYMM` of the release (`202601` = January 2026). Revisions available: HS92, 96, 02, 07, 12, 17, 22. Each starts in its own first year and all run to 2024.

---

## 2. Known pitfalls: check these every time

These were found by checking the actual files. **The CEPII documentation does not mention any of them.**

| # | Pitfall | What goes wrong | Fix |
|---|---|---|---|
| 1 | **Namibia's ISO2 is `NA`** | R reads it as missing, so Namibia drops out of joins | Read the metadata with `na = character()` |
| 2 | **ISO3 is not unique** (BEL, DEU, SDN appear twice) | A join on ISO3 duplicates rows | Join on `country_code` first |
| 3 | **Codes ≠ ISO numeric**: France 251, Norway 579, India 699, Switzerland 757, USA 842 | `countrycode(…, "iso3n")` returns 250 or 840, which match **nothing**, so France and the USA silently vanish from groupings | Never derive trade codes from ISO numeric. Group by `atlas_iso3` in `reference/countries.csv`. |
| 4 | **Sudan changes code**: 736 (to 2011, incl. South Sudan) → 729 + 728 | Filtering on 729 loses Sudan before 2012 | Filter on both codes, or on ISO3 |
| 5 | **Taiwan only exists as 490** ("Other Asia, nes", ISO3 `S19`) | Semiconductor charts miss or mislabel Taiwan | Recode explicitly (e.g. to TWN), and label it honestly |
| 6 | **Accented names are garbled** (double-encoded UTF-8: "CÃ´te d'Ivoire") | Ugly or wrong labels | Never display BACI names. Use the atlas country table. |
| 7 | **`k` loses leading zeros** if read as a number (347 HS92 codes, 571 HS22 codes) | `010111` becomes `10111` and joins fail | Read `k` as character |
| 8 | **Same HS code, different meaning across revisions** (1,146 shared codes changed description) | HS92 and HS22 joined on code give wrong series | Never join revisions on the code. Use a concordance. |
| 9 | **Only positive flows stored** | A missing row means "zero or not reported", and you cannot tell which | See §7 point 4 |
| 10 | **`v` is in thousands of USD** | Charts off by a factor of 1,000 | Rescale before labelling |
| 11 | **Versions must not be mixed** | Past flows are revised between releases | One version per chart, and say which |

---

## 3. Columns: what they are and are not

| Col | Meaning | Read as | Is | Is **not** |
|---|---|---|---|---|
| `t` | Year of the trade | integer | Calendar year | Not the release year |
| `i` | Exporter | integer | Comtrade numeric code | Not always ISO numeric. Not ISO3. Not a name. |
| `j` | Importer | integer | Same list as `i` | Same as `i` |
| `k` | Product | **character (6)** | HS6 code **in that file's revision** | Never numeric. Not comparable across revisions. |
| `v` | Value | double | **Thousands** of **current** USD, **FOB** | Not plain USD, not deflated, not CIF, not what either country reported (it is a reconciled estimate) |
| `q` | Quantity | double, can be missing | **Metric tonnes** | Not pieces or units. Only adds sensibly within one product. |

Country codes: `reference/country-codes.md` has all 238 rows, with status (current, historical or nes) and notes.
Product codes: `reference/hs-products.md` has the structure, chapter list, HS92 vs HS22 comparison and topic-relevant codes.

---

## 4. What BACI does not contain (at least not directly)

| Not in BACI | Consequence for the atlas | Where else to look |
|---|---|---|
| **Shipping routes, transit, chokepoints** | It knows origin and destination, not whether goods passed Hormuz, Suez or Malacca | AIS or shipping data, modelled routing |
| Monthly or quarterly data, recent months | Cannot show the effect of last quarter's sanctions | UN Comtrade (monthly) |
| National tariff lines (8–10 digit) | No detail below HS6 (e.g. specific chip grades) | UN Comtrade tariff-line data |
| Mode of transport, customs procedure | — | UN Comtrade |
| Re-exports and re-imports as separate flows | Entrepôts look like producers (§5.3) | UN Comtrade |
| The original declarations | Cannot see what a government itself claimed | UN Comtrade |
| Services trade | No digital services, finance, tourism | Comtrade services, WTO/OECD BaTIS |
| Ownership, investment, firms | Cannot say *who owns* the mine or factory | FDI data, AidData, firm data |
| Value added / origin of content | A phone "from China" contains Korean chips | OECD TiVA |
| Informal trade, smuggling | Large for gold and some minerals in Africa | Specialist sources |
| Confidential or suppressed flows | Some countries hide sensitive products (arms, some minerals), which end up in residual codes or go missing | — (note it in the prose) |
| Arms trade beyond what customs record | HS chapter 93 exists, but most military transfers are not in customs data | SIPRI |
| Per-observation flags | The only systematic flag is "latest year is provisional" | — |

---

## 5. Methodology, and how it differs from UN Comtrade

### 5.1 The problem
In Comtrade a flow can exist twice: A reports an export to B, and B reports an import from A. The two figures almost never match, because of valuation (imports are **CIF**: the value at the importer's border, including freight and insurance; exports are **FOB**: the value at the exporter's border) and because of errors (unknown final destination, different classification, timing).

### 5.2 The reconciliation
1. **CIF → FOB.** The transport and insurance margin is estimated with a gravity-type regression (distance, contiguity, landlockedness, year effects, the product's world median unit value) and removed from import declarations.
2. **Reporter reliability.** Each country's usual distance from its partners' mirror declarations is measured, controlling for its product and geographic mix. More reliable reporters get more weight when the two figures are averaged.

The result is **one FOB value per flow**, cleaner unit values, and coverage of non-reporters through their partners.

### 5.3 What counts as trade: characteristics inherited from Comtrade
These are **characteristics, not errors**. Name them in a chart note when they matter.
- **Entrepôt and re-export effect.** Hong Kong, Singapore, the Netherlands, Belgium and the UAE appear as large "suppliers" of goods made elsewhere. Comtrade records re-exports separately; BACI does not.
- **Origin and destination are asymmetric.** Importers record the country of *origin*, while exporters record the *last known destination*.
- **General compared with special trade system.** Countries differ in whether goods entering free zones or customs warehouses count as trade. BACI inherits each reporter's choice.
- **Nominal values.** Current USD, so long series mix volume, price and exchange-rate effects. Commodity series are dominated by prices.

### 5.4 Choosing between BACI and Comtrade
**Working rule:** BACI for large trends; UN Comtrade for detailed and recent questions (monthly, raw declarations, tariff lines, transport mode). Comtrade's coverage depends on which countries file what and when. Full comparison and the API question: `_relationships.md`. Comtrade gets its own card.

---

## 6. Spatial attributes

| Question | Answer |
|---|---|
| Geocoded? | **No.** The smallest unit is the country (customs territory). |
| Coordinates | None. Flow maps need centroids from elsewhere (e.g. Natural Earth). |
| Join to geometry | `country_code` → `atlas_iso3` (via `reference/countries.csv`) → map. Watch pitfalls 2–5. |
| Maps in the repo | `reference/geo/world_countries.geojson` (Natural Earth country shapes, 195 features, plus 28 small states as points) and `reference/geo/world_grid.json` (one tile per country, 197 tiles, small states included). `countries.csv` says which BACI entities each map can draw. **Neither has Taiwan or Hong Kong.** |
| Entities without geometry | 490 (map it to Taiwan, with labelling), 697, 711, "nes" residuals, historical entities |
| Suitable | Choropleths (exports, imports, shares), country-to-country flow maps, small multiples by year |
| Not suitable | Point maps, ports, routes or chokepoints, sub-national maps |

---

## 7. What matters for visualisation

1. **Rescale `v`** to "US$ bn" or "US$ m". Never label the raw value.
2. **Nominal dollars** (§5.3). For commodities, consider showing tonnes (`q`) beside value.
3. **What adds up:** `v` adds across anything; `q` adds only within one product; unit values (`v/q`) mean something only within one HS6 code.
4. **Absence ≠ zero ≠ gap.** Proposed rule (to confirm): a missing *bilateral flow* counts as zero in totals and shares, while a *whole country-year* with no data is shown as a gap.
5. **Asterisk on the latest year** (2024 in V202601). It moves every January.
6. **One version and one HS revision per chart.** Both appear in the source line and citation.
7. **Concentration measures fit well**: top-N supplier shares, Herfindahl–Hirschman index (HHI), world-export shares.
8. **HS codes need a grouping layer** for human-readable labels (Kiel classification, BEC, or hand-curated lists). Name that layer in the source line.
9. **Taiwan** (code 490) is labelled explicitly, always.
10. **Volume shapes the architecture:** loader → Parquet → DuckDB. No raw BACI in the browser. CSV exports are the aggregated table behind each chart.

---

## 8. Wrangling: three scripts, in Python

| Step | When | Command | What it does |
|---|---|---|---|
| Download | Once per release (late January) | `python loaders/baci_download.py` | Finds the newest version on the CEPII page, downloads the HS92 and HS22 zips into `data/raw/baci/<today>/`, unzips them, writes `manifest.json` (URLs, checksums, date) |
| Load | Right after download (or add `--load` to the line above) | `python loaders/baci_load.py data/raw/baci/<date>` | Reads every year file as text, converts types on purpose, checks (year in file = year in name, 6-character codes, readable values), writes Parquet to `data/baci/hs_rev=92/t=2024/`. Stops if the release has a country code missing from `reference/countries.csv`. |
| Question | Every chart | copy `templates/baci_question.py`, change 4 blocks, run it | Groups countries by ISO3 (or by the Global South column), filters revision, years and products, sums to US$ bn, saves one CSV named after the chart id |

Rules built into the scripts (each one is a bug from the old Rmd):
- Year, revision and version come from **file names**, never from the order of a list.
- `k` stays text; padded `NA` in `q` becomes missing; mixing versions is refused.
- Groups are defined by `atlas_iso3`, never by numeric code, so France, the USA and pre-2012 Sudan are always included.
- Tonnes are only summed for a single product.
- A BACI code that is not in the country table makes the question script stop instead of silently dropping trade.

All three scripts were tested on synthetic files that copy BACI's format (including padded `NA` and leading zeros). The first real download is the remaining test. Packages: `duckdb`, `pandas` (`requirements.txt`).

---

## 9. Derived tables seen so far

### `global_south_north_trade.csv`
- Made by `ceprii_wrangling_GS_GN_trade.Rmd` (Eduardo, local script) from **BACI V202601, HS92**.
- Columns `year, i, j, q, v`. `i` and `j` are aggregated to Global North / Global South, giving 4 rows per year, **2000–2023**.
- **Definition of South:** `reference/groupings/global_south_UN.csv` (UNCTAD-based, compiled by Eduardo; vintage not recorded), now the `global_south` column of `reference/countries.csv`. It uses **BACI codes** (251, 842…), so the join in the old script was correct.
- **Caveat:** the list marks 490 "Chinese Taipei" as North but 158 "Taiwan Province of China" as South. BACI only uses 490, so Taiwan counted as **North** in this table. 58, 697 and 711 are not in the list.
- 2024 is not included. In the script as it stands, 25 files are named with 24 years (`2000:2023`), so the 2024 file would get the year `NA`. The CSV was probably produced before 2024 was added to the file list.
- Units: `v` in thousands of USD (2023 world total ≈ US$ 22.6 trillion); `q` in tonnes summed over all products.
- At a glance: South→South value grew from US$ 0.58 trillion (2000) to US$ 4.9 trillion (2023), now about equal to South→North; South→South tonnage is now the largest of the four flows.

---

## 10. Decisions still open (they do not block use)

- [ ] Zero-versus-gap rule (§7 point 4): proposed, not yet confirmed.
- [ ] Taiwan in the North/South split: North (as the list says for 490) or South (as UNCTAD says for 158)?
- [ ] Topic product baskets (`reference/hs/baskets/`): written per topic, when that topic is built.
- [ ] Add Taiwan and Hong Kong to the maps.

---

## 11. Learned through use

*Add a dated line whenever a chart or question teaches something about BACI that belongs here.*

- 2026-11-03: the old North/South Rmd showed three silent failures (ISO-numeric groupings, list-position years, a missing Sudan code). All three are now prevented by the scripts in §8.
