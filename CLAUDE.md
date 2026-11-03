# Geoeconomics Atlas

## What this is

A data atlas for geoeconomics and geopolitics, organised by **topic** first,
with region and country as cuts within each topic. It is built for qualitative
researchers — area-studies scholars, analysts, journalists — not for
econometricians. They need reliable numbers that support a written argument,
with honest labelling of where the numbers come from and how far to trust them.

Written output is the point. Charts support prose; they do not replace it.

## Who I am

I am a geoeconomics researcher, not a software engineer, and never have been.
I know R well — dplyr, readr, R Markdown — and I am now moving to **Python in
VS Code** for this project. I can read JavaScript and follow what it does; I
cannot debug it alone. I am new to Python, Claude Code, GitHub and VS Code. I
have a browser-based Coder workspace with VS Code and a terminal, but assume I
have not used either before and do not know where things are in the interface.

**Your job in every session is to be both tutor and enabler.** Every answer has
two parts, in this order:

1. **The concept, in plain language.** What this piece of the system is for,
   why it exists, how it relates to something I already understand. Use
   analogies to R (dplyr in particular), to spreadsheets, to writing and
   publishing — not to other programming tools I do not know. Avoid developer
   idiom and shorthand. If a term is unavoidable (commit, build, repository,
   dependency, package, virtual environment), define it the first time you use
   it, once, in a sentence.
2. **The solution, complete and ready to use.** Whole files or whole functions
   I can copy and paste. Never partial diffs, never "add this line somewhere".
   Comment anything non-obvious for a reader who knows R but not Python or
   JavaScript.

Further rules:

- When I need to run something in the terminal, give me the exact command, say
  what it will do **before** I run it, and tell me what I should see if it
  worked.
- When I need to do something in VS Code or on GitHub, describe where to click.
  Assume I have never seen the interface.
- Never silently install a dependency or change the architecture. Say so first
  and tell me what it costs.
- When there are several reasonable options, give me the trade-off in two
  sentences and recommend one. Do not hand me a menu.
- Build one small thing that runs, then stop and let me look at it.
- Prefer boring, obvious code over clever code. I have to maintain this for
  years.
- **Documents I supply (old scripts, notes) are evidence, not templates.**
  Assess them critically — they may be outdated or wrong — and use them to
  write something better, telling me what you changed and why.

## Stack

- **Observable Notebook Kit** — the open-source tooling behind Observable
  Notebooks 2.0. A notebook is a plain `.html` file in this repository; a build
  command turns a folder of them into a static site. Nothing runs on a server
  while a visitor reads. Pin the version in `package.json`; it is still a
  technology preview and can change between releases.
- **Python** for data loaders and question scripts, with **DuckDB** as the
  query engine (it reads CSV and Parquet directly with SQL). Packages are
  pinned in `requirements.txt` and installed in a project virtual environment
  (`.venv`). *Decision 2026-11-03: Python replaces R for loaders, so that
  scripts can be run and tested by Claude as well as by me.* R stays fine for
  my own exploration, but nothing in the pipeline depends on it.
- **DuckDB + Parquet** as the internal data format.
- **Observable Plot** for charts; D3 only where Plot cannot do it.
- **giga-viz**, a shared component library in this repository (see below).
- **GitHub Actions** for scheduled source checks.
- Hosting: undecided. Keep the build output a plain static folder so it can go
  anywhere.

**Why Notebook Kit and not Observable Framework.** Framework still works, but
Observable's development effort has moved to Notebooks 2.0 and the Framework
repository has been largely static since May 2026. Notebook Kit now has what
this project needs: data loaders, Parquet output, and DuckDB and Postgres
connectors. No project code had been written when the decision was taken, so
the switch happened before the build rather than after.

## Writing code in this project: the dialect rule

**Most Observable code on the public internet is the old Observable JavaScript
dialect. Models trained on it — including you — produce it by reflex. Do not.**

New code in this project is Notebooks 2.0 vanilla JavaScript:

- No `viewof`.
- No implicit returns from a cell. Nothing is displayed because it happens to
  be the last expression.
- Explicit `display()` when something should appear on the page.
- Cells are standard ES modules. Imports are real `import` statements.

If I paste you older Observable code of my own, **tell me what would need to
change and why — do not silently rewrite it.** I need to learn the difference,
not have it hidden from me.

## My other notebooks

I have separate GIGA Focus notebooks on observablehq.com, currently running in
the deprecated 2018 standard library compatibility mode. They work. They are
not being migrated right now, and nothing in this project should assume they
will be. New work goes in the new style. The `giga-viz` library is the bridge
between the two: a chart built for the atlas should be usable in a GIGA Focus
notebook and the other way round.

## How I work week to week

Two kinds of work live in this one repository, and the second is how the first
one grows.

**Working notebooks are the normal week.** The trigger is usually a GIGA
publication or a colleague's question: a figure is needed, and needed soon.
That work goes in `src/working/`, as a notebook with a real chart id, with any
new dataset recorded on the shelf. It is built and deployed along with
everything else, so it has its own URL.

**I share a link, never a file.** Interactivity is the point — a colleague
should be able to change the region or the year themselves, in a browser, with
no account and nothing to install. Do not treat a PNG as the deliverable
unless I ask for one for print.

**Ask me, at the start of every piece of chart work: is this one for the atlas,
or working only?** The answer changes what you do, so do not guess:

- **Atlas-bound** — then the source has to be one I will stand behind in print.
  Say so before you build anything, and tell me if the source is shelf-only, so
  I can decide whether to vet and promote it first.
- **Working only** — a shelf entry is enough. Keep it in `src/working/`, do not
  touch the registry, and do not add it to the navigation.
- **I don't know yet** — assume working only, and ask again when the chart is
  finished and I can see it.

**Promotion is by reference, not by rebuilding.** When a working chart earns a
place in the atlas, I promote its source from shelf to registry, write the
prose, and the topic page refers to the existing chart by its id. The chart
itself does not move and is not rewritten. Never promote anything unasked.

**Treat `src/working/` as unpublished.** Some of it is draft material for
pieces that are not out yet. It is deployed behind a password; never link to a
working notebook from a public atlas page, and ask before making anything in
there publicly reachable.

**Direction of travel with observablehq.com.** Notebook Kit can download a
notebook from observablehq.com into this repository; there is no supported way
to push one up. So authoring happens here. observablehq.com is for the case
where a colleague wants to edit the code themselves — and even then, import
`giga-viz` from its published URL rather than pasting the theme into the page.

## Architecture rules

1. **The registry is the spine.** `registry/sources.yaml` lists every vetted
   data source with its metadata. Loaders, the freshness display and the
   quarterly check all read from it. Nothing reaches a published atlas page
   without an entry.

2. **Many formats in, one format through the middle.** Loaders read whatever a
   source publishes — CSV, xlsx, JSON, Stata, shapefiles, zips. After that,
   everything is Parquet. Exports to the user are CSV and Excel.

3. **Raw snapshots are never deleted and never committed.** Every download goes
   to `data/raw/{source_id}/{YYYY-MM-DD}/` unchanged. Git ignores that folder.

4. **Nothing is fetched at page-view time.** All data is baked in at build.

5. **Loaders are standalone Python scripts, not notebook cells.** Every loader
   is a script in `loaders/`, run deliberately (by me, from the Makefile or
   from GitHub Actions), writing Parquet into `data/`. Where a source has a
   stable download address, the loader downloads it too. **Notebooks only ever
   read Parquet.** An expensive or metered fetch must never happen because a
   page was rebuilt.

6. **Fetch class decides behaviour.** Each source is `open`, `metered` or
   `manual`. Metered and manual sources are fetched deliberately and stored;
   never re-pulled on a routine build.

7. **Credentials come from environment variables.** Never hardcoded, never
   committed, never printed in logs.

8. **One country table.** `reference/countries.csv` is the only place country
   codes, ISO3 keys and country groupings meet. Groupings are defined by ISO3;
   numeric codes are never used to define a group.

## Source kinds

Every source is one of three, recorded as `kind` in the registry:

- **primary** — someone observed, counted or coded the phenomenon itself.
  Expert coding counts (V-Dem, UCDP, AidData, Afrobarometer).
- **aggregate** — harmonises existing databases (BACI, World Bank WDI).
- **index** — rescales and combines indicators into one number (ND-GAIN).

This is shown to users. The atlas is built on primary sources; indices appear
mainly as objects of study.

## Two tiers of data: shelf and registry

Two files, two standards.

**`registry/shelf.yaml` — the shelf.** Any dataset used for any graph. Minimal
fields: id, origin URL, date obtained, which notebook used it. No assessment
note. **Never shown to readers.** The shelf is a working record, so that
routine chart-making accumulates into something rather than evaporating.

**`registry/sources.yaml` — the registry.** A source that has been vetted and
will be stood behind in print. Full metadata and a written assessment note.
Shown to readers with its kind.

**Promotion is a deliberate act, performed by me**, when I decide to build a
topic page on that source. It is never automatic and you should never do it
unasked. The point of the two tiers is that the shelf lets working charts
accumulate **without lowering the standard of what readers see** — so a
shelf-only dataset backs working notebooks and GIGA Focus pieces, not a
published atlas page. Architecture rule 1 is unchanged by the shelf.

## Data cards

Every source gets a data card in `notes/datacards/` before it is used widely:
what one row is, what each column is and is not, codes and coverage, what the
source does not contain, access (API, free, licence), spatial attributes,
what matters for visualisation, how to wrangle it, and a "learned through use"
log. `notes/datacards/_relationships.md` holds what sits between sources;
`notes/datacards/source-update-calendar.md` holds when each one updates.
A concluded card (v1.0) improves through use, not through redrafting.

## Chart identity

**Every chart has a stable id from the moment it is created, e.g.
`01/cobalt-supplier-concentration`.** This is not a nicety to retrofit. The id
is the key for the export filename, the social image, the CSV, the citation,
and later the story references. A chart without an id cannot be exported,
cited or reused.

A chart is defined once and referenced by id from any page. The id scheme is
`{topic code}/{slug}`.

## The giga-viz component library

A plain JavaScript package in this repository, with **no framework
dependency**, usable from a Notebook Kit page, from a notebook on
observablehq.com, or from a bare HTML page. It holds:

- **The GIGA theme** — colour palettes (categorical, diverging, sequential),
  Helvetica Neue for headings, Georgia for body text, spacing.
- **The country table** — ISO3 to name to region, read from `regions.yaml`
  and `reference/countries.csv`.
- **The maps** — `reference/geo/world_countries.geojson` and
  `reference/geo/world_grid.json`.
- **`gigaChart()`** — one wrapper taking a chart id, a title written as the
  takeaway, a render function, the data, and the source metadata, returning a
  finished figure: header, chart, source-and-vintage footer, GIGA logo, and an
  export menu. **The export menu is a small overflow menu, not a row of
  buttons.**

Because `gigaChart` takes a render function rather than a finished picture, the
same definition can be rendered at page size in the browser and at social-card
size headlessly at build time.

## Navigation

Notebook Kit gives a build command and a custom page template, but no built-in
navigation. **Generate the navigation at build time from
`registry/sources.yaml` and `regions/regions.yaml`, and inject it through the
page template. Keep it plain.** No search box, no mega-menu. Working notebooks
never appear in it.

## Data quality: deliberately light

We flag, we do not catalogue.

- One asterisk per observation, taken from what the source itself says
  (provisional, estimated, modelled, interpolated, series break). We pass along
  the source's own admission; we do not make judgements of our own.
- One prose source note per source, written by me.
- Gaps are shown as gaps. Lines break rather than interpolating across missing
  years.

**Explicitly out of scope:** typed missingness categories, judgements about
whether a government suppressed data, computed confidence scores, uncertainty
palettes. Do not build these. Do not suggest them.

## Content structure

**Topics** (the top level):

| Code | Topic |
| --- | --- |
| 01 | Dependency and trade |
| 02 | Development finance |
| 03 | International finance |
| 04 | Diplomacy |
| 05 | Coercion and violence |
| 06 | Infrastructure and technology |
| 07 | Internal dynamics |

**Starting with 01 and 02 only.** Sources for the first build:

- 01: BACI (CEPII), Kiel product classification
- 02: OECD CRS, AidData GCDF

**Regions** come before topics in build order: a `regions.yaml` defining the
regional and sub-regional scheme, with countries allowed in more than one
region. Topics are then cut by that scheme.

**Stories** are the last thing to build: ordered, guided narratives that reuse
charts already built on topic pages. No scroll animation.

## Page anatomy

A topic page, cut to one region:

1. Title as a question
2. Three sentences of answer
3. 600–1000 words of argument, charts placed inside it
4. Three to six charts, each titled with its takeaway
5. Sources, each with its kind and my assessment
6. Related pages

## Export and sharing

Every chart needs: PNG for social, vector for print, CSV of the underlying
numbers, and a citation. The citation generator is a priority, not a nicety.
All four live in the `gigaChart` overflow menu.

**The primary way I share a chart is its link**, not a file — see "How I work
week to week". The exports are for print and for social media, not a substitute
for sending someone the page.

**Social images reuse the chart, not a second drawing path.** Because
`gigaChart` takes a render function, render it headlessly at build time at
social sizes, with the title, source line with vintage, and GIGA logo baked
into the picture — images travel without their page.

**Sharing is static.** Open Graph meta tags in the page template pointing at
that image, plus a copy-link button and a download-image button. **No
third-party share widgets.**

## Repository layout

```
CLAUDE.md                  this file
requirements.txt           pinned Python packages
registry/sources.yaml      vetted sources, shown to readers — the spine
registry/shelf.yaml        working datasets, not shown to readers
regions/regions.yaml       regional scheme
reference/                 shared lookup tables: countries.csv, HS codes and
                           concordances, maps (see reference/README.md)
loaders/                   standalone Python scripts, one or two per source
templates/                 copy-and-edit scripts for one-off questions
data/raw/                  dated snapshots (gitignored)
data/                      Parquet written by the loaders (gitignored)
packages/giga-viz/         shared component library (plain JavaScript)
src/                       notebooks (.html), one per page
src/template.html          Notebook Kit page template: header, nav, OG tags
src/topics/01-dependency/  one folder per topic
src/working/               working notebooks: deployed, password-protected,
                           never in the navigation
src/stories/               guided narratives (later)
notes/                     my source assessments, markdown
notes/datacards/           one data card per source, plus shared references
Makefile                   runs the loaders deliberately
.github/workflows/         scheduled source checks
```

## Things not to do

- Do not add a database server, an API backend, or user accounts.
- Do not add scroll-driven animation or sticky graphics.
- Do not fetch data from the browser at runtime.
- Do not write code that depends on a specific hosting provider.
- Do not build the data-quality features listed as out of scope above.
- Do not refactor broadly without asking. Small and incremental.
