# Reference: country table (BACI / Comtrade codes, V202601)

> The **one** country table of the atlas. Repository file: `reference/countries.csv` (this page prints the same rows).
> Built 2026-11-03 from BACI's `country_codes_V202601.csv` (238 rows), Eduardo's `global_south_UN.csv`, and the two maps in `reference/geo/`.
> Shared by the BACI card and the future UN Comtrade card, because BACI inherits Comtrade's codes.

## Columns
| Column | Meaning |
|---|---|
| `code` | BACI / Comtrade numeric code. **Join trade data on this.** |
| `ISO2`, `ISO3` | As in BACI's file. Namibia's ISO2 is the text `NA`. ISO3 is **not unique** (BEL, DEU, SDN appear twice). |
| `ISO num.` | Filled only where it differs from `code`. `countrycode(..., "iso3n")` and most map files use ISO numeric (France 250, USA 840), which **never match BACI**. |
| `atlas ISO3` | The key to everything else (regions, maps, other sources). 490 → `TWN`; 697 and 711 have none. |
| `status` | `current`, `historical` (only in early years) or `nes` (residual, not a country) |
| `South` | Global South flag from `reference/groupings/global_south_UN.csv` (yes/no; blank = not in that list) |
| `world map` / `grid` | Whether the country can be drawn on `world_countries.geojson` / `world_grid.json` (current entities only) |

## Things to know
- **Taiwan is inconsistent in the Global South list.** The list marks 158 "China, Taiwan Province of" as `yes` but 490 "Chinese Taipei" as `no`. BACI only uses 490, so **Taiwan is counted as North** in every chart built on this list. Decide once which you mean.
- **Neither map has Taiwan or Hong Kong.** Trade charts about semiconductors or China cannot show them on a map until they are added.
- 35 current BACI entities are on neither map, mostly small territories (Bermuda, Gibraltar, Guam, Macao, the Dutch Caribbean…). The world map is missing Greenland; the grid adds 28 small states that the world map draws as points.
- The grid file uses `PSX` for Palestine (ISO is `PSE`); matching on ISO2 `PS` works.
- Display names should come from the atlas country table, not from BACI's `Name` column (shortened Comtrade style; the raw file's accents are double-encoded and are repaired here).

| Code | Name | ISO2 | ISO3 | ISO num. | atlas ISO3 | Status | South | World map | Grid | Note |
|---:|---|---|---|---:|---|---|---|---|---|---|
| 4 | Afghanistan | AF | AFG |  | AFG | current | yes | yes | yes |  |
| 8 | Albania | AL | ALB |  | ALB | current | no | yes | yes |  |
| 12 | Algeria | DZ | DZA |  | DZA | current | yes | yes | yes |  |
| 16 | American Samoa | AS | ASM |  | ASM | current | yes | no | no |  |
| 20 | Andorra | AD | AND |  | AND | current | no | yes | yes |  |
| 24 | Angola | AO | AGO |  | AGO | current | yes | yes | yes |  |
| 28 | Antigua and Barbuda | AG | ATG |  | ATG | current | yes | yes | yes |  |
| 31 | Azerbaijan | AZ | AZE |  | AZE | current | yes | yes | yes |  |
| 32 | Argentina | AR | ARG |  | ARG | current | yes | yes | yes |  |
| 36 | Australia | AU | AUS |  | AUS | current | no | yes | yes |  |
| 40 | Austria | AT | AUT |  | AUT | current | no | yes | yes |  |
| 44 | Bahamas | BS | BHS |  | BHS | current | yes | yes | yes |  |
| 48 | Bahrain | BH | BHR |  | BHR | current | yes | yes | yes |  |
| 50 | Bangladesh | BD | BGD |  | BGD | current | yes | yes | yes |  |
| 51 | Armenia | AM | ARM |  | ARM | current | yes | yes | yes |  |
| 52 | Barbados | BB | BRB |  | BRB | current | yes | yes | yes |  |
| 56 | Belgium | BE | BEL |  | BEL | current | no | yes | yes | From 1999 |
| 58 | Belgium-Luxembourg (...1998) | BE | BEL |  | BEL | historical |  |  |  | Shares ISO3 BEL with 56 |
| 60 | Bermuda | BM | BMU |  | BMU | current | no | no | no |  |
| 64 | Bhutan | BT | BTN |  | BTN | current | yes | yes | yes |  |
| 68 | Bolivia (Plurinational State of) | BO | BOL |  | BOL | current | yes | yes | yes |  |
| 70 | Bosnia Herzegovina | BA | BIH |  | BIH | current | no | yes | yes |  |
| 72 | Botswana | BW | BWA |  | BWA | current | yes | yes | yes |  |
| 76 | Brazil | BR | BRA |  | BRA | current | yes | yes | yes |  |
| 84 | Belize | BZ | BLZ |  | BLZ | current | yes | yes | yes |  |
| 86 | Br. Indian Ocean Terr. | IO | IOT |  | IOT | current | yes | no | no |  |
| 90 | Solomon Isds | SB | SLB |  | SLB | current | yes | yes | yes |  |
| 92 | Br. Virgin Isds | VG | VGB |  | VGB | current | yes | no | no |  |
| 96 | Brunei Darussalam | BN | BRN |  | BRN | current | yes | yes | yes |  |
| 100 | Bulgaria | BG | BGR |  | BGR | current | no | yes | yes |  |
| 104 | Myanmar | MM | MMR |  | MMR | current | yes | yes | yes |  |
| 108 | Burundi | BI | BDI |  | BDI | current | yes | yes | yes |  |
| 112 | Belarus | BY | BLR |  | BLR | current | no | yes | yes |  |
| 116 | Cambodia | KH | KHM |  | KHM | current | yes | yes | yes |  |
| 120 | Cameroon | CM | CMR |  | CMR | current | yes | yes | yes |  |
| 124 | Canada | CA | CAN |  | CAN | current | no | yes | yes |  |
| 132 | Cabo Verde | CV | CPV |  | CPV | current | yes | yes | yes |  |
| 136 | Cayman Isds | KY | CYM |  | CYM | current | yes | no | no |  |
| 140 | Central African Rep. | CF | CAF |  | CAF | current | yes | yes | yes |  |
| 144 | Sri Lanka | LK | LKA |  | LKA | current | yes | yes | yes |  |
| 148 | Chad | TD | TCD |  | TCD | current | yes | yes | yes |  |
| 152 | Chile | CL | CHL |  | CHL | current | yes | yes | yes |  |
| 156 | China | CN | CHN |  | CHN | current | yes | yes | yes |  |
| 162 | Christmas Isds | CX | CXR |  | CXR | current | no | no | no |  |
| 166 | Cocos Isds | CC | CCK |  | CCK | current | no | no | no |  |
| 170 | Colombia | CO | COL |  | COL | current | yes | yes | yes |  |
| 174 | Comoros | KM | COM |  | COM | current | yes | yes | yes |  |
| 175 | Mayotte (Overseas France) | YT | MYT |  | MYT | current | yes | no | no |  |
| 178 | Congo | CG | COG |  | COG | current | yes | yes | yes |  |
| 180 | Dem. Rep. of the Congo | CD | COD |  | COD | current | yes | yes | yes |  |
| 184 | Cook Isds | CK | COK |  | COK | current | yes | no | no |  |
| 188 | Costa Rica | CR | CRI |  | CRI | current | yes | yes | yes |  |
| 191 | Croatia | HR | HRV |  | HRV | current | no | yes | yes |  |
| 192 | Cuba | CU | CUB |  | CUB | current | yes | yes | yes |  |
| 196 | Cyprus | CY | CYP |  | CYP | current | no | yes | yes |  |
| 200 | Czechoslovakia (...1992) | CS | CSK |  | CSK | historical | no |  |  |  |
| 203 | Czechia | CZ | CZE |  | CZE | current | no | yes | yes |  |
| 204 | Benin | BJ | BEN |  | BEN | current | yes | yes | yes |  |
| 208 | Denmark | DK | DNK |  | DNK | current | no | yes | yes |  |
| 212 | Dominica | DM | DMA |  | DMA | current | yes | yes | yes |  |
| 214 | Dominican Rep. | DO | DOM |  | DOM | current | yes | yes | yes |  |
| 218 | Ecuador | EC | ECU |  | ECU | current | yes | yes | yes |  |
| 222 | El Salvador | SV | SLV |  | SLV | current | yes | yes | yes |  |
| 226 | Equatorial Guinea | GQ | GNQ |  | GNQ | current | yes | yes | yes |  |
| 231 | Ethiopia | ET | ETH |  | ETH | current | yes | yes | yes |  |
| 232 | Eritrea | ER | ERI |  | ERI | current | yes | yes | yes |  |
| 233 | Estonia | EE | EST |  | EST | current | no | yes | yes |  |
| 238 | Falkland Isds (Malvinas) | FK | FLK |  | FLK | current | yes | no | no |  |
| 242 | Fiji | FJ | FJI |  | FJI | current | yes | yes | yes |  |
| 246 | Finland | FI | FIN |  | FIN | current | no | yes | yes |  |
| 251 | France | FR | FRA | 250 | FRA | current | no | yes | yes | France customs territory, incl. Monaco |
| 258 | French Polynesia | PF | PYF |  | PYF | current | yes | no | no |  |
| 260 | Fr. South Antarctic Terr. | TF | ATF |  | ATF | current | yes | no | no |  |
| 262 | Djibouti | DJ | DJI |  | DJI | current | yes | yes | yes |  |
| 266 | Gabon | GA | GAB |  | GAB | current | yes | yes | yes |  |
| 268 | Georgia | GE | GEO |  | GEO | current | yes | yes | yes |  |
| 270 | Gambia | GM | GMB |  | GMB | current | yes | yes | yes |  |
| 275 | State of Palestine | PS | PSE |  | PSE | current | yes | yes | yes |  |
| 276 | Germany | DE | DEU |  | DEU | current | no | yes | yes |  |
| 278 | Dem. Rep. of Germany (...1990) | DD | DDR |  | DDR | historical | no |  |  |  |
| 280 | Fed. Rep. of Germany (...1990) | DE | DEU |  | DEU | historical | no |  |  | Shares ISO3 DEU with 276 |
| 288 | Ghana | GH | GHA |  | GHA | current | yes | yes | yes |  |
| 292 | Gibraltar | GI | GIB |  | GIB | current | no | no | no |  |
| 296 | Kiribati | KI | KIR |  | KIR | current | yes | yes | yes |  |
| 300 | Greece | GR | GRC |  | GRC | current | no | yes | yes |  |
| 304 | Greenland | GL | GRL |  | GRL | current | no | no | yes |  |
| 308 | Grenada | GD | GRD |  | GRD | current | yes | yes | yes |  |
| 316 | Guam | GU | GUM |  | GUM | current | yes | no | no |  |
| 320 | Guatemala | GT | GTM |  | GTM | current | yes | yes | yes |  |
| 324 | Guinea | GN | GIN |  | GIN | current | yes | yes | yes |  |
| 328 | Guyana | GY | GUY |  | GUY | current | yes | yes | yes |  |
| 332 | Haiti | HT | HTI |  | HTI | current | yes | yes | yes |  |
| 340 | Honduras | HN | HND |  | HND | current | yes | yes | yes |  |
| 344 | China, Hong Kong SAR | HK | HKG |  | HKG | current | yes | no | no |  |
| 348 | Hungary | HU | HUN |  | HUN | current | no | yes | yes |  |
| 352 | Iceland | IS | ISL |  | ISL | current | no | yes | yes |  |
| 360 | Indonesia | ID | IDN |  | IDN | current | yes | yes | yes |  |
| 364 | Iran | IR | IRN |  | IRN | current | yes | yes | yes |  |
| 368 | Iraq | IQ | IRQ |  | IRQ | current | yes | yes | yes |  |
| 372 | Ireland | IE | IRL |  | IRL | current | no | yes | yes |  |
| 376 | Israel | IL | ISR |  | ISR | current | no | yes | yes |  |
| 380 | Italy | IT | ITA |  | ITA | current | no | yes | yes |  |
| 384 | Côte d'Ivoire | CI | CIV |  | CIV | current | yes | yes | yes |  |
| 388 | Jamaica | JM | JAM |  | JAM | current | yes | yes | yes |  |
| 392 | Japan | JP | JPN |  | JPN | current | no | yes | yes |  |
| 398 | Kazakhstan | KZ | KAZ |  | KAZ | current | yes | yes | yes |  |
| 400 | Jordan | JO | JOR |  | JOR | current | yes | yes | yes |  |
| 404 | Kenya | KE | KEN |  | KEN | current | yes | yes | yes |  |
| 408 | Dem. People's Rep. of Korea | KP | PRK |  | PRK | current | yes | yes | yes |  |
| 410 | Rep. of Korea | KR | KOR |  | KOR | current | no | yes | yes |  |
| 414 | Kuwait | KW | KWT |  | KWT | current | yes | yes | yes |  |
| 417 | Kyrgyzstan | KG | KGZ |  | KGZ | current | yes | yes | yes |  |
| 418 | Lao People's Dem. Rep. | LA | LAO |  | LAO | current | yes | yes | yes |  |
| 422 | Lebanon | LB | LBN |  | LBN | current | yes | yes | yes |  |
| 426 | Lesotho | LS | LSO |  | LSO | current | yes | yes | yes |  |
| 428 | Latvia | LV | LVA |  | LVA | current | no | yes | yes |  |
| 430 | Liberia | LR | LBR |  | LBR | current | yes | yes | yes |  |
| 434 | Libya | LY | LBY |  | LBY | current | yes | yes | yes |  |
| 440 | Lithuania | LT | LTU |  | LTU | current | no | yes | yes |  |
| 442 | Luxembourg | LU | LUX |  | LUX | current | no | yes | yes | From 1999 |
| 446 | China, Macao SAR | MO | MAC |  | MAC | current | yes | no | no |  |
| 450 | Madagascar | MG | MDG |  | MDG | current | yes | yes | yes |  |
| 454 | Malawi | MW | MWI |  | MWI | current | yes | yes | yes |  |
| 458 | Malaysia | MY | MYS |  | MYS | current | yes | yes | yes |  |
| 462 | Maldives | MV | MDV |  | MDV | current | yes | yes | yes |  |
| 466 | Mali | ML | MLI |  | MLI | current | yes | yes | yes |  |
| 470 | Malta | MT | MLT |  | MLT | current | no | yes | yes |  |
| 478 | Mauritania | MR | MRT |  | MRT | current | yes | yes | yes |  |
| 480 | Mauritius | MU | MUS |  | MUS | current | yes | yes | yes |  |
| 484 | Mexico | MX | MEX |  | MEX | current | yes | yes | yes |  |
| 490 | Other Asia, nes | — | S19 | 158 | TWN | nes | no | no | no | De facto Taiwan (CEPII). Global South list says 'no' here but 'yes' for 158 Taiwan |
| 496 | Mongolia | MN | MNG |  | MNG | current | yes | yes | yes |  |
| 498 | Rep. of Moldova | MD | MDA |  | MDA | current | no | yes | yes |  |
| 499 | Montenegro | ME | MNE |  | MNE | current | no | yes | yes |  |
| 500 | Montserrat | MS | MSR |  | MSR | current | yes | no | no |  |
| 504 | Morocco | MA | MAR |  | MAR | current | yes | yes | yes |  |
| 508 | Mozambique | MZ | MOZ |  | MOZ | current | yes | yes | yes |  |
| 512 | Oman | OM | OMN |  | OMN | current | yes | yes | yes |  |
| 516 | Namibia | NA | NAM |  | NAM | current | yes | yes | yes | ISO2 is 'NA': read as text |
| 520 | Nauru | NR | NRU |  | NRU | current | yes | yes | yes |  |
| 524 | Nepal | NP | NPL |  | NPL | current | yes | yes | yes |  |
| 528 | Netherlands | NL | NLD |  | NLD | current | no | yes | yes |  |
| 530 | Netherlands Antilles (...2010) | AN | ANT |  | ANT | historical | yes |  |  | Split into 531, 534, 535 in 2011 |
| 531 | Curaçao | CW | CUW |  | CUW | current | yes | no | no |  |
| 533 | Aruba | AW | ABW |  | ABW | current | yes | no | no |  |
| 534 | Saint Maarten | SX | SXM |  | SXM | current | yes | no | no |  |
| 535 | Bonaire | BQ | BES |  | BES | current | yes | no | no |  |
| 540 | New Caledonia | NC | NCL |  | NCL | current | yes | no | no |  |
| 548 | Vanuatu | VU | VUT |  | VUT | current | yes | yes | yes |  |
| 554 | New Zealand | NZ | NZL |  | NZL | current | no | yes | yes |  |
| 558 | Nicaragua | NI | NIC |  | NIC | current | yes | yes | yes |  |
| 562 | Niger | NE | NER |  | NER | current | yes | yes | yes |  |
| 566 | Nigeria | NG | NGA |  | NGA | current | yes | yes | yes |  |
| 570 | Niue | NU | NIU |  | NIU | current | yes | no | no |  |
| 574 | Norfolk Isds | NF | NFK |  | NFK | current | no | no | no |  |
| 579 | Norway | NO | NOR | 578 | NOR | current | no | yes | yes | incl. Svalbard & Jan Mayen |
| 580 | N. Mariana Isds | MP | MNP |  | MNP | current | yes | no | no |  |
| 583 | FS Micronesia | FM | FSM |  | FSM | current | yes | yes | yes |  |
| 584 | Marshall Isds | MH | MHL |  | MHL | current | yes | yes | yes |  |
| 585 | Palau | PW | PLW |  | PLW | current | yes | yes | yes |  |
| 586 | Pakistan | PK | PAK |  | PAK | current | yes | yes | yes |  |
| 591 | Panama | PA | PAN |  | PAN | current | yes | yes | yes |  |
| 598 | Papua New Guinea | PG | PNG |  | PNG | current | yes | yes | yes |  |
| 600 | Paraguay | PY | PRY |  | PRY | current | yes | yes | yes |  |
| 604 | Peru | PE | PER |  | PER | current | yes | yes | yes |  |
| 608 | Philippines | PH | PHL |  | PHL | current | yes | yes | yes |  |
| 612 | Pitcairn | PN | PCN |  | PCN | current | yes | no | no |  |
| 616 | Poland | PL | POL |  | POL | current | no | yes | yes |  |
| 620 | Portugal | PT | PRT |  | PRT | current | no | yes | yes |  |
| 624 | Guinea-Bissau | GW | GNB |  | GNB | current | yes | yes | yes |  |
| 626 | Timor-Leste | TL | TLS |  | TLS | current | yes | yes | yes |  |
| 634 | Qatar | QA | QAT |  | QAT | current | yes | yes | yes |  |
| 642 | Romania | RO | ROU |  | ROU | current | no | yes | yes |  |
| 643 | Russian Federation | RU | RUS |  | RUS | current | no | yes | yes |  |
| 646 | Rwanda | RW | RWA |  | RWA | current | yes | yes | yes |  |
| 652 | Saint Barthélemy | BL | BLM |  | BLM | current | yes | no | no |  |
| 654 | Saint Helena | SH | SHN |  | SHN | current | yes | no | no |  |
| 659 | Saint Kitts and Nevis | KN | KNA |  | KNA | current | yes | yes | yes |  |
| 660 | Anguilla | AI | AIA |  | AIA | current | yes | no | no |  |
| 662 | Saint Lucia | LC | LCA |  | LCA | current | yes | yes | yes |  |
| 666 | Saint Pierre and Miquelon | PM | SPM |  | SPM | current | no | no | no |  |
| 670 | Saint Vincent and the Grenadines | VC | VCT |  | VCT | current | yes | yes | yes |  |
| 674 | San Marino | SM | SMR |  | SMR | current | no | yes | yes |  |
| 678 | Sao Tome and Principe | ST | STP |  | STP | current | yes | yes | yes |  |
| 682 | Saudi Arabia | SA | SAU |  | SAU | current | yes | yes | yes |  |
| 686 | Senegal | SN | SEN |  | SEN | current | yes | yes | yes |  |
| 688 | Serbia | RS | SRB |  | SRB | current | no | yes | yes |  |
| 690 | Seychelles | SC | SYC |  | SYC | current | yes | yes | yes |  |
| 694 | Sierra Leone | SL | SLE |  | SLE | current | yes | yes | yes |  |
| 697 | Europe EFTA, nes | — | R20 |  | — | nes |  |  |  | Unallocated EFTA trade |
| 699 | India | IN | IND | 356 | IND | current | yes | yes | yes |  |
| 702 | Singapore | SG | SGP |  | SGP | current | yes | yes | yes |  |
| 703 | Slovakia | SK | SVK |  | SVK | current | no | yes | yes |  |
| 704 | Viet Nam | VN | VNM |  | VNM | current | yes | yes | yes |  |
| 705 | Slovenia | SI | SVN |  | SVN | current | no | yes | yes |  |
| 706 | Somalia | SO | SOM |  | SOM | current | yes | yes | yes |  |
| 710 | South Africa | ZA | ZAF |  | ZAF | current | yes | yes | yes |  |
| 711 | Southern African Customs Union (...1999) | — | ZA1 |  | — | historical |  |  |  | SACU bloc until 1999 (ZAF, BWA, NAM, LSO, SWZ) |
| 716 | Zimbabwe | ZW | ZWE |  | ZWE | current | yes | yes | yes |  |
| 724 | Spain | ES | ESP |  | ESP | current | no | yes | yes |  |
| 728 | South Sudan | SS | SSD |  | SSD | current | yes | yes | yes | From 2012 |
| 729 | Sudan | SD | SDN |  | SDN | current | yes | yes | yes | From 2012 (without South Sudan) |
| 736 | Sudan (...2011) | SD | SDN |  | SDN | historical | yes |  |  | Shares ISO3 SDN with 729; includes South Sudan |
| 740 | Suriname | SR | SUR |  | SUR | current | yes | yes | yes |  |
| 748 | Eswatini | SZ | SWZ |  | SWZ | current | yes | yes | yes |  |
| 752 | Sweden | SE | SWE |  | SWE | current | no | yes | yes |  |
| 757 | Switzerland | CH | CHE | 756 | CHE | current | no | yes | yes | incl. Liechtenstein |
| 760 | Syria | SY | SYR |  | SYR | current | yes | yes | yes |  |
| 762 | Tajikistan | TJ | TJK |  | TJK | current | yes | yes | yes |  |
| 764 | Thailand | TH | THA |  | THA | current | yes | yes | yes |  |
| 768 | Togo | TG | TGO |  | TGO | current | yes | yes | yes |  |
| 772 | Tokelau | TK | TKL |  | TKL | current | yes | no | no |  |
| 776 | Tonga | TO | TON |  | TON | current | yes | yes | yes |  |
| 780 | Trinidad and Tobago | TT | TTO |  | TTO | current | yes | yes | yes |  |
| 784 | United Arab Emirates | AE | ARE |  | ARE | current | yes | yes | yes |  |
| 788 | Tunisia | TN | TUN |  | TUN | current | yes | yes | yes |  |
| 792 | Türkiye | TR | TUR |  | TUR | current | yes | yes | yes |  |
| 795 | Turkmenistan | TM | TKM |  | TKM | current | yes | yes | yes |  |
| 796 | Turks and Caicos Isds | TC | TCA |  | TCA | current | yes | no | no |  |
| 798 | Tuvalu | TV | TUV |  | TUV | current | yes | yes | yes |  |
| 800 | Uganda | UG | UGA |  | UGA | current | yes | yes | yes |  |
| 804 | Ukraine | UA | UKR |  | UKR | current | no | yes | yes |  |
| 807 | North Macedonia | MK | MKD |  | MKD | current | no | yes | yes |  |
| 810 | USSR (...1990) | SU | SUN |  | SUN | historical | no |  |  |  |
| 818 | Egypt | EG | EGY |  | EGY | current | yes | yes | yes |  |
| 826 | United Kingdom | GB | GBR |  | GBR | current | no | yes | yes |  |
| 834 | United Rep. of Tanzania | TZ | TZA |  | TZA | current | yes | yes | yes |  |
| 842 | USA | US | USA | 840 | USA | current | no | yes | yes | incl. Puerto Rico & US Virgin Islands |
| 849 | US Misc. Pacific Isds | PU | PUS | 581 | PUS | current | no | no | no | US Minor Outlying Islands |
| 854 | Burkina Faso | BF | BFA |  | BFA | current | yes | yes | yes |  |
| 858 | Uruguay | UY | URY |  | URY | current | yes | yes | yes |  |
| 860 | Uzbekistan | UZ | UZB |  | UZB | current | yes | yes | yes |  |
| 862 | Venezuela | VE | VEN |  | VEN | current | yes | yes | yes |  |
| 876 | Wallis and Futuna Isds | WF | WLF |  | WLF | current | yes | no | no |  |
| 882 | Samoa | WS | WSM |  | WSM | current | yes | yes | yes |  |
| 887 | Yemen | YE | YEM |  | YEM | current | yes | yes | yes |  |
| 891 | Serbia and Montenegro (...2005) | CS | SCG |  | SCG | historical | no |  |  | Split into 688 and 499 in 2006 |
| 894 | Zambia | ZM | ZMB |  | ZMB | current | yes | yes | yes |  |
