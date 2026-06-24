# Checkpoint 3: Model Evaluation Plan

## 1. Documentation, Transparency, and Split Strategy
* **Unit of Analysis:** A single patient record at the point of initial clinical/histological breast cancer diagnosis.
* **Data Split Strategy:** To test if the model can successfully generalize to entirely unseen hospital environments, we completely avoid random row shuffling. We isolate a permanent **20% Final Holdout Set** at the root level and evaluate the remaining 80% using a **Group 5-Fold Cross-Validation** partitioned strictly by the hospital `Cohort` column.

## 2. Data Splits and Leakage Mitigation Profile
* **Group-Level & Geographic Leakage:** Institutional treatment biases are trapped via `sklearn.model_selection.GroupKFold` using the `Cohort` column, ensuring no patient crossover between separate medical networks.
* **Post-Outcome & Temporal Leakage:** Real-time diagnostic models cannot use future timelines. Columns tracking future post-surgery event milestones specifically `Overall_Survival_(Months)` and `Relapse_Free_Status_(Months)` are dropped from the feature space.
* **Feature Leakage (Collinearity Pruning):** As caught in our EDA pairplot, redundant feature pairs like `Mutation_Count` and `TMB_(nonsynonymous)` exhibit perfect linear alignment () and are pruned down to a single representative feature to prevent model instability.
* **Overfitting the Split:** Parameter adjustments are restricted to the inner cross-validation loop. The holdout set is only evaluated once at the very end to prevent data snooping.

## 3. Metrics and Objectives Profile
* **Class Imbalance Protection:** Survival datasets contain highly skewed target categories (`0:LIVING` vs. `1:DECEASED`). Traditional accuracy is discarded. The model optimizes for **Precision, Recall, F1-Score per class**, and **Precision-Recall Area Under the Curve (PR-AUC)**.
* **Clinical Trade-offs:** Precision protects low-risk patients from unnecessary, aggressive over-treatment anxiety, while Recall ensures high-risk, spreading cases are caught for prompt surgical or therapeutic intervention.
* **Probability Trust (Calibration):** To guarantee that a model's predicted risk score corresponds directly to actual patient statistics, we will evaluate the model using `calibration_curve` and implement `CalibratedClassifierCV` adjustments.

## 4. Robustness and Adversarial Stress Testing
* **Outlier & Skewness Sensitivity:** Our newly engineered feature (`Lymph_Node_Spread_Ratio`) exhibits a heavy right-skewed distribution. The processing pipeline embeds a `RobustScaler` (median/quantile-based) to isolate extreme outlier patients and protect model boundaries.
* **Adversarial Target Shuffling:** The pipeline decouples and shuffles target labels randomly. If validation metrics drop entirely to random chance (F1-score ), it mathematically confirms that the pipeline code is completely free of data leakage.
* **Demographic Shifts:** Models are evaluated across isolated age subsets (younger vs. older patient cohorts) to ensure stable accuracy boundaries across changing patient backgrounds.
