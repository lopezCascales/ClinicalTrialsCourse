# Setup: MIMIC-III Clinical Database Demo

> Source: PhysioNet, "MIMIC-III Clinical Database Demo" v1.4 (Johnson, Pollard & Mark, 2019).
> https://physionet.org/content/mimiciii-demo/1.4/
> DOI: 10.13026/C2HM2Q
> License: Open Data Commons Open Database License v1.0 (ODbL) — **openly accessible, no credentialing
> required**, unlike the full MIMIC-III database. Verified directly on the PhysioNet page: "Access Policy:
> Anyone can access the files, as long as they conform to the terms of the specified license."

## What it is

- 100 real, de-identified ICU patients from Beth Israel Deaconess Medical Center (subset of the full
  MIMIC-III database of 40,000+ patients).
- Same schema as the full MIMIC-III database (26 tables), except the `NOTEEVENTS` table (free-text clinical
  notes) is empty in the demo.
- Total uncompressed size: ~103 MB.
- All patients in this demo eventually die (selected on purpose, per PhysioNet's methods note), so every
  patient has a `dod` (date of death), though not necessarily during the admission/ICU stay captured here.

## Download

```bash
# Option 1: direct zip download
curl -O https://physionet.org/static/published-projects/mimiciii-demo/mimic-iii-clinical-database-demo-1.4.zip
unzip mimic-iii-clinical-database-demo-1.4.zip -d mimic-iii-demo

# Option 2: wget, mirrors the full folder
wget -r -N -c -np https://physionet.org/files/mimiciii-demo/1.4/
```

## Tables we'll use in this course's SQL and R practice sessions

| Table               | Key columns (verified)                                                                 | What it's for |
|---------------------|------------------------------------------------------------------------------------------|---------------|
| `PATIENTS`          | `subject_id`, `gender`, `dob`, `dod`, `dod_hosp`, `dod_ssn`, `expire_flag`                | One row per patient — demographics |
| `ADMISSIONS`        | `subject_id`, `hadm_id`, `admittime`, `dischtime`, `deathtime`, `admission_type`, `ethnicity`, `diagnosis` | One row per hospital admission |
| `ICUSTAYS`          | `subject_id`, `hadm_id`, `icustay_id`, `first_careunit`, `intime`, `outtime`, `los`       | One row per ICU stay |
| `DIAGNOSES_ICD`     | `subject_id`, `hadm_id`, `seq_num`, `icd9_code`                                          | Diagnosis codes per admission (fact table) |
| `D_ICD_DIAGNOSES`   | `icd9_code`, `short_title`, `long_title`                                                 | Lookup table: what each ICD-9 code means |
| `LABEVENTS`         | `subject_id`, `hadm_id`, `itemid`, `charttime`, `value`, `valuenum`, `valueuom`, `flag`    | Lab results (fact table) |
| `D_LABITEMS`        | `itemid`, `label`, `fluid`, `category`, `loinc_code`                                      | Lookup table: what each lab itemid means |

## Loading into SQLite (recommended by PhysioNet for the demo)

```bash
sqlite3 mimic3_demo.db
```

```sql
.mode csv
.import mimic-iii-demo/PATIENTS.csv PATIENTS
.import mimic-iii-demo/ADMISSIONS.csv ADMISSIONS
.import mimic-iii-demo/ICUSTAYS.csv ICUSTAYS
.import mimic-iii-demo/DIAGNOSES_ICD.csv DIAGNOSES_ICD
.import mimic-iii-demo/D_ICD_DIAGNOSES.csv D_ICD_DIAGNOSES
.import mimic-iii-demo/LABEVENTS.csv LABEVENTS
.import mimic-iii-demo/D_LABITEMS.csv D_LABITEMS
```

(the header row gets imported as data on the first `.import` — drop it with
`DELETE FROM PATIENTS WHERE subject_id = 'subject_id';` or similar, or use `.import --skip 1` if your
sqlite3 version supports it)

## Citation (required by the data license)

Johnson, A., Pollard, T., & Mark, R. (2019). MIMIC-III Clinical Database Demo (version 1.4). PhysioNet.
https://doi.org/10.13026/C2HM2Q

Johnson, A. E. W., Pollard, T. J., Shen, L., Lehman, L. H., Feng, M., Ghassemi, M., Moody, B., Szolovits, P.,
Celi, L. A., & Mark, R. G. (2016). MIMIC-III, a freely accessible critical care database. Scientific Data, 3,
160035.
