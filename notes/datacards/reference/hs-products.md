# Reference: Harmonized System (HS) products in BACI

> Written 2026-11-03 from `product_codes_HS92_V202601.csv` and `product_codes_HS22_V202601.csv` (BACI V202601).
> Shared by the BACI card and the future UN Comtrade card. Comtrade uses the same HS codes, plus national 8–10 digit lines.

## Where the full lists are
The full lists are **in the GitHub repository**, not printed here (about 1.1 MB, which would crowd out everything else when this file is read):
- `reference/hs/products/`: every 6-digit code BACI uses, for HS92 and HS22
- `reference/hs/descriptions/`: official 2-, 4- and 6-digit descriptions for **all seven HS editions** (1992–2022)
- `reference/hs/concordance/`: conversion tables from every edition to every older one (21 files)

Claude Code working in the repository searches these files directly. This file holds what you need in order to reason about them.

## File format (both revisions)
- Columns: `code, description`. All codes are **6 characters, read as text** (HS92 has 347 codes with a leading zero; HS22 has 571).
- Residual codes: `999999` "Commodities not specified according to kind". HS92 also has `9999AA` (legacy non-WCO code).
- All 97 chapters (2-digit) exist in both revisions. Chapter 77 is reserved and empty. Chapter 98 is national use.

## HS92 compared with HS22: the numbers

| | HS92 | HS22 |
|---|---:|---:|
| 6-digit codes | 5,022 | 5,609 |
| Codes present in both | 3,963 | 3,963 |
| …of which the **description changed** | 1,146 | 1,146 |
| Codes only in this revision | 1,059 | 1,646 |
| BACI years | 1995–2024 | 2022–2024 |

The chapters with the most HS22-only codes are 03 (fish, 178), 29 (organic chemicals, 170), 85 (electrical, 104), 44 (wood, 99), 84 (machinery, 90), 38 (chemical products, 69), 72 (iron and steel, 53) and 81 (other base metals, 41).

**Trap: the same code can mean different things in different revisions.** 1,146 shared codes have a changed description, and a code whose description did *not* change may still have lost part of its scope to a new code. **Never join HS92 and HS22 series on the code itself.** Use the concordance, and record that you used one.

## Concordance: converting between editions
- **Source:** UNSD conversion tables, as packaged in the R package `concordance` 2.1.0 (MIT licence). Stored as CSV in `reference/hs/concordance/hs{newer}_to_hs{older}.csv`.
- **Direction:** newer → older only. Each newer code maps to **exactly one** older code. When a code was split, UNSD assigns the whole value to one older code, so converted values are approximate.
- **Coverage against BACI:** all HS22 codes in BACI are covered except `271000` (a BACI aggregate for petroleum oils, which also exists in HS92). Every target code exists in BACI's HS92 list. 486 HS92 codes are never a target, because they were merged away or renamed.
- **When you need it:** rarely for BACI itself, because CEPII already publishes every edition converted (BACI HS92 for 2024 *is* a conversion). You need it (a) to find which HS92 code contains a modern product, (b) for Comtrade data reported in different editions, and (c) if a product list (e.g. Kiel) is defined in a different edition from the data.
- Examples (HS22 → HS92): lithium-ion batteries `850760` → `850780`; processors `854231` → `854211`; chip-making machines `848610` → `847989` (a catch-all "other machines" code); battery-electric cars `870380` → `870390`; gallium and similar `811231` → `811291`. **A modern product converted into a broad old code cannot be separated from the rest of that code.**

## Codes the atlas topics care about (how they differ between revisions)

| Product | HS92 | HS22 | Consequence |
|---|---|---|---|
| Lithium-ion batteries | not separate (inside `8507xx`, "other accumulators") | `850760` | Battery trade before HS2012 cannot be isolated |
| Semiconductor manufacturing equipment | does not exist (`8486` was created in HS2007) | `848610`–`848690` | Chip-equipment export-control questions need HS07 or later |
| Integrated circuits | `854211, 854219, 854220, 854280, 854290` | `854231, 854232, 854233, 854239, 854290` (by function: processors, memory, amplifiers, other) | Complete re-split, so no code-to-code match |
| Diodes, transistors, photovoltaic cells | `854140`, `854150` | `854141`–`854149` (LEDs and PV split out), `854151`, `854159` | Solar cells are only separable in recent revisions |
| Cobalt (unwrought, mattes, waste) | `810510, 810590` | `810520, 810530, 810590` | Re-split |
| Gallium, germanium, indium, vanadium etc. (`8112`) | `811211`–`811299` | `811212`–`811252` and more | Several minor metals (China's 2023 export-control targets) only get their own codes in HS22 |
| Rare-earth compounds | `284610, 284690` | `284610, 284690` | Same codes, but the descriptions may differ |
| Rare-earth metals (`2805`) | `280511, 280519, 280521, 280522, 280530, 280540` | `280511, 280512, 280519, 280530, 280540` | Re-split |
| Ores: manganese, copper, cobalt, tin, tungsten… | `2602`, `2603`, `2605`, `2609`, `2611`… | same | Mostly stable, so long series are fine |
| Lithium carbonate | `283691` | `283691` | Stable code |
| Cars by drive type | `8703` with no electric split | `870340`–`870380` (hybrids, plug-ins, battery-electric) | EV trade only from HS17 |

These rows come from comparing the two code lists, not from a concordance. **Treat them as signposts, not mappings.**

## How to choose a revision, as a rule of thumb
- **Long trend, broad product groups** (energy, food, "manufactures", North/South): HS92.
- **A specific modern product** (chips, batteries, EVs, minor metals): HS17 or HS22, and accept a short series.
- **The same chart never mixes revisions.** The revision is part of the chart's source line and citation.

## HS chapters (2-digit), short titles

| Ch | Title | Ch | Title |
|---|---|---|---|
| 01 | Live animals | 50 | Silk |
| 02 | Meat | 51 | Wool, animal hair |
| 03 | Fish, crustaceans | 52 | Cotton |
| 04 | Dairy, eggs, honey | 53 | Other vegetable textile fibres |
| 05 | Other animal products | 54 | Man-made filaments |
| 06 | Live plants, flowers | 55 | Man-made staple fibres |
| 07 | Vegetables | 56 | Wadding, felt, twine, ropes |
| 08 | Fruit, nuts | 57 | Carpets |
| 09 | Coffee, tea, spices | 58 | Special woven fabrics |
| 10 | Cereals | 59 | Coated, laminated textiles |
| 11 | Milling products | 60 | Knitted fabrics |
| 12 | Oil seeds | 61 | Apparel, knitted |
| 13 | Lacs, gums, resins | 62 | Apparel, not knitted |
| 14 | Vegetable plaiting materials | 63 | Other made-up textiles |
| 15 | Fats and oils | 64 | Footwear |
| 16 | Meat and fish preparations | 65 | Headgear |
| 17 | Sugar | 66 | Umbrellas, walking sticks |
| 18 | Cocoa | 67 | Feathers, artificial flowers |
| 19 | Cereal preparations | 68 | Stone, plaster, cement articles |
| 20 | Vegetable and fruit preparations | 69 | Ceramics |
| 21 | Misc. edible preparations | 70 | Glass |
| 22 | Beverages | 71 | Pearls, precious stones and metals, **gold** |
| 23 | Food residues, animal feed | 72 | Iron and steel |
| 24 | Tobacco | 73 | Articles of iron or steel |
| 25 | Salt, sulphur, earths, stone, cement | 74 | Copper |
| 26 | **Ores, slag and ash** | 75 | Nickel |
| 27 | **Mineral fuels, oils** (oil, gas, coal) | 76 | Aluminium |
| 28 | **Inorganic chemicals** (incl. rare-earth compounds, lithium) | 77 | (reserved) |
| 29 | Organic chemicals | 78 | Lead |
| 30 | Pharmaceuticals | 79 | Zinc |
| 31 | Fertilisers | 80 | Tin |
| 32 | Tanning, dyes, paints | 81 | **Other base metals** (cobalt, tungsten, gallium, germanium…) |
| 33 | Essential oils, cosmetics | 82 | Tools, cutlery |
| 34 | Soap, waxes | 83 | Misc. base-metal articles |
| 35 | Albuminoids, glues, enzymes | 84 | **Machinery, computers** |
| 36 | Explosives, pyrotechnics | 85 | **Electrical machinery, electronics, semiconductors** |
| 37 | Photographic goods | 86 | Railway equipment |
| 38 | Misc. chemical products | 87 | Vehicles |
| 39 | Plastics | 88 | Aircraft, spacecraft |
| 40 | Rubber | 89 | Ships, boats |
| 41 | Raw hides, leather | 90 | Optical, medical, measuring instruments |
| 42 | Leather articles | 91 | Clocks, watches |
| 43 | Furskins | 92 | Musical instruments |
| 44 | Wood | 93 | **Arms and ammunition** |
| 45 | Cork | 94 | Furniture, lighting |
| 46 | Basketwork | 95 | Toys, sports equipment |
| 47 | Pulp | 96 | Misc. manufactured articles |
| 48 | Paper | 97 | Works of art, antiques |
| 49 | Printed matter | 99 | Not specified (`999999`) |

Chapter titles are shortened. The official wording is in `reference/hs/descriptions/` (2-digit rows).

## Still to add
- [ ] Kiel product classification: its join key and its HS edition.
- [ ] Topic product baskets (e.g. `reference/hs/baskets/critical_minerals.csv`): which codes count as "cobalt" or "semiconductors" is a research decision, made once and named in the source line.
