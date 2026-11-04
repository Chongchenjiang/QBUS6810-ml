"""Apply source-checked, local corrections to the final QBUS6810 report."""

import copy
import hashlib
import json
from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from docx.table import Table
from docx.text.paragraph import Paragraph


PATH = Path("doc/QBUS6810_Final_Report.docx")
STAGED = PATH.with_name(".QBUS6810_Final_Report.codex_stage.docx")
doc = Document(str(PATH))
body = list(doc.element.body.iterchildren())


def paragraph(index):
    assert body[index].tag == qn("w:p"), index
    return Paragraph(body[index], doc)


def table(index):
    assert body[index].tag == qn("w:tbl"), index
    return Table(body[index], doc)


def set_text_in_first_run(p, value):
    assert p.runs, "Expected formatted paragraph with a text run"
    p.runs[0].text = value
    for run in p.runs[1:]:
        run.text = ""


def replace_paragraph(index, old, new):
    p = paragraph(index)
    assert p.text.count(old) == 1, (index, old)
    set_text_in_first_run(p, p.text.replace(old, new))


def set_cell(cell, expected, new):
    assert cell.text == expected, (cell.text, expected)
    p = cell.paragraphs[0]
    set_text_in_first_run(p, new)


def shade(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_borders(cell):
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.find(qn("w:tcBorders"))
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for side in ("top", "left", "bottom", "right"):
        edge = borders.find(qn("w:" + side))
        if edge is None:
            edge = OxmlElement("w:" + side)
            borders.append(edge)
        edge.set(qn("w:val"), "single")
        edge.set(qn("w:sz"), "4")
        edge.set(qn("w:color"), "D9D9D9")


# 2b: describe the transformation rule file and actual retained indicators.
p = paragraph(17)
assert "Redundant boolean missing indicators were removed" in p.text
set_text_in_first_run(
    p,
    "To handle unusual values, continuous features were clipped at training-set "
    "1st and 99th percentiles; selected skewed variables such as char_land_sf "
    "then underwent Yeo-Johnson transformation and training-fitted standardisation. "
    "The column lists for clipping, transformation, scaling and binning came from "
    "data/featureengineer.csv. Fields with at least 30 training categories used "
    "five-fold out-of-fold target encoding of log_sale_price (shuffle seed 42; "
    "smoothing weight 50). Each held-out fold was encoded from its fitting rows; "
    "validation and test mappings came from the full training split. For lower-cardinality "
    "fields, rare categories were grouped using training frequencies before one-hot "
    "encoding with training-defined columns. Missing-value indicators were retained. "
    "Their training-period target associations were inspected descriptively, and a "
    "fixed-model validation ablation assessed whether the numeric indicators helped. "
    "All learned fill values, clipping bounds, transformations and category schemas "
    "came from training data.",
)

# 2c: align the prose with the plotted year-by-month points and the pooled summaries.
set_text_in_first_run(
    paragraph(21),
    "Training-only sale prices show higher medians in the first half of 2024 than "
    "in the same calendar months of 2023, alongside within-year monthly variation. "
    "The full-year 2023 median was $315,000, compared with $340,000 in January-June "
    "2024; the resulting 7.94% difference compares unequal windows. A like-for-like "
    "January-June comparison is $313,000 in 2023 versus $340,000 in 2024 (+8.63%). "
    "Changes in the characteristics and locations of homes sold may contribute to "
    "both differences, so these summaries do not isolate market appreciation.",
)
set_text_in_first_run(
    paragraph(23),
    "The training-only plot peaks in June in both observed years: the monthly median "
    "was $340,000 in June 2023 and $372,000 in June 2024. Pooling the two Junes "
    "gives $355,000, a different statistic from either plotted point. Pooled January "
    "and February medians were $285,000 and $299,000; the single observed "
    "October-December period (2023) had medians of $307,000, $315,000 and $300,000. "
    "Seasonal demand, school schedules and weather are possible explanations, but "
    "transaction volume and the mix of homes sold may also contribute. The raw mean "
    "is more sensitive than the median to high-priced sales, while the log-scale "
    "plot compresses the long right tail. These descriptive summaries do not "
    "establish a causal seasonal premium.",
)

# 3e: two pre-enqueued references count within the 24 Optuna trials.
for row_index in range(4, 8):
    cell = table(119).rows[row_index].cells[1]
    if "24 TPE trials" in cell.text:
        set_cell(cell, cell.text, cell.text.replace("24 TPE trials", "24 Optuna trials (2 fixed)"))
    else:
        raise AssertionError("Expected 24-trial text in Table 3.5 row " + str(row_index))
replace_paragraph(
    130,
    "Each of the four implementations received 24 Optuna TPE trials with seed 6810, "
    "including fixed raw-price and log1p-price reference trials.",
    "Each of the four implementations received 24 Optuna trials with seed 6810: "
    "two pre-enqueued raw-price and log1p-price reference configurations and "
    "22 further sampler-generated configurations (TPESampler with eight startup "
    "trials).",
)
replace_paragraph(
    130,
    "All candidates used squared-error fitting objectives on their chosen target scale;",
    "Additional retained hyperparameters are listed in Table B5. All candidates "
    "used squared-error fitting objectives on their chosen target scale;",
)
replace_paragraph(
    132,
    "CatBoost K002 combined depth 6, learning rate 0.05, L2 leaf penalty 1, "
    "90% row and feature sampling, and 1,376 trees.",
    "CatBoost K002 combined Bernoulli bootstrap, depth 6, learning rate 0.05, "
    "L2 leaf penalty 1, 90% row and feature sampling, and 1,376 trees.",
)

# 4c: the best tested Ridge configuration differs slightly from retained D.
set_cell(table(166).rows[3].cells[1], "D α12; $153,109.49", "F1 α12; $153,089.21")
replace_paragraph(
    167,
    "CatBoost K002 wins 2:1 at $126,068.74;",
    "For Ridge, the lowest tested 2:1 WAE came from F1 (α=12; $153,089.21); "
    "Tables 3.2 and 3.6 retain the simpler D (α=12; $153,109.49), only $20.28 "
    "higher. CatBoost K002 wins 2:1 at $126,068.74;",
)

# Sources: name the custom rule list explicitly.
replace_paragraph(
    203,
    "The modelling extension was informed by the course Gradient Boosting practical.",
    "The preprocessing feature rules are recorded in data/featureengineer.csv. "
    "The modelling extension was informed by the course Gradient Boosting practical.",
)

# Appendix B: full retained settings complement the compact main-text table.
p = paragraph(236)
assert not p.text
p.add_run("Table B5. Additional hyperparameters of retained boosting configurations")
p.paragraph_format.keep_with_next = True

extra = doc.add_table(rows=5, cols=2)
extra.style = table(119).style
extra.autofit = False
for row in extra.rows:
    row.cells[0].width = Inches(1.45)
    row.cells[1].width = Inches(5.95)

settings = [
    (
        "Model",
        "Additional retained settings; depth, learning rate and tree count are in Table 3.5",
    ),
    (
        "LightGBM C022",
        "min_child_samples=47; subsample=0.9262; subsample_freq=1; "
        "colsample_bytree=0.8642; reg_alpha=0.0000190; reg_lambda=77.3516",
    ),
    (
        "XGBoost X021",
        "min_child_weight=82; subsample=0.9865; colsample_bytree=0.6701; "
        "reg_alpha=0.000260; reg_lambda=1.5225; tree_method=hist",
    ),
    (
        "HistBoost H023",
        "min_samples_leaf=45; max_features=0.7294; l2_regularization=37.7788; "
        "final refit uses early_stopping=False",
    ),
    (
        "CatBoost K002",
        "bootstrap_type=Bernoulli; subsample=0.9; rsm=0.9; l2_leaf_reg=1",
    ),
]
for row_index, (name, details) in enumerate(settings):
    for column_index, text in enumerate((name, details)):
        cell = extra.rows[row_index].cells[column_index]
        cell.text = text
        set_borders(cell)
        if row_index == 0:
            shade(cell, "E7E6E6")
        for par in cell.paragraphs:
            par.paragraph_format.space_after = Pt(2)
            for run in par.runs:
                run.font.size = Pt(9)
                if row_index == 0:
                    run.bold = True
    extra.rows[row_index].cells[0].vertical_alignment = 1
    extra.rows[row_index].cells[1].vertical_alignment = 1

body[236].addnext(extra._tbl)
note = paragraph(237)
assert not note.text
note.add_run(
    "Note: all four boosting families used seed 6810 and two threads. Each search "
    "allowed up to 1,400 rounds, with the best dollar-WAE 2:1 round selected under "
    "100-round patience. Full-precision settings are in M4_boosting_candidates.csv."
)

# The user's DOCX is the deliverable; stage it first so failures cannot truncate it.
doc.save(str(STAGED))
staged_doc = Document(str(STAGED))
assert len(staged_doc.inline_shapes) == 12
assert len(staged_doc.tables) == 16
assert "F1 α12; $153,089.21" in staged_doc.tables[9].rows[3].cells[1].text
STAGED.replace(PATH)
print("Updated", PATH, "SHA-256", hashlib.sha256(PATH.read_bytes()).hexdigest())
