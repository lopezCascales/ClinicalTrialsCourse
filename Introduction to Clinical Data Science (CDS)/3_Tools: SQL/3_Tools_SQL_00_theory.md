# 3) Tools: SQL

> Module: Introduction to Clinical Data Science (CDS)
> This is standard, verifiable SQL knowledge (not proprietary course content) applied to a clinical data context.

## Why SQL for clinical data

Clinical data is almost always stored in relational databases — separate tables for patients, encounters,
diagnoses, lab results, medications, etc., linked by keys (e.g. a patient ID). SQL (Structured Query
Language) is the standard language for querying relational databases, and is the entry point for pulling a
usable analytic dataset out of a clinical data warehouse or a common-data-model database like OMOP.

## Core concepts

### SELECT — retrieving data

```sql
SELECT patient_id, diagnosis_code, diagnosis_date
FROM diagnoses
WHERE diagnosis_code = 'E11.9';  -- ICD-10 code for Type 2 diabetes without complications
```

- `SELECT` chooses which columns to return.
- `FROM` specifies the source table.
- `WHERE` filters rows by a condition.

### JOIN — combining tables

Clinical data is normalized across many tables, so most real queries need to combine them:

```sql
SELECT p.patient_id, p.birth_date, d.diagnosis_code, d.diagnosis_date
FROM patients p
INNER JOIN diagnoses d
  ON p.patient_id = d.patient_id
WHERE d.diagnosis_code LIKE 'E11%';
```

- `INNER JOIN` returns only rows with a match in both tables.
- `LEFT JOIN` returns all rows from the left table, with NULLs where there's no match in the right table
  (important in clinical data — e.g. "all patients, whether or not they have this diagnosis").

### Aggregation — GROUP BY and aggregate functions

```sql
SELECT diagnosis_code, COUNT(DISTINCT patient_id) AS n_patients
FROM diagnoses
GROUP BY diagnosis_code
ORDER BY n_patients DESC;
```

Used constantly in clinical data science for cohort counts, prevalence estimates, and data quality checks
(e.g. counting how many records per patient, per source, per time period).

### Filtering on dates and time

Because clinical events are timestamped and irregular (see submodule 2), date filtering and ordering are
central to almost every clinical SQL query — for example, identifying a patient's *first* diagnosis of a
condition:

```sql
SELECT patient_id, MIN(diagnosis_date) AS first_diagnosis_date
FROM diagnoses
WHERE diagnosis_code LIKE 'E11%'
GROUP BY patient_id;
```

## Notes on the practical dataset used in this course

The Specialization uses a real clinical dataset (per its public description) with a Google Cloud–hosted
computational environment. I don't yet know the exact schema of that dataset. For the practice notebook in
this repo, I'll use **MIMIC-III** (or its demo/subset version) since it is the same dataset referenced
later in the "Clinical Data Models and Data Quality Assessments" module of this course, is publicly
documented, and doesn't require guessing at an unseen schema.

## My own note

This is close to SQL work I already do against sequencing metadata databases — the JOIN and GROUP BY logic
is identical; only the domain vocabulary (diagnosis codes vs. sample IDs, batches) changes.
