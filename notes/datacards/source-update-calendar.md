# Source update calendar

> One row per source. It records when each source publishes, how we notice, and what has to change in the project when it does.
> This is the human-readable version of what the quarterly GitHub Actions check (PROMPTS.md step 17) will automate.
> Last edited 2026-11-10. **BACI is filled in from use; OECD CRS from documentation only** (its card is v0.2 draft and no data has been loaded into the repository yet). The other rows are placeholders until each source has its own card. Nothing here is guessed: anything not confirmed says *to verify*.

## Calendar

| Source | Card | Release pattern | Usual month | Last release seen | Next expected | Latest year in data | How we notice |
|---|---|---|---|---|---|---|---|
| BACI (CEPII), HS92 + HS22 | `baci-cepii.md` | Annual, one version for all HS revisions | **January** (V202501: 30 Jan 2025; V202601: 22 Jan 2026) | **V202601**, 2026-01-22 | **V202701, late January 2027** | 2024 (provisional) → 2025 expected | Version string on the CEPII download page |
| UN Comtrade | (to write) | Continuous: countries submit monthly and annual data on their own schedules | n/a | — | — | — | API `getLiveUpdate` / data-availability endpoint |
| OECD CRS | `oecd-crs.md` (v0.2 draft) | Annual, activity-level data for the previous year. Preliminary **aggregate** ODA, which is not CRS, appears separately each April. | **December** | Dataflow `DSD_CRS@DF_CRS` **v1.7**, Data Explorer "last updated" 2026-10-08 | **December 2026**, for 2025 flows | 2024 *(to verify)* | Dataflow version string and the "Last updated" timestamp for `OECD.DCD.FSD:DSD_CRS@DF_CRS` in the Data Explorer |
| AidData GCDF | (to write) | Irregular, major versions | to verify | — | — | — | — |
| Kiel product classification | (to write) | to verify | to verify | — | — | — | — |

## What to do when a source updates

### BACI: annual routine (late January)
1. Run `python loaders/baci_download.py --load`. It finds the new version, downloads HS92 and HS22 into a new `data/raw/baci/{today}/` folder (the previous snapshot is never touched), unzips them and builds the Parquet. If it stops on a new country code, add that code to `reference/countries.csv` and run `python loaders/baci_load.py data/raw/baci/{today}` again.
2. Re-read the new readme and the release notes on the CEPII page. If anything changed in the variables, units or country list, update the card.
3. Diff the new `country_codes` and `product_codes` against the reference files (`reference/country-codes.md`, `reference/hs-products.md`) and record any changes.
4. The loader always rebuilds **all years** of a revision, not only the new one. Past flows are revised, and CEPII advises against mixing versions.
5. **Move the asterisk.** The year that was provisional (e.g. 2024) is no longer flagged, and the new latest year (e.g. 2025) is.
6. Update the card header (`describes release …`), this calendar, and `current_vintage` in the registry if BACI has been promoted by then.
7. Rebuild. Every chart footer and citation picks up the new version automatically, provided it is read from the data and not typed in.
8. Spot-check two or three charts you know well against the previous version. Large jumps usually come from revised source data, not from errors, but it is worth knowing before a reader asks.

### OECD CRS: annual routine (December) — planned, not yet exercised
1. Check the dataflow version in the Data Explorer. A move from 1.7 to 1.8 is not cosmetic: dimensions and code lists can change, and the version is pinned in every request URL.
2. Re-run the loader for **all years**, not only the new one. Providers resubmit, so past years change between releases; Germany's reporting in 2024 was flagged by the OECD as late, which is exactly the kind of thing that moves earlier figures.
3. Diff the recipient and channel code lists against `reference/countries.csv` and the card's channel table. A new channel code, or an organisation moved to a different parent category, changes any channel-share series.
4. Re-check the first year with channel and modality coverage. If it moves, the "share channelled through NGOs" charts change their starting year.
5. Record the new extraction date and dataflow version in the manifest; both appear in the chart footer and the citation.
6. Spot-check the Germany→Tunisia benchmark in the card (§9) before trusting the rebuild.

### Template for the other sources
Steps: download/snapshot → re-read docs → diff reference tables → re-run loader → move provisional flags → update card + calendar + registry → rebuild → spot-check.
