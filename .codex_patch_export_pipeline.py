import hashlib
import json
import os
from pathlib import Path


project_dir = Path(__file__).resolve().parent
notebook_path = project_dir / "assignment_6810.ipynb"

with notebook_path.open("r", encoding="utf-8") as handle:
    notebook = json.load(handle)


def source_digest(cells):
    payload = [cell.get("source", []) for cell in cells]
    return hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()


model_digest_before = source_digest(notebook["cells"][132:152])

cell_97_source = '''from sklearn.preprocessing import PowerTransformer, StandardScaler

rule_df = pd.read_csv("data/featureengineer.csv")


def get_cols(column_name):
    """Return unique non-empty feature names from one rule column."""
    if column_name not in rule_df.columns:
        return []
    return (
        rule_df[column_name]
        .dropna()
        .astype(str)
        .str.strip()
        .loc[lambda values: values.ne("")]
        .unique()
        .tolist()
    )


cols_yeojohnson = get_cols("yeojohnson")
cols_scaler = get_cols("standardscaler")
cols_clipping = get_cols("clipping")
cols_binning = get_cols("binning")
cols_remain = get_cols("remain")

# Preserve a deterministic feature order while applying the established
# clipping -> Yeo-Johnson -> scaling sequence.
continuous_cols = list(
    dict.fromkeys(cols_yeojohnson + cols_scaler + cols_clipping)
)
continuous_cols = [
    column for column in continuous_cols if column in train_data.columns
]

print(f"Continuous transformation features: {len(continuous_cols)}")
print(f"Binning features: {len(cols_binning)}")
print(f"Unchanged features: {len(cols_remain)}")

# Fit clipping limits on the training period only.
clip_bounds = {
    column: (
        train_data[column].quantile(0.01),
        train_data[column].quantile(0.99),
    )
    for column in continuous_cols
}


def clip_with_training_bounds(frame):
    clipped = frame[continuous_cols].copy()
    for column, (lower, upper) in clip_bounds.items():
        clipped[column] = clipped[column].clip(lower, upper)
    return clipped


train_clipped = clip_with_training_bounds(train_data)

# PowerTransformer can numerically collapse a non-constant feature when the
# fitted lambda is extreme. Fit on training data, detect that failure on the
# transformed training values, and fall back to clipped physical values before
# applying the training-fitted StandardScaler.
pt = PowerTransformer(method="yeo-johnson", standardize=False)
train_power_array = pt.fit_transform(train_clipped)
train_power = pd.DataFrame(
    train_power_array,
    index=train_clipped.index,
    columns=continuous_cols,
)
unstable_power_columns = [
    column
    for column in continuous_cols
    if train_clipped[column].nunique(dropna=True) > 1
    and (
        not np.isfinite(train_power[column].to_numpy(dtype=float)).all()
        or train_power[column].nunique(dropna=True) <= 1
    )
]
train_transform_input = train_power.copy()
train_transform_input.loc[:, unstable_power_columns] = train_clipped[
    unstable_power_columns
].to_numpy()

scaler = StandardScaler()
scaler.fit(train_transform_input)

for frame in (train_data, val_data, test_data):
    frame_clipped = clip_with_training_bounds(frame)
    frame_power = pd.DataFrame(
        pt.transform(frame_clipped),
        index=frame.index,
        columns=continuous_cols,
    )
    frame_power.loc[:, unstable_power_columns] = frame_clipped[
        unstable_power_columns
    ].to_numpy()
    frame_scaled = pd.DataFrame(
        scaler.transform(frame_power),
        index=frame.index,
        columns=continuous_cols,
    )
    frame.loc[:, continuous_cols] = frame_scaled

for column in continuous_cols:
    if train_clipped[column].nunique(dropna=True) > 1:
        assert train_data[column].nunique(dropna=True) > 1, (
            f"Information loss after continuous transformation: {column}"
        )

print("Continuous transformations completed with training-only fitted parameters.")
print(
    "Yeo-Johnson stability fallbacks: "
    + (", ".join(unstable_power_columns) if unstable_power_columns else "None")
)
'''

cell_98_source = '''print("Processing binned features with training-only category schemas...")


def apply_binning(frame, binning_list):
    transformed = frame.copy()

    if "char_beds" in binning_list and "char_beds" in transformed.columns:
        transformed["char_beds_bin"] = (
            transformed["char_beds"].clip(lower=1, upper=5).fillna(1).astype(int)
        )
    if "char_rooms" in binning_list and "char_rooms" in transformed.columns:
        transformed["char_rooms_bin"] = (
            transformed["char_rooms"].clip(lower=0, upper=10).fillna(0).astype(int)
        )
    if (
        "prox_num_school_in_half_mile" in binning_list
        and "prox_num_school_in_half_mile" in transformed.columns
    ):
        transformed["prox_num_school_bin"] = (
            transformed["prox_num_school_in_half_mile"]
            .clip(lower=0, upper=10)
            .fillna(0)
            .astype(int)
        )
    if (
        "prox_avg_school_rating_in_half_mile" in binning_list
        and "prox_avg_school_rating_in_half_mile" in transformed.columns
    ):
        transformed["prox_avg_school_rating_bin"] = (
            transformed["prox_avg_school_rating_in_half_mile"]
            .round()
            .clip(lower=1, upper=10)
            .fillna(1)
            .astype(int)
        )
    if (
        "other_school_district_elementary_avg_rating" in binning_list
        and "other_school_district_elementary_avg_rating" in transformed.columns
    ):
        transformed["other_elementary_rating_bin"] = (
            transformed["other_school_district_elementary_avg_rating"]
            .round()
            .clip(lower=1, upper=10)
            .fillna(1)
            .astype(int)
        )
    if (
        "other_school_district_secondary_avg_rating" in binning_list
        and "other_school_district_secondary_avg_rating" in transformed.columns
    ):
        transformed["other_secondary_rating_bin"] = (
            transformed["other_school_district_secondary_avg_rating"]
            .round()
            .clip(lower=1, upper=10)
            .fillna(1)
            .astype(int)
        )
    return transformed


train_data = apply_binning(train_data, cols_binning)
val_data = apply_binning(val_data, cols_binning)
test_data = apply_binning(test_data, cols_binning)

bin_column_candidates = [
    "char_beds_bin",
    "char_rooms_bin",
    "prox_num_school_bin",
    "prox_avg_school_rating_bin",
    "other_elementary_rating_bin",
    "other_secondary_rating_bin",
]
bin_column_names = [
    column for column in bin_column_candidates if column in train_data.columns
]


def one_hot_binned_from_training(
    training_frame,
    validation_frame,
    test_frame,
    column,
):
    training_categories = sorted(
        training_frame[column].dropna().unique().tolist()
    )

    def encode(frame):
        categorical = pd.Categorical(
            frame[column],
            categories=training_categories,
        )
        encoded = pd.get_dummies(
            categorical,
            prefix=column,
            drop_first=True,
            dtype=int,
        )
        encoded.index = frame.index
        return encoded

    encoded_training = encode(training_frame)
    encoded_validation = encode(validation_frame).reindex(
        columns=encoded_training.columns,
        fill_value=0,
    )
    encoded_test = encode(test_frame).reindex(
        columns=encoded_training.columns,
        fill_value=0,
    )
    return (
        pd.concat(
            [training_frame.drop(columns=column), encoded_training],
            axis=1,
        ),
        pd.concat(
            [validation_frame.drop(columns=column), encoded_validation],
            axis=1,
        ),
        pd.concat(
            [test_frame.drop(columns=column), encoded_test],
            axis=1,
        ),
    )


for bin_column in bin_column_names:
    train_data, val_data, test_data = one_hot_binned_from_training(
        train_data,
        val_data,
        test_data,
        bin_column,
    )

# Remove the original variables that the established binning rules replace.
original_binning_columns = [
    column for column in cols_binning if column in train_data.columns
]
for frame in (train_data, val_data, test_data):
    frame.drop(
        columns=original_binning_columns,
        inplace=True,
        errors="ignore",
    )

assert train_data.columns.tolist() == val_data.columns.tolist() == test_data.columns.tolist()
print(f"Training-fitted binned indicators: {len(bin_column_names)} source bins.")
print(
    f"Shapes after binning: Train={train_data.shape}, "
    f"Validation={val_data.shape}, Test={test_data.shape}"
)
'''

cell_124_source = '''### Safe chronological feature snapshot export

The transaction membership remains fixed from the original identifiers and dates. The export cell writes regenerated snapshots to a candidate directory, validates membership order, targets, schema, numeric information retention and CSV round-trip fidelity, then atomically replaces the official files. The pre-repair files and manifest are retained in `data/split/backup_before_export_fix_20261026/`. All learned preprocessing parameters and category mappings are fitted on the training split only.
'''

cell_125_source = '''from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import shutil

split_dir = Path("data") / "split"
candidate_dir = split_dir / "candidate_export"
backup_dir = split_dir / "backup_before_export_fix_20261026"
split_dir.mkdir(parents=True, exist_ok=True)
candidate_dir.mkdir(parents=True, exist_ok=True)
backup_dir.mkdir(parents=True, exist_ok=True)
expected_rows = {"train": 54853, "validation": 18132, "test": 36322}


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


raw_sales = pd.read_csv(
    Path("data") / "sales.csv",
    usecols=["transaction_id", "property_id", "sale_date", "sale_price"],
    dtype={"transaction_id": "string", "property_id": "string"},
)
raw_sales["transaction_id"] = raw_sales["transaction_id"].str.strip()
raw_sales["property_id"] = raw_sales["property_id"].str.strip()
raw_sales["sale_date"] = pd.to_datetime(raw_sales["sale_date"], errors="raise")

raw_split_masks = {
    "train": raw_sales["sale_date"].between("2023-01-01", "2024-06-30"),
    "validation": raw_sales["sale_date"].between("2024-07-01", "2024-12-31"),
    "test": raw_sales["sale_date"].between("2025-01-01", "2025-12-31"),
}
raw_splits = {
    name: raw_sales.loc[mask].reset_index(drop=True)
    for name, mask in raw_split_masks.items()
}
current_frames = {
    "train": train_data.reset_index(drop=True),
    "validation": val_data.reset_index(drop=True),
    "test": test_data.reset_index(drop=True),
}

# Verify and preserve the identifier-based membership records.
membership_details = {}
for name, raw_split in raw_splits.items():
    assert len(raw_split) == expected_rows[name], f"Unexpected {name} row count."
    identity = raw_split[["transaction_id", "property_id", "sale_date"]].copy()
    identity["sale_date"] = identity["sale_date"].dt.strftime("%Y-%m-%d")
    identity_path = split_dir / f"{name}_membership.csv"
    if identity_path.exists():
        saved_identity = pd.read_csv(
            identity_path,
            dtype={"transaction_id": "string", "property_id": "string"},
        )
        pd.testing.assert_frame_equal(saved_identity, identity, check_dtype=False)
    else:
        identity.to_csv(identity_path, index=False)
    membership_details[name] = {
        "file": identity_path.name,
        "rows": len(identity),
        "sha256": sha256_file(identity_path),
    }

# Confirm target order before creating any candidate file. The 2025 target is
# checked for export alignment only and is not used to fit preprocessing.
for name, current_frame in current_frames.items():
    assert len(current_frame) == expected_rows[name]
    assert not {"property_id", "transaction_id", "sale_price"}.intersection(
        current_frame.columns
    )
    expected_log_target = np.log1p(
        raw_splits[name]["sale_price"].to_numpy(dtype=float)
    )
    np.testing.assert_allclose(
        current_frame["log_sale_price"].to_numpy(dtype=float),
        expected_log_target,
        rtol=1e-12,
        atol=1e-12,
    )

assert (
    current_frames["train"].columns.tolist()
    == current_frames["validation"].columns.tolist()
    == current_frames["test"].columns.tolist()
)

# Detect unexplained information loss across every surviving raw numeric feature.
raw_properties = pd.read_csv(
    Path("data") / "properties_2022.csv",
    dtype={"property_id": "string"},
    low_memory=False,
)
raw_properties["property_id"] = raw_properties["property_id"].str.strip()
variable_dictionary = pd.read_csv(Path("data") / "variable_dictionary.csv")
numeric_source_features = variable_dictionary.loc[
    variable_dictionary["type"].eq("numeric"),
    "variable",
].tolist()
raw_training_features = raw_splits["train"][["property_id"]].merge(
    raw_properties,
    on="property_id",
    how="left",
    validate="many_to_one",
    sort=False,
)
surviving_numeric_features = [
    column
    for column in numeric_source_features
    if column in current_frames["train"].columns
    and pd.api.types.is_numeric_dtype(current_frames["train"][column])
]
unexpected_constant_features = []
for column in surviving_numeric_features:
    raw_values = pd.to_numeric(raw_training_features[column], errors="coerce")
    exported_values = pd.to_numeric(
        current_frames["train"][column],
        errors="coerce",
    )
    if (
        raw_values.nunique(dropna=True) > 1
        and exported_values.nunique(dropna=True) <= 1
    ):
        unexpected_constant_features.append(column)
assert not unexpected_constant_features, (
    "Unexpected information loss in numeric features: "
    f"{unexpected_constant_features}"
)

candidate_snapshots = {}
candidate_hashes = {}
for name, current_frame in current_frames.items():
    snapshot = current_frame.copy()
    snapshot.insert(0, "sale_price", raw_splits[name]["sale_price"].to_numpy())
    candidate_path = candidate_dir / f"{name}.csv"
    snapshot.to_csv(candidate_path, index=False, float_format="%.17g")
    saved_candidate = pd.read_csv(candidate_path)
    pd.testing.assert_frame_equal(
        saved_candidate,
        snapshot,
        check_dtype=False,
        check_exact=False,
        rtol=1e-12,
        atol=1e-12,
    )
    candidate_snapshots[name] = snapshot
    candidate_hashes[name] = sha256_file(candidate_path)

# A second independent serialization must produce the same bytes.
for name, snapshot in candidate_snapshots.items():
    repeat_path = candidate_dir / f"{name}.repeat.csv"
    snapshot.to_csv(repeat_path, index=False, float_format="%.17g")
    assert sha256_file(repeat_path) == candidate_hashes[name]
    repeat_path.unlink()

# Preserve the pre-fix official files once, then atomically publish validated candidates.
manifest_path = split_dir / "manifest.json"
for source_path in [
    split_dir / "train.csv",
    split_dir / "validation.csv",
    split_dir / "test.csv",
    manifest_path,
]:
    if source_path.exists():
        backup_path = backup_dir / source_path.name
        if not backup_path.exists():
            shutil.copy2(source_path, backup_path)

for name in current_frames:
    official_path = split_dir / f"{name}.csv"
    temporary_path = split_dir / f".{name}.csv.tmp"
    shutil.copy2(candidate_dir / f"{name}.csv", temporary_path)
    os.replace(temporary_path, official_path)

# Re-read the official files after replacement.
snapshot_details = {}
for name, expected_snapshot in candidate_snapshots.items():
    official_path = split_dir / f"{name}.csv"
    saved_snapshot = pd.read_csv(official_path)
    pd.testing.assert_frame_equal(
        saved_snapshot,
        expected_snapshot,
        check_dtype=False,
        check_exact=False,
        rtol=1e-12,
        atol=1e-12,
    )
    snapshot_details[name] = {
        "file": official_path.name,
        "rows": len(saved_snapshot),
        "columns": len(saved_snapshot.columns),
        "sha256": sha256_file(official_path),
    }

notebook_content = json.loads(
    Path("assignment_6810.ipynb").read_text(encoding="utf-8")
)
split_cell_index = next(
    index
    for index, cell in enumerate(notebook_content["cells"])
    if "candidate_export" in "".join(cell.get("source", []))
)
pipeline_sources = [
    {"cell_type": cell["cell_type"], "source": cell.get("source", [])}
    for cell in notebook_content["cells"][: split_cell_index + 1]
]
pipeline_digest = hashlib.sha256(
    json.dumps(
        pipeline_sources,
        sort_keys=True,
        ensure_ascii=False,
    ).encode("utf-8")
).hexdigest()

source_files = [
    "data/properties_2022.csv",
    "data/sales.csv",
    "data/variable_dictionary.csv",
    "data/featureengineer.csv",
]
previous_manifest = (
    json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest_path.exists()
    else {}
)
manifest = {
    "created_utc": previous_manifest.get(
        "created_utc",
        datetime.now(timezone.utc).isoformat(),
    ),
    "last_verified_utc": datetime.now(timezone.utc).isoformat(),
    "format": "csv",
    "source_notebook": "assignment_6810.ipynb",
    "pipeline_code_sha256": pipeline_digest,
    "input_sha256": {path: sha256_file(path) for path in source_files},
    "target": "sale_price",
    "derived_target": "log_sale_price",
    "preprocessing_fit_scope": "training split only",
    "numeric_information_loss_check": {
        "surviving_raw_numeric_features_checked": len(
            surviving_numeric_features
        ),
        "unexpected_constant_features": unexpected_constant_features,
    },
    "time_split": {
        "train": "2023-01-01 through 2024-06-30",
        "validation": "2024-07-01 through 2024-12-31",
        "test": "2025-01-01 through 2025-12-31",
    },
    "membership": membership_details,
    "splits": snapshot_details,
    "backup_directory": backup_dir.name,
    "candidate_directory": candidate_dir.name,
}
manifest_path.write_text(
    json.dumps(manifest, indent=2) + "\n",
    encoding="utf-8",
)

print("Candidate snapshots passed all checks and replaced the official files.")
print("Preprocessing parameters and category schemas were fitted on training data only.")
print(f"Unexpected constant numeric features: {unexpected_constant_features}")
for name, details in snapshot_details.items():
    print(
        f"{name}: {details['rows']:,} rows x {details['columns']:,} columns; "
        f"sha256={details['sha256']}"
    )
'''

for cell_index, source in {
    97: cell_97_source,
    98: cell_98_source,
    124: cell_124_source,
    125: cell_125_source,
}.items():
    notebook["cells"][cell_index]["source"] = source.splitlines(keepends=True)
    if notebook["cells"][cell_index]["cell_type"] == "code":
        notebook["cells"][cell_index]["outputs"] = []
        notebook["cells"][cell_index]["execution_count"] = None

cell_110_source = "".join(notebook["cells"][110]["source"])
old_block = '''        category_stats = fit_part.groupby(column)[target].agg(["mean", "count"])
        smoothed_map = (
            category_stats["count"] * category_stats["mean"]
            + smoothing * training_global_mean
        ) / (category_stats["count"] + smoothing)
        training_encoded[heldout_positions] = (
            heldout_part[column].map(smoothed_map).fillna(training_global_mean)
        )
'''
new_block = '''        fit_global_mean = fit_part[target].mean()
        category_stats = fit_part.groupby(column)[target].agg(["mean", "count"])
        smoothed_map = (
            category_stats["count"] * category_stats["mean"]
            + smoothing * fit_global_mean
        ) / (category_stats["count"] + smoothing)
        training_encoded[heldout_positions] = (
            heldout_part[column].map(smoothed_map).fillna(fit_global_mean)
        )
'''
if old_block not in cell_110_source:
    raise RuntimeError("The expected target-encoding block was not found in Cell 110.")
cell_110_source = cell_110_source.replace(old_block, new_block, 1)
notebook["cells"][110]["source"] = cell_110_source.splitlines(keepends=True)
notebook["cells"][110]["outputs"] = []
notebook["cells"][110]["execution_count"] = None

model_digest_after = source_digest(notebook["cells"][132:152])
if model_digest_before != model_digest_after:
    raise RuntimeError("Cells 132-151 changed during the export-only patch.")

temporary_path = notebook_path.with_suffix(".ipynb.tmp")
with temporary_path.open("w", encoding="utf-8", newline="\n") as handle:
    json.dump(notebook, handle, ensure_ascii=False, indent=1)
    handle.write("\n")
os.replace(temporary_path, notebook_path)

print("Patched Cells 97, 98, 110, 124 and 125.")
print(f"Cells 132-151 source digest unchanged: {model_digest_after}")
