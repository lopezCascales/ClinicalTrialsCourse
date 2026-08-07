# Exercises — Tools: SQL

Dataset: MIMIC-III Clinical Database Demo (see `00_setup_mimic_demo.md`). All exercises are answerable
directly from the real data — there is a correct, checkable answer for each.

1. How many distinct patients (`subject_id`) are female vs. male, according to `PATIENTS.gender`?
2. Which `subject_id` has the most hospital admissions in `ADMISSIONS`? How many?
3. Using `DIAGNOSES_ICD` and `D_ICD_DIAGNOSES`, find the 5 most common **primary** diagnoses
   (`seq_num = 1`) in this cohort.
4. For each admission, how many distinct diagnosis codes were recorded (`seq_num` count)? What's the
   admission with the highest number of recorded diagnoses?
5. Using `ICUSTAYS`, what is the average, minimum, and maximum ICU length of stay (`los`) in this cohort?
6. Using `LABEVENTS` and `D_LABITEMS`, find the 5 most frequently measured lab tests by `category`.
7. **Harder**: for patients who died in-hospital (`ADMISSIONS.deathtime IS NOT NULL`), what was their most
   common primary diagnosis? Does it differ from the overall cohort's most common primary diagnosis
   (exercise 3)?

_(Solve these in `practice/01_clinical_queries.sql`, adding new query blocks below the existing ones.)_
