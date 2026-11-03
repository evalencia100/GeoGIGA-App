# loaders/baci.R
# ---------------------------------------------------------------------------
# What this does
#   Turns one BACI release (the CSV files you downloaded from CEPII) into
#   Parquet files the atlas can query quickly. It runs once per release
#   (each January), never on a routine site build.
#
# Input   data/raw/baci/<snapshot-date>/   the unzipped CEPII files, unchanged:
#           BACI_HS92_Y1995_V202601.csv ... BACI_HS22_Y2024_V202601.csv
#           country_codes_V202601.csv
#           product_codes_HS92_V202601.csv, product_codes_HS22_V202601.csv
#
# Output  data/baci/hs_rev=92/t=2024/part-0.parquet   (one file per revision-year)
#         data/baci_meta/countries.parquet           (cleaned country table)
#         data/baci_meta/products_hs92.parquet, products_hs22.parquet
#
# Run it from the repository root, in the terminal:
#   Rscript loaders/baci.R 2026-01-22
#
# Packages: readr, dplyr, stringr, arrow
# ---------------------------------------------------------------------------

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(stringr)
  library(arrow)
})

# 1. Where to read from and write to -----------------------------------------

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) {
  stop("Tell me which snapshot to load, e.g.:  Rscript loaders/baci.R 2026-01-22")
}
raw_dir  <- file.path("data", "raw", "baci", args[1])
out_dir  <- file.path("data", "baci")
meta_dir <- file.path("data", "baci_meta")
if (!dir.exists(raw_dir)) stop("Folder not found: ", raw_dir)

# 2. Find the trade files and read year/revision/version from their NAMES ----
# Never from their position in a list: adding or removing one file would
# silently shift every year (this happened in the old Rmd).

trade_files <- tibble(path = list.files(
    raw_dir, pattern = "^BACI_HS\\d{2}_Y\\d{4}_V\\d{6}\\.csv$", full.names = TRUE)) |>
  mutate(
    hs_rev  = str_match(basename(path), "_HS(\\d{2})_")[, 2],      # "92", "22"
    year    = as.integer(str_match(basename(path), "_Y(\\d{4})_")[, 2]),
    version = str_match(basename(path), "_V(\\d{6})")[, 2]         # "202601"
  )

if (nrow(trade_files) == 0) stop("No BACI trade files in ", raw_dir)
if (n_distinct(trade_files$version) > 1) {
  stop("More than one BACI version in this folder. CEPII advises never mixing versions.")
}
version <- trade_files$version[1]
message("BACI version ", version, ": ", nrow(trade_files), " files, revisions ",
        paste(unique(trade_files$hs_rev), collapse = ", "))

# 3. Column types: the most important line in this script ---------------------
# k must be TEXT, otherwise "010111" becomes 10111 and stops matching.
# q is sometimes missing; readr trims spaces and reads "NA" as missing.

baci_cols <- cols(
  t = col_integer(), i = col_integer(), j = col_integer(),
  k = col_character(), v = col_double(), q = col_double()
)

# 4. Convert each year file to Parquet, one at a time -------------------------
# One year (~10 million rows) fits comfortably in memory; thirty at once do not.

for (n in seq_len(nrow(trade_files))) {
  f <- trade_files[n, ]
  flows <- read_csv(f$path, col_types = baci_cols, na = c("", "NA"),
                    progress = FALSE)

  # Safety check: the year inside the file must match the year in its name.
  if (!all(flows$t == f$year)) stop("Year mismatch inside ", basename(f$path))

  flows <- flows |>
    mutate(version = version) |>
    select(-t)   # the year is stored in the folder name (t=2024) instead

  target <- file.path(out_dir, paste0("hs_rev=", f$hs_rev), paste0("t=", f$year))
  dir.create(target, recursive = TRUE, showWarnings = FALSE)
  write_parquet(flows, file.path(target, "part-0.parquet"))
  message("  HS", f$hs_rev, " ", f$year, ": ", format(nrow(flows), big.mark = ","), " rows")
}

# 5. Country table, cleaned ----------------------------------------------------
# Three known problems in the raw file are fixed here:
#   - na = character()  keeps Namibia's ISO2 "NA" as text, not missing
#   - names are double-encoded UTF-8 ("CÃ´te d'Ivoire"): repaired below
#   - code 490 ("Other Asia, nes") is Taiwan in practice: atlas_iso3 = "TWN"

repair_name <- function(x) {
  # Undo the double encoding. Names that were already fine come back unchanged.
  y <- iconv(x, from = "UTF-8", to = "latin1")
  out <- ifelse(is.na(y), x, y)
  Encoding(out) <- "UTF-8"
  out
}

country_file <- list.files(raw_dir, pattern = "^country_codes_V\\d{6}\\.csv$", full.names = TRUE)
countries <- read_csv(country_file, col_types = cols(.default = col_character()),
                      na = character()) |>
  mutate(
    country_code = as.integer(country_code),
    country_name = repair_name(country_name),
    status = case_when(
      str_detect(country_name, fixed("(...")) ~ "historical",
      str_detect(country_name, ", nes$")     ~ "nes",
      TRUE                                   ~ "current"
    ),
    # The ISO3 the atlas uses to join to everything else (regions, maps, other sources).
    atlas_iso3 = case_when(
      country_code == 490          ~ "TWN",
      country_code %in% c(697, 711) ~ NA_character_,   # EFTA nes, SACU bloc: no single country
      TRUE                          ~ country_iso3
    ),
    version = version
  )

dir.create(meta_dir, recursive = TRUE, showWarnings = FALSE)
write_parquet(countries, file.path(meta_dir, "countries.parquet"))

# 6. Product tables, one per revision -----------------------------------------

for (rev in unique(trade_files$hs_rev)) {
  pfile <- file.path(raw_dir, paste0("product_codes_HS", rev, "_V", version, ".csv"))
  if (!file.exists(pfile)) { warning("Missing ", basename(pfile)); next }
  products <- read_csv(pfile, col_types = cols(.default = col_character()))
  write_parquet(products, file.path(meta_dir, paste0("products_hs", rev, ".parquet")))
}

message("Done. Parquet written to ", out_dir, " and ", meta_dir)
