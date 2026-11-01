# Shared CSV Linear Comparison

Training rows: 54,853; validation rows: 18,132; predictors: 209. No 2025 outcomes were loaded.

WAE (2:1) is selected in advance as the primary metric. Higher predictions than actual sales receive weight 2; other errors receive weight 1. MAE is in dollars, MSE in squared dollars, and R² is unitless.

scikit-learn version: 1.8.0. All models use the same 209 exported numeric predictors without additional imputation, encoding, scaling, or feature engineering.

## Best converged candidate per model

| Model             | Data Representation          |      alpha |        WAE_2_1 |            MAE |                   MSE |       R2 |
|:------------------|:-----------------------------|-----------:|---------------:|---------------:|----------------------:|---------:|
| Linear Regression | Shared Exported CSV Pipeline | nan        | 192,979.185936 | 127,426.799123 | 65,858,789,930.242401 | 0.654701 |
| Ridge             | Shared Exported CSV Pipeline | 100.000000 | 190,929.164827 | 126,875.707469 | 66,286,384,364.572578 | 0.652459 |
| Lasso             | Shared Exported CSV Pipeline | 100.000000 | 189,367.774872 | 126,647.480985 | 66,155,138,390.242363 | 0.653148 |

## All tested configurations

| Model             | Data Representation          |      alpha |        WAE_2_1 |            MAE |                   MSE |       R2 | converged   | convergence_warning   |        n_iter |          dual_gap |   dual_gap_threshold |   nonzero_coefficients |
|:------------------|:-----------------------------|-----------:|---------------:|---------------:|----------------------:|---------:|:------------|:----------------------|--------------:|------------------:|---------------------:|-----------------------:|
| Linear Regression | Shared Exported CSV Pipeline | nan        | 192,979.185936 | 127,426.799123 | 65,858,789,930.242401 | 0.654701 | True        | False                 |    nan        |        nan        |           nan        |                    209 |
| Ridge             | Shared Exported CSV Pipeline |   5.000000 | 192,794.125819 | 127,360.561246 | 65,880,004,495.574371 | 0.654590 | True        | False                 |    891.000000 |        nan        |           nan        |                    209 |
| Ridge             | Shared Exported CSV Pipeline |  10.000000 | 192,643.841805 | 127,309.374171 | 65,902,921,583.234306 | 0.654470 | True        | False                 |    672.000000 |        nan        |           nan        |                    209 |
| Ridge             | Shared Exported CSV Pipeline |  12.000000 | 192,586.491840 | 127,290.293929 | 65,912,107,053.880943 | 0.654422 | True        | False                 |    655.000000 |        nan        |           nan        |                    209 |
| Ridge             | Shared Exported CSV Pipeline |  20.000000 | 192,373.561722 | 127,222.603607 | 65,948,476,943.293816 | 0.654231 | True        | False                 |    587.000000 |        nan        |           nan        |                    209 |
| Ridge             | Shared Exported CSV Pipeline |  30.000000 | 192,135.453627 | 127,152.340617 | 65,992,939,219.119308 | 0.653998 | True        | False                 |    481.000000 |        nan        |           nan        |                    209 |
| Ridge             | Shared Exported CSV Pipeline |  50.000000 | 191,717.221150 | 127,038.888469 | 66,079,313,565.035118 | 0.653545 | True        | False                 |    407.000000 |        nan        |           nan        |                    209 |
| Ridge             | Shared Exported CSV Pipeline | 100.000000 | 190,929.164827 | 126,875.707469 | 66,286,384,364.572578 | 0.652459 | True        | False                 |    317.000000 |        nan        |           nan        |                    209 |
| Lasso             | Shared Exported CSV Pipeline | 100.000000 | 189,367.774872 | 126,647.480985 | 66,155,138,390.242363 | 0.653148 | True        | False                 | 47,508.000000 | 15,301,356.751208 |    15,303,681.888647 |                    170 |
| Lasso             | Shared Exported CSV Pipeline |  60.000000 | 190,634.252592 | 126,852.394618 | 66,002,412,029.575912 | 0.653948 | True        | False                 | 30,526.000000 | 15,302,651.550881 |    15,303,681.888647 |                    185 |
| Lasso             | Shared Exported CSV Pipeline |  30.000000 | 191,677.293820 | 127,059.621957 | 65,904,320,871.506454 | 0.654463 | True        | False                 | 32,160.000000 | 15,301,859.324230 |    15,303,681.888647 |                    191 |
| Lasso             | Shared Exported CSV Pipeline |  20.000000 | 192,064.624514 | 127,154.877262 | 65,882,205,300.448196 | 0.654579 | True        | False                 | 27,686.000000 | 15,303,538.612382 |    15,303,681.888647 |                    193 |
| Lasso             | Shared Exported CSV Pipeline |  10.000000 | 192,485.952160 | 127,271.378968 | 65,865,646,107.084572 | 0.654665 | True        | False                 | 31,569.000000 | 15,301,103.184903 |    15,303,681.888647 |                    195 |

## Original Feature Set D comparison

| Model             | Data Representation      | feature_set                           |      alpha |        WAE_2_1 |            MAE |                   MSE |       R2 | run_id   |
|:------------------|:-------------------------|:--------------------------------------|-----------:|---------------:|---------------:|----------------------:|---------:|:---------|
| Linear Regression | Original Linear Pipeline | D - Combined + Size x Age Interaction | nan        | 157,254.419439 | 113,051.173551 | 54,137,242,604.027603 | 0.716158 | V005     |
| Ridge             | Original Linear Pipeline | D                                     |  12.000000 | 153,109.493712 | 110,441.403549 | 52,303,501,089.964081 | 0.725772 | V028     |
| Lasso             | Original Linear Pipeline | D                                     |  20.000000 | 152,566.388979 | 110,000.675201 | 51,756,702,159.382683 | 0.728639 | V155     |

The two preprocessing pipelines have different feature representations, so their score differences cannot be attributed to the regression algorithm alone. This supplement does not replace the original linear selection or decide the final group model.

Historical record note: `linear_feature_set_results.csv` differs from the 155-run register for Linear D by $0.00 in WAE (2:1). The comparison table uses the 155-run register and does not alter either historical file.

Linear Regression matrix rank: 205/209; singular-value condition ratio: 1.12e+16.

Ridge grid: 5, 10, 12, 20, 30, 50, 100; one bounded extension after the initial minimum reached alpha 20. Lasso path: 100, 60, 30, 20, 10; warm starts and 100,000 maximum iterations address the non-convergence observed at alpha 10-30 without changing the exported features. Only converged fits are eligible for each model summary.

Target-encoded predictors: 13. Their training values were created out of fold and validation mappings were fitted on training only by the frozen export pipeline.

Month encoding check: validation has 3,087 October transactions and `month_10` sums to 3,087. The repaired export pipeline uses January as the reference category in every split. The pre-fix supplementary results are archived under backup_before_month_fix_20261027.
