# Exercises — Tools: R and Tidyverse

Dataset: MIMIC-III Clinical Database Demo (see `00_setup_mimic_demo.md`). Same questions as the SQL
exercises, but solved with dplyr/tidyr/ggplot2 — a good way to see the two approaches side by side.

1. Using `dplyr::count()`, how many distinct patients are female vs. male?
2. Which patient has the most hospital admissions? Use `group_by()` + `summarise()` or `count()`.
3. Find the 5 most common primary diagnoses (`seq_num == 1`) using `filter()` + `inner_join()` +
   `count()`.
4. For each admission, count the number of distinct diagnosis codes recorded. Which admission has the
   most?
5. Using `icustays`, compute mean/min/max `los` with `summarise()`.
6. Find the 5 most frequently measured lab categories using `count()`.
7. **Harder**: filter admissions where `deathtime` is not `NA`, join to primary diagnosis, and compare the
   most common diagnosis in that subset vs. the overall cohort (exercise 3). Try visualizing both with
   `ggplot2` side by side (e.g. `facet_wrap()`).

_(Solve these in `practice/01_clinical_workflow.Rmd`, adding new chunks below the existing ones.)_
