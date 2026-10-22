# Fixed notebook split

These files contain the final `train_data`, `val_data`, and `test_data` DataFrames produced by `assignment_6810.ipynb` after its existing preparation cells. That notebook is the single assignment notebook and contains the export and baseline cells at the end.

| File | Time period | Rows | Columns |
| --- | --- | ---: | ---: |
| `train.csv` | January 2023 through June 2024 | 54,853 | 199 |
| `validation.csv` | July through December 2024 | 18,132 | 199 |
| `test.csv` | January through December 2025 | 36,322 | 199 |

The CSV files preserve the final column order and row order and can be inspected outside Python. Load them with `pd.read_csv("data/split/train.csv")`, `pd.read_csv("data/split/validation.csv")`, or `pd.read_csv("data/split/test.csv")`. CSV does not store pandas-specific dtypes or the positional DataFrame index, so the notebook verifies the saved values, columns, and shapes after reading each file. `manifest.json` records the input checksums, original pipeline code checksum, and checksums of all three split files.

The final frames contain both `sale_price` and its derived `log_sale_price`. Exclude both columns from predictive features. The original `property_id` index was removed by the notebook's existing encoding steps; the saved index is positional and is not a property identifier.

The Global Mean baseline appears in the final code cell of `assignment_6810.ipynb`. It predicts the training mean sale price for every validation transaction and reports MSE, R2, and MAE. No test-set metrics are calculated or saved.

To reproduce the files and metrics, open `assignment_6810.ipynb` from the project directory and run its cells in order. The final two code cells perform the export and baseline calculation.
