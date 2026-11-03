# Reference: BACI / Comtrade country codes (V202601)

> Generated 2026-11-03 from `country_codes_V202601.csv` (BACI release V202601, 238 rows).
> Shared by the BACI card and the future UN Comtrade card, because BACI inherits Comtrade's codes.
> **Changes from the raw file:** accented names are repaired (the raw file is double-encoded UTF-8), and Namibia's ISO2 `NA` is shown as text. Nothing else is altered.

## How to use this table
- **Join trade data on `code`** (BACI `i`/`j`, Comtrade `reporterCode`/`partnerCode`). Never join on ISO3 alone, because BEL, DEU and SDN appear twice.
- `ISO num.` is filled **only where it differs** from the BACI code. The `countrycode` R package returns ISO numeric, so `countrycode("France","country.name","iso3n")` gives 250, **which does not exist in BACI** (France is 251). The same happens for the USA (842), India (699), Norway (579) and Switzerland (757).
- `Status`: `current`, `historical` (only exists in early years), or `nes` (residual, not a country).
- Display names should come from the atlas country table, not from the `Name` column.

| Code | Name | ISO2 | ISO3 | ISO num. | Status | Note |
|---:|---|---|---|---:|---|---|
| 4 | Afghanistan | AF | AFG |  | current |  |
| 8 | Albania | AL | ALB |  | current |  |
| 12 | Algeria | DZ | DZA |  | current |  |
| 16 | American Samoa | AS | ASM |  | current |  |
| 20 | Andorra | AD | AND |  | current |  |
| 24 | Angola | AO | AGO |  | current |  |
| 28 | Antigua and Barbuda | AG | ATG |  | current |  |
| 31 | Azerbaijan | AZ | AZE |  | current |  |
| 32 | Argentina | AR | ARG |  | current |  |
| 36 | Australia | AU | AUS |  | current |  |
| 40 | Austria | AT | AUT |  | current |  |
| 44 | Bahamas | BS | BHS |  | current |  |
| 48 | Bahrain | BH | BHR |  | current |  |
| 50 | Bangladesh | BD | BGD |  | current |  |
| 51 | Armenia | AM | ARM |  | current |  |
| 52 | Barbados | BB | BRB |  | current |  |
| 56 | Belgium | BE | BEL |  | current | From 1999 |
| 58 | Belgium-Luxembourg (...1998) | BE | BEL |  | historical | Shares ISO3 BEL with code 56 |
| 60 | Bermuda | BM | BMU |  | current |  |
| 64 | Bhutan | BT | BTN |  | current |  |
| 68 | Bolivia (Plurinational State of) | BO | BOL |  | current |  |
| 70 | Bosnia Herzegovina | BA | BIH |  | current |  |
| 72 | Botswana | BW | BWA |  | current |  |
| 76 | Brazil | BR | BRA |  | current |  |
| 84 | Belize | BZ | BLZ |  | current |  |
| 86 | Br. Indian Ocean Terr. | IO | IOT |  | current |  |
| 90 | Solomon Isds | SB | SLB |  | current |  |
| 92 | Br. Virgin Isds | VG | VGB |  | current |  |
| 96 | Brunei Darussalam | BN | BRN |  | current |  |
| 100 | Bulgaria | BG | BGR |  | current |  |
| 104 | Myanmar | MM | MMR |  | current |  |
| 108 | Burundi | BI | BDI |  | current |  |
| 112 | Belarus | BY | BLR |  | current |  |
| 116 | Cambodia | KH | KHM |  | current |  |
| 120 | Cameroon | CM | CMR |  | current |  |
| 124 | Canada | CA | CAN |  | current |  |
| 132 | Cabo Verde | CV | CPV |  | current |  |
| 136 | Cayman Isds | KY | CYM |  | current |  |
| 140 | Central African Rep. | CF | CAF |  | current |  |
| 144 | Sri Lanka | LK | LKA |  | current |  |
| 148 | Chad | TD | TCD |  | current |  |
| 152 | Chile | CL | CHL |  | current |  |
| 156 | China | CN | CHN |  | current |  |
| 162 | Christmas Isds | CX | CXR |  | current |  |
| 166 | Cocos Isds | CC | CCK |  | current |  |
| 170 | Colombia | CO | COL |  | current |  |
| 174 | Comoros | KM | COM |  | current |  |
| 175 | Mayotte (Overseas France) | YT | MYT |  | current |  |
| 178 | Congo | CG | COG |  | current |  |
| 180 | Dem. Rep. of the Congo | CD | COD |  | current |  |
| 184 | Cook Isds | CK | COK |  | current |  |
| 188 | Costa Rica | CR | CRI |  | current |  |
| 191 | Croatia | HR | HRV |  | current |  |
| 192 | Cuba | CU | CUB |  | current |  |
| 196 | Cyprus | CY | CYP |  | current |  |
| 200 | Czechoslovakia (...1992) | CS | CSK |  | historical | Not relevant from 1995 on |
| 203 | Czechia | CZ | CZE |  | current |  |
| 204 | Benin | BJ | BEN |  | current |  |
| 208 | Denmark | DK | DNK |  | current |  |
| 212 | Dominica | DM | DMA |  | current |  |
| 214 | Dominican Rep. | DO | DOM |  | current |  |
| 218 | Ecuador | EC | ECU |  | current |  |
| 222 | El Salvador | SV | SLV |  | current |  |
| 226 | Equatorial Guinea | GQ | GNQ |  | current |  |
| 231 | Ethiopia | ET | ETH |  | current |  |
| 232 | Eritrea | ER | ERI |  | current |  |
| 233 | Estonia | EE | EST |  | current |  |
| 238 | Falkland Isds (Malvinas) | FK | FLK |  | current |  |
| 242 | Fiji | FJ | FJI |  | current |  |
| 246 | Finland | FI | FIN |  | current |  |
| 251 | France | FR | FRA | 250 | current | France customs territory, incl. Monaco |
| 258 | French Polynesia | PF | PYF |  | current |  |
| 260 | Fr. South Antarctic Terr. | TF | ATF |  | current |  |
| 262 | Djibouti | DJ | DJI |  | current |  |
| 266 | Gabon | GA | GAB |  | current |  |
| 268 | Georgia | GE | GEO |  | current |  |
| 270 | Gambia | GM | GMB |  | current |  |
| 275 | State of Palestine | PS | PSE |  | current |  |
| 276 | Germany | DE | DEU |  | current | From 1991 |
| 278 | Dem. Rep. of Germany (...1990) | DD | DDR |  | historical | Not relevant from 1995 on |
| 280 | Fed. Rep. of Germany (...1990) | DE | DEU |  | historical | Shares ISO3 DEU with code 276 |
| 288 | Ghana | GH | GHA |  | current |  |
| 292 | Gibraltar | GI | GIB |  | current |  |
| 296 | Kiribati | KI | KIR |  | current |  |
| 300 | Greece | GR | GRC |  | current |  |
| 304 | Greenland | GL | GRL |  | current |  |
| 308 | Grenada | GD | GRD |  | current |  |
| 316 | Guam | GU | GUM |  | current |  |
| 320 | Guatemala | GT | GTM |  | current |  |
| 324 | Guinea | GN | GIN |  | current |  |
| 328 | Guyana | GY | GUY |  | current |  |
| 332 | Haiti | HT | HTI |  | current |  |
| 340 | Honduras | HN | HND |  | current |  |
| 344 | China, Hong Kong SAR | HK | HKG |  | current |  |
| 348 | Hungary | HU | HUN |  | current |  |
| 352 | Iceland | IS | ISL |  | current |  |
| 360 | Indonesia | ID | IDN |  | current |  |
| 364 | Iran | IR | IRN |  | current |  |
| 368 | Iraq | IQ | IRQ |  | current |  |
| 372 | Ireland | IE | IRL |  | current |  |
| 376 | Israel | IL | ISR |  | current |  |
| 380 | Italy | IT | ITA |  | current |  |
| 384 | Côte d'Ivoire | CI | CIV |  | current |  |
| 388 | Jamaica | JM | JAM |  | current |  |
| 392 | Japan | JP | JPN |  | current |  |
| 398 | Kazakhstan | KZ | KAZ |  | current |  |
| 400 | Jordan | JO | JOR |  | current |  |
| 404 | Kenya | KE | KEN |  | current |  |
| 408 | Dem. People's Rep. of Korea | KP | PRK |  | current |  |
| 410 | Rep. of Korea | KR | KOR |  | current |  |
| 414 | Kuwait | KW | KWT |  | current |  |
| 417 | Kyrgyzstan | KG | KGZ |  | current |  |
| 418 | Lao People's Dem. Rep. | LA | LAO |  | current |  |
| 422 | Lebanon | LB | LBN |  | current |  |
| 426 | Lesotho | LS | LSO |  | current |  |
| 428 | Latvia | LV | LVA |  | current |  |
| 430 | Liberia | LR | LBR |  | current |  |
| 434 | Libya | LY | LBY |  | current |  |
| 440 | Lithuania | LT | LTU |  | current |  |
| 442 | Luxembourg | LU | LUX |  | current | From 1999 |
| 446 | China, Macao SAR | MO | MAC |  | current |  |
| 450 | Madagascar | MG | MDG |  | current |  |
| 454 | Malawi | MW | MWI |  | current |  |
| 458 | Malaysia | MY | MYS |  | current |  |
| 462 | Maldives | MV | MDV |  | current |  |
| 466 | Mali | ML | MLI |  | current |  |
| 470 | Malta | MT | MLT |  | current |  |
| 478 | Mauritania | MR | MRT |  | current |  |
| 480 | Mauritius | MU | MUS |  | current |  |
| 484 | Mexico | MX | MEX |  | current |  |
| 490 | Other Asia, nes | — | S19 | 158 | nes | De facto Taiwan. File says S19; label as 'Taiwan (reported as Other Asia, n.e.s.)' |
| 496 | Mongolia | MN | MNG |  | current |  |
| 498 | Rep. of Moldova | MD | MDA |  | current |  |
| 499 | Montenegro | ME | MNE |  | current |  |
| 500 | Montserrat | MS | MSR |  | current |  |
| 504 | Morocco | MA | MAR |  | current |  |
| 508 | Mozambique | MZ | MOZ |  | current |  |
| 512 | Oman | OM | OMN |  | current |  |
| 516 | Namibia | NA | NAM |  | current | ISO2 is 'NA': read with na = character() |
| 520 | Nauru | NR | NRU |  | current |  |
| 524 | Nepal | NP | NPL |  | current |  |
| 528 | Netherlands | NL | NLD |  | current |  |
| 530 | Netherlands Antilles (...2010) | AN | ANT |  | historical | Split into 531, 534, 535 in 2011 |
| 531 | Curaçao | CW | CUW |  | current |  |
| 533 | Aruba | AW | ABW |  | current |  |
| 534 | Saint Maarten | SX | SXM |  | current |  |
| 535 | Bonaire | BQ | BES |  | current |  |
| 540 | New Caledonia | NC | NCL |  | current |  |
| 548 | Vanuatu | VU | VUT |  | current |  |
| 554 | New Zealand | NZ | NZL |  | current |  |
| 558 | Nicaragua | NI | NIC |  | current |  |
| 562 | Niger | NE | NER |  | current |  |
| 566 | Nigeria | NG | NGA |  | current |  |
| 570 | Niue | NU | NIU |  | current |  |
| 574 | Norfolk Isds | NF | NFK |  | current |  |
| 579 | Norway | NO | NOR | 578 | current | incl. Svalbard & Jan Mayen |
| 580 | N. Mariana Isds | MP | MNP |  | current |  |
| 583 | FS Micronesia | FM | FSM |  | current |  |
| 584 | Marshall Isds | MH | MHL |  | current |  |
| 585 | Palau | PW | PLW |  | current |  |
| 586 | Pakistan | PK | PAK |  | current |  |
| 591 | Panama | PA | PAN |  | current |  |
| 598 | Papua New Guinea | PG | PNG |  | current |  |
| 600 | Paraguay | PY | PRY |  | current |  |
| 604 | Peru | PE | PER |  | current |  |
| 608 | Philippines | PH | PHL |  | current |  |
| 612 | Pitcairn | PN | PCN |  | current |  |
| 616 | Poland | PL | POL |  | current |  |
| 620 | Portugal | PT | PRT |  | current |  |
| 624 | Guinea-Bissau | GW | GNB |  | current |  |
| 626 | Timor-Leste | TL | TLS |  | current |  |
| 634 | Qatar | QA | QAT |  | current |  |
| 642 | Romania | RO | ROU |  | current |  |
| 643 | Russian Federation | RU | RUS |  | current |  |
| 646 | Rwanda | RW | RWA |  | current |  |
| 652 | Saint Barthélemy | BL | BLM |  | current |  |
| 654 | Saint Helena | SH | SHN |  | current |  |
| 659 | Saint Kitts and Nevis | KN | KNA |  | current |  |
| 660 | Anguilla | AI | AIA |  | current |  |
| 662 | Saint Lucia | LC | LCA |  | current |  |
| 666 | Saint Pierre and Miquelon | PM | SPM |  | current |  |
| 670 | Saint Vincent and the Grenadines | VC | VCT |  | current |  |
| 674 | San Marino | SM | SMR |  | current |  |
| 678 | Sao Tome and Principe | ST | STP |  | current |  |
| 682 | Saudi Arabia | SA | SAU |  | current |  |
| 686 | Senegal | SN | SEN |  | current |  |
| 688 | Serbia | RS | SRB |  | current |  |
| 690 | Seychelles | SC | SYC |  | current |  |
| 694 | Sierra Leone | SL | SLE |  | current |  |
| 697 | Europe EFTA, nes | — | R20 |  | nes | Unallocated EFTA trade, no geometry |
| 699 | India | IN | IND | 356 | current | India |
| 702 | Singapore | SG | SGP |  | current |  |
| 703 | Slovakia | SK | SVK |  | current |  |
| 704 | Viet Nam | VN | VNM |  | current |  |
| 705 | Slovenia | SI | SVN |  | current |  |
| 706 | Somalia | SO | SOM |  | current |  |
| 710 | South Africa | ZA | ZAF |  | current |  |
| 711 | Southern African Customs Union (...1999) | — | ZA1 |  | historical | SACU bloc until 1999 (ZAF, BWA, NAM, LSO, SWZ) |
| 716 | Zimbabwe | ZW | ZWE |  | current |  |
| 724 | Spain | ES | ESP |  | current |  |
| 728 | South Sudan | SS | SSD |  | current | From 2012 |
| 729 | Sudan | SD | SDN |  | current | From 2012 (without South Sudan) |
| 736 | Sudan (...2011) | SD | SDN |  | historical | Shares ISO3 SDN with code 729; includes South Sudan |
| 740 | Suriname | SR | SUR |  | current |  |
| 748 | Eswatini | SZ | SWZ |  | current |  |
| 752 | Sweden | SE | SWE |  | current |  |
| 757 | Switzerland | CH | CHE | 756 | current | incl. Liechtenstein |
| 760 | Syria | SY | SYR |  | current |  |
| 762 | Tajikistan | TJ | TJK |  | current |  |
| 764 | Thailand | TH | THA |  | current |  |
| 768 | Togo | TG | TGO |  | current |  |
| 772 | Tokelau | TK | TKL |  | current |  |
| 776 | Tonga | TO | TON |  | current |  |
| 780 | Trinidad and Tobago | TT | TTO |  | current |  |
| 784 | United Arab Emirates | AE | ARE |  | current |  |
| 788 | Tunisia | TN | TUN |  | current |  |
| 792 | Türkiye | TR | TUR |  | current |  |
| 795 | Turkmenistan | TM | TKM |  | current |  |
| 796 | Turks and Caicos Isds | TC | TCA |  | current |  |
| 798 | Tuvalu | TV | TUV |  | current |  |
| 800 | Uganda | UG | UGA |  | current |  |
| 804 | Ukraine | UA | UKR |  | current |  |
| 807 | North Macedonia | MK | MKD |  | current |  |
| 810 | USSR (...1990) | SU | SUN |  | historical | Not relevant from 1995 on |
| 818 | Egypt | EG | EGY |  | current |  |
| 826 | United Kingdom | GB | GBR |  | current |  |
| 834 | United Rep. of Tanzania | TZ | TZA |  | current |  |
| 842 | USA | US | USA | 840 | current | incl. Puerto Rico & US Virgin Islands |
| 849 | US Misc. Pacific Isds | PU | PUS | 581 | current | US Minor Outlying Islands |
| 854 | Burkina Faso | BF | BFA |  | current |  |
| 858 | Uruguay | UY | URY |  | current |  |
| 860 | Uzbekistan | UZ | UZB |  | current |  |
| 862 | Venezuela | VE | VEN |  | current |  |
| 876 | Wallis and Futuna Isds | WF | WLF |  | current |  |
| 882 | Samoa | WS | WSM |  | current |  |
| 887 | Yemen | YE | YEM |  | current |  |
| 891 | Serbia and Montenegro (...2005) | CS | SCG |  | historical | Split into 688 Serbia and 499 Montenegro in 2006 |
| 894 | Zambia | ZM | ZMB |  | current |  |
