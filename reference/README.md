# reference/

Lookup tables that every source and every script shares. They are small, public and rarely change, so they live in the repository (unlike `data/`, which is never committed).

| Path | What it is | Origin |
|---|---|---|
| **`countries.csv`** | **The country table of the atlas.** One row per BACI/Comtrade code (238): repaired names, ISO codes, `atlas_iso3` (490 → TWN), `status` (current / historical / nes), `global_south`, and whether each map can draw it. Human-readable copy: `notes/datacards/reference/country-codes.md` | Built 2026-11-03 from the files below |
| `baci/country_codes_V202601.csv` | BACI country table **exactly as downloaded** | CEPII, BACI V202601 |
| `groupings/global_south_UN.csv` | Global South yes/no by BACI code, **as supplied** | UNCTAD-based list compiled by Eduardo; vintage not recorded |
| `geo/world_countries.geojson` | Country shapes (Natural Earth admin-0, 195 features) plus 28 small states as points. Key: `iso_a3` (shapes) or `iso_a2` (points) | Eduardo's map file |
| `geo/world_grid.json` | Tile grid map: one tile per country (`x`, `y`, 28 × 23), small states included. Key: `alpha3`, `alpha2` | Eduardo's map file |
| `hs/products/product_codes_HS{92,22}_V202601.csv` | Every HS 6-digit code BACI uses | CEPII, BACI V202601 |
| `hs/descriptions/hs{1992…2022}_descriptions.csv` | Official descriptions at 2, 4 and 6 digits for all seven HS editions | UNSD, via R package `concordance` 2.1.0 (MIT) |
| `hs/concordance/hs{newer}_to_hs{older}.csv` | Conversion from every edition to every older one (21 files), one older code per newer code | UNSD conversion tables, via `concordance` 2.1.0 |

## Known gaps in the maps
- **Neither map has Taiwan or Hong Kong.** Both matter for semiconductor and China trade charts.
- The world map has no Greenland. The grid uses `PSX` for Palestine (ISO: `PSE`), so match on `alpha2` = `PS`.
- The grid's `countryCode` is ISO numeric (France 250, USA 840), **not** BACI's code. Join through `atlas_iso3`.
- The grid's `region` / `subRegion` fields have errors (Kosovo is coded as Eastern Asia). Use `regions/regions.yaml` for regions, never the map file.

## Concordance notes
- Newer → older only. Each newer code maps to exactly one older code; a split is assigned whole, so converted values are approximate.
- `hs1992` means HS 1988/92.
- BACI already publishes every edition converted. The concordance is for finding where a modern product sits in an old code, and for Comtrade data reported in different editions.
- `271000` (petroleum oils) is in BACI's HS22 list but not in the UNSD table.
