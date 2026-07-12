# summer26-breast-cancer-survival
This repository contains the data and analysis for the Summer 2026 Breast Cancer Survival team project

## Problem Statements
1. How does survival differ across breast cancer subtypes — and how much worse off are triple-negative patients after adjusting for stage, grade, and treatment?
2. Can we predict 5-year survival at diagnosis using clinical and tumor features available at time of diagnosis, and does the same model generalize across subtypes — including the hard-to-treat TNBC group?

# Unit of analysis
Survival in cancer subtypes

## Data Source and Structure
We collected the data from [METABRIC](https://www.cbioportal.org/study/summary?id=brca_metabric).<br>
Downloaded raw data can be found in `data/raw/brca_metabric_clinical_data.tsv`
- Original records: 2509 patients from UK and Canada
- File size: 730K
- Errors accessing data: None

Each instances in the data contains the following fields:

| Category | METABRIC columns |
|----------|------------------|
| Demographics | `AGE_AT_DIAGNOSIS`, `SEX`, `INFERRED_MENOPAUSAL_STATE` |
| Receptors | `ER_STATUS`, `PR_STATUS`, `HER2_STATUS`, `ER_IHC`, `HER2_SNP6` |
| Subtype (molecular) | `CLAUDIN_SUBTYPE`, `THREEGENE`, `INTCLUST` |
| Tumor | `TUMOR_STAGE`, `GRADE`, `TUMOR_SIZE`, `LYMPH_NODES_EXAMINED_POSITIVE`, `NPI`, `HISTOLOGICAL_SUBTYPE`, `CELLULARITY` |
| Genomic | `MUTATION_COUNT`, `TMB_NONSYNONYMOUS` |
| Treatment | `CHEMOTHERAPY`, `RADIO_THERAPY`, `HORMONE_THERAPY`, `BREAST_SURGERY` |
| Outcomes | `OS_MONTHS`, `OS_STATUS`, `VITAL_STATUS`, `RFS_MONTHS`, `RFS_STATUS` |

Where RFS: Recurrence Free Survival
...
| Outcomes | `OS_MONTHS`, `OS_STATUS`, `VITAL_STATUS`, `RFS_MONTHS`, `RFS_STATUS` |
Where RFS: Recurrence Free Survival

### Molecular Subtype Classification
The `CLAUDIN_SUBTYPE` column is central to both problem statements. It classifies each tumor into one of six molecular subtypes based on gene expression:

| Subtype | Key characteristics |
|---|---|
| Luminal A | ER+, slow-growing, best prognosis |
| Luminal B | ER+, faster-growing, worse than Luminal A |
| HER2-enriched | HER2 amplified, ER- |
| Basal | Triple-negative proxy (ER−/PR−/HER2−), poorest early survival |
| Claudin-low | Low cell-adhesion gene expression, overlaps with TNBC |
| Normal-like | Resembles normal breast tissue |

For our analysis, Basal and Claudin-low are the primary groups of interest as proxies for triple-negative breast cancer (TNBC).

## Raw Data Statistics
...

Raw Data Statistics

| Metric | Value |
|---|---|
| Total Patients | 2,509 |
| Patients with Survival Data | 1,981 |
| Patients with Mutation Data | 2,369 |
| Deceased | 1,144 (57.7%) |
| Living | 837 (42.3%) |
| Recurred | 1,002 (40.3%) |
| Not Recurred | 1,486 (59.7%) |

Detailed column statistics can be found in `data/raw_data/metabric_column_statistics.md` and these statistics were calculated with `data/raw_data/columns_statistics.py`
