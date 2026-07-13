::: center
**Executive Summary**
:::

# Executive Summary {#executive-summary .unnumbered}

**Five Year Survival Prediction of The Breast Cancer Patients from UK
and Canada Based on the Clinical Information**\
**Project members:** Gopal Narayan Srivastava, Monika Pandey, Mehri
Mehrnia

**GitHub repository:**
[GitHub](https://github.com/Erdos-Projects/summer26-breast-cancer-survival)

## Problem Description {#problem-description .unnumbered}

Breast cancer is the most common cancer diagnosed in
women[@who_breast_cancer_2024], and doctors lean heavily on the "5-year
survival" mark when they talk to patients about what to expect, decide
how often to see them for follow-up, and choose how aggressive treatment
should be [@seer_breast_cancer_2026]. But 5-year outcomes are far from
uniform as some patients with aggressive tumors end up surviving for
longer than 5 years, on the other hand, others with non-agressive
sometimes show frequent relapse. Thus, figuring out patients outcome can
help doctors making treatment decisions, inform patients of their
options, and insurance companies in making policies and financial
decisions related to patients with breast cancers. For our study the
stakeholders include patients, hospitals, pharma and insurance
companies.

## Project Aims {#project-aims .unnumbered}

To explore into this, we asked two specific questions.

1.  Will the patient survive at least 5 years after being diagnosed?

2.  Is there any difference in survival of TNBC (Basal) cancer subtype
    compared to other subtypes?

**Note:** We define "surviving 5 years" as being alive 60 months or more
after diagnosis.

## Dataset {#dataset .unnumbered}

Clinical data of 2,509 female breast-cancer patients from the UK and
Canada, was downloaded from cBioPortal [@cbioportal_metabric_2026].

From the dataset we removed 528 patients as their survival status along
with 10 clinical features were missing.

## Feature Selection, Model Selection, and Performance {#feature-selection-model-selection-and-performance .unnumbered}

Since, we framed our task as a binary classification problem focused 5
years survival (positive class: "survived $\geq$ 5y"), we focused on
patients from the METABRIC [@cbioportal_metabric_2026] cohort whose
5-year outcome was unambiguously known. Patients with living survival
status and overall survival less than 5-year mark were excluded, since
in medicine 5-year survival is the gold standard. Our final analytical
dataset included 1,917 patients drawn from 5 cohorts, of whom roughly
77% survived 5 years and 33% died within 5 years.

1.  In our study, we made use of the fact that METABRIC's patients come
    from 5 distinct cohorts and split by cohort: cohorts 1--3 (1,518
    patients) formed the development pool and cohorts 4 and 5 (399
    patients) were separated as an external holdout.

2.  Missing values in the clinical fields were filled using Multivariate
    Imputation by Chained Equations (MICE), per cohort so that no
    information leaked across the cohort boundary before splitting.

For feature selection, we started with the imputed data then ranked
candidate features by importance in a preliminary *RandomForest* screen
and performed elbow analysis to get top 11 features: *Age at Diagnosis,
Nottingham prognostic index, hetloss, gain, Tumor Size, amp, TMB
(nonsynonymous), homdel, Integrative Cluster, Pam50 + Claudin-low
subtype, and Type of Breast Surgery.*

For model selection, we used leave-one-cohort-out cross-validation on
the development pool (3-fold GroupKFold, 3 Cohorts in Dev pool) to
compare four classifiers: (a) Logistic Regression with L1/L2 penalties,
(b) LightGBM, (c) XGBoost, and (d) Support Vector Machine with an RBF
kernel. Class imbalance was handled inside each pipeline as follows:
*class_weight='balanced'* for LR and SVM, *scale_pos_weight = n_neg /
n_pos* for LightGBM and XGBoost, so that the minority negative ("died
$<$`<!-- -->`{=html}5y") class contributed equally to the loss. Each
model was tuned by GridSearchCV scored on ROC-AUC and refit on the
entire dev pool with its best hyperparameters before ever touching the
holdout.

The four tuned models produced very similar cross-validated ROC-AUCs on
the dev pool, with an $\sim$`<!-- -->`{=html}0.03 spread between the
strongest and weakest. On the sealed holdout, we then reported ROC-AUC,
PR-AUC, MCC, and per-class precision, recall, and F1:

[]{#tab:model_results label="tab:model_results"}

::: {#tab:model_results}
+------------+----------+----------+----------+--------------------------+--------------------------+--------------------------+
| Model      | ROC-AUC  | PR-AUC   | MCC      | ::: {#tab:model_results} | ::: {#tab:model_results} | ::: {#tab:model_results} |
|            |          |          |          |   -----------------      |   --------------         |   ------------           |
|            |          |          |          |    Precision (died       |    Recall (died          |     F1 (died /           |
|            |          |          |          |      / survived)         |    / survived)           |      survived)           |
|            |          |          |          |   -----------------      |   --------------         |   ------------           |
|            |          |          |          |                          |                          |                          |
|            |          |          |          |   : Model Evaluation     |   : Model Evaluation     |   : Model Evaluation     |
|            |          |          |          |   Results on Unseen      |   Results on Unseen      |   Results on Unseen      |
|            |          |          |          |   Cohorts 4, 5           |   Cohorts 4, 5           |   Cohorts 4, 5           |
|            |          |          |          | :::                      | :::                      | :::                      |
+:===========+:========:+:========:+:========:+:========================:+:========================:+=========================:+
| Logistic   | 0.76     | 0.89     | 0.36     | 0.40 / 0.91              | 0.80 / 0.63              | 0.53 / 0.74              |
| Regression |          |          |          |                          |                          |                          |
+------------+----------+----------+----------+--------------------------+--------------------------+--------------------------+
| LightGBM   | 0.76     | 0.91     | 0.39     | 0.43 / 0.91              | 0.77 / 0.69              | 0.55 / 0.78              |
+------------+----------+----------+----------+--------------------------+--------------------------+--------------------------+
| XGBoost    | 0.77     | 0.91     | **0.40** | 0.43 / 0.91              | 0.78 / 0.69              | **0.56** /0.78           |
+------------+----------+----------+----------+--------------------------+--------------------------+--------------------------+
| **SVM (RBF | **0.79** | **0.92** | 0.38     | 0.42 / 0.91              | 0.79 / 0.66              | 0.54 / 0.76              |
| kernel)**  |          |          |          |                          |                          |                          |
+------------+----------+----------+----------+--------------------------+--------------------------+--------------------------+

: Model Evaluation Results on Unseen Cohorts 4, 5
:::

## Key Takeaways {#key-takeaways .unnumbered}

1.  The RBF-SVM achieved the best threshold-independent ranking (ROC-AUC
    0.79, PR-AUC 0.92), meaning it performs best in ordering patients
    from lowest to highest risk of dying within 5 years.

2.  XGBoost achieved the best balanced classification score (MCC 0.40)
    and F1 on the clinically important minority class, meaning it makes
    the best individual decisions (yes/no calls) at 0.5 probability
    threshold.

3.  Since, the gap in performance between linear and non-linear models
    is small ($\approx$`<!-- -->`{=html}0.03 AUC), it signals that most
    of the predictive information in these features is linear.

4.  Feature importance analysis identified age at diagnosis, the
    Nottingham Prognostic Index, tumor size, and the Pam50 + Claudin-low
    molecular subtype as the strongest predictors. Copy-number
    Alterations (CNA), mainly gain and hetloss and the Integrative
    Cluster labels contributed additional signal beyond what standard
    clinical features alone would provide.

    1.  Standard clinical prognostic factors still carry the most
        weight. Age, tumor size, grade, and NPI, dominate the model,
        confirming that decades-old clinical intuition is not far off
        from what a modern ML model would use.

    2.  Molecular subtype adds meaningful information beyond staging.
        Pam50 + Claudin-low classification contributed independent
        signal to the prediction, consistent with the growing role of
        subtype-directed therapy in the clinic.

    3.  Copy-number burden matters at the genome-wide level. The four
        CNA were more useful than individual gene-level events,
        suggesting overall genomic instability is a more robust signal
        than any single alteration for predicting 5-year outcome.

In conclusion, our model provides an effective means of distinguishing
between breast cancer patients who will and will not survive 5 years
from diagnosis, using only information available at the time of that
diagnosis.

# Future work {#future-work .unnumbered}

1.  We would replace binary classification with survival analysis such
    as Cox proportional hazards or DeepSurv to use censored patients
    rather than drop them.

2.  Incorporate gene expression signatures alongside the clinical and
    copy-number features, validate the model on a non-METABRIC cohort
    such as TCGA-BRCA to test generalization beyond a single consortium.

3.  For clinical use, tune the decision threshold to reflect the
    relative cost of false negatives versus false positives in
    downstream care decisions
