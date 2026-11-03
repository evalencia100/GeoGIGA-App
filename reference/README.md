# reference/

Lookup tables that every source and every script shares: country codes, product codes and the conversions between product-code editions. They are small, public and rarely change, so they live in the repository (unlike `data/raw/`, which is never committed).

| Path | What it is | Origin |
|---|---|---|
| `baci/country_codes_V202601.csv` | BACI country table **exactly as downloaded** | CEPII, BACI V202601 |
| `baci/country_codes_V202601_clean.csv` | Same table, repaired: names fixed, Namibia's `NA` kept, plus `iso_numeric`, `atlas_iso3` (490 → TWN) and `status` (current / historical / nes) | Derived, 2026-11-03 |
| `hs/products/product_codes_HS92_V202601.csv` | Every HS92 6-digit code BACI uses (5,022) | CEPII, BACI V202601 |
| `hs/products/product_codes_HS22_V202601.csv` | Every HS22 6-digit code BACI uses (5,609) | CEPII, BACI V202601 |
| `hs/descriptions/hs{1992…2022}_descriptions.csv` | Official descriptions at 2, 4 and 6 digits for all seven HS editions (`code, desc`) | UNSD, via the R package `concordance` 2.1.0 (MIT licence) |
| `hs/concordance/hs{newer}_to_hs{older}.csv` | Conversion from every edition to every older one (21 files). **One row per newer code, mapped to exactly one older code.** | UNSD conversion tables, via `concordance` 2.1.0 |

## Things to know before using the concordance files
- **The tables go one way only, from newer to older.** Converting old codes into new ones is not one-to-one: an old code may have been split into several.
- **A split is assigned whole to one code.** If an HS22 code came from two HS92 codes, UNSD picks one. Values converted this way are approximations.
- **`hs1992` means HS 1988/92** (the first edition, "HS0").
- **BACI already publishes every edition converted for you.** For a long series you normally just use the BACI HS92 files and need no concordance. The concordance is for *finding* which old code holds a modern product (e.g. lithium-ion batteries HS22 `850760` → HS92 `850780`), and for Comtrade data reported in different editions.
- `271000` (petroleum oils) is in BACI's HS22 list but not in the UNSD table. BACI uses it as an aggregate, and it also exists in HS92.
