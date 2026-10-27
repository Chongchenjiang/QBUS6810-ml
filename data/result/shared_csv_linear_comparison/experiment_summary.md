# Shared CSV Linear Comparison

Training rows: 54,853; validation rows: 18,132; predictors: 209. No 2025 outcomes were loaded.

WAE (2:1) is selected in advance as the primary metric. Higher predictions than actual sales receive weight 2; other errors receive weight 1. MAE is in dollars, MSE in squared dollars, and R² is unitless.

scikit-learn version: 1.0.2. All models use the same 209 exported numeric predictors without additional imputation, encoding, scaling, or feature engineering.

## Best converged candidate per model

| Model             | Data Representation          |      alpha |        WAE_2_1 |            MAE |                   MSE |       R2 |
|:------------------|:-----------------------------|-----------:|---------------:|---------------:|----------------------:|---------:|
| Linear Regression | Shared Exported CSV Pipeline | nan        | 184,558.379270 | 121,800.453902 | 63,181,968,850.117912 | 0.668736 |
| Ridge             | Shared Exported CSV Pipeline | 100.000000 | 182,447.601226 | 121,085.411089 | 63,387,718,417.768707 | 0.667657 |
| Lasso             | Shared Exported CSV Pipeline | 100.000000 | 180,751.622378 | 120,854.078798 | 63,328,748,447.098015 | 0.667966 |

## All tested configurations

| Model             | Data Representation          |      alpha |        WAE_2_1 |            MAE |                   MSE |       R2 | converged   | convergence_warning   |        n_iter |          dual_gap |   dual_gap_threshold |   nonzero_coefficients |
|:------------------|:-----------------------------|-----------:|---------------:|---------------:|----------------------:|---------:|:------------|:----------------------|--------------:|------------------:|---------------------:|-----------------------:|
| Linear Regression | Shared Exported CSV Pipeline | nan        | 184,558.379270 | 121,800.453902 | 63,181,968,850.117912 | 0.668736 | True        | False                 |    nan        |        nan        |           nan        |                    209 |
| Ridge             | Shared Exported CSV Pipeline |   5.000000 | 184,384.184494 | 121,729.350426 | 63,185,058,152.494316 | 0.668720 | True        | False                 |    853.000000 |        nan        |           nan        |                    208 |
| Ridge             | Shared Exported CSV Pipeline |  10.000000 | 184,235.925062 | 121,670.262197 | 63,192,833,367.397705 | 0.668679 | True        | False                 |    652.000000 |        nan        |           nan        |                    208 |
| Ridge             | Shared Exported CSV Pipeline |  12.000000 | 184,179.072853 | 121,647.998532 | 63,196,317,849.440880 | 0.668661 | True        | False                 |    628.000000 |        nan        |           nan        |                    208 |
| Ridge             | Shared Exported CSV Pipeline |  20.000000 | 183,963.020855 | 121,565.339227 | 63,211,318,292.613777 | 0.668582 | True        | False                 |    572.000000 |        nan        |           nan        |                    208 |
| Ridge             | Shared Exported CSV Pipeline |  30.000000 | 183,715.996766 | 121,475.039633 | 63,231,547,877.114883 | 0.668476 | True        | False                 |    493.000000 |        nan        |           nan        |                    208 |
| Ridge             | Shared Exported CSV Pipeline |  50.000000 | 183,287.610837 | 121,330.407415 | 63,274,712,808.113808 | 0.668250 | True        | False                 |    406.000000 |        nan        |           nan        |                    208 |
| Ridge             | Shared Exported CSV Pipeline | 100.000000 | 182,447.601226 | 121,085.411089 | 63,387,718,417.768707 | 0.667657 | True        | False                 |    325.000000 |        nan        |           nan        |                    208 |
| Lasso             | Shared Exported CSV Pipeline | 100.000000 | 180,751.622378 | 120,854.078798 | 63,328,748,447.098015 | 0.667966 | True        | False                 | 47,028.000000 | 15,303,523.865787 |    15,303,681.888647 |                    167 |
| Lasso             | Shared Exported CSV Pipeline |  60.000000 | 182,176.241328 | 121,158.166892 | 63,253,208,125.679558 | 0.668362 | True        | False                 | 30,433.000000 | 15,301,552.241053 |    15,303,681.888647 |                    184 |
| Lasso             | Shared Exported CSV Pipeline |  30.000000 | 183,288.388677 | 121,430.645487 | 63,205,811,942.377747 | 0.668611 | True        | False                 | 31,873.000000 | 15,299,479.451179 |    15,303,681.888647 |                    191 |
| Lasso             | Shared Exported CSV Pipeline |  20.000000 | 183,693.516604 | 121,546.492264 | 63,196,886,598.806793 | 0.668658 | True        | False                 | 27,364.000000 | 15,303,535.972581 |    15,303,681.888647 |                    195 |
| Lasso             | Shared Exported CSV Pipeline |  10.000000 | 184,114.013367 | 121,669.195798 | 63,184,740,162.774429 | 0.668721 | True        | False                 | 31,202.000000 | 15,300,274.726560 |    15,303,681.888647 |                    198 |

## Original Feature Set D comparison

| Model             | Data Representation      | feature_set                           |      alpha |        WAE_2_1 |            MAE |                   MSE |       R2 | run_id   |
|:------------------|:-------------------------|:--------------------------------------|-----------:|---------------:|---------------:|----------------------:|---------:|:---------|
| Linear Regression | Original Linear Pipeline | D - Combined + Size x Age Interaction | nan        | 157,254.530691 | 113,051.204225 | 54,135,001,187.274078 | 0.716169 | V005     |
| Ridge             | Original Linear Pipeline | D                                     |  12.000000 | 153,109.493697 | 110,441.403536 | 52,303,501,091.830894 | 0.725772 | V028     |
| Lasso             | Original Linear Pipeline | D                                     |  20.000000 | 152,566.388979 | 110,000.675201 | 51,756,702,159.375198 | 0.728639 | V155     |

The two preprocessing pipelines have different feature representations, so their score differences cannot be attributed to the regression algorithm alone. This supplement does not replace the original linear selection or decide the final group model.

Historical record note: `linear_feature_set_results.csv` differs from the 155-run register for Linear D by $0.00 in WAE (2:1). The comparison table uses the 155-run register and does not alter either historical file.

Linear Regression matrix rank: 204/209; singular-value condition ratio: 1.12e+16.

Ridge grid: 5, 10, 12, 20, 30, 50, 100; one bounded extension after the initial minimum reached alpha 20. Lasso path: 100, 60, 30, 20, 10; warm starts and 100,000 maximum iterations address the non-convergence observed at alpha 10-30 without changing the exported features. Only converged fits are eligible for each model summary.

Target-encoded predictors: 13. Their training values were created out of fold and validation mappings were fitted on training only by the frozen export pipeline.

Month encoding check: validation has 3,087 October transactions and `month_10` sums to 3,087. The repaired export pipeline uses January as the reference category in every split. The pre-fix supplementary results are archived under backup_before_month_fix_20261027.
