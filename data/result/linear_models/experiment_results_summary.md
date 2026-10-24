# QBUS6810 Validation Experiment Results

## Scope and evaluation design

These results were produced using the frozen chronological development split: January 2023 to June 2024 for training and July 2024 to December 2024 for validation. The training set contains 54,853 transactions and the validation set contains 18,132 transactions. The 2025 test set was not used for feature development, hyperparameter tuning, or model selection.

All learned preprocessing was fitted on the training data and then applied to the validation data. `sale_price` was the response. `sale_price`, `log_sale_price`, `property_id`, and `transaction_id` were excluded from the predictors. Property identifiers were used only for the repeated-property diagnostic.

The reported metrics are MSE, R-squared, MAE, and weighted absolute error (WAE). MSE is measured in squared dollars, while MAE and WAE are measured in dollars. Lower MSE, MAE, and WAE values are better, whereas higher R-squared values are better. The WAE scenarios use overvaluation-to-undervaluation weights of 2:1, 1:1, and 1:2. Predictions remain fixed when the weights change. The prespecified main decision criterion is WAE 2:1, reflecting greater concern about overvaluation.

## Repeated property overlap check

The overlap diagnostic found that 1,677 of the 18,132 validation transactions belonged to properties that also appeared in the training period. These transactions represented 1,666 distinct overlapping properties. The remaining 16,455 validation transactions were classified as unseen, so 9.2488% of validation transactions were classified as seen.

This property overlap is not, by itself, evidence of data leakage. It represents the realistic case in which a property sold during the training period and sold again during the later validation period. Leakage would occur if information unavailable at the valuation date, including future outcomes or statistics fitted using validation data, entered the training process. The chronological split and training-only preprocessing prevent that form of leakage. However, seen and unseen performance can still be reported separately as a sensitivity check because repeat-sale properties may differ from the broader valuation population.

## Global Mean baseline

The Global Mean baseline predicted the training-set mean sale price of $418,490.00 for every validation transaction.

| Baseline | MSE ($ squared) | R-squared | MAE ($) | WAE 2:1 ($) | WAE 1:1 ($) | WAE 1:2 ($) |
|---|---:|---:|---:|---:|---:|---:|
| Global Mean | 191,693,119,024.9674 | -0.0050 | 238,599.6175 | 342,381.8231 | 238,599.6175 | 373,417.0295 |

The negative validation R-squared shows that the constant training-mean prediction performed slightly worse than predicting the validation mean after the fact. The baseline remains appropriate because it is a simple, training-only reference and does not use validation information.

## Linear Regression feature-set experiment

The feature sets were compared using the same training and validation observations. Feature Set A contained location variables, Feature Set B contained property variables, Feature Set C combined A and B, and Feature Set D added the size-by-archive-age interaction to C.

| Feature set | Original features | Encoded features | MSE ($ squared) | R-squared | MAE / WAE 1:1 ($) | WAE 2:1 ($) | WAE 1:2 ($) |
|---|---:|---:|---:|---:|---:|---:|---:|
| A - Location | 67 | 3,725 | 79,606,412,714.7681 | 0.582622 | 136,668.6075 | 192,466.8207 | 217,539.0019 |
| B - Property | 30 | 91 | 98,796,264,497.1309 | 0.482010 | 173,945.1838 | 246,665.9038 | 275,169.6475 |
| C - Combined | 97 | 3,816 | 54,778,997,046.8485 | 0.712793 | 113,324.3697 | 157,671.3518 | 182,301.7572 |
| D - Combined plus Size x Archive Age | 98 | 3,817 | 54,135,001,187.2741 | 0.716169 | 113,051.2042 | 157,254.5307 | 181,899.0820 |

Feature Set C substantially improved on either group alone, showing that location and property characteristics provide complementary information. Adding the size-by-archive-age interaction in Feature Set D produced a small further improvement across all reported validation metrics. This is evidence for retaining the interaction, although the gain is modest.

## Initial model-family comparison on Feature Set D

Linear Regression, Ridge, and Lasso were compared using Feature Set D. The initial results were:

| Model | Alpha | MSE ($ squared) | R-squared | MAE ($) | WAE 2:1 ($) | WAE 1:2 ($) | Note |
|---|---:|---:|---:|---:|---:|---:|---|
| Linear Regression | N/A | 54,135,001,187.2741 | 0.716169 | 113,051.2042 | 157,254.5307 | 181,899.0820 | Unregularised reference |
| Ridge | 0.1 | 53,520,706,768.8026 | 0.719390 | 112,516.9398 | 156,444.7693 | 181,106.0502 | Initial grid |
| Ridge | 1 | 52,337,623,332.2872 | 0.725593 | 111,279.3378 | 154,530.7309 | 179,307.2824 | Initial grid |
| Ridge | 10 | 52,210,667,718.5284 | 0.726259 | 110,436.6422 | 153,116.6621 | 178,193.2646 | Best initial Ridge candidate |
| Ridge | 100 | 54,293,136,968.2231 | 0.715340 | 111,740.5135 | 154,987.7816 | 180,233.7589 | Initial grid |
| Ridge | 1,000 | 58,805,160,700.6641 | 0.691684 | 116,111.9510 | 161,630.3513 | 186,705.5019 | Initial grid |
| Lasso | 10 | 52,020,786,161.2794 | 0.727254 | 110,164.7037 | 153,042.4509 | 177,451.6601 | Did not converge at 500 iterations |
| Lasso | 100 | 53,147,850,447.0833 | 0.721345 | 112,218.7424 | 155,512.6113 | 181,143.6159 | 354 non-zero coefficients |
| Lasso | 1,000 | 59,889,230,450.6355 | 0.686000 | 119,519.2456 | 166,641.9415 | 191,915.7954 | 88 non-zero coefficients |
| Lasso | 10,000 | 72,038,978,936.9234 | 0.622299 | 130,311.5683 | 182,799.2691 | 208,135.4359 | 19 non-zero coefficients |

The initial screen indicated that moderate regularisation improved on unregularised Linear Regression. Ridge was numerically stable, while the most competitive initial Lasso candidate required a stricter convergence check.

## Refined Ridge tuning

Ridge was refined around the initial optimum. Alpha 10 produced the lowest main-scenario WAE in this grid and also gave the best Ridge result under the other two WAE scenarios.

| Ridge alpha | MAE / WAE 1:1 ($) | WAE 2:1 ($) |
|---:|---:|---:|
| 2 | 110,849.5734 | 153,853.5900 |
| 5 | 110,539.4221 | 153,324.5789 |
| 8 | 110,460.3788 | 153,169.0623 |
| 10 | 110,436.6422 | 153,116.6621 |
| 12 | 110,454.9104 | 153,133.0516 |
| 15 | 110,463.9679 | 153,126.3880 |
| 20 | 110,526.3503 | 153,198.5963 |
| 30 | 110,676.4204 | 153,399.6729 |
| 50 | 111,024.9748 | 153,911.1992 |

The relatively flat results around alpha 10 show that the Ridge choice is not dependent on a single sharply isolated value.

## Refined Lasso tuning and convergence check

The Lasso screen used a higher iteration allowance and focused on alpha values from 10 to 200.

| Lasso alpha | MAE / WAE 1:1 ($) | WAE 2:1 ($) | Screening convergence result |
|---:|---:|---:|---|
| 10 | 110,160.3113 | 153,037.9142 | Warning at 5,000 iterations |
| 20 | 110,000.9998 | 152,566.4861 | No warning in screening run |
| 30 | 110,284.6904 | 152,846.8038 | No warning |
| 50 | 110,988.1836 | 153,735.1189 | No warning |
| 70 | 111,582.2874 | 154,582.0578 | No warning |
| 100 | 112,220.2530 | 155,515.8289 | No warning |
| 150 | 113,230.3878 | 157,013.4615 | No warning |
| 200 | 114,013.9668 | 158,203.9149 | No warning |

The earlier alpha-20 strict fit reached its 5,000-iteration limit, so the convergence experiment was repeated with training-only centering and a precomputed Gram matrix. This accelerates the same Lasso objective without changing Feature Set D, the training observations, the dollar-scale target, or the alpha values. Every alpha from 10 to 10,000 converged at `tol=1e-4` within 50,000 iterations. Alpha 20 remained the main-scenario winner and was then confirmed at `tol=1e-5`, converging in 3,112 iterations. Its independently calculated dual gap was 1,529,466.05, below the training-only threshold of 1,530,368.19. The confirmed validation results were MSE 51,756,702,159.3747, R-squared 0.728639, MAE $110,000.6752, WAE 2:1 $152,566.3890, and WAE 1:2 $177,435.6366, with 1,074 non-zero coefficients. Tightening the tolerance changed validation predictions by only $5.78 on average relative to the converged `tol=1e-4` solution. The convergence problem is therefore resolved. Lasso sparsity can support feature selection, but a zero coefficient under penalisation does not prove that the corresponding original feature is unimportant in every context.

## Domain-guided interaction experiments

The interaction experiment added only interactions with a plausible property-valuation interpretation. The candidates covered a time-aware base, building size by age, building size by class, building size by township, log land size by township, and basement type by floodplain status. A combined specification included all selected domain interactions. Meta CDU was not interacted because its training distribution was extremely imbalanced: 53,963 observations were `AV`, compared with 691 `GD`, 94 `VG`, 43 `FR`, 4 `PR`, 1 `VP`, and 57 missing observations. Avoiding these sparse interactions reduced the risk of unstable estimates.

The best Ridge alpha for each interaction feature set under the main WAE 2:1 criterion was:

| Feature set | Original features | Encoded features | Selected alpha | MSE ($ squared) | R-squared | MAE / WAE 1:1 ($) | WAE 2:1 ($) | WAE 1:2 ($) |
|---|---:|---:|---:|---:|---:|---:|---:|
| C0 - Supplied Combined | 97 | 3,816 | 12 | 53,040,217,461.0408 | 0.721909 | 110,697.8682 | 153,518.4843 | 178,575.1204 |
| E0 - Time-Aware Base | 99 | 3,818 | 8 | 52,397,122,880.7728 | 0.725281 | 110,006.1795 | 169,543.5477 | 160,474.9907 |
| E1 - Time Base plus Size x Age | 100 | 3,819 | 8 | 51,672,163,775.8034 | 0.729082 | 109,585.0811 | 168,916.0634 | 159,839.1800 |
| E2 - Time Base plus Size x Class | 112 | 3,831 | 8 | 48,984,822,558.2806 | 0.743172 | 108,225.1038 | 166,941.2348 | 157,734.0766 |
| E3 - Time Base plus Size x Township | 136 | 3,855 | 12 | 47,412,465,076.5588 | 0.751416 | 106,626.5969 | 165,529.3436 | 154,350.4471 |
| E4 - Time Base plus Log Land x Township | 137 | 3,856 | 5 | 48,039,418,357.4202 | 0.748129 | 107,785.6875 | 166,767.2649 | 156,589.7977 |
| E5 - Time Base plus Basement x Flood | 102 | 3,821 | 8 | 52,400,555,885.5938 | 0.725263 | 110,015.9458 | 169,567.0602 | 160,480.7771 |
| E6 - Combined Domain Interactions | 191 | 3,910 | 5 | 41,971,105,547.5078 | 0.779945 | 104,071.2354 | 161,807.3522 | 150,406.3539 |

The combined interaction model E6 materially improved MSE, R-squared, MAE, and WAE 1:2. Its main-scenario WAE 2:1 was nevertheless worse than the Feature Set D Ridge and converged Lasso models. This pattern shows that the interactions were informative, but they changed the balance between overvaluation and undervaluation errors rather than improving every business-weighted objective simultaneously.

## Overall validation-stage model selection

All eligible validation candidates were compared under the three fixed WAE scenarios. The selected model changes when the error-direction priority changes:

| Scenario | Selected validation model | Alpha | MSE ($ squared) | R-squared | MAE ($) | Scenario WAE ($) |
|---|---|---:|---:|---:|---:|---:|
| Main: greater concern about overvaluation (2:1) | Lasso with Feature Set D | 20 | 51,756,702,159.3747 | 0.728639 | 110,000.6752 | 152,566.3890 |
| Alternative: equal priority (1:1) | Ridge with E6: Combined Domain Interactions | 8 | 42,178,351,976.5333 | 0.778858 | 104,070.8691 | 104,070.8691 |
| Alternative: greater concern about undervaluation (1:2) | Ridge with E6: Combined Domain Interactions | 8 | 42,178,351,976.5333 | 0.778858 | 104,070.8691 | 150,381.6516 |

For the E6 model at alpha 8, the main-scenario WAE 2:1 was $161,830.9556. This was higher than $153,116.6621 for Feature Set D Ridge alpha 10 and $152,566.3890 for Feature Set D Lasso alpha 20. Therefore, the interactions remain useful, but the preferred model depends on the error-direction priority specified before model selection. Under the prespecified 2:1 overvaluation priority, the validation-stage choice is the converged Lasso alpha-20 model with Feature Set D. Under equal weighting or greater concern about undervaluation, the combined-interaction Ridge model is preferred.

## Development-stage decision and limitations

The current evidence supports Lasso alpha 20 with Feature Set D as the provisional model under the prespecified main WAE 2:1 scenario. With these predictions held fixed, its WAE was $152,566.39 under 2:1, $110,000.68 under 1:1, and $177,435.64 under 1:2. These values were respectively 55.44%, 53.90%, and 52.48% lower than the Global Mean baseline. The combined-interaction Ridge model is retained as an important sensitivity result because it achieved the strongest general accuracy and was preferred under the two alternative weighting scenarios.

These are validation results, not final estimates of out-of-sample performance. The 2025 test set must remain untouched until the model specification and main decision rule are frozen. The final test should be run once for the selected model and the unchanged baseline. Property overlap does not establish leakage, and `unseen` in this diagnostic means only that a property was absent from this training period; it does not prove that the property had no earlier sale outside the available training window. Lasso coefficients should not be interpreted as causal importance.

## Machine-readable result files

The exact candidate-level outputs are stored in the same `data/result/linear_models` directory:

- `linear_feature_set_results.csv`: Linear Regression results for Feature Sets A to D.
- `model_candidate_results.csv`: Initial Linear Regression, Ridge, and Lasso comparison.
- `refined_alpha_results.csv`: Refined Ridge and Lasso alpha results.
- `refined_scenario_winners.csv`: Scenario winners from refined tuning.
- `interaction_feature_inventory.csv`: Constructed interaction-feature inventory.
- `interaction_feature_set_results.csv`: Best main-scenario result for each interaction set.
- `interaction_ridge_candidate_results.csv`: All interaction-set and Ridge-alpha candidates.
- `interaction_scenario_winners.csv`: Best interaction candidate under each WAE scenario.
- `overall_model_selection_candidates.csv`: Combined eligible validation candidates.
- `overall_model_selection_winners.csv`: Overall validation winner under each WAE scenario.
- `lasso_convergence_results.csv`: Strict Lasso convergence diagnostics and validation metrics.
- `lasso_validation_predictions.csv`: Validation predictions from each strict Lasso fit.
- `validation_results_all_runs.csv`: Complete 115-row register of recorded validation runs.
- `validation_results_table.csv`: Compact 15-row comparison with one representative per model family and feature set.
- `validation_results_table.md`: Report-readable unified results table and complete run register.
- `selected_model_fixed_scenario_comparison.csv`: Fixed selected-model predictions compared with the baseline under all three WAE scenarios.

