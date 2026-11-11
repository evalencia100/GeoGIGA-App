# Meta-card: how the data sources relate

> This file maps the atlas's sources: where they come from, the keys they share, which questions each one answers, and where they overlap or disagree.
> Each source has its own card. This card holds only what sits *between* cards.
> Draft v0.3 · 2026-11-11

## 1. Lineage: who feeds whom

```
National customs authorities
        │  (declarations, CIF imports / FOB exports)
        ▼
UN Comtrade (UNSD) ── raw reported flows, monthly + annual, two figures per flow
        │
        │  CEPII reconciliation: CIF→FOB, weighting by reporter reliability
        ▼
BACI (CEPII) ── one FOB figure per flow, annual, mirror-filled for non-reporters
        │
        ├── + Kiel product classification (groups HS codes into topics)
        └── + atlas regions.yaml / North–South list (groups countries)
```

**What this means in practice:** BACI and Comtrade are **not independent evidence**. If both show the same thing, that is one source agreeing with itself after processing, not a confirmation. Where they *disagree*, the difference comes from CEPII's processing (valuation, reliability weights, mirror filling), and that difference can itself be a finding.

Development finance (topic 02) has a separate lineage. OECD CRS is donor-reported. AidData GCDF is compiled by researchers from many sources, for lenders that do not report to the OECD. They overlap in subject but not in method. Those cards will hold the detail.

**One consequence already worth recording:** the CRS covers providers who report to the DAC. It excludes aid from non-DAC bilateral providers, which is why China is largely absent (hence AidData) and why there is no East German provider in any German series.

## 2. Shared keys and reference tables

| Key | Reference file | Used by | Notes |
|---|---|---|---|
| Comtrade country code (numeric) | `reference/country-codes.md` | BACI, Comtrade | Not ISO numeric for France 251, Norway 579, India 699, Switzerland 757, USA 842; Taiwan = 490 |
| ISO3 | `reference/country-codes.md` → atlas country table | Everything else (CRS, AidData, V-Dem, World Bank, geometries) | The bridge between trade data and all other data. Not unique inside BACI (BEL, DEU, SDN). |
| HS 6-digit | `reference/hs-products.md` | BACI, Comtrade, Kiel | Codes are tied to a revision, and the same code can differ between revisions |
| HS national 8–10 digit | — | Comtrade only (tariff-line data) | BACI does not go below 6 digits |
| CRS recipient code | `oecd-crs.md` §3, §6 | OECD CRS | ISO3 for countries, so it joins the atlas table directly — **but** the same dimension also holds region and "unspecified" codes that are not countries and must be filtered and reported |
| CRS channel of delivery | `oecd-crs.md` §3.2 | OECD CRS | Hybrid list: broad categories (10000, 20000, 40000, 51000…) and named organisations in one code list. An organisation can change parent category while keeping its code. |
| Region / grouping | `regions/regions.yaml`; North–South = `global_south` column in `reference/countries.csv` | All topic pages | Defined once, used by every source |
| Map geometry | `reference/geo/world_countries.geojson`, `reference/geo/world_grid.json` | All map charts | Joined on ISO3/ISO2, never on numeric codes. No Taiwan or Hong Kong yet. |

**Rule:** a country grouping is defined **once**, by ISO3, in the atlas's own files. Scripts never type lists of country names or call `countrycode()` to get trade codes. That is how France and the USA silently drop out of groupings (see BACI card §3.2).

## 3. Division of labour: trade

| Question | Use | Why |
|---|---|---|
| Long-run structure: who depends on whom, concentration, North/South, 1995 onwards | **BACI** | Complete, consistent, one figure per flow, covers non-reporters |
| Recent months, "what happened since sanctions / export controls" | **UN Comtrade** | Monthly, published sooner |
| What a particular government *declared* | **UN Comtrade** | Raw declarations, not reconciled |
| Detail finer than HS6, mode of transport, re-exports separately | **UN Comtrade** | BACI doesn't have these |
| Which countries report at all, and when | **UN Comtrade** (availability endpoint) | Coverage depends on who files what |
| Unit values (price per tonne) over time | **BACI** | Reconciliation makes unit values cleaner |

**Working rule (Eduardo, 2026-11-03):** BACI for large trends, Comtrade for detailed and recent questions.

## 4. How data is accessed, and the browser question

| Source | Access | Key needed | Where the call happens |
|---|---|---|---|
| BACI | Bulk zip, scripted (`loaders/baci_download.py`) | No | Python loader, once per release |
| UN Comtrade | API | Yes (free key: 500 calls/day, 100k records/call) | **To decide.** See below. |
| OECD CRS | SDMX REST API (`sdmx.oecd.org`), plus bulk text files for pre-1995 | **No** | Python loader for anything published; browser `fetch` is fine for Eduardo's own exploration, because no key is involved. Broad queries are refused, so requests must be chunked. |
| Eurostat FDI | Statistics API (JSON-stat), plus bulk TSV/SDMX files | **No** | Browser `fetch` in principle; **the API was down for a full day on 2026-11-11**, so the loader should prefer the file download. |
| OECD FDI | SDMX, v2 **named** component filters (`c[COUNTERPART_AREA]=TUN`) | **No** | Verified working from an observablehq.com notebook. Filter on the counterpart only and select reporters client-side. |
| V-Dem, World Bank | API / download | Mostly no | Currently called inside Eduardo's observablehq.com notebooks |

**The Comtrade-in-the-browser question.** Eduardo would like to call the Comtrade API from the notebook, as he already does for V-Dem, OECD and the World Bank. Two things are different about Comtrade:
1. **It needs a key.** Code that runs in a reader's browser is visible to the reader, so the key would be published, which breaks CLAUDE.md rule 7. V-Dem, OECD and the World Bank need no key, so for them this problem does not arise.
2. **The daily limit is shared.** Every visitor's page view would spend calls from the same 500/day.

CLAUDE.md rule 4 ("nothing fetched at page-view time") was written for these reasons.

**Observable's own answer, "Secrets", only half helps.** On observablehq.com you can store the key as a workspace secret and read it with `Secret("COMTRADE_KEY")`. This only works in **private** notebooks: as soon as a notebook is shared or published, any cell using `Secret` errors. Notebook Kit has no `Secret()`; the equivalent there is an environment variable read by a data loader at build time.

Whether Comtrade's API accepts calls made from a browser (CORS) is **not yet verified**. Test it once in a private notebook before relying on it.

**Recommendation:** write the Comtrade call **in JavaScript, as a Notebook Kit data loader**. It looks almost like the notebook code Eduardo is used to, but it runs once at build time, with the key read from an environment variable, and the result is saved as a file. Readers get a fast page, and the key and the quota stay private. Interactive exploration in an observablehq.com notebook, with Eduardo's own key, stays fine for *his own* research, as long as that notebook is never published.

**The CRS is the easy case, and now verified.** No key, no quota, and cross-origin browser calls work — confirmed against dataflow 1.7 on 2026-11-10 — so exploration needs no special arrangement. Rule 4 still applies to anything that reaches a page: the loader fetches, Parquet is what the notebook reads.

## 5. Known overlaps and contradictions to write about
- **BACI compared with Comtrade:** the size of the reconciliation adjustment, by country. Large gaps show where national reporting is weak.
- **OECD CRS compared with AidData:** to be filled in when the AidData card exists. The question to answer first: what AidData counts that the CRS cannot (non-DAC lenders, above all China), and whether the two can be shown on one chart without implying they were measured the same way.
- **OECD CRS compared with IATI:** same code lists for flow type, finance type, aid type and recipient, and a direct activity link through the CRS identifier — so IATI can add timing and some sub-national detail to a CRS activity. Worth a card of its own if topic 02 needs it.
- **Eurostat FDI compared with OECD FDI:** not independent evidence — both rest largely on the same
  national balance-of-payments returns. They differ in benchmark (BPM6 presentation versus BMD4),
  activity classification (NACE versus ISIC) and, decisively, in who reports: OECD membership is not
  EU membership, so Bulgaria, Croatia, Cyprus, Malta and Romania are missing from the OECD tables.
  One source per chart, named in the footer. Where they disagree, the explanation is compilation
  practice, and OECD's metadata dataflow is where it is written down.
- **Bilateral reporting compared with total effort:** a provider's CRS series excludes its share of EU Institutions spending, which is reported by the EU as its own provider. Any "how much does Germany give country X" chart has to say which of the two it is.

## 6. Card index

| Card | Source | Kind | Status |
|---|---|---|---|
| `baci-cepii.md` | BACI, CEPII | aggregate | v1.0 |
| `un-comtrade.md` | UN Comtrade | primary (compiled official declarations) | to write |
| `oecd-crs.md` | OECD CRS | primary | **v0.2 draft** — API recipe verified in use; data-level facts not yet |
| `aiddata-gcdf.md` | AidData GCDF | primary | to write |
| `eurostat-fdi.md` | Eurostat FDI (BPM6) | primary | **v0.2 draft** — API was down on first use; no data yet |
| `oecd-fdi.md` | OECD FDI (BMD4) | primary | **v0.1 draft** — first extract verified 2026-11-11 |
| `kiel-classification.md` | Kiel product classification | classification (not data) | to write |
