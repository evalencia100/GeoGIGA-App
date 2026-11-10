# Data card: OECD CRS (Creditor Reporting System)

> **Status:** **v0.2, draft** 2026-11-10. **The request recipe in §8 is verified in use** — it ran
> successfully against the live API on 2026-11-10. The *data-level* facts are not: anything marked
> *to verify* is still a reading of the documentation, not an observation. The card becomes v1.0 when the
> diagnostics listed at the end of §9 are pasted in.
> **Purpose:** a self-contained reference, so nobody has to reopen the OECD Data Explorer or the DAC
> reporting directives. It describes the dataset *in general*, not any one chart, and §8 describes the API
> independently of the language calling it.
> **Atlas status:** not promoted; not yet on the shelf either. Promotion to `registry/sources.yaml` is
> Eduardo's call.
> **Related files:** `_relationships.md` (CRS ↔ AidData ↔ IATI) · `source-update-calendar.md` ·
> `reference/country-codes.md` (the atlas country table is the bridge: CRS uses ISO3)
> **In the repository:** nothing yet. Planned: `loaders/crs_download.py`, `loaders/crs_load.py`,
> `templates/crs_question.py`.
> **Name collision, before anything else:** in OECD development statistics *CRS* is the **Creditor
> Reporting System**. In OECD tax work *CRS* is the **Common Reporting Standard**, an unrelated
> bank-account information exchange. Half of a naive web search for "OECD CRS 2026" returns the tax one.

---

## 1. At a glance

| Attribute | Value |
|---|---|
| Full name | Creditor Reporting System (CRS), activity-level aid statistics. In the Data Explorer: "CRS: Creditor Reporting System (flows)" |
| Publisher | OECD Development Co-operation Directorate (DCD), for the Development Assistance Committee (DAC) |
| Homepage | https://data-explorer.oecd.org (Development → ODA → Flows on individual projects) |
| What it measures | Development finance **activity by activity**: ODA, other official flows and some private flows, from each reporting provider to each recipient, with sector, channel, aid modality and project text |
| Unit of observation | **One row = one observation**, not one project: activity × year × flow type × measure × price base × unit. One project produces many rows. See pitfall 9. |
| Source kind (atlas) | **primary** — providers report their own activities against agreed definitions; the OECD validates but does not re-observe |
| Who reports | DAC member countries, multilateral agencies, a growing number of non-DAC providers voluntarily, and (in a separate dataflow) large private foundations |
| Countries | All recipients on the DAC List of ODA Recipients, **plus regional and "unspecified" recipient codes** that are not countries (pitfall 6) |
| Time span | Aggregate DAC data from **1960**; activity-level CRS from **1973** |
| Usable span | Considered **complete from 1995 for commitments and 2002 for disbursements**. The OECD states that the Data Explorer carries commitments from 1995 and disbursements from 2002, and that earlier data exist only as downloads, with gaps for some providers and years. |
| Frequency | Annual, calendar year |
| Update cadence | Annual, published in **December** for the previous year's flows. Preliminary *aggregate* ODA (not CRS) appears each **April**. |
| Latest full year | **2024** *(to verify)*; 2025 flows expected December 2026 |
| Revisions | Providers resubmit. Past years change between releases, so a vintage must be recorded per chart. |
| Free? | **Yes.** No registration, no key, no quota published. |
| Licence | OECD Terms and Conditions. OECD content published from 1 July 2024 is generally CC BY 4.0; data may carry further restrictions, so attribute explicitly and give the extraction date. |
| Public API? | **Yes**, SDMX REST, no key. Verified working 2026-11-10, including **from a browser** — the endpoint allows cross-origin requests, so a notebook can call it directly with no proxy and no key. Full recipe in §8. |
| Geocoded? | **No.** Recipient country or region only (§6). |
| Format | SDMX: `csvfilewithlabels`, `csvfile`, JSON, XML. The CSV comes back as a **file attachment**, which matters for tooling (§8.5). |
| Size | Large. Broad queries are refused rather than truncated; chunk them (§8.3). |
| Citation | OECD (2026), *Creditor Reporting System (CRS)*, OECD Data Explorer, dataflow `DSD_CRS@DF_CRS` v1.7, extracted YYYY-MM-DD. |
| Proposed fetch class | `open` (no key), but still fetched deliberately by a loader, never at page-view time |
| Proposed change check | Dataflow version string and the "Last updated" timestamp shown in the Data Explorer for `OECD.DCD.FSD:DSD_CRS@DF_CRS` |

### Sibling dataflows, same agency
Pick deliberately; they answer different questions.

| Dataflow | What it is | When to use it |
|---|---|---|
| `DSD_CRS@DF_CRS` | CRS on a **flow** basis (commitments, disbursements) | Activity-level work; this card |
| `DSD_GREQ@DF_CRS_GREQ` | CRS on a **grant-equivalent** basis | When the number must line up with headline ODA since 2018 (pitfall 13) |
| `DSD_MULTI@DF_MULTI` | Providers' total use of the multilateral system | Core plus earmarked multilateral funding. Published from **2011** data onwards; activity-level multilateral data are incomplete before that. |
| `DSD_CRS@DF_PSI` *(name to verify)* | Private sector instruments | Equity, guarantees, mezzanine |
| Private Philanthropy for Development | ~40 large foundations | Gates, etc.; not official flows |
| CRS – Private: mobilised private finance | Amounts mobilised from the private sector | Leveraging questions |

---

## 2. Known pitfalls: check these every time

Numbers 1–5 and 9 are the ones that silently produce a wrong total.

| # | Pitfall | What goes wrong | Fix |
|---|---|---|---|
| 1 | **MEASURE holds aggregates and their components in one dimension.** `100` is "Official Development Assistance"; the grant, loan and equity codes sit under it. | Leaving MEASURE blank returns the parent *and* the children. Summing gives roughly double the truth. | Pin a measure code, or group by measure and never add two levels together. Print the measure inventory before trusting any total, and run the parent test in §8.6. |
| 2 | **SECTOR likewise mixes levels** — 3-digit DAC categories and 5-digit CRS purpose codes, plus a total *(to verify which codes are which level)*. | Same double count, by sector. | Pin the level you want; check that sector sums equal the pinned-measure total. |
| 3 | **FLOW_TYPE: `D` = disbursements, `C` = commitments.** | Summing across flow type adds money promised to money paid. The two are not comparable in the same year — a disbursement often belongs to a commitment from an earlier year. | Pin one. Say which in the chart source line. |
| 4 | **PRICE_BASE: `V` = current, `Q` = constant.** | Mixing them adds dollars from different price bases. | Pin one; for constant prices, state the base year in the footer. |
| 5 | **MD_DIM: `DD` = activity detail, `_T` = aggregate.** | Blank mixes aggregate rows with the detailed rows they summarise. | `DD` for activity-level work, always. |
| 6 | **Recipient codes include regions and "unspecified"** (e.g. "Africa, regional", "Bilateral, unspecified"). | They cannot be drawn as a country and they are not a country total. Mapping them silently drops money; summing them with countries double counts. | Filter to the ISO3 country list explicitly, and **report the excluded share** rather than hiding it. |
| 7 | **UNIT_MULT is not 0.** Expect 6 (millions). | Amounts wrong by a factor of a million. | Always `OBS_VALUE × 10^UNIT_MULT`. Never hardcode the multiplier. |
| 8 | **Channel and modality detail only exist for recent years.** The aid-typology (modality) codes arrived with the **2010** typology; channel-of-delivery coding was recommended well before that but is only usable systematically from around 2010–2011 *(start year to verify)*. | "Aid through German NGOs since 1973" cannot be answered from CRS. A share computed over the whole period silently means "share of the years that have channel data". | Compute channel shares only over years with channel coverage, and show the pre-coverage years as a gap. |
| 9 | **One project = many rows**, and row counts are not project counts. | "Number of activities" inflated several-fold. | Count distinct activity ids. Note that id stability across years is **to verify** per provider. |
| 10 | **"Donor" is the reporting provider, not the origin of the money.** German contributions to the EU budget appear under **EU Institutions**, not Germany. | A "German flows to Tunisia" chart built on DONOR=DEU excludes the German share of EU spending — a large omission in North Africa. | Say in the prose that the series is German bilateral reporting only. If total German effort is the question, EU Institutions and multilateral imputations are separate work. |
| 11 | **A channel organisation can change parent category while keeping its channel code** (stated in the CRS reporting checklist). | Category membership is not stable over time, so a channel-category time series can move for coding reasons. | Classify from the detailed code *and* keep the parent as reported; do not re-derive history. |
| 12 | **Pre-1995 data are thin or absent through the API** although the series starts in 1973. | Chunked requests for the 1970s and 1980s may come back empty, which looks like "no German aid to Tunisia" rather than "not in this interface". | Treat an empty early chunk as *unknown*, not zero. Pre-1995 work needs the bulk text files. |
| 13 | **Flow basis ≠ grant-equivalent basis.** Headline ODA since 2018 is grant-equivalent; this dataflow is flows. | CRS totals will not match the ODA figures in OECD press releases or the DAC tables. | Use `DF_CRS_GREQ` if the number has to match headline ODA, and never mix the two in one chart. |
| 14 | **The dataflow version is pinned in the URL** (`,1.6` or `,1.7`). | A pinned old version can be retired without notice; an unpinned one changes under you. | Pin, and record the version in the chart source line, exactly as BACI's release version is recorded. |
| 15 | **Gross vs net.** Disbursements are usually gross; loan repayments flow back separately. | A long German series to Tunisia, which is loan-heavy (KfW), looks larger than the net transfer. | State "gross disbursements". Net lending is a separate question. |
| 16 | **In-donor costs inflate "bilateral ODA".** Refugee costs in the donor country and imputed student costs count as bilateral ODA (for Germany, 21.6% of gross bilateral ODA in 2024). | Donor-level shares are not comparable with country-allocated aid. | Mostly these sit under unspecified recipients, so a Tunisia-filtered query is largely unaffected — but never quote a Tunisia share of German bilateral ODA without saying which denominator. |

---

## 3. Dimensions and key fields: what they are and are not

### 3.1 The key: eleven dimensions, ten dots

`DSD_CRS@DF_CRS` takes its dimensions in this order. The SDMX key is positional, so an empty position still needs its dot.

| # | Dimension | Example | Is | Is **not** |
|---|---|---|---|---|
| 1 | `DONOR` | `DEU`, `TUR`, `DAC` | The reporting provider: ISO3 for countries, codes for agencies and groups | Not the origin of the funds (pitfall 10) |
| 2 | `RECIPIENT` | `TUN` | ISO3 for countries, **plus** region and "unspecified" codes | Not a clean country list (pitfall 6) |
| 3 | `SECTOR` | `` (all) | CRS purpose codes and DAC sector categories | Not one single level (pitfall 2) |
| 4 | `MEASURE` | `100` | Flow category: ODA and its components | Not the aid modality, not the finance instrument (pitfall 1) |
| 5 | `CHANNEL` | `` (all), `_T` | Channel of delivery: parent category or a specific organisation | Not the contractor, not the extending agency |
| 6 | `MODALITY` | `` (all) | Type of aid (budget support, project, technical co-operation, scholarships, debt relief, core support to NGOs…) | Only populated from the 2010 typology onwards |
| 7 | `FLOW_TYPE` | `D` | `D` disbursements, `C` commitments | Never both at once (pitfall 3) |
| 8 | `PRICE_BASE` | `V` | `V` current, `Q` constant | — |
| 9 | `MD_DIM` | `DD` | Drilldown: `DD` detailed, `_T` aggregate | — |
| 10 | `MD_ID` | `` (all) | Activity identifier within the microdata | — |
| 11 | `UNIT_MEASURE` | `USD` | Currency | Not the multiplier (pitfall 7) |

Time is not part of the key; it goes in `startPeriod` / `endPeriod`.

### 3.2 Channel of delivery: the parent categories

The channel field is hybrid: broad categories **and** named organisations in one code list. Parent categories observed in the DAC code lists:

| Parent | Meaning | Notable children |
|---|---|---|
| 10000 | Public sector | 11000 donor government, 11004 other public entities in donor country, 12000/12004 recipient-country public entities, 13000 third-country government (delegated co-operation) |
| 20000 | NGOs and civil society | **21000 international NGO · 22000 donor country-based NGO · 23000 developing country-based NGO**, plus named NGOs (e.g. 21033 Transparency International) |
| 30000 | Public-private partnerships and networks | — |
| 40000 | Multilateral organisations | 41xxx UN, 43xxx IMF, 44xxx World Bank group, 46xxx regional banks, 47xxx other |
| 51000 | University, college, other teaching institution, research institute or think-tank | — |
| 60000 | Private sector institutions | 61000 provider country, 62000 recipient country, 63000 third country |
| 90000 | Other | — |

**Note the 51000.** Bucketing by `floor(code / 10000) * 10000` puts it in a 50000 bucket that does not exist as a parent code. Harmless as a display bucket, wrong if written back as a code.

### 3.3 Identifying a provider's own NGOs — the method, and its limit

For a query with the donor pinned to one country, **22000 "donor country-based NGO" means an NGO based in that donor country.** With `DONOR=DEU`, channel codes in 22000–22999 are German NGOs. This is structural and defensible.

Three caveats:
1. **23000 is not German** — it is an NGO based in the recipient country.
2. **21000 international NGOs** may be German-founded or German-headquartered and will not appear as 22xxx. A name match on the channel name (Deutsche…, Welthungerhilfe, Misereor, Brot für die Welt, Kindernothilfe, the political foundations: Friedrich-Ebert, Konrad-Adenauer, Heinrich-Böll, Friedrich-Naumann, Hanns-Seidel, Rosa-Luxemburg) catches some. A name match is a **heuristic and must be labelled as one** — keep it separable from the 22xxx test so the two are never reported as one number.
3. **GIZ and KfW are not NGOs.** They are the implementing agency and the development bank, coded in the public sector / multilateral-adjacent space, and they carry the bulk of German bilateral money. Any NGO total that includes them is wrong by an order of magnitude.

Modality helps distinguish *what kind* of NGO funding: **B01** core support to NGOs, other private bodies, PPPs and research institutes, versus earmarked project funding routed through an NGO. For reference, Germany's own 2023 profile reports 2.4% of gross bilateral ODA as core contributions to CSOs and 4.6% channelled through CSOs for donor-initiated projects — so a Tunisia-level German NGO share far above roughly a tenth of the total should be treated as a coding or double-counting error until proven otherwise.

### 3.4 Attributes worth knowing about
Project title, short and long description (free text, provider-written, multilingual in practice), channel name as reported, finance type (grant, standard loan, concessional loan, equity, guarantee), tying status, policy markers (gender, environment, and the Rio markers for climate mitigation, climate adaptation, biodiversity, desertification), DAC/CRS identifiers. The marker columns are the reason the raw CSV has duplicated headings (§8.5).

---

## 4. What the CRS does not contain

| Not in the CRS | Consequence for the atlas | Where else to look |
|---|---|---|
| **Non-DAC lenders' full activity**, China above all | The biggest story in infrastructure finance is largely absent | **AidData GCDF** (its own card) |
| **East German (GDR) aid** | There is no German Democratic Republic provider. The CRS excludes aid from non-DAC bilateral providers, and the GDR never reported. Pre-1990 "Germany" is the Federal Republic alone. | Archival and scholarly work on GDR solidarity aid. Precise figures barely exist even in the secondary literature. |
| Soviet and CMEA aid generally | Cold-war aid competition cannot be shown from this source | Specialist historical datasets |
| **Military aid and arms transfers** | ODA excludes military assistance by definition | SIPRI |
| Geocoordinates, sub-national allocation | No within-country maps | AidData's geocoded datasets; IATI for some providers |
| Transaction-level timing inside a year | Annual only | IATI (provider-dependent) |
| Contractors and tender outcomes | The extending agency and channel are known; who actually held the contract is not systematic | National procurement data |
| Results and outcomes | Money, not effect | Evaluations |
| Private grants from DAC countries (historically excluded) | NGO own-funds are not here | Private Philanthropy dataflow for large foundations |
| Anything about the recipient's own budget | No counterfactual, no fiscal context | IMF, World Bank |

---

## 5. Concepts that have to be right

**Commitments and disbursements** are reported separately and are not alternatives: a commitment is money approved, a disbursement money paid. Because disbursement follows commitment by years, the two series cannot be compared within a year, and a rise in commitments shows up in disbursements only with a lag.

**Completeness is graded, not binary.** The DAC publishes coverage ratios; commitments are more complete than disbursements; coverage improves over time. The practical boundaries: 1995 for commitments, 2002 for disbursements, and the conventional advice not to analyse disbursements before 2002.

**The aggregates will not match.** The OECD itself notes that for historical data, totals in the DAC tables and in the CRS do not always agree. The DAC tables come from a different questionnaire; the CRS is activity-level. Do not present one as a check on the other.

**ODA changed basis in 2018.** Headline ODA is now grant-equivalent; the CRS flow dataflow is cash flows. Pitfall 13.

**Germany, specifically.** BMZ leads; KfW Development Bank handles financial co-operation (loans) and GIZ technical co-operation. Germany has been a DAC member since 1960 and was the second-largest DAC provider for most of the last decade, becoming the largest in the 2025 preliminary figures. Tunisia is a significant partner: BMZ's **first "reform partner"** from 2017, and in the 2021 peer review Germany was the **second-largest development partner in Tunisia**, disbursing **about USD 290 million a year on average over 2018–19**, with Tunisia ranked 17th among Germany's partner countries. Those figures are the benchmark for validating any Germany→Tunisia total (§9).

---

## 6. Spatial attributes

| Question | Answer |
|---|---|
| Geocoded? | **No.** Recipient country or region. |
| Codes | ISO3 for countries, which joins straight to the atlas country table — easier than BACI, which needs its own numeric codes |
| Non-country recipients | Region codes and "unspecified" codes, which have no geometry and must be filtered and reported, not mapped (pitfall 6) |
| Join to geometry | `RECIPIENT` (ISO3) → `atlas_iso3` → `reference/geo/world_countries.geojson` or `world_grid.json` |
| Suitable | Choropleths of aid received, provider→recipient flow maps, grid-map small multiples by year |
| Not suitable | Anything sub-national, project locations, corridors |

---

## 7. What matters for visualisation

1. **Four things in every source line:** dataflow version, flow type (commitments or disbursements), price base (and base year if constant), and which measure. A CRS chart without these cannot be reproduced.
2. **Never one series across both flow types.** Two panels, or one, clearly labelled.
3. **Long series need constant prices** (`PRICE_BASE=Q`); name the base year, which moves between releases.
4. **The distribution is extremely skewed.** A handful of large KfW loans will dwarf everything else in Tunisia. Top-N with an "all other" residual, or a log scale with the reason stated.
5. **Channel-share charts start where channel coverage starts** (pitfall 8). Show earlier years as a gap, never as zero.
6. **Gaps as gaps**, per CLAUDE.md: a year with no reporting breaks the line.
7. **Activity counts need deduplication** by activity id, and should be labelled "activities reported", not "projects".
8. **Project text is a liability in charts.** Provider-written, inconsistent, sometimes in German, sometimes a code fragment. Good for tooltips and for finding a case to write about; bad as a category.
9. **The excluded share is part of the chart.** State what percentage of the money sat in regional or unspecified recipients and was left out.
10. **Volume shapes the architecture:** loader → Parquet → DuckDB, and no CRS API call at page-view time (CLAUDE.md rules 4 and 5). Browser fetching is for exploration only.

---

## 8. The API: a language-neutral reference

**Verified working 2026-11-10.** Everything in this section is a property of the API, not of any one language. The notebook, a Python loader and an R script differ only in syntax; the request, the failure modes and the post-processing rules are identical, and §8.7 lists the few places where a language's CSV reader behaves differently.

### 8.1 Anatomy of a request

```
https://sdmx.oecd.org/dcd-public/rest/v1/data/{dataflow}/{key}?{query}
```

| Part | Value | Notes |
|---|---|---|
| Host | `sdmx.oecd.org` | `/dcd-public/rest/v1` for development-finance data; `/public/rest` also serves it |
| `{dataflow}` | `OECD.DCD.FSD,DSD_CRS%40DF_CRS,1.7` | agency, dataflow, version. The `@` **must be percent-encoded as `%40`**. |
| `{key}` | `DEU.TUN......V.DD..USD` | the eleven dimensions of §3.1, joined by dots |
| `{query}` | `startPeriod=1995&endPeriod=2004&dimensionAtObservation=AllDimensions&format=csvfilewithlabels` | time is a query parameter, never part of the key |

No API key, no registration, no authentication header. The endpoint sends permissive CORS headers, so a browser can call it directly.

### 8.2 Building the key safely

The key is **positional**: an omitted dimension still needs its dot, and a key with the wrong number of dots is an HTTP 400, not an empty result. Build it from a list of eleven items and assert the length — in any language. Germany → Tunisia, all sectors, all measures, all channels, all modalities, both flow types, current prices, activity detail, US dollars:

```
["DEU", "TUN", "", "", "", "", "", "V", "DD", "", "USD"]  →  DEU.TUN......V.DD..USD
```

Multiple values in one position are joined by `+` (`DEU+FRA`), and `_T` means the dimension's total where one exists.

### 8.3 Chunk the request

Broad queries are **refused, not truncated**. For a large provider over a long period, request in blocks — a decade works for one provider and one recipient; a single year may be needed for a whole-region query — and concatenate. Keep concurrency low (three parallel requests was comfortable); this is a public service with no published quota, and hammering it is both rude and counterproductive.

### 8.4 Status codes: what each one means

| Status | Meaning | What a loader should do |
|---|---|---|
| 200 | Data | Parse it |
| **404** | Valid key, **no observations match** | **Not an error.** Record "empty" and carry on. Common for pre-1995 chunks (pitfall 12). |
| **400** | A code is not in the code list, **or the key has the wrong number of dots** | Record and carry on if probing codes deliberately; otherwise check the dot count first |
| 5xx | Server trouble | Retry once, then record and carry on |

A multi-chunk download must never abort on 404 or 400 — otherwise one empty decade kills the whole extract.

### 8.5 The response, and two traps

- **It arrives as a file attachment**, not as a web page. Tools that preview a URL render nothing. Any HTTP client that reads the body is fine; a browser-based URL preview is not.
- **The CSV has duplicated column names.** The marker columns (RMNCH, DRR) repeat because code and label columns share a heading. This is the data, not a parser bug. Decide deliberately whether to suffix or drop — never overwrite silently.
- `format=csvfilewithlabels` gives both codes and labels and is roughly twice the size of `format=csvfile`, which gives codes only. Labels are worth it for exploration; a loader that joins its own code lists can take the smaller one.

### 8.6 Post-processing rules, identical in every language

1. **Multiply by the multiplier:** `amount = OBS_VALUE * 10^UNIT_MULT`. Expect `UNIT_MULT = 6`. Never hardcode millions.
2. **Keep every identifier as text.** CRS ids have leading zeros and alphanumeric suffixes; read as numbers they are corrupted irreversibly.
3. **Filter before summing**, on four dimensions: one `FLOW_TYPE`, one `PRICE_BASE`, `MD_DIM = DD`, and one level of `MEASURE`.
4. **Run the parent-measure test** before quoting any total: group by measure code and sum. If the largest measure is roughly equal to the sum of all the others, it is their parent (code `100`, "Official Development Assistance"), and a total across measures is about double the truth.
5. **Count activities by distinct id**, never by rows.
6. **Record the vintage**: dataflow version and extraction date, stored next to the data, not typed into a chart footer.

### 8.7 The same request in three places

The JavaScript version has run; the other two are written from the same verified recipe but have **not yet been run in this project** — treat them as a starting point, not as tested code.

**Shell, to eyeball one chunk:**

```sh
curl -sS -o crs_deu_tun_2015.csv \
  "https://sdmx.oecd.org/dcd-public/rest/v1/data/OECD.DCD.FSD,DSD_CRS%40DF_CRS,1.7/DEU.TUN......V.DD..USD?startPeriod=2015&endPeriod=2015&dimensionAtObservation=AllDimensions&format=csvfilewithlabels"
head -1 crs_deu_tun_2015.csv | tr ',' '\n' | nl   # the column list, one per line
```

**Python** (`requests` + `pandas`): build the URL as a string so the `%40` survives, and read everything as text.

```python
import io
import requests
import pandas as pd

BASE = "https://sdmx.oecd.org/dcd-public/rest/v1/data"
DATAFLOW = "OECD.DCD.FSD,DSD_CRS%40DF_CRS,1.7"

def crs_key(parts):
    assert len(parts) == 11, f"CRS key needs 11 dimensions, got {len(parts)}"
    return ".".join(parts)

key = crs_key(["DEU", "TUN", "", "", "", "", "", "V", "DD", "", "USD"])
url = (
    f"{BASE}/{DATAFLOW}/{key}"
    "?startPeriod=2015&endPeriod=2019"
    "&dimensionAtObservation=AllDimensions"
    "&format=csvfilewithlabels"
)

response = requests.get(url, timeout=120)

if response.status_code == 404:          # valid key, no observations
    frame = pd.DataFrame()
else:
    response.raise_for_status()
    frame = pd.read_csv(io.StringIO(response.text), dtype=str)

# Only now convert, deliberately:
frame["amount_usd"] = (
    pd.to_numeric(frame["OBS_VALUE"], errors="coerce")
    * 10 ** pd.to_numeric(frame["UNIT_MULT"], errors="coerce").fillna(0)
)
```

**R** (`httr2` + `readr`):

```r
library(httr2)
library(readr)
library(dplyr)

crs_key <- function(parts) {
  stopifnot(length(parts) == 11)
  paste(parts, collapse = ".")
}

key <- crs_key(c("DEU", "TUN", "", "", "", "", "", "V", "DD", "", "USD"))

url <- paste0(
  "https://sdmx.oecd.org/dcd-public/rest/v1/data/",
  "OECD.DCD.FSD,DSD_CRS%40DF_CRS,1.7/", key,
  "?startPeriod=2015&endPeriod=2019",
  "&dimensionAtObservation=AllDimensions",
  "&format=csvfilewithlabels"
)

response <- request(url) |>
  req_error(is_error = \(resp) FALSE) |>   # handle 404 ourselves
  req_perform()

crs <- if (resp_status(response) == 404) {
  tibble()
} else {
  read_csv(
    resp_body_string(response),
    col_types = cols(.default = col_character()),
    name_repair = "unique"
  ) |>
    mutate(
      amount_usd = as.numeric(OBS_VALUE) *
        10 ^ coalesce(as.numeric(UNIT_MULT), 0)
    )
}
```

**Where the languages genuinely differ — the duplicate headings.** Each CSV reader renames the repeated marker columns its own way: pandas appends `.1`, `readr` with `name_repair = "unique"` appends `...n`, and the notebook code suffixes `_LABEL`. So a Python loader and a notebook will disagree about those column *names* while agreeing about the data. Pin one convention in the loader and let everything downstream read Parquet, which is the point of architecture rule 2.

### 8.8 Two routes, for two purposes

| Route | Where | For |
|---|---|---|
| Direct API call | notebook, script, shell | Exploration, learning the shape of the data, answering a colleague's question today. No key is needed, so the `Secret()` problem that blocks UN Comtrade does not arise here (`_relationships.md` §4). |
| Python loader → Parquet | this repository | Anything that reaches a page. `loaders/crs_download.py` writes the raw chunks to `data/raw/oecd-crs/{date}/` with a manifest; `loaders/crs_load.py` converts to Parquet, applying the rules in §8.6 and stopping if a recipient code is missing from `reference/countries.csv`. |

---

## 9. First use: German flows to Tunisia, whole coverage

**The question (2026-11-10):** German flows to Tunisia across the whole CRS coverage, West and East Germany to the extent that data exist, with German NGOs identified where possible.

**What the source can and cannot answer:**

| Part of the question | Answer from this card |
|---|---|
| German flows to Tunisia | Yes, `DONOR=DEU`, `RECIPIENT=TUN`. German bilateral reporting only — not the German share of EU Institutions spending (pitfall 10). |
| Whole coverage | Series starts 1973; usable from 1995 (commitments) and 2002 (disbursements); expect the API to return little or nothing before 1995 (pitfall 12). Pre-1995 needs the bulk text files. |
| West Germany | Pre-1990 rows under `DEU` **are** the Federal Republic. Germany has reported since the DAC's founding in 1960. |
| East Germany | **Not in the source at all.** No GDR provider code; the CRS excludes non-DAC bilateral providers. This is a property of the data, not a gap to fill, and belongs in the prose of any long German series. |
| German NGOs | From channel codes 22000–22999 with the donor pinned to Germany, plus a labelled name heuristic for German organisations coded as international NGOs (§3.3). Only for years with channel coverage — roughly 2010 onwards (pitfall 8). |

**Validation benchmark before believing any total:** about **USD 290 million a year** in German disbursements to Tunisia on average over 2018–19, Germany the second-largest partner in Tunisia (OECD peer review of Germany, 2021). A Tunisia total far from that order of magnitude for those years means a dimension is wrong — most likely measure double counting (pitfall 1) or flow types summed together (pitfall 3).

**Status 2026-11-10:** the two exploration cells (chunked fetch with per-request diagnostics; wrangling cell classifying channels and exposing measure, channel and donor inventories) **ran successfully** on observablehq.com against dataflow 1.7. The diagnostics have not yet been read back into this card. Still to paste here, and the card stays a draft until they are:

- `meta.donorsWithData` — which donor codes returned rows, settling the DDR probe
- `meta.requests` — which year chunks were empty, i.e. where coverage actually starts
- `missingFields` — which column names in §3 and §8 were guesses
- `parentMeasureCheck` — whether a blank `MEASURE` at `MD_DIM=DD` really returns a parent alongside its components
- `firstYearWithChannelCoding` — the real start of the NGO question
- the Germany→Tunisia disbursement total for 2018 and 2019, against the USD 290 million benchmark

---

## 10. Decisions still open

- [ ] Pin `MEASURE` in requests, or fetch all measures and group? (Pinning is safer; grouping shows composition. Decide once, and encode it in the loader.)
- [ ] Which measure code is the atlas default for "aid": ODA total, or grants and loans separately?
- [ ] Flow basis or grant-equivalent for topic 02 headline charts?
- [ ] Whether to carry pre-1995 data at all, given it needs a second access route and has provider gaps.
- [ ] Rule for regional and unspecified recipients: excluded with a stated share, or shown as a separate "not allocated by country" band?
- [ ] Which duplicate-column convention the loader pins (§8.7).
- [ ] Verify: first year of usable channel coding; whether activity ids are stable across years; SECTOR code levels; the PSI dataflow id.

---

## 11. Learned through use

*Add a dated line whenever a query or chart teaches something about the CRS that belongs here.*

- 2026-11-10: **The SDMX key is positional and unforgiving.** `DEU.TUN.....V.DD..USD` (nine dots) returned a client error; `DEU.TUN......V.DD..USD` (ten) reached the data. Build keys from a list with a length assertion, in whatever language.
- 2026-11-10: **`format=csvfilewithlabels` responds as a file attachment.** A plain URL-preview tool reports binary and cannot show the header row, so the column names in §3 were originally guesses; the exploration cell resolves every column from a candidate list and reports which names it actually found.
- 2026-11-10: **Duplicated CSV headings are real**, not a parser bug: the marker columns (RMNCH, DRR) repeat because code and label columns share a name. Each language's CSV reader renames them differently (§8.7).
- 2026-11-10: **The dataflow has moved to 1.7** (Data Explorer, last updated 2026-10-08) while older notebook code pins 1.6, which still resolves. Version belongs in the source line.
- 2026-11-10: **`MEASURE=100` is "Official Development Assistance"** — an aggregate, in the same dimension as its components. This is the most dangerous property of the dataflow for anyone used to one-row-per-project thinking.
- 2026-11-10: **The recipe works, and it works from a browser.** Chunked requests (decade blocks, three in parallel, 404 treated as empty) completed against 1.7 for Germany→Tunisia with no key and no proxy, confirming the endpoint allows cross-origin calls. Diagnostics not yet read back (§9).
