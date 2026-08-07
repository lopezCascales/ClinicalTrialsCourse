-- =============================================================================
-- Practice: SQL for Clinical Data
-- Dataset: MIMIC-III Clinical Database Demo v1.4 (real, openly-accessible, 100 patients)
-- See ../00_setup_mimic_demo.md for how to load this into SQLite.
-- All table/column names below are verified against the real MIMIC-III schema.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. Orientation: how many patients, admissions, ICU stays do we have?
-- -----------------------------------------------------------------------------

SELECT COUNT(*) AS n_patients FROM PATIENTS;
SELECT COUNT(*) AS n_admissions FROM ADMISSIONS;
SELECT COUNT(DISTINCT subject_id) AS n_patients_with_admissions FROM ADMISSIONS;

-- -----------------------------------------------------------------------------
-- 2. Basic SELECT + WHERE: patients who died in-hospital
--    (expire_flag = 1 means the patient died, per the PATIENTS table)
-- -----------------------------------------------------------------------------

SELECT subject_id, gender, dob, dod
FROM PATIENTS
WHERE expire_flag = 1;

-- -----------------------------------------------------------------------------
-- 3. JOIN: link admissions to their diagnosis codes and human-readable labels
--    DIAGNOSES_ICD is a "fact" table (codes only); D_ICD_DIAGNOSES is the
--    "lookup" table that translates icd9_code into a readable title.
-- -----------------------------------------------------------------------------

SELECT
    d.subject_id,
    d.hadm_id,
    d.seq_num,        -- 1 = primary diagnosis, higher numbers = secondary
    d.icd9_code,
    i.short_title,
    i.long_title
FROM DIAGNOSES_ICD d
INNER JOIN D_ICD_DIAGNOSES i
    ON d.icd9_code = i.icd9_code
ORDER BY d.subject_id, d.seq_num
LIMIT 20;

-- -----------------------------------------------------------------------------
-- 4. GROUP BY: most common diagnoses in this cohort (by number of admissions)
-- -----------------------------------------------------------------------------

SELECT
    i.short_title,
    COUNT(DISTINCT d.hadm_id) AS n_admissions
FROM DIAGNOSES_ICD d
INNER JOIN D_ICD_DIAGNOSES i
    ON d.icd9_code = i.icd9_code
GROUP BY i.short_title
ORDER BY n_admissions DESC
LIMIT 10;

-- -----------------------------------------------------------------------------
-- 5. Three-table JOIN: patient demographics + admission + primary diagnosis
--    This is the kind of query you'd run to build an analytic cohort table.
-- -----------------------------------------------------------------------------

SELECT
    p.subject_id,
    p.gender,
    a.hadm_id,
    a.admittime,
    a.admission_type,
    i.short_title AS primary_diagnosis
FROM PATIENTS p
INNER JOIN ADMISSIONS a
    ON p.subject_id = a.subject_id
INNER JOIN DIAGNOSES_ICD d
    ON a.hadm_id = d.hadm_id AND d.seq_num = 1   -- seq_num = 1 -> primary diagnosis
INNER JOIN D_ICD_DIAGNOSES i
    ON d.icd9_code = i.icd9_code
ORDER BY a.admittime;

-- -----------------------------------------------------------------------------
-- 6. Working with lab results: LABEVENTS is a fact table, D_LABITEMS is the
--    lookup for what each itemid actually measures.
-- -----------------------------------------------------------------------------

-- What lab tests exist, and how many results do we have for each?
SELECT
    li.label,
    li.fluid,
    li.category,
    COUNT(*) AS n_results
FROM LABEVENTS le
INNER JOIN D_LABITEMS li
    ON le.itemid = li.itemid
GROUP BY li.label, li.fluid, li.category
ORDER BY n_results DESC
LIMIT 10;

-- Abnormal lab results only (LABEVENTS.flag = 'abnormal' when out of range)
SELECT
    le.subject_id,
    li.label,
    le.charttime,
    le.value,
    le.valueuom,
    le.flag
FROM LABEVENTS le
INNER JOIN D_LABITEMS li
    ON le.itemid = li.itemid
WHERE le.flag = 'abnormal'
ORDER BY le.charttime
LIMIT 20;

-- -----------------------------------------------------------------------------
-- 7. Dates and time: length of ICU stay per patient (uses ICUSTAYS.los, which
--    MIMIC-III precomputes in days -- no need to calculate it manually)
-- -----------------------------------------------------------------------------

SELECT
    subject_id,
    hadm_id,
    icustay_id,
    first_careunit,
    intime,
    outtime,
    los AS length_of_stay_days
FROM ICUSTAYS
ORDER BY los DESC
LIMIT 10;
