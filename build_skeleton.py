#!/usr/bin/env python3
"""
build_skeleton.py

Creates a standard theory + practice + exercises skeleton for every module
and submodule in the ClinicalTrialsCourse repo, based on the current README.

USAGE:
    1. Clone your repo and cd into it:
         git clone https://github.com/lopezCascales/ClinicalTrialsCourse.git
         cd ClinicalTrialsCourse
    2. Copy this script into the repo root.
    3. Run it:
         python3 build_skeleton.py
    4. Review the changes (git status / git diff), then commit and push:
         git add .
         git commit -m "Add theory/practice/exercises skeleton for all modules"
         git push

WHAT IT CREATES, per submodule folder:
    00_theory.md        <- theory notes (title + description prefilled from README)
    practice/            <- folder for .Rmd / .qmd notebooks
        .gitkeep
    exercises.md         <- unsolved practice questions, prefilled with a template
    data/                 <- folder for small local data (gitignored by default)
        .gitkeep

It DOES NOT overwrite files that already exist, so it's safe to re-run.
"""

import os
import re

# ---------------------------------------------------------------------------
# Course structure, parsed from the current README.md
# Each entry: (module_name, [(submodule_number, submodule_title, description), ...])
# ---------------------------------------------------------------------------

COURSE = [
    ("Introduction to Clinical Data Science (CDS)", [
        ("1", "Clinical Data Science",
         "Learn what clinical data science is."),
        ("2", "Introduction: clinical data",
         "Clinical data are complex. Walk through the four-W's of clinical data to understand where they come from and what they look like."),
        ("3", "Tools: SQL",
         "Develop basic skills in SQL (Structured Query Language) and query the real clinical data set used in the Clinical Data Science Specialization."),
        ("4", "Tools: R and Tidyverse",
         "Learn how to use the tidyverse to implement your Clinical Data Science Workflow in R."),
    ]),
    ("Design and Conduct of Clinical Trials", [
        ("1", "Bias Control: Randomization and Masking",
         "Approaches to bias control, randomization strategies (simple, restricted, adaptive), and masking procedures."),
        ("2", "Trial Stages and Design",
         "Sound design choices across trial stages: research questions/hypotheses, design types, error identification."),
        ("3", "Outcomes in Clinical Trials",
         "Well-defined outcomes as the foundation of trial design, and their influence on trial type, randomization, masking, sample size."),
        ("4", "Ethical Issues",
         "Personnel, documents, terminology and practices for ethically sound informed consent."),
        ("5", "Recruitment and Retention",
         "Ethical and effective participant recruitment/retention and strategic clinical site selection."),
    ]),
    ("Clinical Trials Management and Advanced Operations", [
        ("1", "Protocol Events",
         "Recognizing, documenting and responding to protocol events affecting patient safety or data integrity."),
        ("2", "Regulatory Affairs and Trial Misconduct",
         "Regulatory affairs in clinical trials, trial misconduct, IRBs, federal agency enforcement."),
        ("3", "Standardization, Transparency and Research Reproducibility",
         "Standardization of research practices, transparency of study activities, and research reproducibility; protocol registries."),
        ("4", "Evidence Synthesis: Introduction to systematic reviews and Meta-analysis",
         "Systematic reviews and meta-analysis to synthesize evidence across trials."),
    ]),
    ("Clinical Data Models and Data Quality Assessments", [
        ("1", "Introduction: Clinical Data Models and Common Data Models",
         "Clinical data models, common data models in national/international networks, Entity-Relationship Diagrams (ERDs)."),
        ("2", "Tools: Querying Clinical Data Models",
         "Technical features of clinical data models using MIMIC3, and common data models using OMOP."),
        ("3", "Techniques: Extract-Transform-Load and Terminology mapping",
         "ETL processes and challenges, with real-world examples in data and terminology mapping."),
        ("4", "Techniques: Data Quality Assessments",
         "Dimensions of data quality, measurements, and rules to assess acceptability for use."),
        ("5", "Practical application: Create an ETL process to Transform MIMIC3 to OMOP common data model",
         "Hands-on exercise: ETL methods to convert MIMIC3 data into the OMOP common data model."),
    ]),
    ("Identifying Patient Populations", [
        ("1", "Introduction: Identifying Patients Populations",
         "Computational phenotyping to identify patient populations."),
        ("2", "Tools: Clinical Data types",
         "Using different clinical data types to identify patient populations; phenotyping algorithm for type II diabetes."),
        ("3", "Techniques: Data manipulations and combinations",
         "Manipulating and combining data types in computational phenotyping algorithms."),
        ("4", "Techniques: Algorithms selection",
         "Selecting a single 'best' computational phenotyping algorithm; finalize/justify for type II diabetes."),
        ("5", "Practical application: Develop a computational phenotyping algorithm to identify patients",
         "Develop a computational phenotyping algorithm to identify patients with hypertension."),
    ]),
    ("Clinical Natural Language Processing", [
        ("1", "Introduction: Clinical Natural Language Processing",
         "Basics of text mining, text processing, NLP, and linguistic foundations underlying NLP tools."),
        ("2", "Tools: Regular Expressions",
         "Regular expressions for text processing and working with text data in R."),
        ("3", "Techniques: Note sections",
         "How the section of a clinical note affects meaning of text within it."),
        ("4", "Techniques: Keyword windows",
         "Building windows of text around keywords of interest to understand context and meaning."),
        ("5", "Practical application: Identifying Patients with diabetes complications",
         "Apply NLP tools/techniques to a real-world example."),
    ]),
    ("Predictive Modeling and Transforming Clinical Practice", [
        ("1", "Introduction: Clinical prediction models",
         "Types of clinical prediction models and how they are put into practice."),
        ("2", "Tools: Ensuring Model Usability",
         "Qualitative methods to develop clinical prediction models more likely to transform clinical practice."),
        ("3", "Techniques: Model Implementation and sustainability",
         "Tools for implementing clinical prediction models in practice and factors affecting implementation over time."),
        ("4", "Techniques: Data selection, Model Building and Evaluation",
         "How different clinical data types are used in prediction models, and how model construction choices affect utility."),
        ("5", "Practical application: Develop a clinical prediction model",
         "Develop a clinical prediction model to assess risk of death during an ICU stay."),
    ]),
    ("Advanced Clinical Data Science", [
        ("1", "Introduction: Advanced Clinical Data Science",
         "How to perform high quality and replicable clinical analyses."),
        ("2", "Tools and Techniques: temporality",
         "Handling the impact of time on clinical data science analyses."),
        ("3", "Tools and Techniques: Missing data",
         "Handling missing data in clinical data science."),
        ("4", "Techniques: Data selection, Model Building and Evaluation",
         "Data types used in prediction models and how model construction choices affect utility."),
        ("5", "Practical application: Careers in Clinical Data Science",
         "Exploring potential career options in clinical data science."),
    ]),
    ("Representation in Clinical Trials", [
        ("1", "Introduction: Importance of clinical Trials",
         "Why disparities in healthcare exist, how treatments affect different populations; self-reflective activity on diversity/bias."),
        ("2", "Barriers and challenges",
         "Barriers preventing historically underrepresented populations from participating in trials; trust in healthcare institutions."),
        ("3", "Bias on Clinical Research",
         "Conscious and unconscious bias in clinical research, and ways to recognize/reduce personal bias."),
        ("4", "Clinical Trial Sample Size",
         "Sample size calculation: determining how large a trial needs to be to detect a difference between groups."),
        ("5", "Trial monitoring",
         "Statistical methods to assess a trial while underway: safety, integrity, efficacy, recruitment, data quality."),
        ("6", "Reporting results from Randomized clinical Trials (RCTs)",
         "Best practices for reporting trial results in journal publications and data monitoring reports."),
        ("7", "Analyzing Trials",
         "The analyst's role throughout the trial, not just at the end."),
        ("8", "Advanced Topics",
         "Advanced operational functions: simulations, adaptive designs, Bayesian statistics."),
    ]),
    ("Statistical Analysis with R for Public Health", [
        ("1.1", "Types of variables, common distributions and sampling",
         "Key building blocks of statistical analysis: variable types, common distributions, sampling."),
        ("1.2", "Hands On Clinical Reporting Using R",
         "Context on clinical reporting in R and the industry shift toward open-source tools."),
        ("1.3", "Introduction to R and Rstudio",
         "Getting started with R and RStudio; import a data set and run descriptive analyses."),
        ("1.4", "Hypothesis Testing in R",
         "Applying hypothesis testing in R; p-values and confidence intervals for averages and proportions."),
        ("2.1", "Introduction to Linear Regression",
         "Correlation (Pearson's, Spearman's) and introduction to linear regression and model assumptions."),
        ("2.2", "Linear Regression in R",
         "The COPD data set; descriptive analyses, correlations, and linear regression with one/several predictors."),
        ("2.3", "Multiple Regression and Interaction",
         "Extending linear regression with binary/categorical predictors and interaction terms."),
        ("2.4", "Model Building",
         "Automated model-building procedures, their problems, and a more defensible/robust approach."),
        ("3.1", "Introduction to Logistic Regression",
         "Why linear regression fails for binary outcomes; odds and odds ratios."),
        ("3.2", "Logistic Regression in R",
         "Preparing data, running a simple logistic regression model in R, and interpreting output."),
        ("3.3", "Multiple Logistic Regression in R",
         "Running multiple logistic regression in R."),
        ("3.4", "Assessing model fit",
         "Assessing model fit/performance, avoiding overfitting, choosing variables for a multiple regression model."),
        ("4.1", "Kaplan-Meier plot",
         "Survival analysis: Kaplan-Meier plot, log-rank test, and censoring."),
        ("4.2", "Cox model",
         "Cox proportional hazards regression: hazards, risk set; simulated heart-failure admission data."),
        ("4.3", "The Multiple Cox Model",
         "Extending the simple Cox model to the multiple Cox model."),
        ("4.4", "The proportionality assumption",
         "Assessing model fit and testing the proportional hazards assumption via residuals."),
        ("5.1", "Study Data Tabulation Model (SDTM)",
         "SDTM data mappings for CRF/non-CRF data; programming SDTMs in R."),
        ("5.2", "ADaM Transformations",
         "ADaM datasets, the 3 ADaM structures, and creating ADaM in R using Pharmaverse packages (OCCDS, ADAE)."),
        ("5.3", "OCCDS and creating ADAE with {admiral} and Pharmaverse packages",
         "What OCCDS is, Adverse Events, and creating ADAE using {admiral} and other Pharmaverse packages."),
        ("5.4", "Static TLGs (NEST)",
         "Generating regulatory outputs with the NEST packages: tables, listings, graphs (TLGs); TLG-Catalog."),
        ("5.5", "Interactive Data Displays",
         "The teal family of R packages for production-level interactive review, safety and efficacy applications."),
    ]),
    ("Conclusions", [
        ("1", "Course review and next steps",
         "Brief review of the course and suggested next steps in your learning journey."),
    ]),
]

THEORY_TEMPLATE = """# {title}

> Module: {module}
> Submodule {number}

## Summary

{description}

## Key concepts

- TODO

## Notes

- TODO

## References

- TODO
"""

EXERCISES_TEMPLATE = """# Exercises — {title}

1. TODO: write a question that tests the core concept of this submodule.
2. TODO
3. TODO

_(Leave unsolved here; solve them in `practice/` notebooks.)_
"""


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text).strip()
    return re.sub(r"[\s_]+", "_", text)


def write_if_missing(path: str, content: str) -> None:
    if os.path.exists(path):
        print(f"  skip (exists): {path}")
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  created: {path}")


def main():
    for module, submodules in COURSE:
        module_dir = module
        print(f"Module: {module}")
        for number, title, description in submodules:
            sub_slug = f"{number}_{slugify(title)}"
            base = os.path.join(module_dir, sub_slug)

            write_if_missing(
                os.path.join(base, "00_theory.md"),
                THEORY_TEMPLATE.format(title=title, module=module, number=number, description=description),
            )
            write_if_missing(
                os.path.join(base, "exercises.md"),
                EXERCISES_TEMPLATE.format(title=title),
            )
            write_if_missing(os.path.join(base, "practice", ".gitkeep"), "")
            write_if_missing(os.path.join(base, "data", ".gitkeep"), "")

    print("\nDone. Review with `git status`, then commit and push.")


if __name__ == "__main__":
    main()
