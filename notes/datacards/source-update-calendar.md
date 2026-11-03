# Source update calendar

> One row per source. It records when each source publishes, how we notice, and what has to change in the project when it does.
> This is the human-readable version of what the quarterly GitHub Actions check (PROMPTS.md step 17) will automate.
> Last edited 2026-11-03. **Only BACI is filled in.** The other rows are placeholders until each source has its own card. Nothing here is guessed.

## Calendar

| Source | Card | Release pattern | Usual month | Last release seen | Next expected | Latest year in data | How we notice |
|---|---|---|---|---|---|---|---|
| BACI (CEPII), HS92 + HS22 | `baci-cepii.md` | Annual, one version for all HS revisions | **January** (V202501: 30 Jan 2025; V202601: 22 Jan 2026) | **V202601**, 2026-01-22 | **V202701, late January 2027** | 2024 (provisional) → 2025 expected | Version string on the CEPII download page |
| UN Comtrade | (to write) | Continuous: countries submit monthly and annual data on their own schedules | n/a | — | — | — | API `getLiveUpdate` / data-availability endpoint |
| OECD CRS | (to write) | to verify | to verify | — | — | — | — |
| AidData GCDF | (to write) | Irregular, major versions | to verify | — | — | — | — |
| Kiel product classification | (to write) | to verify | to verify | — | — | — | — |

## What to do when a source updates

### BACI: annual routine (late January)
1. Download the new zip(s) for **each HS revision we keep** (HS92 and HS22). Store them unchanged in `data/raw/baci/{YYYY-MM-DD}/`. Never overwrite the previous snapshot.
2. Re-read the new readme and the release notes on the CEPII page. If anything changed in the variables, units or country list, update the card.
3. Diff the new `country_codes` and `product_codes` against the reference files (`reference/country-codes.md`, `reference/hs-products.md`) and record any changes.
4. Re-run the BACI loader for **all years**, not only the new one. Past flows are revised, and CEPII advises against mixing versions.
5. **Move the asterisk.** The year that was provisional (e.g. 2024) is no longer flagged, and the new latest year (e.g. 2025) is.
6. Update the card header (`describes release …`), this calendar, and `current_vintage` in the registry if BACI has been promoted by then.
7. Rebuild. Every chart footer and citation picks up the new version automatically, provided it is read from the data and not typed in.
8. Spot-check two or three charts you know well against the previous version. Large jumps usually come from revised source data, not from errors, but it is worth knowing before a reader asks.

### Template for the other sources
Steps: download/snapshot → re-read docs → diff reference tables → re-run loader → move provisional flags → update card + calendar + registry → rebuild → spot-check.
