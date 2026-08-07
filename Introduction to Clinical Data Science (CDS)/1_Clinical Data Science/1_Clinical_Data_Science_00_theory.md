# 1) Clinical Data Science

> Module: Introduction to Clinical Data Science (CDS)
> Source: Based on the publicly available description of the *Clinical Data Science Specialization*
> (University of Colorado System / Washington University in St. Louis, Coursera, instructor Laura K. Wiley, PhD,
> co-developed with Michael G. Kahn, MD, PhD). Course description verified via Coursera's public specialization
> page; I have not accessed the paywalled video/lecture content itself.

## What clinical data science is

Clinical data science sits at the intersection of clinical medicine, biomedical informatics, and data
science/statistics. It is the practice of taking data that is generated as a byproduct of routine healthcare
delivery — most importantly data captured in Electronic Health Records (EHRs) — and turning it into
knowledge that can improve the care of current and future patients.

This is distinct from data collected specifically for research purposes (e.g. a designed clinical trial CRF).
Clinical/EHR data is **secondary-use data**: it was generated to support billing, clinical documentation, and
care coordination, not to answer a specific research question. That origin shapes almost everything about how
it needs to be handled — its structure, its biases, its gaps, and the ethical/legal constraints around it.

## What the field aims to teach (per the Specialization's stated learning outcomes)

According to the Specialization's public description, completing it is meant to leave a learner able to:

1. Understand EHR data types and structures.
2. Deploy basic informatics methodologies on clinical data.
3. Provide appropriate clinical and scientific interpretation of applied analyses.
4. Anticipate barriers in implementing informatics tools into complex clinical settings.

## Why this differs from "generic" data science

A few things make clinical data science its own discipline rather than just "data science applied to
hospitals":

- **Regulatory and ethical constraints.** Patient data is protected health information (PHI) — legally
  and ethically restricted, requiring institutional review, de-identification/anonymisation, and strict
  data governance before it can be shared, published, or reused.
- **Data was not designed for analysis.** EHR data is a byproduct of clinical workflows (billing codes,
  free-text notes, orders), not a purpose-built research dataset — this drives most of the technical
  challenges covered later in this course (data quality, missingness, coding inconsistency).
- **The stakes of misinterpretation are high.** Analyses feed into decisions that affect patient care, so
  clinical and domain-specific interpretation of a result is as important as the statistical method used to
  produce it.

## My own note (not from the course)

This maps closely onto something I already do in my own work: my postdoctoral research involves taking data
generated in a clinical/translational context (patient tissue samples, sequencing data tied to clinical
metadata) and turning it into something interpretable and actionable, while working within GDPR/institutional
data governance constraints. The core discipline is the same; the data modality (genomic vs. EHR-structured)
is what differs.

## Open questions to fill in once I have direct course access

- The specific "basic informatics methodologies" the course references.
- Any named framework or terminology the course uses for classifying EHR data types (see submodule 2 for
  how I'm handling this honestly, without inventing course-specific content).
