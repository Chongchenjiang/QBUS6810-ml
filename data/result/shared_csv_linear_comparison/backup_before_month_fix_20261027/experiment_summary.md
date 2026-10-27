# Shared CSV Linear Comparison

Training rows: 54,853; validation rows: 18,132; predictors: 209. No 2025 outcomes were loaded.

WAE (2:1) is selected in advance as the primary metric. Higher predictions than actual sales receive weight 2; other errors receive weight 1. MAE is in dollars, MSE in squared dollars, and R² is unitless.

scikit-learn version: 1.0.2. All models use the same 209 exported numeric predictors without additional imputation, encoding, scaling, or feature engineering.

## Best converged candidate per model

| Model             | Data Representation          |      alpha |        WAE_2_1 |            MAE |                   MSE |       R2 |
|:------------------|:-----------------------------|-----------:|---------------:|---------------:|----------------------:|---------:|
| Linear Regression | Shared Exported CSV Pipeline | nan        | 182,474.177235 | 121,848.562141 | 63,226,202,834.180908 | 0.668504 |
| Ridge             | Shared Exported CSV Pipeline | 100.000000 | 180,907.649374 | 121,105.010171 | 63,412,323,443.135796 | 0.667528 |
| Lasso             | Shared Exported CSV Pipeline | 100.000000 | 179,891.823454 | 120,841.470815 | 63,336,389,368.210526 | 0.667926 |

## All tested configurations

| Model             | Data Representation          |      alpha |        WAE_2_1 |            MAE |                   MSE |       R2 | converged   | convergence_warning   |        n_iter |          dual_gap |   dual_gap_threshold |   nonzero_coefficients |
|:------------------|:-----------------------------|-----------:|---------------:|---------------:|----------------------:|---------:|:------------|:----------------------|--------------:|------------------:|---------------------:|-----------------------:|
| Linear Regression | Shared Exported CSV Pipeline | nan        | 182,474.177235 | 121,848.562141 | 63,226,202,834.180908 | 0.668504 | True        | False                 |    nan        |        nan        |           nan        |                    209 |
| Ridge             | Shared Exported CSV Pipeline |   5.000000 | 182,331.404688 | 121,775.154966 | 63,228,169,073.717049 | 0.668494 | True        | False                 |    853.000000 |        nan        |           nan        |                    208 |
| Ridge             | Shared Exported CSV Pipeline |  10.000000 | 182,216.090830 | 121,713.778240 | 63,234,505,642.432884 | 0.668461 | True        | False                 |    652.000000 |        nan        |           nan        |                    208 |
| Ridge             | Shared Exported CSV Pipeline |  12.000000 | 182,172.085853 | 121,690.496176 | 63,237,431,125.860245 | 0.668445 | True        | False                 |    628.000000 |        nan        |           nan        |                    208 |
| Ridge             | Shared Exported CSV Pipeline |  20.000000 | 182,006.837130 | 121,604.409877 | 63,250,306,301.557991 | 0.668378 | True        | False                 |    572.000000 |        nan        |           nan        |                    208 |
| Ridge             | Shared Exported CSV Pipeline |  30.000000 | 181,821.613726 | 121,510.886945 | 63,268,098,984.196213 | 0.668284 | True        | False                 |    493.000000 |        nan        |           nan        |                    208 |
| Ridge             | Shared Exported CSV Pipeline |  50.000000 | 181,511.634715 | 121,363.383205 | 63,307,035,728.863007 | 0.668080 | True        | False                 |    406.000000 |        nan        |           nan        |                    208 |
| Ridge             | Shared Exported CSV Pipeline | 100.000000 | 180,907.649374 | 121,105.010171 | 63,412,323,443.135796 | 0.667528 | True        | False                 |    325.000000 |        nan        |           nan        |                    208 |
| Lasso             | Shared Exported CSV Pipeline | 100.000000 | 179,891.823454 | 120,841.470815 | 63,336,389,368.210526 | 0.667926 | True        | False                 | 47,028.000000 | 15,303,523.865787 |    15,303,681.888647 |                    167 |
| Lasso             | Shared Exported CSV Pipeline |  60.000000 | 180,811.555134 | 121,156.044271 | 63,271,271,855.863503 | 0.668268 | True        | False                 | 30,433.000000 | 15,301,552.241053 |    15,303,681.888647 |                    184 |
| Lasso             | Shared Exported CSV Pipeline |  30.000000 | 181,570.533911 | 121,447.840431 | 63,234,854,490.059837 | 0.668459 | True        | False                 | 31,873.000000 | 15,299,479.451179 |    15,303,681.888647 |                    191 |
| Lasso             | Shared Exported CSV Pipeline |  20.000000 | 181,877.693432 | 121,566.434362 | 63,228,583,335.841263 | 0.668492 | True        | False                 | 27,364.000000 | 15,303,535.972581 |    15,303,681.888647 |                    195 |
| Lasso             | Shared Exported CSV Pipeline |  10.000000 | 182,160.741288 | 121,702.344186 | 63,222,605,657.319901 | 0.668523 | True        | False                 | 31,202.000000 | 15,300,274.726560 |    15,303,681.888647 |                    198 |

## Original Feature Set D comparison

| Model             | Data Representation      | feature_set                           |      alpha |        WAE_2_1 |            MAE |                   MSE |       R2 | run_id   |
|:------------------|:-------------------------|:--------------------------------------|-----------:|---------------:|---------------:|----------------------:|---------:|:---------|
| Linear Regression | Original Linear Pipeline | D - Combined + Size x Age Interaction | nan        | 157,248.195315 | 113,045.100138 | 54,132,581,209.875946 | 0.716182 | V005     |
| Ridge             | Original Linear Pipeline | D                                     |  12.000000 | 153,109.493695 | 110,441.403535 | 52,303,501,090.818863 | 0.725772 | V028     |
| Lasso             | Original Linear Pipeline | D                                     |  20.000000 | 152,566.388979 | 110,000.675201 | 51,756,702,159.375252 | 0.728639 | V155     |

The two preprocessing pipelines have different feature representations, so their score differences cannot be attributed to the regression algorithm alone. This supplement does not replace the original linear selection or decide the final group model.

Historical record note: `linear_feature_set_results.csv` differs from the 155-run register for Linear D by $6.34 in WAE (2:1). The comparison table uses the 155-run register and does not alter either historical file.

Linear Regression matrix rank: 204/209; singular-value condition ratio: 1.12e+16.

Ridge grid: 5, 10, 12, 20, 30, 50, 100; one bounded extension after the initial minimum reached alpha 20. Lasso path: 100, 60, 30, 20, 10; warm starts and 100,000 maximum iterations address the non-convergence observed at alpha 10-30 without changing the exported features. Only converged fits are eligible for each model summary.

Target-encoded predictors: 13. Their training values were created out of fold and validation mappings were fitted on training only by the frozen export pipeline.

Known frozen-representation issue: validation has 3,087 October transactions but `month_10` sums to 0. The export code creates month dummies separately by split with `drop_first=True`, so October is the validation reference category. This experiment intentionally does not edit the frozen inputs; interpret the month effect cautiously.
