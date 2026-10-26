import io
import hashlib
import json
import os
from contextlib import redirect_stdout
from pathlib import Path

import numpy as np
import pandas as pd


project_dir = Path(__file__).resolve().parent
os.chdir(project_dir)

with (project_dir / "assignment_6810.ipynb").open("r", encoding="utf-8") as handle:
    notebook = json.load(handle)

namespace = {"__name__": "__main__"}
captured_outputs = {}


def source_digest(cells):
    payload = [cell.get("source", []) for cell in cells]
    return hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()


model_digest_before = source_digest(notebook["cells"][132:152])


def run_cell(cell_index):
    source = "".join(notebook["cells"][cell_index]["source"])
    output = io.StringIO()
    with redirect_stdout(output):
        exec(compile(source, f"assignment_6810.ipynb:cell_{cell_index}", "exec"), namespace)
    captured_outputs[cell_index] = captured_outputs.get(cell_index, "") + output.getvalue()


audit_columns = [
    "char_bldg_sf",
    "char_land_sf",
    "loc_longitude",
    "acs5_median_income_per_capita_past_year",
    "acs5_median_household_renter_occupied_gross_rent",
    "acs5_median_household_owner_occupied_value",
]


def describe_columns(frame, stage):
    rows = []
    for column in audit_columns:
        values = pd.to_numeric(frame[column], errors="coerce")
        rows.append(
            {
                "stage": stage,
                "column": column,
                "dtype": str(frame[column].dtype),
                "missing": int(values.isna().sum()),
                "minimum": float(values.min()),
                "maximum": float(values.max()),
                "std": float(values.std()),
                "nunique": int(values.nunique(dropna=True)),
            }
        )
    return rows


stage_rows = []
raw_properties = pd.read_csv(
    project_dir / "data" / "properties_2022.csv",
    usecols=["property_id", *audit_columns],
    dtype={"property_id": "string"},
    low_memory=False,
)
stage_rows.extend(describe_columns(raw_properties, "raw_properties"))

for cell_index in (2, 4, 11, 15, 19, 23, 24, 25, 28, 30, 32, 35, 37):
    run_cell(cell_index)
stage_rows.extend(describe_columns(namespace["property_list"], "merged_transactions"))

for cell_index in (39, 41):
    run_cell(cell_index)
for frame_name in ("train_data", "val_data", "test_data"):
    frame = namespace[frame_name]
    frame["log_sale_price"] = np.log1p(frame["sale_price"])

for cell_index in (49, 51, 53, 54, 56, 57, 58, 60, 67, 68):
    run_cell(cell_index)
namespace["datasets"] = {
    "Train": namespace["train_data"],
    "Val": namespace["val_data"],
    "Test": namespace["test_data"],
}
for cell_index in (75, 76, 82, 87):
    run_cell(cell_index)

pre_transform_train = namespace["train_data"].copy()
stage_rows.extend(describe_columns(pre_transform_train, "pre_continuous_transform_train"))
run_cell(97)
post_transform_train = namespace["train_data"].copy()
stage_rows.extend(describe_columns(post_transform_train, "post_continuous_transform_train"))

for cell_index in (98, 103, 110):
    run_cell(cell_index)
stage_rows.extend(describe_columns(namespace["train_data"], "post_encoding_train"))

for cell_index in (112, 114, 116, 117, 119, 121, 123):
    run_cell(cell_index)

final_frames = {
    "train": namespace["train_data"],
    "validation": namespace["val_data"],
    "test": namespace["test_data"],
}
for name, frame in final_frames.items():
    stage_rows.extend(describe_columns(frame, f"export_frame_{name}"))

run_cell(125)

for name, frame in final_frames.items():
    saved = pd.read_csv(
        project_dir / "data" / "split" / f"{name}.csv",
        usecols=audit_columns,
    )
    stage_rows.extend(describe_columns(saved, f"saved_csv_{name}"))

raw_train = namespace["sales_property"].loc[
    namespace["sales_property"]["sale_year"].eq(2023)
    | (
        namespace["sales_property"]["sale_year"].eq(2024)
        & namespace["sales_property"]["sale_month"].le(6)
    )
].copy()
final_train = final_frames["train"]
shared_numeric = [
    column
    for column in final_train.select_dtypes(include=[np.number]).columns
    if column in raw_train.columns
]
unexpected_constant_columns = []
for column in shared_numeric:
    raw_values = pd.to_numeric(raw_train[column], errors="coerce")
    final_values = pd.to_numeric(final_train[column], errors="coerce")
    if raw_values.nunique(dropna=True) > 1 and final_values.nunique(dropna=True) <= 1:
        unexpected_constant_columns.append(
            {
                "column": column,
                "raw_nunique": int(raw_values.nunique(dropna=True)),
                "final_nunique": int(final_values.nunique(dropna=True)),
                "final_value": (
                    None if final_values.dropna().empty else float(final_values.dropna().iloc[0])
                ),
            }
        )

report = {
    "stage_statistics": stage_rows,
    "unexpected_constant_columns_in_regenerated_train": unexpected_constant_columns,
    "final_shapes": {name: list(frame.shape) for name, frame in final_frames.items()},
    "final_columns": final_frames["train"].columns.tolist(),
}

backup_dir = project_dir / "data" / "split" / "backup_before_export_fix_20261026"
for name in ("train", "validation", "test"):
    before = pd.read_csv(backup_dir / f"{name}.csv", usecols=["sale_price"])
    after = pd.read_csv(
        project_dir / "data" / "split" / f"{name}.csv",
        usecols=["sale_price"],
    )
    report.setdefault("target_order_matches_backup", {})[name] = bool(
        np.array_equal(
            before["sale_price"].to_numpy(dtype=float),
            after["sale_price"].to_numpy(dtype=float),
        )
    )

execution_number = max(
    [
        cell.get("execution_count") or 0
        for cell in notebook["cells"]
        if cell.get("cell_type") == "code"
    ]
) + 1
for cell_index in (97, 98, 110, 125):
    cell = notebook["cells"][cell_index]
    text = captured_outputs.get(cell_index, "")
    cell["execution_count"] = execution_number
    cell["outputs"] = (
        [
            {
                "name": "stdout",
                "output_type": "stream",
                "text": text.splitlines(keepends=True),
            }
        ]
        if text
        else []
    )
    execution_number += 1

model_digest_after = source_digest(notebook["cells"][132:152])
if model_digest_before != model_digest_after:
    raise RuntimeError("Cells 132-151 changed during export execution.")

notebook_path = project_dir / "assignment_6810.ipynb"
temporary_notebook_path = notebook_path.with_suffix(".ipynb.tmp")
with temporary_notebook_path.open("w", encoding="utf-8", newline="\n") as handle:
    json.dump(notebook, handle, ensure_ascii=False, indent=1)
    handle.write("\n")
os.replace(temporary_notebook_path, notebook_path)

report_path = project_dir / ".codex_export_audit.json"
report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(f"Audit report written to {report_path.name}")
print(f"Unexpected regenerated constant columns: {unexpected_constant_columns}")
print(f"Final shapes: {report['final_shapes']}")
