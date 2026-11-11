# Data card: OECD FDI statistics (BMD4)

> **Status:** **v0.1, draft** 2026-11-11. **First extract verified in use**: positions by counterpart
> area for Tunisia, 41,263 rows for EU-OECD reporters, fetched from an observablehq.com notebook.
> Data-level facts beyond that are still documentation readings.
> **Purpose:** the OECD's own foreign direct investment statistics, which are a different source from
> Eurostat's and from the OECD CRS, and the SDMX access pattern that actually works for them.
> **Atlas status:** not promoted. Working only.
> **Related files:** `eurostat-fdi.md` (the EU-side source for the same phenomenon — §5) ·
> `oecd-crs.md` (same publisher, aid rather than investment) · `_relationships.md` ·
> `source-update-calendar.md`
> **In the repository:** nothing yet. One exploration cell exists for observablehq.com.
> **Do not confuse with the OECD CRS.** Same organisation, different directorate, different
> questionnaire: CRS is development co-operation (`OECD.DCD.FSD`), this is investment
> (`OECD.DAF.INV`).

---

## 1. At a glance

| Attribute | Value |
|---|---|
| Full name | FDI statistics according to the OECD Benchmark Definition of Foreign Direct Investment, 4th edition (BMD4) |
| Publisher | OECD, Directorate for Financial and Enterprise Affairs — SDMX agency `OECD.DAF.INV` |
| What it measures | Inward and outward FDI positions, flows and income, by partner country and by economic activity, for OECD reporting economies |
| Unit of observation | One observation = reporter × counterpart × measure × principle × activity × period |
| Source kind (atlas) | **primary** — compiled by national compilers (central banks, statistical offices) from balance-of-payments returns, mostly following BPM6 and BMD4; some entries come from notifications or approvals instead |
| Reporters | **OECD members**, which is not the EU. Bulgaria, Croatia, Cyprus, Malta and Romania are absent (pitfall 1). |
| Counterparts | Partner countries and groupings, ISO3 codes (`TUN` for Tunisia — verified) |
| Coverage | BMD4 from the March 2015 launch onwards; the historical dataflow carries BMD3 series as well, which reach further back (pitfall 6) |
| Frequency | Annual by counterpart area; quarterly for some aggregates |
| Free? | **Yes.** No key, no registration. |
| Public API | SDMX at `https://sdmx.oecd.org/public/rest`, both a v1 positional-key style and a **v2 named-filter style** (§3). **CORS works from `observablehq.com`** — verified. |
| Formats | `csvfilewithlabels`, `csvfile`, SDMX-ML, JSON |
| Response size | One counterpart across all reporters, measures and years: **34.4 MB** for positions. Large but a browser handles it. |
| Citation | OECD, *FDI statistics by partner country (BMD4)*, dataflow `OECD.DAF.INV:DSD_FDI@DF_FDI_POS_CTRY(1.0)`, extracted YYYY-MM-DD |
| Proposed fetch class | `open` |
| Proposed change check | The "last updated" timestamp per dataflow in the OECD Data Explorer |

### The dataflows, with verified identifiers

| Dataflow | What it holds |
|---|---|
| `DSD_FDI@DF_FDI_POS_CTRY` | **Positions by counterpart area** — used for the first extract |
| `DSD_FDI@DF_FDI_FLOW_CTRY` | **Flows by counterpart area** — co-primary with positions, and usually the richer table of the two (`eurostat-fdi.md` §7) |
| `DSD_FDI@DF_FDI_INC_CTRY` | Income by counterpart area |
| `DSD_FDI@DF_FDI_POS_IND` · `DF_FDI_FLOW_IND` · `DF_FDI_INC_IND` | The same three, by economic activity instead of partner |
| `DSD_FDI@DF_FDI_CTRY_IND_SUMM` | Partner **and** activity together, simplified: fewer breakdowns than the dedicated tables |
| `DSD_FDI@DF_FDI_CTRY_IND_HIST` | Partner and activity, **BMD4 plus historical BMD3** — the longest series, at the price of a methodology break |
| `DSD_FDI@DF_FDI_AGGR_SUMM` · `DF_FDI_POS_AGGR` · `DF_FDI_FLOW_AGGR` · `DF_FDI_INC_AGGR` | Main aggregates, including quarterly |
| `DSD_QDD_FDI@DF_FDI_BMD4` | **Metadata**: each country's methods and practices. The place to look before writing a footnote about why two reporters disagree. |

All are version `1.0` under agency `OECD.DAF.INV`.

---

## 2. Dimensions

The positions-by-counterpart structure has **13 dimensions**. The ones that carry the argument:

| Dimension | Notes |
|---|---|
| `REF_AREA` | The reporting economy, ISO3. Verified to contain `FRA`, `DEU` and the rest. |
| `COUNTERPART_AREA` | The partner, ISO3. `TUN` verified. `W` is world. |
| `MEASURE` | What is being measured (positions, flows, income, and their components). **Check for totals before summing** (pitfall 3). |
| `UNIT_MEASURE` | Includes reported currency and share-of-FDI percentages — pin it, or you will add euros to percentages (pitfall 7). |
| `MEASUREMENT_PRINCIPLE` | **Directional** (inward/outward) versus **asset/liability**. BMD4 publishes both; they are different numbers for the same reality (pitfall 4). |
| `ACTIVITY` | ISIC Rev. 4 economic activity, where the dataflow carries it |
| `TIME_PERIOD` | Annual, as `startPeriod`/`endPeriod` or `c[TIME_PERIOD]` |

The full 13 come back in position order from the structure endpoints, and the 44-column CSV names every
one of them — see §3.

---

## 3. Access: the recipe that works

### 3.1 Named filters, not a positional key

SDMX 3.0 lets a component be named instead of counted. This is the verified, readable route:

```
https://sdmx.oecd.org/public/rest/v2/data/dataflow/OECD.DAF.INV/
  DSD_FDI%40DF_FDI_POS_CTRY/1.0
  ?c[COUNTERPART_AREA]=TUN
  &format=csvfilewithlabels
```

The `@` in the dataflow id must be percent-encoded as `%40`. Per the SDMX 3.0 specification, several
values for one component are **comma-separated and mean OR** (`c[FREQ]=A,M`), a **plus means AND**, and
operators are prefixes (`c[TIME_PERIOD]=ge:2015`). The `c` parameter filters dimensions only, not
attributes or measures.

The older v1 positional style also works on the same server — it is what the CRS card documents — but it
requires knowing the dimension order and the exact dot count. With 13 dimensions, named filters are the
better choice for anything written by hand.

### 3.2 Two ways to learn the structure

Both return SDMX-ML, which parses in a browser with `DOMParser` and
`getElementsByTagNameNS("*", "Dimension")`, reading the `position` attribute:

```
https://sdmx.oecd.org/public/rest/dataflow/OECD.DAF.INV/DSD_FDI%40DF_FDI_POS_CTRY/1.0?references=all
https://sdmx.oecd.org/public/rest/datastructure/OECD.DAF.INV/DSD_FDI/1.0?references=children
```

Both answered 200 and both yielded the 13 dimensions, at about 2 MB each.

### 3.3 The response

`csvfilewithlabels` returns **SDMX-CSV 2.0**: the first four columns are metadata — `STRUCTURE`,
`STRUCTURE_ID`, `STRUCTURE_NAME`, `ACTION` — followed by each dimension as a code column and a
human-label column, then `OBS_VALUE`, `TIME_PERIOD` and attributes. For positions by counterpart that is
**44 columns**. Column names can repeat, so dedupe the header rather than overwriting.

### 3.4 Observed limits and hazards

| Behaviour | What was seen |
|---|---|
| One counterpart, everything else open | 200, **34.4 MB**, parsed to tens of thousands of rows. No refusal. |
| Wildcard key `all` on v1 with `lastNObservations=1` | **200 with zero bytes.** A silent empty success — worse than an error, because status-code checks pass (pitfall 5). |
| `c[COUNTERPART_AREA]=TUN` | Works. |
| Adding `c[REF_AREA]=FRA,DEU` or a single `c[REF_AREA]=FRA` | **Returned no rows.** Unresolved — see §7. The syntax matches the specification, so the cause is either OECD's implementation of that filter or request volume, and one two-line probe settles it. |

**Working rule until that is resolved:** filter server-side on `COUNTERPART_AREA` only, and do the
reporter selection in the client. 34 MB is cheap; four failed iterations were not.

---

## 4. Pitfalls

| # | Pitfall | Consequence | Fix |
|---|---|---|---|
| 1 | **OECD membership is not the EU.** Bulgaria, Croatia, Cyprus, Malta and Romania do not report here. | An "EU total" built from this source is wrong and silently short. | Use it for "which European countries invest in X"; use Eurostat for anything claiming to be the EU. |
| 2 | **Immediate versus ultimate investing country** is available for *some* reporting economies only. | A chart mixing the two views, or treating the ultimate view as complete, misattributes conduit investment. | State which view each series uses; never average across them. |
| 3 | **`MEASURE` may contain totals alongside components.** | Summing across measures double counts, exactly as in the CRS. | Group by measure, inspect, pin one. Run the same parent test the CRS card describes. |
| 4 | **Directional and asset/liability principles coexist** in `MEASUREMENT_PRINCIPLE`. | Two legitimate numbers for the same flow; mixing them is meaningless. | Pin one principle per chart and name it in the footer. |
| 5 | **Silent empty success.** A 200 can carry zero bytes. | Error handling keyed on status treats a failure as success and the chart shows nothing. | Require ok **and** non-empty **and** parsed rows > 0 before believing a response. |
| 6 | **BMD3 history is a different methodology.** The `_HIST` dataflow is the only route to the earliest years. | A long series across the break mixes benchmarks. | Mark the break, or stop at the BMD4 start. |
| 7 | **`UNIT_MEASURE` mixes currency and percentages.** | Adding euros to shares. | Always pin `UNIT_MEASURE`. |
| 8 | **Negative positions and flows are real** — divestment, intra-group repayment, affiliate claims exceeding the parent stake. | Clipping them hides the interesting moments. | Keep them and explain them. |

---

## 5. OECD FDI compared with Eurostat FDI

They are **not independent evidence**. Both rest largely on the same national balance-of-payments
returns. They differ in three ways that matter:

| | Eurostat (`bop_fdi6_*`) | OECD (`DSD_FDI@*`) |
|---|---|---|
| Reporters | All EU Member States plus EU and euro-area aggregates | OECD members only — five EU states missing |
| Benchmark | BPM6 presentation | BMD4, which adds the directional/asset-liability distinction explicitly |
| Activity classification | NACE Rev. 2 | ISIC Rev. 4 |
| Earliest year | 2007 | BMD4 from 2015 onwards, with BMD3 history in the `_HIST` dataflow |
| Ultimate counterpart | A dedicated dimension on positions | Available for some reporters |
| Conduit/SPE treatment | Published with and without special purpose entities | Varies by reporter; see the metadata dataflow |

**Rule for the atlas:** one source per chart, named in the footer. When both are available, Eurostat is
the EU-wide figure and OECD is the cross-OECD comparison. If the two disagree, that is a finding about
compilation practice, and `DSD_QDD_FDI@DF_FDI_BMD4` is where the explanation lives.

---

## 6. What matters for visualisation

1. **Footer must carry four things:** dataflow and version, measure, measurement principle, unit.
2. **Never an "EU total" from this source** (pitfall 1). "EU-OECD reporters" is the honest label.
3. **Skew is extreme**: France and Italy will dominate a Tunisia chart. Top-N plus residual, or log.
4. **Gaps as gaps**, per CLAUDE.md. Many reporter-partner-year cells are genuinely absent.
5. **Negative values on the axis**, not clipped.
6. **The metadata dataflow is chart furniture**: when one reporter looks anomalous, the explanation is
   usually a documented national practice rather than an error.

---

## 7. First use: European FDI positions in Tunisia

**What was asked (2026-11-11):** European FDI to Tunisia, as far back and as granular as possible,
fetched from a browser notebook. Eurostat was the intended source; it was down all day
(`eurostat-fdi.md` §6.2), so OECD became the substitute.

**What worked:** `DF_FDI_POS_CTRY` with `c[COUNTERPART_AREA]=TUN` and nothing else, parsed in the
browser, then filtered to the 22 EU states that are OECD members. **41,263 rows.** Still to read off
that extract: year range, which measures and principles are populated, and whether any reporter carries
the ultimate-investing-country view for Tunisia.

**Next, and not optional:** the same extract from `DF_FDI_FLOW_CTRY`. Flows are co-primary with
positions rather than a secondary cut, and for FDI they tend to be the richer series — they carry the
instrument composition and they are what responds to an event. The request is identical but for the
dataflow id, since the counterpart filter is the only server-side filter used.

### Why the earlier attempts returned nothing — the retro

Four attempts returned an empty array before one worked. The causes were all different and the symptom
was identical, which is the lesson worth keeping.

1. **Eurostat, attempt 1 and 2:** the service was down. Browser symptom: `TypeError: Failed to fetch`.
2. **DBnomics (mirror), attempt 3:** host not reachable from the browser at all. Same symptom.
3. **OECD v1 positional key, attempt 4:** the key order was unknown, so the request was malformed or
   over-broad. Symptom: an empty array.
4. **OECD v2 with `c[REF_AREA]`, attempt 5:** the counterpart filter alone works, but adding a reporter
   filter returned nothing. Symptom: an empty array again.

**What made it slow was not the APIs. It was three habits.**

**Diagnostics were hidden.** Every cell caught its errors, recorded them in a **non-enumerable** `meta`
property, and returned `[]`. The information existed and was invisible: the notebook inspector shows
`Array(0)` and nothing else. **Rule: diagnostics go in enumerable properties, on the surface.** Better
still, a request that fails for an unanticipated reason should make the cell *throw*. An empty array is a
legitimate answer to a well-formed question, so it must never also be the signature of a broken one.

**Each new attempt changed more than one thing.** The probe established that exactly one filter worked.
The next cell added a second untested filter, a batching heuristic, and a fallback path — three new
things on top of one known-good thing — so when it failed there were three candidate causes and no way
to isolate them. **Rule: take the exact request that returned bytes, change nothing, and move every
remaining choice to the client.** That is what finally worked.

**Server-side filtering was treated as a requirement rather than an optimisation.** Filtering 34 MB in
the browser is instant. The attempt to be economical in the query cost four round trips. **Rule: get it
working with the broadest proven query, measure the size, and narrow only if size actually hurts.**

**The remaining open question**, which two one-line requests would settle: does
`c[REF_AREA]=FRA&c[COUNTERPART_AREA]=TUN` return rows? If yes, the reporter filter is fine and the
failure was request volume — the fallback path fired 88 requests at three concurrently, which a public
gateway may well have throttled. If no, OECD's implementation does not honour `c[]` on that component
for this dataflow, despite the specification, and the client-side rule above becomes permanent.

---

## 8. Learned through use

- 2026-11-11: **Named SDMX 3.0 filters work on this server** and remove all key-order guesswork:
  `/rest/v2/data/dataflow/OECD.DAF.INV/{DSD%40DF}/1.0?c[COUNTERPART_AREA]=TUN`. The structure endpoints
  return the 13 dimensions in position order for the cases where a positional key is still wanted.
- 2026-11-11: **A 200 can be empty.** The v1 wildcard key returned zero bytes with a success status.
  Validate on parsed rows, never on the status code alone.
- 2026-11-11: **34 MB arrives and parses fine in a browser.** Breadth in the query is not the problem it
  looks like; cleverness in the query was.
- 2026-11-11: **Flows are co-primary with positions.** The first extract here was positions because that
  was the standing default at the time; the default was revised the same day. Nothing about the access
  pattern changes — only the dataflow id.
- 2026-11-11: **Four empty arrays, four different causes.** Full retro in §7. The habits that cost the
  time — hidden diagnostics, changing several things at once, premature server-side filtering — are
  worth more than the dataflow ids.
