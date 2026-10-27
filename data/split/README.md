# Fixed notebook split

The official `train.csv`, `validation.csv`, and `test.csv` files contain the final feature snapshots produced by `assignment_6810.ipynb`. Use these files for the shared Train, Validation, and Test data.

| File | Time period | Rows | Columns |
| --- | --- | ---: | ---: |
| `train.csv` | January 2023 through June 2024 | 54,853 | 211 |
| `validation.csv` | July through December 2024 | 18,132 | 211 |
| `test.csv` | January through December 2025 | 36,322 | 211 |

The CSV files preserve the final column order and row order and can be inspected outside Python. Load them with `pd.read_csv("data/split/train.csv")`, `pd.read_csv("data/split/validation.csv")`, or `pd.read_csv("data/split/test.csv")`. CSV does not store pandas-specific dtypes or the positional DataFrame index. `manifest.json` records the input and pipeline checksums, split membership, and checksums of all three official files.

`candidate_export/` contains the validated repaired CSVs that were used to publish the official files. Their SHA-256 hashes match the official CSVs. It is a publication reference, not a separate dataset for group members to load.

Month indicators now use a fixed January reference category in all three splits. The October 2024 validation transactions have `month_10=1`; the other month columns, schema, row order, and targets were unchanged by this correction. `month_fix_staging_20261027/` contains the independently compared candidates used to verify the correction before publication.

`backup_before_export_fix_20261026/` contains the three pre-fix CSVs and their old manifest. Keep it only for rollback or historical comparison; do not use those CSVs for modelling. The notebook's export cell and the manifest refer to these directories, so update those references if the directories are later removed.

`backup_before_month_fix_20261027/` contains the official CSVs and manifest immediately before the October month-indicator correction. Use the current official CSVs for modelling.

The final frames contain both `sale_price` and its derived `log_sale_price`. Exclude both columns from predictive features. The original `property_id` index was removed by the notebook's existing encoding steps; the saved index is positional and is not a property identifier.

The Global Mean baseline appears in Cell 127 of `assignment_6810.ipynb`. It predicts the training mean sale price for every validation transaction and reports MSE, R2, and MAE. No test-set metrics are calculated or saved.

Group members can read the official CSVs directly without running the notebook's full modelling experiments.
