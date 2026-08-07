# 4) Tools: R and Tidyverse

> Module: Introduction to Clinical Data Science (CDS)
> Standard, verifiable R/tidyverse knowledge (not proprietary course content) applied to a clinical workflow.

## Why the tidyverse for clinical data workflows

The tidyverse is a collection of R packages built around a shared philosophy ("tidy data": each variable is
a column, each observation is a row, each type of observational unit is a table) and a consistent syntax.
For clinical data science it's a natural fit once data has been pulled out of a database via SQL (submodule
3), because most subsequent steps — reshaping, filtering, joining, summarising, and plotting — map directly
onto tidyverse verbs.

## Core packages and verbs

### dplyr — data manipulation

```r
library(dplyr)

diagnoses_t2dm <- diagnoses |>
  filter(str_starts(diagnosis_code, "E11")) |>
  group_by(patient_id) |>
  summarise(first_diagnosis_date = min(diagnosis_date), .groups = "drop")
```

- `filter()` — keep rows matching a condition (equivalent to SQL `WHERE`).
- `select()` — keep/drop columns (equivalent to SQL `SELECT`).
- `mutate()` — create or modify columns.
- `group_by()` + `summarise()` — aggregate (equivalent to SQL `GROUP BY`).
- `left_join()`, `inner_join()`, etc. — combine tables (equivalent to SQL `JOIN`), with the join key(s)
  specified via `by =`.

### tidyr — reshaping data

Clinical data is frequently "wide" (one row per patient, one column per lab test) or "long" (one row per
patient-per-test-per-date) depending on the source, and needs reshaping between the two depending on the
analysis:

```r
library(tidyr)

labs_wide <- labs_long |>
  pivot_wider(names_from = test_name, values_from = result_value)
```

### stringr — working with text fields

Relevant given how much of clinical data involves codes and free text (diagnosis code prefixes, note text
matching) — e.g. `str_starts()`, `str_detect()`, `str_extract()`.

### ggplot2 — visualization

Following the tidyverse's grammar-of-graphics approach, useful for exploratory plots of clinical cohorts
(e.g. diagnosis counts over time, lab value distributions by group):

```r
library(ggplot2)

ggplot(diagnoses_t2dm, aes(x = first_diagnosis_date)) +
  geom_histogram(binwidth = 30) +
  labs(title = "New T2DM diagnoses over time", x = "Date", y = "Count")
```

## The pipe operator

The native pipe `|>` (or the tidyverse's `%>%`) chains operations left to right, which keeps clinical data
pipelines — extraction → cleaning → cohort definition → summary — readable as a sequence of named steps
rather than nested function calls.

## My own note

This maps almost exactly onto my own daily R/Bioconductor + tidyverse workflow for processing single-cell
and multi-omic data: `dplyr` for metadata wrangling, `tidyr` for reshaping expression/annotation tables,
`ggplot2` for QC and result plots. The syntax and logic transfer directly; only the tables being joined
differ (sample/cell metadata vs. patient/diagnosis tables).
