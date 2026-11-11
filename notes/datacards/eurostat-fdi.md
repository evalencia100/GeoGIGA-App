# Data card: Eurostat FDI and the balance-of-payments family

> **Status:** **v0.2, draft** 2026-11-11. Written from Eurostat's own API documentation and dataset pages.
> **No data has been fetched yet, and not for want of trying:** the dissemination API was **down** all day
> on 2026-11-11 (§6.2), so every behavioural claim in §6.1 is still documentation rather than
> observation. The work was completed from **OECD FDI** instead — see `oecd-fdi.md`.
> The four classification decisions in §7 are settled.
> **Purpose:** what Eurostat's FDI statistics actually contain, how the API behaves, and which parts of a
> European dataset carry a global argument. Written for a topic-first atlas, where "EU data" has to earn
> its place in a chapter about the world.
> **Atlas status:** not promoted. **Working only** for now (§7).
> **Related files:** `oecd-fdi.md` (the substitute source, and the retro on how this went) ·
> `_relationships.md` · `source-update-calendar.md` · `oecd-crs.md` (the other topic-02 source; CRS is
> aid, this is investment — §5)
> **In the repository:** nothing yet. Two exploration cells exist for observablehq.com: a reusable
> Eurostat client with a JSON-stat flattener, and a Tunisia extract built on it. Neither has yet returned
> data, for want of a working server.

---

## 1. What this source is, in prose

Eurostat does not publish "foreign direct investment" as one table. It publishes a **family of tables cut
from the same balance-of-payments machinery**, and the choice between them is the first analytical
decision, not a technical detail.

The spine is three annual tables under the sixth edition of the IMF's Balance of Payments Manual
(BPM6), each covering **2007 to 2024**:

- **`bop_fdi6_pos` — positions.** The stock of investment: how much European capital is sitting in a
  partner economy at the end of the year. This is the right table for questions about presence,
  dependency and accumulated exposure. It is also the only one of the three that distinguishes the
  *immediate* from the *ultimate* counterpart, which is the single most important thing in this card
  (§3). **The atlas default** (§7).
- **`bop_fdi6_flow` — flows.** Transactions during the year: new investment, divestment, loans between
  affiliates. This is the right table for questions about momentum and about reaction to events — a
  coup, a bailout, an interconnector agreement. Flows are volatile and frequently negative, and a
  negative flow is a real phenomenon, not a data error (§4).
- **`bop_fdi6_inc` — income.** What the investment earned: dividends, reinvested earnings, interest on
  intra-group debt, split into credits and debits. This is the table almost nobody uses and the one with
  the most political content, because it measures what flows *back* (§5).

Two further tables are worth knowing. **`bop_fdi6_geo`** carries positions, flows and income by
partner country without the economic-activity breakdown — much smaller, and the sensible table for a
first map or a many-country comparison. **`bop_fdi6_ind`** holds derived indicators: FDI as a share of
GDP, impact indicators, and the **rate of return** on direct investment, which is the natural way to ask
whether European capital earns more in one region than another.

Each of these is a hypercube with up to nine dimensions. For positions: reporting country (42 values,
EU Member States plus EU and euro-area aggregates), partner (around 300, countries and regional
groupings), economic activity under NACE Rev. 2 (81 values), FDI item (20 — equity, debt instruments,
and their subdivisions), stock-or-flow (assets, liabilities, net), entity (with and without special
purpose entities), type of counterpart (immediate or ultimate), currency (million euro), and time. The
cross-product is in the millions of cells and overwhelmingly empty: Eurostat publishes what Member
States report and what confidentiality rules permit, which for a small partner is a small fraction of
the grid.

**A change is coming.** Eurostat's balance-of-payments vademecum describes new FDI data structures from
**reference year 2025**, moving to NACE Rev. 2.1 and adding dataflows for investment by **ultimate
investing economy** and **ultimate host economy**, plus **greenfield investment**. If those become
published tables, the conduit problem below becomes directly measurable rather than something to
caveat. Worth re-reading this card when the 2025 reference year lands.

---

## 2. Why a European dataset belongs in an atlas about global issues

The honest framing is that this is **one bloc's books, not the world's**. Eurostat records what EU
Member States report about themselves and their partners; it has nothing to say about Chinese, Gulf or
Turkish investment except as a partner column seen from Europe. Used carelessly, it produces a chart
that says "Europe matters" because Europe is the only thing measured.

Used carefully, it does three things no global aggregate does.

**It is the counterparty record for a dependency argument.** When the question is whether a country's
productive base is tied to European capital, the EU's own position data is the creditor-side evidence,
and it is more detailed by activity than most recipient countries' own statistics. Tunisia is a good
example: the interesting claim is not how much the EU invests but *into which activities*, because that
is what connects to European industrial supply chains.

**It separates stocks from flows from income**, which lets a page make an argument rather than show a
number. The combination — a large accumulated position, thin new flows, and steady income flowing back
— is a specific and arguable condition, and it is visible only because the three tables exist
separately.

**It exposes the plumbing of global capital.** The immediate-versus-ultimate distinction and the
special-purpose-entity flag are not European curiosities. They are the measurement problem that makes
*all* bilateral FDI statistics partly fictional, and Eurostat is one of the few publishers that lets you
see the size of the distortion. A chart about that is a chart about the global financial system, built
from European data.

---

## 3. The datapoints with global implications — flag these

Ordered by how much they change an argument.

**1. Immediate versus ultimate counterpart (`counterp`: `IMM` / `UIE`, positions only).** Bilateral FDI
as normally published records the *immediate* counterpart, so investment routed through Luxembourg, the
Netherlands or Ireland is attributed to those countries rather than to whoever ultimately owns it. The
ultimate-investing-economy view reassigns it. The gap between the two views is a measure of how much of
world FDI is conduit structure, and for small recipients it can reverse the ranking of investors
entirely. **Any chart naming "the biggest investor in country X" that does not say which view it uses is
making an unsupported claim.** This is also where to look for investment that is European on paper and
Chinese, Gulf or American in substance — or the reverse: capital that left a country and came back
wearing an EU passport. **Atlas default: the ultimate view** (§7), which means accepting thinner
coverage in exchange for a defensible claim about ownership.

**2. Special purpose entities (`entity`).** SPEs are holding companies with no real activity, and their
inclusion inflates both sides of a bilateral position. Eurostat publishes with and without them. The
difference is the standard measure of "phantom" investment. For a story about tax structuring, treaty
shopping or the real size of a bilateral relationship, the SPE-excluded series is the honest one, and
the gap itself is the finding. **Atlas default: carry both and label the difference** (§7), so the
phantom share is visible on the face of the chart rather than in a note.

**3. Economic activity (`nace_r2`, 81 values).** This is where European FDI becomes a statement about
European *dependence*, not generosity. Investment in extractive activities, in textiles and apparel, in
manufacture of electrical equipment and automotive components, in electricity generation — each of these
is a European industry locating part of its chain abroad. North African automotive wiring and component
plants supplying German assembly lines are the textbook case: a reshoring or disruption story is visible
in the activity breakdown and invisible in the total. Equally, FDI in electricity and renewables is the
leading edge of European energy-import strategy, so it reads as infrastructure and energy dependency
(atlas topic 06) rather than finance.

**4. Income, and specifically reinvested earnings versus dividends (`bop_fdi6_inc`).** Income is the
return leg. Whether earnings are reinvested locally or repatriated as dividends is a measurable
distinction with a direct bearing on arguments about extraction versus development — and it is one of
the few places where a North–South transfer can be quantified from official statistics rather than
asserted. Credits and debits are reported separately, so direction is unambiguous.

**5. Rate of return (`bop_fdi6_ind`).** Return on European direct investment, comparable across
partners. It supports the question of whether capital is priced for risk in some regions and not others,
and it is a ratio, so it survives the comparison across economies of very different size that absolute
euro figures do not.

**6. Negative positions and flows.** Not an anomaly. A negative flow is divestment or intra-group debt
repayment; a negative position means affiliate claims on the parent exceed the parent's stake.
Politically these are the moments worth writing about, and a chart that clips or hides them is
misleading.

**7. Confidentiality suppression, as a subject.** Bilateral cells for a small partner, cut by activity,
are frequently suppressed because one or two firms would be identifiable. This is the main limit on the
Tunisia question and it is **not** an API problem. It also tells you something real: where a single firm
dominates a country's relationship with Europe. The observation flags come back with the data and belong
in the atlas's asterisk, per CLAUDE.md's light-touch data-quality rule.

---

## 4. Concepts that have to be right

**BPM6 uses an assets-and-liabilities presentation**, not the older directional one. "Direct investment
abroad" and "direct investment in the reporting economy" are both present as FDI items, and from an EU
reporter's point of view, European investment *into* Tunisia is the abroad/asset side with Tunisia as
partner. Mixing the two directions, or summing an item with its own components, is the equivalent of the
measure-aggregation trap in the OECD CRS card: **check whether an FDI item is a total before adding it
to its parts.**

**Sign conventions follow the financial account**, so a positive flow is a net acquisition of assets and
a negative one a net disposal. State the convention in the chart footer.

**Positions are end-of-period stocks and flows are within-period transactions**, so a position change
between two years will not equal that year's flow: revaluation, exchange-rate movement and
reclassification sit in between. Never present a flow series as the derivative of a position series.

**Currency is million euro.** For a non-euro reporter the euro figures embed an exchange-rate effect,
which matters for long series.

**Reporting is by the EU side only.** Tunisia's own statistics, and UNCTAD's, will not match, for
reasons of coverage, SPE treatment and which counterpart is recorded. The mismatch is worth a sentence
in any page, and is itself an argument about who gets to count.

---

## 5. How this relates to the atlas's other sources

| Source | Overlap | What to say about it |
|---|---|---|
| **OECD FDI** (`oecd-fdi.md`) | The same phenomenon, largely the same underlying national returns | **Not independent evidence.** Different benchmark (BMD4), different activity classification (ISIC), and OECD membership rather than EU membership, so five EU states are missing. Eurostat for an EU-wide figure; OECD for a cross-OECD comparison; one source per chart, named in the footer. |
| **OECD CRS** (`oecd-crs.md`) | Both are cross-border money from rich economies, both are donor/creditor-reported | Aid and investment are different instruments with different logics. The pairing is genuinely interesting for a country like Tunisia — concessional finance alongside equity — but they must never be added together or drawn on one axis. |
| **BACI** (`baci-cepii.md`) | Trade and investment are the two halves of a dependency argument | FDI in an activity plus trade in that activity's products is the strongest version of a supply-chain claim. The join is NACE-to-HS, which is a concordance and therefore a judgement — a known hard problem, not a lookup. |
| **AidData GCDF** (to write) | Chinese development finance versus European investment | The natural contrast for topic 02, and the honest way to stop a European dataset from implying Europe is the only actor. |
| **UNCTAD World Investment Report** | Global FDI aggregates | Where to go when the question is genuinely global rather than European. Eurostat is the detail; UNCTAD is the frame. |
| **DBnomics** (mirror, not a source) | Re-serves Eurostat's own datasets under the same dataset and dimension codes | Looked like the obvious fallback during the outage. **It is not reachable from a browser notebook** (§6.2), so it is only useful from a script. A mirror is never cited in place of Eurostat, and its vintage can lag. |

---

## 6. How the API behaves

### 6.1 From the documentation

| Property | Value |
|---|---|
| Base | `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{dataset}` |
| Required | nothing beyond the dataset code; `format=JSON` and `lang=EN` in practice |
| Response | **JSON-stat 2.0** — a hypercube: one sparse `value` object keyed by flat position, plus `size`, `dimension`, and an optional `status` map of observation flags |
| Filters | `{dimension}={code}`, repeatable for several values |
| Time filters | `time` (or `time_period`), `sinceTimePeriod`, `untilTimePeriod` (the two combine into a range), `lastTimePeriod=N` |
| `geoLevel` | Selects a geographic level; **cannot be combined with `geo`** — doing so returns a 400 naming exactly that conflict |
| Key needed | **No.** No registration, no quota published. |
| CORS | Eurostat's documentation states the Statistics API supports CORS and is intended for online visualisation built with the JSON-stat Toolkit. **Still unverified in practice** — the outage prevented any successful browser call. |
| Category limit | Roughly **50 categories per query** when values are enumerated; the documented failure is "Too many categories have been requested". **Omit a dimension to get all its values** — omission is not enumeration and does not count against this. |
| Size refusal | Large extractions are **refused, not truncated**: HTTP 413, an error array, or an `EXTRACTION_TOO_BIG`-style code. *(The specific row ceiling circulating in third-party clients is not in Eurostat's own documentation — treat it as unverified.)* |
| Errors | In the body as well as the status line: `{"error":{"status":"400","label":"..."}}`. Error id 140 is a syntax error, 150 a semantic one (a dimension or code that does not exist). |
| Languages | English, French, German |
| Licence | Eurostat open data; reuse permitted with attribution. Cite the dataset code, the DOI (`10.2908/{dataset}`) and the extraction date. |
| Update cadence | Per dataset, shown as "last update" on the dataset page. `bop_fdi6_flow` was updated 05/11/2026; `bop_fdi6_pos` and `bop_fdi6_inc` cover 2007–2024. **To verify:** whether FDI updates arrive on a fixed annual month. |

### 6.2 Observed, 2026-11-11: the API was down

The first live attempt found the service unavailable, and the way it failed is worth recording because it
will happen again and it is easy to misdiagnose as a bug in your own code.

**What was seen, in order.** A server-side request from a cloud machine was redirected to
`sorry.ec.europa.eu` before reaching the API. From the browser, every request — eight escalating
variants across three datasets — failed identically with `TypeError: Failed to fetch`, with no HTTP
status and no error label. Opening the same URL in a browser tab returned the Commission's multilingual
"Server temporarily unavailable" page rather than JSON. **Eurostat's own demonstration notebook for this
API failed in the same way at the same time**, which is what settles it: the fault was Eurostat's, not
the query's.

**The DBnomics mirror was not a way round it.** `api.db-nomics.world` failed from the same notebook with
the same `TypeError: Failed to fetch`, on a host entirely unrelated to the EU outage — so either it
refuses cross-origin calls or the browser's network path blocks it. Either way: **the mirror is a
script-side fallback, not a browser-side one.**

**The lesson for debugging.** In a browser, `TypeError: Failed to fetch` carries no diagnostic
information at all: it covers an unreachable host, a refused connection, a missing CORS header, and an
HTML error page served from a redirect. It is *not* an API error, so it can never be read as "wrong
parameter". The cheap way to tell the cases apart is to open the same URL in a tab — a human request
from the same address — and, in the notebook, to retry with `mode: "no-cors"`: an opaque response means
the host is reachable and the headers are the problem, while a throw means it is not reachable at all.

**What is still unknown** because of the outage: whether the whole-period request succeeds or must be
chunked; the true dimension list and category counts; how much NACE and FDI-item detail survives
confidentiality for a partner the size of Tunisia; which observation flags appear; and whether CORS
actually works from `observablehq.com`. The checklist is in 6.3 and the cells are written and waiting.

**Consequence for the architecture, already clear.** A source whose API can disappear for a day is a
source that must be snapshotted, which is what architecture rule 3 already requires. It also means the
loader should prefer Eurostat's **bulk TSV or SDMX file download** over the Statistics API where both
serve the same table, and treat the API as the exploration tool. If the hosted build runner is blocked
the way this machine was, that preference becomes a requirement.

### 6.3 Still to be filled in from the first successful run
- [ ] Does the whole-period request succeed, or does it fall back to per-year chunks?
- [ ] True dimension list and category counts per dataset (against §1, which is from documentation)
- [ ] How many NACE activities and FDI items actually return data for Tunisia, versus the 81 and 20 on offer
- [ ] Which observation flags appear, and how much of the grid is suppressed
- [ ] Whether `bop_fdi6_pos` really carries both `IMM` and `UIE` for a partner this small
- [ ] Whether CORS genuinely permits a call from `observablehq.com`
- [ ] Response size and wall-clock time, which decide whether chunking is needed at all

---

## 7. First use: European FDI to Tunisia

**The question (2026-11-11):** European FDI to Tunisia, earliest year available, as granular as the API
allows, called directly from an observablehq.com notebook.

**What the source can answer:** positions, flows and income from 2007 to 2024, by EU reporting country,
by economic activity, by FDI item, with and without special purpose entities, and — for positions —
under both the immediate and the ultimate-counterpart view.

**What it cannot:** anything before 2007 (the BPM5 predecessors run only 2008–2012 and
`bop_fdi_main` was discontinued in 2018, so there is no longer series to recover); non-European
investors; and, probably, a large share of the activity-level detail, which confidentiality will
suppress for a partner this size.

**The approach taken:** filter only on partner and currency, leave every other dimension unfiltered so
it returns in full, request the whole period in one call per table and fall back to per-year chunks only
if Eurostat refuses — and record which of the two happened, so §6 can be written from behaviour rather
than from assumption. **Not yet executed:** the outage in 6.2 intervened, and the question was answered
from OECD FDI instead (`oecd-fdi.md` §7), which gave 41,263 rows of positions for EU-OECD reporters.
Eurostat remains the better source for an EU-wide figure, so this is unfinished rather than abandoned.

### Classification decisions (Eduardo, 2026-11-11)

| Decision | Choice | What it means in practice |
|---|---|---|
| Default measure | **Positions (stocks)** | "FDI to country X" means the accumulated stock unless asked otherwise. Flows and income are reached for when the question is about momentum or about returns. |
| Counterpart view | **Ultimate investing economy** | Charts attribute capital to its ultimate owner, not to the conduit. The cost is thinner coverage and more suppressed cells; the benefit is that "biggest investor" claims survive scrutiny. |
| SPE treatment | **Both, with the difference labelled** | Every default position chart carries two series, or one series plus a visible phantom-investment gap. The gap is content, not a caveat. |
| Atlas or working | **Working only, for now** | Shelf entry, lives in `src/working/`, no registry entry, not in the navigation. Ask again when a chart exists and can be looked at. Topic placement deferred — the activity breakdown pulls towards 01, 02 and 06 at once. |

**A tension in those choices, recorded so it is not a surprise later.** Ultimate counterpart *and*
SPE-split *and* NACE activity detail *and* a small partner are four constraints that multiply. Each cut
narrows the published grid, and confidentiality suppression bites hardest exactly where all four meet.
The likely outcome is that the ultimate-counterpart view is available for Tunisia at the total-activity
level and largely empty once cut by NACE. If so, the workable shape is: ultimate counterpart for the
headline "who really invests" chart, immediate counterpart for anything cut by activity, and the
discrepancy stated in the prose. The run will settle which of these is fantasy.

---

## 8. Learned through use

*Add a dated line whenever a query or chart teaches something that belongs here.*

- 2026-11-11: **The Statistics API was unavailable for a day**, returning the Commission's
  "Server temporarily unavailable" page; Eurostat's own API demonstration notebook failed at the same
  time. Full account and the debugging lesson in 6.2. A source that can vanish for a day is a source
  that must be snapshotted.
- 2026-11-11: **`TypeError: Failed to fetch` is not diagnostic.** It covers an unreachable host, a
  refused connection, a missing CORS header and an HTML error page from a redirect, with no status and
  no message. Distinguish with a browser tab plus a `mode: "no-cors"` retry before suspecting the query.
- 2026-11-11: **The DBnomics mirror is unreachable from a browser notebook**, so it cannot serve as the
  browser-side fallback for a Eurostat outage. Script-side only.
- 2026-11-11: **Granularity comes from omitting dimensions, not from listing codes.** Enumerated values
  hit a ~50-category limit; an omitted dimension returns everything it has.
- 2026-11-11: **There is no pre-2007 European FDI series to stitch.** `bop_fdi_pos_r2` covers 2008–2012
  only and `bop_fdi_main` is discontinued, so the BPM6 tables are both the most detailed *and* the
  longest. One methodology, no break — unusually clean for this kind of question.
- 2026-11-11: **JSON-stat is a hypercube, not a table.** Positions are row-major with the last dimension
  varying fastest, and `status` carries Eurostat's own observation flags — which is exactly what the
  atlas asterisk is supposed to be built from.
- 2026-11-11: **Four classification decisions taken** (§7): positions as default, ultimate counterpart,
  SPE difference shown rather than hidden, working-only for now. The first three are deliberately the
  more demanding options, and they stack — see the tension note in §7.
- 2026-11-11: **When a source is down, substitute rather than wait, and label the substitution.** The
  Tunisia question was answered from OECD FDI the same day. The two sources are not interchangeable
  (§5), so the chart footer, not a footnote, has to say which one it is.
