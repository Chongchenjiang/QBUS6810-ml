# QBUS6810 notebook verification report (25 Oct 2026)

Scope: `QBUS6810-ml/assignment_6810.ipynb` and the files it writes. The Word report was not opened or modified. The agreed chronological split (train Jan 2023 to Jun 2024, validation Jul to Dec 2024, test 2025) and the WAE 2:1 selection rule were not changed, and no 2025 outcome was used.

## Environment

All runs used Python 3.9.13, numpy 1.21.5, pandas 1.4.4, scipy 1.9.1, scikit-learn 1.0.2, statsmodels 0.13.2, matplotlib 3.5.2, seaborn 0.11.2, tabulate 0.8.10, with MKL 2021.4. These are the Anaconda 2022.10 versions that the original outputs came from. The environment was built from conda-forge. It must be activated, i.e. `Library\bin` must be on PATH; otherwise numpy crashes on the first plot.

## Checks actually executed

| # | Check | Result |
|---|---|---|
| 1 | Clean sequential run of all 153 cells in one fresh kernel | Passed. All 82 non-empty code cells ran with counts 1–82 in order, with no errors and no convergence warnings. The only stderr is the Yeo-Johnson divide-by-zero warning in cell 97, which the original run also printed. Outputs are saved in the notebook. |
| 2a | `property_id` merge | Passed. In the legacy merge (cell 19) and both modelling rebuilds (cells 132 and 148), every sale's 97 features equal the `properties_2022.csv` record for its `property_id`. Rows keep `sales.csv` order. |
| 2b | Pre-repair merge | Reproduced in pandas 1.4.4. It joined on the `property_id` index, so each sale did get its own property's features. The join returned the rows sorted by `property_id`, however, and later steps dropped the IDs. The archived snapshots therefore cannot be linked back to `transaction_id`, and the overlap check printed 0. |
| 2c | Chronological split membership | Passed. Train has 54,853 sales, validation 18,132 and test 36,322. The sets are disjoint, cover all 109,307 sales and respect the exact date boundaries; modelling rows follow membership order. Overlap: 1,677 validation sales (1,666 properties) involve a property sold during training. |
| 2d | Target alignment | Passed. Every target vector equals the raw `sale_price` looked up by `transaction_id`. The saved `data/split/{train,validation,test}.csv` equal the regenerated frames cell for cell. |
| 2e | Exclusion of ID-derived features | Passed. None of the 17 modelling feature lists, the fitted Feature Set D encoder (98 inputs → 3,817 columns) or the legacy matrices contains an ID, target or date column, or a copy of `property_id`. |
| 3 | Independence of the Linear/Ridge/Lasso experiments from the old merge | Confirmed and re-run. These cells rebuild their data from the raw CSVs with their own `property_id` merge and never read the legacy snapshots. |
| 4 | Lasso D (α=20) and Ridge D (α=10) validation WAE | Lasso D α=20 is unchanged: WAE 2:1 $152,566.3890, 3,112 iterations. Ridge D α=10 moved from $153,116.66 to $153,123.27; see "Ridge tolerance" below. |
| 5 | Isolation of the 2025 test targets | Passed. The modelling cells load prices only for rows dated 2024 or earlier. In a copy of the project with all 36,322 prices from 2025 scrambled, every training/validation frame, design matrix, target and result CSV came out byte-identical. Only `test.csv`, which stores the 2025 prices, differed. |

## Ridge tolerance (fixed at the user's request)

The original Ridge fits used `sparse_cg` with `tol=1e-4`. That setting stops early: the coefficients were up to about 9,000 away from the exact solution, and results differed between machines. Ridge now uses `tol=1e-10`. Every Ridge D value then equals an independent exact Cholesky solution.

| Ridge D | Original (tol=1e-4) | Now (tol=1e-10) = exact |
|---|---|---|
| α=10 | 153,116.66 | 153,123.27 |
| α=12 | 153,133.05 | **153,109.49** (best Ridge D) |

Final selections are unchanged. The main-scenario model is Lasso D α=20. With its predictions held fixed across the three weightings:

| Scenario | Lasso D α=20 WAE | Reduction vs Global Mean baseline |
|---|---|---|
| Main (2:1) | $152,566.39 | 55.44% |
| Equal (1:1) | $110,000.68 | 53.90% |
| Undervaluation (1:2) | $177,435.64 | 52.48% |

Under the two alternative scenarios the lowest-WAE candidate is still Ridge E6 α=8: $104,068.43 under 1:1 and $150,381.70 under 1:2.

## Cells changed

- Cell 0: required packages, the conda command, how to run, runtime and memory.
- Cell 124: describes the snapshot rule that cell 125 actually applies.
- Cell 125: corrected archive-note wording.
- Cells 138, 140, 142, 148: Ridge `tol=1e-4` → `tol=1e-10` (five calls).
- Cell 151: Lasso log line computed from results instead of hard-coded; Ridge rows in the run register record `tol=1e-10`.
- Cells 149, 152: hard-coded numbers updated to the new outputs.
- Cell 2: `save_figure()` helper. Cells 43, 45, 63, 65, 89, 90, 101, 105 and 108 call it before each `plt.show()`, saving every figure as a PNG in `data/result/figures/`.
- Cell 127: saves the Global Mean baseline tables to `data/result/baseline/`.
- Cell 129: saves the repeated-property overlap summary to `data/result/diagnostics/`.
- All code-cell outputs were regenerated by a final clean sequential run on 26 Oct 2026. In that run all 28 checks passed again, and every model result file was byte-identical to the previous run.

## Files changed

- `assignment_6810.ipynb`
- 24 regenerated CSV/MD files in `data/result/linear_models/`
- New: `data/result/figures/` holds 44 PNGs. Files 01–11 are the EDA figures; the `12_category_*` files are one per categorical feature. Cell 108 also saves a `property_id` plot, which is irrelevant output.
- New: `data/result/baseline/global_mean_baseline_metrics.csv` and `global_mean_baseline_wae_sensitivity.csv`
- New: `data/result/diagnostics/property_overlap_summary.csv`
- `data/split/manifest.json`: verification timestamp and code hash
- `data/split/archive_invalid_index_merge/README.txt`: corrected wording

The split CSVs, the membership files and `continuous_outlier_report.csv` are unchanged.

## Remaining issues (not fixed)

- `data/result/linear_models/experiment_results_summary.md` is a hand-written summary that still quotes Ridge D α=10 ($153,116.66) and other tol=1e-4 Ridge numbers.
- `data/split/README.md` is outdated: it says 199 columns (now 211) and says the baseline is the final cell.
- The Word report may cite "Ridge D α=10, $153,116.66" or describe the old merge as a "row index" join. Both should be revised.
- Cell 108 (legacy EDA) treats `property_id` as a categorical feature and plots, prints and now saves it (`12_category_property_id.png`). It never reaches a model, but it is irrelevant output.
- Ridge and Linear Regression validation predictions are not saved per transaction; only Lasso's are.
- Cell 125 keeps an existing snapshot without comparing its feature values. They were checked separately and match.
- Cell 125 compares prices with zero tolerance. This works because all prices are whole dollars.
- The code uses `OneHotEncoder(sparse=True)`, which requires scikit-learn < 1.4. The header states this.
