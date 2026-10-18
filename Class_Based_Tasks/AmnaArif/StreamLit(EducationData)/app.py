
import io
from pathlib import Path

import joblib
import matplotlib
import numpy as np
import pandas as pd
import streamlit as st
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, PercentFormatter
from sklearn.inspection import permutation_importance
from sklearn.metrics import (
    average_precision_score,
    precision_recall_curve,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split

st.set_page_config(
    page_title="Out-of-School Risk Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# 1. DESIGN TOKENS  (maroon + off-white)
# =============================================================================
PAGE_BG = "#FAF6F0"      # off-white page
CARD_BG = "#FFFDFA"
BORDER = "#E3D6C8"
MAROON = "#7A1F2E"       # brand maroon (UI)
MAROON_DARK = "#4A0F1A"
MAROON_TRACK = "#EBD3D6"

INK = "#2B1A1D"          # primary text
INK_2 = "#5C4A4D"        # secondary text
MUTED = "#7A6B6D"        # axis labels (4.7:1 on the page)
GRID = "#E8DED3"         # hairline grid
BASELINE = "#CDBFB1"     # axis line

# Chart colours - validated for colour-blind separation and contrast on PAGE_BG.
C_OUT = "#9B2C3F"        # maroon : out of school / selected model / raises risk
C_IN = "#00809A"         # teal   : in school / lowers risk
C_3 = "#A86C00"          # ochre  : third series
MODEL_COLORS = {"Logistic Regression": C_OUT, "Random Forest": C_IN, "Gradient Boosting": C_3}
ORD5 = ["#e897a0", "#d7697a", "#b7445a", "#8a3041", "#58252d"]            # ordered maroon ramps
ORD6 = ["#e897a0", "#dc7281", "#c65166", "#a63a4f", "#812d3d", "#58252d"]
SEQ_CMAP = LinearSegmentedColormap.from_list(
    "maroon_seq", ["#FBEFEF", "#E8A5AD", "#C65166", "#8F3144", "#58252D"])
STATUS = {"good": "#0ca30c", "warning": "#fab219", "critical": "#d03b3b"}

matplotlib.rcParams.update({
    "font.size": 9.5,
    "axes.facecolor": "none",
    "axes.edgecolor": BASELINE,
    "axes.labelcolor": INK_2,
    "axes.titlecolor": INK,
    "text.color": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "legend.frameon": False,
    "legend.labelcolor": INK,
})

st.markdown(
    """
<style>
.stApp { background: #FAF6F0; }
.block-container { padding-top: 1.3rem; padding-bottom: 3rem; max-width: 1280px; }
section[data-testid="stSidebar"] { background: #F1E7DC; border-right: 1px solid #E3D6C8; }
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
h1, h2, h3, h4 { color: #4A0F1A; }

.hero { background: linear-gradient(135deg, #7A1F2E 0%, #571320 100%); border-radius: 16px;
        padding: 26px 32px 22px 32px; margin-bottom: 18px; }
.hero-eyebrow { color: #E9C9CD; font-size: .74rem; letter-spacing: .14em; text-transform: uppercase; font-weight: 600; }
.hero-title { color: #FAF6F0; font-size: 2.1rem; font-weight: 700; line-height: 1.15; margin-top: 6px; }
.hero-sub { color: #F0DEDB; font-size: .98rem; margin-top: 8px; max-width: 760px; }
.hero-chips { margin-top: 14px; }
.hero-chips span { display: inline-block; background: rgba(250,246,240,.14); color: #FAF6F0; border-radius: 999px;
                   padding: 4px 12px; font-size: .78rem; margin-right: 8px; }

.kpi { background: #FFFDFA; border: 1px solid #E8DED3; border-top: 3px solid #7A1F2E; border-radius: 12px;
       padding: 13px 16px 12px 16px; min-height: 112px; }
.kpi-label { font-size: .72rem; letter-spacing: .07em; text-transform: uppercase; color: #7A6B6D; font-weight: 600; }
.kpi-value { font-size: 2rem; font-weight: 700; color: #4A0F1A; line-height: 1.15; margin-top: 5px; }
.kpi-value.text { font-size: 1.22rem; line-height: 1.25; margin-top: 9px; }
.kpi-sub { font-size: .78rem; color: #5C4A4D; margin-top: 5px; line-height: 1.3; }
.kpi.small { min-height: 92px; }
.kpi.small .kpi-value { font-size: 1.6rem; }

.section-title { font-size: 1.15rem; font-weight: 700; color: #4A0F1A; margin: 22px 0 2px 0; }
.section-sub { font-size: .9rem; color: #5C4A4D; margin-bottom: 8px; }
.callout { background: #F6ECE6; border-left: 4px solid #7A1F2E; border-radius: 8px; padding: 12px 16px;
           color: #2B1A1D; font-size: .92rem; line-height: 1.5; margin: 6px 0 10px 0; }
.callout b { color: #4A0F1A; }

.meter { background: #EBD3D6; border-radius: 999px; height: 14px; position: relative; margin: 10px 0 4px 0; }
.meter-fill { background: #9B2C3F; border-radius: 999px; height: 14px; }
.meter-tick { position: absolute; top: -4px; width: 2px; height: 22px; background: #2B1A1D; }
.badge { display: inline-block; border-radius: 999px; padding: 5px 14px; font-weight: 600; font-size: .92rem;
         background: #FFFDFA; border: 1px solid #E3D6C8; color: #2B1A1D; }
.badge .dot { display: inline-block; width: 11px; height: 11px; border-radius: 50%; margin-right: 8px; vertical-align: -1px; }

.stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid #E3D6C8; }
.stTabs [data-baseweb="tab"] { height: 44px; padding: 0 16px; color: #5C4A4D; font-weight: 600; }
.stTabs [aria-selected="true"] { color: #7A1F2E; }
.stTabs [data-baseweb="tab-highlight"] { background-color: #7A1F2E; }

div.stButton > button, div.stDownloadButton > button, div[data-testid="stFormSubmitButton"] > button {
    background: #7A1F2E; color: #FAF6F0; border: none; border-radius: 8px; font-weight: 600; padding: .5rem 1.2rem; }
div.stButton > button:hover, div.stDownloadButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {
    background: #571320; color: #FAF6F0; }
span[data-baseweb="tag"] { background-color: #7A1F2E; color: #FAF6F0; }
div[data-testid="stExpander"] { border: 1px solid #E3D6C8; border-radius: 10px; background: #FFFDFA; }
</style>
""",
    unsafe_allow_html=True,
)

# =============================================================================
# 2. LOAD MODEL + DATA
# =============================================================================
APP_DIR = Path(__file__).resolve().parent
MODEL_PATH = APP_DIR / "out_of_school_model.joblib"
META_PATH = APP_DIR / "model_metadata.joblib"
DATA_PATH = APP_DIR / "out_of_school_clean.csv"
TARGET = "out_of_school"

missing_files = [p.name for p in (MODEL_PATH, META_PATH, DATA_PATH) if not p.exists()]
if missing_files:
    st.error(
        "These files must be in the same folder as app.py: **" + ", ".join(missing_files) + "**. "
        "Run the notebook through section 15 (\"Save the model\"), then copy them here."
    )
    st.stop()


@st.cache_resource(show_spinner=False)
def load_model():
    return joblib.load(MODEL_PATH), joblib.load(META_PATH)


@st.cache_data(show_spinner=False)
def load_data():
    # keep_default_na=False: the text "None" is a real education level, not a missing value.
    return pd.read_csv(DATA_PATH, keep_default_na=False, na_values=[""])


@st.cache_data(show_spinner=False)
def split_data(df):
    """Recreate the notebook's train/test split (same seed, same stratification)."""
    X = df.drop(columns=[TARGET])
    y = df[TARGET]
    return train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)


@st.cache_data(show_spinner=False)
def predict_test(_model, X_test):
    return _model.predict_proba(X_test)[:, 1]


@st.cache_data(show_spinner=False)
def train_feature_means(_model, X_train):
    return transform_dense(_model, X_train).mean(axis=0)


@st.cache_data(show_spinner=False)
def perm_importance(_model, X_test, y_test):
    result = permutation_importance(
        _model, X_test, y_test, n_repeats=8, random_state=42, scoring="roc_auc", n_jobs=1)
    return pd.Series(result.importances_mean, index=X_test.columns).sort_values(ascending=False)


def transform_dense(model, X):
    out = model.steps[0][1].transform(X)
    return out.toarray() if hasattr(out, "toarray") else np.asarray(out)


def add_features(data):
    """Same two engineered features as the notebook."""
    data = data.copy()
    data["fee_to_income_ratio"] = data["school_fee"] / data["household_income"]
    data["children_per_member"] = data["number_of_children"] / data["household_size"]
    return data


def coef_table(model, raw_cols):
    """Logistic-regression coefficients mapped back to the original columns (None for other models)."""
    est = model.steps[-1][1]
    if not hasattr(est, "coef_"):
        return None
    names = list(model.steps[0][1].get_feature_names_out())
    coefs = np.ravel(est.coef_)
    rows = []
    for name, coef in zip(names, coefs):
        base = name.split("__", 1)[1] if "__" in name else name
        match = [c for c in raw_cols if base == c or base.startswith(c + "_")]
        col = max(match, key=len) if match else base
        level = base[len(col) + 1:] if base != col else ""
        rows.append({"column": col, "level": level, "coef": float(coef)})
    return pd.DataFrame(rows)


def metrics_at(y, proba, t):
    pred = (proba >= t).astype(int)
    tp = int(((pred == 1) & (y == 1)).sum())
    fp = int(((pred == 1) & (y == 0)).sum())
    fn = int(((pred == 0) & (y == 1)).sum())
    tn = int(((pred == 0) & (y == 0)).sum())
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn, "precision": prec, "recall": rec,
            "f1": f1, "accuracy": (tp + tn) / len(y), "flagged": tp + fp}


NICE_NAMES = {
    "urban_rural": "Urban or rural",
    "fee_to_income_ratio": "Fee-to-income ratio",
    "children_per_member": "Children per member",
    "internet_access": "Internet access",
}
ENGINEERED = ["fee_to_income_ratio", "children_per_member"]


def nice(name):
    return NICE_NAMES.get(name, name.replace("_", " ").capitalize())


try:
    model, meta = load_model()
except Exception as exc:  # most often a scikit-learn version mismatch
    st.error(
        "The saved model could not be loaded. This usually means this computer has a different scikit-learn "
        "version from the one that saved the model. Re-run the notebook through section 15 on this computer "
        "to recreate the model files, then restart the app. Details: " + str(exc)
    )
    st.stop()
df = load_data()
X_train, X_test, y_train, y_test = split_data(df)
y_test_arr = y_test.to_numpy()
proba = predict_test(model, X_test)
m50 = metrics_at(y_test_arr, proba, 0.5)
auc = float(roc_auc_score(y_test_arr, proba))

feature_cols = list(meta.get("feature_columns", X_test.columns))
edu_order = list(meta.get("edu_order", ["None", "Primary", "Middle", "Matric", "Intermediate", "Graduate+"]))
estimator = model.steps[-1][1]
model_name = meta.get("model_name", type(estimator).__name__)
best_params = meta.get("best_params", {})
params_text = ", ".join(f"{k.split('__')[-1]} = {v}" for k, v in best_params.items()) or "default settings"
overall_rate = float(df[TARGET].mean())
n_raw_inputs = len([c for c in feature_cols if c not in ENGINEERED])   # the 16 columns a user fills in

# =============================================================================
# 3. CHART HELPERS  (matplotlib; every chart is cached and returns PNG bytes + its data table)
# =============================================================================
def pct(x, d=0):
    return f"{x * 100:.{d}f}%"


def style(ax, grid="y"):
    ax.set_facecolor("none")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(BASELINE)
        ax.spines[side].set_linewidth(1)
    ax.tick_params(length=0, labelsize=9, pad=6)
    # Passing a colour to grid(False, ...) would switch the grid ON, so only style the axis we want.
    for axis, key in ((ax.yaxis, "y"), (ax.xaxis, "x")):
        if grid == key:
            axis.grid(True, color=GRID, linewidth=0.8)
        else:
            axis.grid(False)
    ax.set_axisbelow(True)


def new_fig(w, h, grid="y"):
    fig = Figure(figsize=(w, h))
    ax = fig.subplots()
    style(ax, grid)
    return fig, ax


def title(ax, text):
    ax.set_title(text, loc="left", fontsize=11, fontweight="bold", color=INK, pad=16)


def to_png(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200, bbox_inches="tight", transparent=True)
    return buf.getvalue()


def empty_chart(message):
    fig, ax = new_fig(6, 2.4)
    ax.axis("off")
    ax.text(0.5, 0.5, message, ha="center", va="center", color=MUTED, transform=ax.transAxes)
    return to_png(fig), pd.DataFrame()


def palette_for(n):
    base = ORD5 if n <= 5 else ORD6
    if n == len(base):
        return list(base)
    idx = np.linspace(0, len(base) - 1, n).round().astype(int)
    return [base[i] for i in idx]


def spread(values, min_gap):
    """Nudge label positions apart so direct labels never overlap."""
    order = np.argsort(values)
    out = np.array(values, dtype=float)
    for a, b in zip(order[:-1], order[1:]):
        if out[b] - out[a] < min_gap:
            out[b] = out[a] + min_gap
    return out


def rate_by(data, col):
    return data.groupby(col, observed=True)[TARGET].agg(rate="mean", n="size")


# ---------- Overview charts ----------
@st.cache_data(show_spinner=False)
def chart_province(data, overall):
    g = rate_by(data, "province").sort_values("rate", ascending=False)
    labels = [f"{p}  (n={n:,})" for p, n in zip(g.index, g["n"])]
    y = np.arange(len(g))
    fig, ax = new_fig(6, 1.1 + 0.42 * len(g), grid="x")
    ax.barh(y, g["rate"], height=0.38, color=C_OUT, zorder=3)
    ax.axvline(overall, color=MUTED, linewidth=1, zorder=2)
    ax.text(overall, -0.8, f"All children {pct(overall)}", ha="center", va="bottom", fontsize=8.5, color=MUTED)
    for yi, v in zip(y, g["rate"]):
        ax.text(v + 0.015, yi, pct(v), va="center", ha="left", fontsize=9, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_ylim(len(g) - 0.45, -1.0)
    ax.set_xlim(0, 1)
    ax.xaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    ax.spines["left"].set_visible(False)
    title(ax, "Out-of-school rate by province")
    table = pd.DataFrame({"Province": g.index, "Children": g["n"].to_numpy(),
                          "Out-of-school rate (%)": (g["rate"] * 100).round(1).to_numpy()})
    return to_png(fig), table


def hist_by_status(data, col, bins, ttl, xlabel, x_fmt, med_fmt):
    fig, ax = new_fig(6, 3.4)
    handles, rows = [], []
    for status, color, name in ((0, C_IN, "In school"), (1, C_OUT, "Out of school")):
        vals = data.loc[data[TARGET] == status, col].dropna()
        if vals.empty:
            continue
        vals = vals.clip(lower=bins[0], upper=bins[-1] - 1e-9)
        counts, edges = np.histogram(vals, bins=bins)
        share = counts / counts.sum()
        ax.stairs(share, edges, color=color, linewidth=2)
        ax.stairs(share, edges, color=color, alpha=0.10, fill=True, linewidth=0)
        handles.append(Line2D([0], [0], color=color, lw=2,
                              label=f"{name} (median {med_fmt(vals.median())})"))
        for lo, s in zip(edges[:-1], share):
            rows.append({"Group": name, xlabel: x_fmt(lo, None), "Share of children (%)": round(s * 100, 1)})
    ax.set_xlim(bins[0], bins[-1])
    ax.set_ylim(bottom=0)
    ax.xaxis.set_major_formatter(FuncFormatter(x_fmt))
    ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    ax.set_xlabel(xlabel)
    if handles:
        ax.legend(handles=handles, loc="upper right", fontsize=9)
    title(ax, ttl)
    return to_png(fig), pd.DataFrame(rows)


@st.cache_data(show_spinner=False)
def chart_distance(data):
    bins = np.arange(0, 25, 1.0)
    return hist_by_status(data, "distance_to_school", bins, "How far children live from school",
                          "Distance to school (km)", lambda v, _: f"{v:.0f}", lambda v: f"{v:.1f} km")


@st.cache_data(show_spinner=False)
def chart_income(data):
    bins = np.arange(10000, 170000, 10000)
    return hist_by_status(data, "household_income", bins, "Household income of children in and out of school",
                          "Household income (PKR per month)", lambda v, _: f"{v / 1000:.0f}k",
                          lambda v: f"{v / 1000:.0f}k")


GAP_GROUPS = [
    ("Location", "urban_rural", [("Rural", "Rural"), ("Urban", "Urban")]),
    ("Gender", "gender", [("Girls", "Female"), ("Boys", "Male")]),
    ("Disability", "disability", [("Has\ndisability", "Yes"), ("No\ndisability", "No")]),
    ("Electricity", "electricity", [("No\nelectricity", "No"), ("Has\nelectricity", "Yes")]),
    ("Internet", "internet_access", [("No\ninternet", "No"), ("Has\ninternet", "Yes")]),
]


@st.cache_data(show_spinner=False)
def chart_gaps(data):
    fig = Figure(figsize=(12, 3.3))
    axes = fig.subplots(1, len(GAP_GROUPS), sharey=True)
    rows = []
    for k, (ax, (ttl, col, items)) in enumerate(zip(axes, GAP_GROUPS)):
        style(ax, "y")
        vals, labels = [], []
        for label, value in items:
            sub = data[data[col] == value]
            r = float(sub[TARGET].mean()) if len(sub) else np.nan
            vals.append(r)
            labels.append(label)
            rows.append({"Group": ttl, "Category": label.replace("\n", " "), "Children": len(sub),
                         "Out-of-school rate (%)": round(r * 100, 1) if len(sub) else np.nan})
        x = np.arange(len(vals))
        ax.bar(x, np.nan_to_num(vals), width=0.30, color=C_OUT, zorder=3)
        for xi, v in zip(x, vals):
            if not np.isnan(v):
                ax.text(xi, v + 0.025, pct(v), ha="center", va="bottom", fontsize=9.5, color=INK)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=9)
        ax.set_xlim(-0.65, len(vals) - 0.35)
        ax.set_ylim(0, 1)
        ax.set_title(ttl, loc="left", fontsize=10.5, fontweight="bold", color=INK, pad=10)
        if k == 0:
            ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
        else:
            ax.spines["left"].set_visible(False)
            ax.tick_params(axis="y", labelleft=False)
    fig.subplots_adjust(wspace=0.10)
    return to_png(fig), pd.DataFrame(rows)


@st.cache_data(show_spinner=False)
def chart_age(data):
    g = data.groupby("child_age")[TARGET].agg(rate="mean", n="size")
    fig, ax = new_fig(6, 3.4)
    ax.plot(g.index, g["rate"], color=C_OUT, linewidth=2, solid_capstyle="round", zorder=3)
    ax.scatter(g.index, g["rate"], s=60, color=C_OUT, edgecolor=PAGE_BG, linewidth=2, zorder=4)
    hi, lo = g["rate"].idxmax(), g["rate"].idxmin()
    for age in {hi, lo}:
        ax.text(age, g.loc[age, "rate"] + 0.05, pct(g.loc[age, "rate"]), ha="center", fontsize=9, color=INK)
    ax.set_xticks(g.index)
    ax.set_ylim(0, 1)
    ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    ax.set_xlabel("Child age (years)")
    title(ax, "Out-of-school rate by child age")
    table = pd.DataFrame({"Age": g.index, "Children": g["n"].to_numpy(),
                          "Out-of-school rate (%)": (g["rate"] * 100).round(1).to_numpy()})
    return to_png(fig), table


# ---------- Risk-factor charts ----------
DIST_LABELS = ["< 1 km", "1–3 km", "3–5 km", "5–10 km", "10+ km"]
INC_LABELS = ["Lowest 20%", "2nd 20%", "Middle 20%", "4th 20%", "Highest 20%"]


@st.cache_data(show_spinner=False)
def chart_ordinal(data, kind, edu):
    """Column chart for ORDERED groups: the ramp goes light to dark with the order."""
    try:
        if kind == "distance":
            s = pd.cut(data["distance_to_school"], [0, 1, 3, 5, 10, np.inf], labels=DIST_LABELS, right=False)
            order, ttl, xl = DIST_LABELS, "Out-of-school rate by distance to school", "Distance to school"
        elif kind == "income":
            s = pd.qcut(data["household_income"].rank(method="first"), 5, labels=INC_LABELS)
            order, ttl, xl = INC_LABELS, "Out-of-school rate by household income", "Household income group"
        else:
            s = data[kind]
            order = [e for e in edu]
            ttl = f"Out-of-school rate by {kind.replace('_', ' ')}"
            xl = nice(kind.replace("_education", "")) + "'s highest level of schooling"
        s = pd.Series(np.asarray(s, dtype=object), index=data.index)
        g = (pd.DataFrame({"x": s, "y": data[TARGET]}).dropna(subset=["x"])
             .groupby("x")["y"].agg(rate="mean", n="size").reindex(order).dropna())
    except ValueError:
        return empty_chart("Not enough children in this selection")
    if g.empty:
        return empty_chart("Not enough children in this selection")
    pal = palette_for(len(order))
    colors = [pal[order.index(lbl)] for lbl in g.index]
    x = np.arange(len(g))
    fig, ax = new_fig(6, 3.5)
    ax.bar(x, g["rate"], width=0.26, color=colors, zorder=3)
    for xi, v in zip(x, g["rate"]):
        ax.text(xi, v + 0.025, pct(v), ha="center", va="bottom", fontsize=9.5, color=INK)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{lbl}\nn={int(n):,}" for lbl, n in zip(g.index, g["n"])], fontsize=8.5)
    ax.set_ylim(0, 1)
    ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    ax.set_xlabel(xl)
    title(ax, ttl)
    table = pd.DataFrame({"Group": list(g.index), "Children": g["n"].astype(int).to_numpy(),
                          "Out-of-school rate (%)": (g["rate"] * 100).round(1).to_numpy()})
    return to_png(fig), table


@st.cache_data(show_spinner=False)
def chart_heatmap(data):
    cols = ["Rural", "Urban"]
    g = data.groupby(["province", "urban_rural"])[TARGET].agg(rate="mean", n="size")
    rate = g["rate"].unstack().reindex(columns=cols)
    n = g["n"].unstack().reindex(columns=cols)
    if rate.empty:
        return empty_chart("Not enough children in this selection")
    order = data.groupby("province")[TARGET].mean().sort_values(ascending=False).index
    rate, n = rate.reindex(order), n.reindex(order)
    values = rate.where(n >= 30).to_numpy(dtype=float)
    fig = Figure(figsize=(6, 1.3 + 0.5 * len(order)))
    ax = fig.subplots()
    mesh = ax.pcolormesh(np.ma.masked_invalid(values), cmap=SEQ_CMAP, vmin=0, vmax=1,
                         edgecolors=PAGE_BG, linewidth=3)
    ax.set_xticks(np.arange(len(cols)) + 0.5)
    ax.set_xticklabels(cols, fontsize=9.5)
    ax.set_yticks(np.arange(len(order)) + 0.5)
    ax.set_yticklabels(list(order), fontsize=9)
    ax.xaxis.tick_top()
    ax.invert_yaxis()
    ax.tick_params(length=0)
    for side in ax.spines.values():
        side.set_visible(False)
    for i in range(len(order)):
        for j in range(len(cols)):
            v, cnt = values[i, j], n.iloc[i, j]
            if np.isnan(v):
                txt = "n < 30" if not np.isnan(cnt) else "no data"
                ax.text(j + 0.5, i + 0.5, txt, ha="center", va="center", fontsize=8.5, color=MUTED)
            else:
                ax.text(j + 0.5, i + 0.5, f"{v * 100:.0f}%\nn={int(cnt):,}", ha="center", va="center",
                        fontsize=9, color="#FFFFFF" if v >= 0.55 else INK)
    cbar = fig.colorbar(mesh, ax=ax, fraction=0.045, pad=0.04)
    cbar.outline.set_visible(False)
    cbar.ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    cbar.ax.tick_params(length=0, labelsize=8.5)
    ax.set_title("Out-of-school rate: province and location", loc="left", fontsize=11,
                 fontweight="bold", color=INK, pad=34)
    table = pd.DataFrame({"Province": [p for p in order for _ in cols],
                          "Location": cols * len(order),
                          "Children": [None if np.isnan(n.iloc[i, j]) else int(n.iloc[i, j])
                                       for i in range(len(order)) for j in range(len(cols))],
                          "Out-of-school rate (%)": [None if np.isnan(rate.iloc[i, j]) else round(rate.iloc[i, j] * 100, 1)
                                                     for i in range(len(order)) for j in range(len(cols))]})
    return to_png(fig), table


NUMERIC_FEATURES = ["child_age", "distance_to_school", "household_size", "number_of_children",
                    "household_income", "school_fee", "fee_to_income_ratio", "children_per_member"]


def diverging_barh(ax, labels, values, fmt, pos_label, neg_label):
    y = np.arange(len(values))
    colors = [C_OUT if v >= 0 else C_IN for v in values]
    ax.barh(y, values, height=0.38, color=colors, zorder=3)
    span = max(abs(np.min(values)), abs(np.max(values)), 1e-9)
    for yi, v in zip(y, values):
        ax.text(v + (0.03 * span if v >= 0 else -0.03 * span), yi, fmt(v), va="center",
                ha="left" if v >= 0 else "right", fontsize=9, color=INK)
    ax.axvline(0, color=BASELINE, linewidth=1, zorder=2)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlim(-span * 1.3, span * 1.3)
    ax.spines["left"].set_visible(False)
    ax.legend(handles=[Line2D([0], [0], marker="o", color="none", markerfacecolor=C_OUT, markersize=8, label=pos_label),
                       Line2D([0], [0], marker="o", color="none", markerfacecolor=C_IN, markersize=8, label=neg_label)],
              loc="lower right", fontsize=8.5)


@st.cache_data(show_spinner=False)
def chart_corr(data):
    cols = [c for c in NUMERIC_FEATURES if c in data.columns]
    corr = data[cols].corrwith(data[TARGET]).dropna().sort_values(ascending=False)
    if corr.empty:
        return empty_chart("Not enough children in this selection")
    fig, ax = new_fig(6, 0.9 + 0.4 * len(corr), grid="x")
    diverging_barh(ax, [nice(c) for c in corr.index], corr.to_numpy(), lambda v: f"{v:+.2f}",
                   "Higher value, more risk", "Higher value, less risk")
    title(ax, "Correlation of each numeric factor with being out of school")
    table = pd.DataFrame({"Factor": [nice(c) for c in corr.index], "Correlation": corr.round(3).to_numpy()})
    return to_png(fig), table


# ---------- Model-performance charts ----------
@st.cache_data(show_spinner=False)
def chart_model_comparison(cv_df, chosen):
    labels = {"accuracy": "Accuracy", "precision": "Precision", "recall": "Recall",
              "f1": "F1-score", "roc_auc": "ROC-AUC"}
    metrics = [m for m in labels if m in cv_df.columns]
    fig, ax = new_fig(6, 3.7, grid="x")
    y = np.arange(len(metrics))
    for yi, m in zip(y, metrics):
        ax.plot([cv_df[m].min(), cv_df[m].max()], [yi, yi], color=BASELINE, linewidth=1.5, zorder=1)
    for name in cv_df.index:
        xs = [cv_df.loc[name, m] for m in metrics]
        ax.scatter(xs, y, s=95, color=MODEL_COLORS.get(name, C_3), edgecolor=PAGE_BG, linewidth=2,
                   zorder=5 if name == chosen else 3,
                   label=name + (" (selected)" if name == chosen else ""))
        if name == chosen:
            # value labels go BELOW the dots so the first row never collides with the legend
            for xi, yi in zip(xs, y):
                ax.text(xi, yi + 0.26, f"{xi:.3f}", ha="center", va="top", fontsize=8.5, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels([labels[m] for m in metrics])
    ax.set_ylim(len(metrics) - 0.35, -0.55)
    lo, hi = cv_df[metrics].min().min(), cv_df[metrics].max().max()
    ax.set_xlim(lo - 0.04, hi + 0.04)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.2f}"))
    ax.spines["left"].set_visible(False)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3, fontsize=8.5, handletextpad=0.2,
              columnspacing=1.0)
    ax.set_title("Cross-validated scores of the three candidate models", loc="left", fontsize=11,
                 fontweight="bold", color=INK, pad=34)
    table = cv_df[metrics].rename(columns=labels).round(3).reset_index().rename(columns={"index": "Model"})
    return to_png(fig), table


def heat_matrix(ax, mat, row_labels, col_labels, fmt):
    ax.pcolormesh(mat, cmap=SEQ_CMAP, vmin=0, vmax=max(mat.max(), 1), edgecolors=PAGE_BG, linewidth=3)
    ax.set_xticks(np.arange(len(col_labels)) + 0.5)
    ax.set_xticklabels(col_labels, fontsize=9)
    ax.set_yticks(np.arange(len(row_labels)) + 0.5)
    ax.set_yticklabels(row_labels, fontsize=9)
    ax.invert_yaxis()
    ax.tick_params(length=0)
    for side in ax.spines.values():
        side.set_visible(False)
    top = max(mat.max(), 1)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            ax.text(j + 0.5, i + 0.5, fmt(i, j), ha="center", va="center", fontsize=10,
                    color="#FFFFFF" if mat[i, j] / top >= 0.55 else INK)


@st.cache_data(show_spinner=False)
def chart_confusion(y, p, t):
    m = metrics_at(y, p, t)
    mat = np.array([[m["tn"], m["fp"]], [m["fn"], m["tp"]]], dtype=float)
    fig = Figure(figsize=(4, 3.6))
    ax = fig.subplots()
    row_tot = mat.sum(axis=1, keepdims=True)
    heat_matrix(ax, mat, ["In school", "Out of school"], ["In school", "Out of school"],
                lambda i, j: f"{int(mat[i, j]):,}\n{mat[i, j] / row_tot[i, 0] * 100:.0f}% of row")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Confusion matrix", loc="left", fontsize=11, fontweight="bold", color=INK, pad=14)
    table = pd.DataFrame(mat.astype(int), index=["Actual: in school", "Actual: out of school"],
                         columns=["Predicted: in school", "Predicted: out of school"]).reset_index(names="")
    return to_png(fig), table


@st.cache_data(show_spinner=False)
def chart_roc(y, p, t):
    fpr, tpr, _ = roc_curve(y, p)
    m = metrics_at(y, p, t)
    op_fpr = m["fp"] / max(m["fp"] + m["tn"], 1)
    op_tpr = m["tp"] / max(m["tp"] + m["fn"], 1)
    fig, ax = new_fig(4, 3.6, grid="y")
    ax.plot([0, 1], [0, 1], color=BASELINE, linewidth=1, zorder=1)
    ax.fill_between(fpr, tpr, alpha=0.10, color=C_OUT, linewidth=0)
    ax.plot(fpr, tpr, color=C_OUT, linewidth=2, zorder=3)
    ax.scatter([op_fpr], [op_tpr], s=80, color=C_OUT, edgecolor=PAGE_BG, linewidth=2, zorder=4)
    ax.text(op_fpr + 0.04, op_tpr - 0.09, f"threshold {t:.2f}", fontsize=8.5, color=INK)
    ax.text(0.97, 0.05, f"AUC = {roc_auc_score(y, p):.3f}", ha="right", fontsize=9.5, color=INK)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("False positive rate")
    ax.set_ylabel("True positive rate (recall)")
    title(ax, "ROC curve")
    table = pd.DataFrame({"False positive rate": fpr[::8].round(3), "True positive rate": tpr[::8].round(3)})
    return to_png(fig), table


@st.cache_data(show_spinner=False)
def chart_pr(y, p, t):
    prec, rec, _ = precision_recall_curve(y, p)
    m = metrics_at(y, p, t)
    fig, ax = new_fig(4, 3.6, grid="y")
    ax.axhline(y.mean(), color=BASELINE, linewidth=1, zorder=1)
    ax.text(0.02, y.mean() + 0.02, "no-skill baseline", fontsize=8.5, color=MUTED)
    ax.fill_between(rec, prec, alpha=0.10, color=C_OUT, linewidth=0)
    ax.plot(rec, prec, color=C_OUT, linewidth=2, zorder=3)
    ax.scatter([m["recall"]], [m["precision"]], s=80, color=C_OUT, edgecolor=PAGE_BG, linewidth=2, zorder=4)
    ax.text(m["recall"] - 0.03, m["precision"] + 0.05, f"threshold {t:.2f}", ha="right", fontsize=8.5, color=INK)
    ax.text(0.03, 0.05, f"Avg. precision = {average_precision_score(y, p):.3f}", fontsize=9.5, color=INK)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    title(ax, "Precision-recall curve")
    table = pd.DataFrame({"Recall": rec[::8].round(3), "Precision": prec[::8].round(3)})
    return to_png(fig), table


@st.cache_data(show_spinner=False)
def chart_threshold_sweep(y, p, t):
    ts = np.round(np.arange(0.05, 0.951, 0.01), 2)
    rows = [metrics_at(y, p, x) for x in ts]
    series = [("Recall", [r["recall"] for r in rows], C_OUT),
              ("Precision", [r["precision"] for r in rows], C_IN),
              ("F1-score", [r["f1"] for r in rows], C_3)]
    fig, ax = new_fig(6, 3.5)
    ax.axvline(t, color=MUTED, linewidth=1, zorder=2)
    ends = spread([s[1][-1] for s in series], 0.09)
    for (name, vals, color), ey in zip(series, ends):
        ax.plot(ts, vals, color=color, linewidth=2, solid_capstyle="round", zorder=3, label=name)
        k = int(np.argmin(np.abs(ts - t)))
        ax.scatter([ts[k]], [vals[k]], s=55, color=color, edgecolor=PAGE_BG, linewidth=2, zorder=4)
        ax.text(ts[-1] + 0.015, ey, name, va="center", fontsize=9, color=INK)
    ax.text(t, 1.03, f"selected threshold {t:.2f}", ha="center", fontsize=8.5, color=INK)
    ax.set_xlim(0.05, 1.12)
    ax.set_ylim(0, 1.08)
    ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    ax.set_xlabel("Decision threshold (flag a child when the predicted risk is at least this high)")
    ax.legend(loc="lower left", fontsize=8.5, ncol=3)
    ax.set_title("What changes when the threshold moves", loc="left", fontsize=11, fontweight="bold",
                 color=INK, pad=22)
    table = pd.DataFrame({"Threshold": ts[::5], "Precision": np.round(series[1][1][::5], 3),
                          "Recall": np.round(series[0][1][::5], 3), "F1-score": np.round(series[2][1][::5], 3)})
    return to_png(fig), table


@st.cache_data(show_spinner=False)
def chart_proba_dist(y, p, t):
    bins = np.arange(0, 1.0001, 0.05)
    fig, ax = new_fig(6, 3.5)
    handles, rows = [], []
    for status, color, name in ((0, C_IN, "In school"), (1, C_OUT, "Out of school")):
        counts, edges = np.histogram(p[y == status], bins=bins)
        share = counts / max(counts.sum(), 1)
        ax.stairs(share, edges, color=color, linewidth=2)
        ax.stairs(share, edges, color=color, alpha=0.10, fill=True, linewidth=0)
        handles.append(Line2D([0], [0], color=color, lw=2, label=f"Actually {name.lower()}"))
        rows += [{"Group": name, "Predicted risk from": round(lo, 2), "Share of children (%)": round(s * 100, 1)}
                 for lo, s in zip(edges[:-1], share)]
    ax.axvline(t, color=MUTED, linewidth=1, zorder=2)
    ax.text(t, ax.get_ylim()[1] * 1.02, f"threshold {t:.2f}", ha="center", fontsize=8.5, color=INK)
    ax.set_xlim(0, 1)
    ax.set_ylim(bottom=0)
    ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    ax.set_xlabel("Predicted risk of being out of school")
    ax.legend(handles=handles, loc="upper center", fontsize=8.5, ncol=2)
    ax.set_title("How well the model separates the two groups", loc="left", fontsize=11,
                 fontweight="bold", color=INK, pad=22)
    return to_png(fig), pd.DataFrame(rows)


# ---------- Feature-importance charts ----------
@st.cache_data(show_spinner=False)
def chart_perm(importance, top=12):
    top_imp = importance.head(top)
    fig, ax = new_fig(6, 0.9 + 0.38 * len(top_imp), grid="x")
    y = np.arange(len(top_imp))
    ax.barh(y, top_imp.to_numpy(), height=0.38, color=C_OUT, zorder=3)
    span = max(top_imp.max(), 1e-9)
    for yi, v in zip(y, top_imp.to_numpy()):
        ax.text(v + 0.015 * span, yi, f"{v:.3f}", va="center", fontsize=9, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels([nice(c) for c in top_imp.index])
    ax.invert_yaxis()
    ax.set_xlim(0, span * 1.15)
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("Drop in ROC-AUC when the column is shuffled")
    title(ax, "Which factors the model relies on most")
    table = pd.DataFrame({"Factor": [nice(c) for c in importance.index],
                          "Drop in ROC-AUC": importance.round(4).to_numpy()})
    return to_png(fig), table


def coef_label(row):
    return nice(row["column"]) + (f": {row['level']}" if row["level"] else "")


@st.cache_data(show_spinner=False)
def chart_coefs(ctable, top=14):
    t = ctable.copy()
    t["label"] = t.apply(coef_label, axis=1)
    t = t.reindex(t["coef"].abs().sort_values(ascending=False).index).head(top)
    t = t.sort_values("coef", ascending=False)
    fig, ax = new_fig(6, 0.9 + 0.38 * len(t), grid="x")
    diverging_barh(ax, list(t["label"]), t["coef"].to_numpy(), lambda v: f"{v:+.2f}",
                   "Raises the risk", "Lowers the risk")
    ax.set_xlabel("Effect on the log-odds of being out of school")
    title(ax, "Direction of each factor's effect (logistic regression)")
    table = t[["label", "coef"]].rename(columns={"label": "Factor", "coef": "Coefficient"}).round(3)
    return to_png(fig), table


@st.cache_data(show_spinner=False)
def chart_contrib(contrib):
    top = contrib.reindex(contrib.abs().sort_values(ascending=False).index).head(8).sort_values(ascending=False)
    fig, ax = new_fig(6, 0.9 + 0.4 * len(top), grid="x")
    diverging_barh(ax, [nice(c) for c in top.index], top.to_numpy(), lambda v: f"{v:+.2f}",
                   "Pushes the risk up", "Pushes the risk down")
    ax.set_xlabel("Effect on the log-odds, compared with an average child")
    title(ax, "Why the model gave this estimate")
    table = pd.DataFrame({"Factor": [nice(c) for c in top.index], "Effect (log-odds)": top.round(3).to_numpy()})
    return to_png(fig), table


# =============================================================================
# 4. LAYOUT HELPERS
# =============================================================================
def kpi(label, value, sub="", text=False, small=False):
    cls = "kpi small" if small else "kpi"
    vcls = "kpi-value text" if text else "kpi-value"
    return (f'<div class="{cls}"><div class="kpi-label">{label}</div>'
            f'<div class="{vcls}">{value}</div><div class="kpi-sub">{sub}</div></div>')


def kpi_row(items, small=False):
    cols = st.columns(len(items), gap="small")
    for col, item in zip(cols, items):
        label, value, sub = item[0], item[1], item[2]
        text = item[3] if len(item) > 3 else False
        with col:
            st.markdown(kpi(label, value, sub, text, small), unsafe_allow_html=True)


def section(text, sub=None):
    html = f'<div class="section-title">{text}</div>'
    if sub:
        html += f'<div class="section-sub">{sub}</div>'
    st.markdown(html, unsafe_allow_html=True)


def callout(html):
    st.markdown(f'<div class="callout">{html}</div>', unsafe_allow_html=True)


def chart(fn, *args, tables=None, name=""):
    png, table = fn(*args)
    st.image(png)
    if tables is not None:
        tables.append((name, table))


def table_view(tables):
    with st.expander("View the numbers behind these charts"):
        for name, table in tables:
            if table is not None and len(table):
                st.caption(name)
                st.dataframe(table, hide_index=True)


# =============================================================================
# 5. SIDEBAR FILTERS
# =============================================================================
with st.sidebar:
    st.markdown("### Filters")
    st.caption("These filters apply to the score cards at the top, and to the Overview, Risk factors and Data tabs. "
               "The Model performance tab always uses all test children.")
    provinces = sorted(df["province"].unique())
    sel_prov = st.multiselect("Province", provinces, default=provinces)
    sel_loc = st.multiselect("Location", ["Rural", "Urban"], default=["Rural", "Urban"])
    sel_gender = st.multiselect("Gender", ["Female", "Male"], default=["Female", "Male"])
    age_min, age_max = int(df["child_age"].min()), int(df["child_age"].max())
    sel_age = st.slider("Child age", age_min, age_max, (age_min, age_max))
    st.markdown("---")
    st.caption("Data is synthetic: it shows how the method works and does not describe a real country.")

view = df[df["province"].isin(sel_prov) & df["urban_rural"].isin(sel_loc) & df["gender"].isin(sel_gender)
          & df["child_age"].between(sel_age[0], sel_age[1])]

# =============================================================================
# 6. HEADER + KPI CARDS
# =============================================================================
n_features_out = len(model.steps[0][1].get_feature_names_out())
st.markdown(
    '<div class="hero"><div class="hero-eyebrow">Machine learning · Education access</div>'
    '<div class="hero-title">Out-of-School Risk Dashboard</div>'
    '<div class="hero-sub">Can we predict whether a child is at risk of being out of school from their household, '
    'location and school-access conditions?</div>'
    f'<div class="hero-chips"><span>{len(df):,} children</span><span>{n_raw_inputs} input features</span>'
    f'<span>{model_name}</span><span>Synthetic data</span></div></div>',
    unsafe_allow_html=True,
)

# Model scores for the children in the sidebar selection (only children the model never saw during training).
MIN_TEST_CHILDREN = 30
test_mask = (X_test["province"].isin(sel_prov) & X_test["urban_rural"].isin(sel_loc)
             & X_test["gender"].isin(sel_gender)
             & X_test["child_age"].between(sel_age[0], sel_age[1])).to_numpy()
n_sel = int(test_mask.sum())
is_filtered = n_sel < len(y_test_arr)
reliable = n_sel >= MIN_TEST_CHILDREN
if is_filtered and reliable:
    y_sel, p_sel = y_test_arr[test_mask], proba[test_mask]
    ms = metrics_at(y_sel, p_sel, 0.5)
    auc_sel = float(roc_auc_score(y_sel, p_sel)) if len(np.unique(y_sel)) == 2 else float("nan")
    glance_sub = (f"Scores for the <b>{n_sel:,}</b> of {len(y_test_arr):,} test children who match the sidebar filters "
                  "(decision threshold 0.50). Small groups give less stable scores.")
else:
    ms, auc_sel = m50, auc
    glance_sub = f"Scores on {len(y_test):,} children the model never saw during training (decision threshold 0.50)."
    if is_filtered:   # too few test children in the selection to score reliably
        glance_sub += (f" Only {n_sel} test children match the sidebar filters, which is too few for reliable scores, "
                       "so the overall scores are shown.")
show_overall = is_filtered and reliable


def vs_all(label, value_all):
    return f"{label}<br>all test children: {value_all}" if show_overall else label


section("Model at a glance", glance_sub)
kpi_row([
    ("Model used", model_name, f"{params_text} · 5-fold CV", True),
    ("Accuracy", pct(ms["accuracy"], 1), vs_all("of children classified correctly", pct(m50["accuracy"], 1))),
    ("Precision", pct(ms["precision"], 1), vs_all("of children flagged really are out of school", pct(m50["precision"], 1))),
    ("Recall", pct(ms["recall"], 1), vs_all("of out-of-school children are found", pct(m50["recall"], 1))),
    ("F1-score", f"{ms['f1']:.3f}", vs_all("balance of precision and recall", f"{m50['f1']:.3f}")),
    ("ROC-AUC", "n/a" if np.isnan(auc_sel) else f"{auc_sel:.3f}",
     vs_all("ranking quality (0.5 = coin flip)", f"{auc:.3f}")),
])

section("The children in view", "These cards follow the filters in the sidebar.")
if view.empty:
    st.warning("No children match the current filters. Widen the filters in the sidebar.")
else:
    kpi_row([
        ("Children", f"{len(view):,}", f"of {len(df):,} in the dataset"),
        ("Out-of-school rate", pct(view[TARGET].mean(), 1), f"all children: {pct(overall_rate, 1)}"),
        ("Rural share", pct((view["urban_rural"] == "Rural").mean(), 0), "of children in view"),
        ("Average distance", f"{view['distance_to_school'].mean():.1f} km", "to the nearest school"),
        ("Median income", f"{view['household_income'].median():,.0f}", "PKR per month"),
        ("Without electricity", pct((view["electricity"] == "No").mean(), 0), "of households in view"),
    ], small=True)

# =============================================================================
# 7. TABS
# =============================================================================
tab_over, tab_risk, tab_model, tab_imp, tab_pred, tab_data = st.tabs(
    ["Overview", "Risk factors", "Model performance", "Feature importance", "Predict a child", "Data & about"])

# ----------------------------------------------------------------------------- Overview
with tab_over:
    if view.empty:
        st.info("Adjust the sidebar filters to see charts.")
    else:
        tables = []
        prov = rate_by(view, "province")
        prov = prov[prov["n"] >= 50].sort_values("rate", ascending=False)
        rural = view.loc[view["urban_rural"] == "Rural", TARGET]
        urban = view.loc[view["urban_rural"] == "Urban", TARGET]
        points = []
        if len(prov) >= 2:
            points.append(f"<b>{prov.index[0]}</b> has the highest out-of-school rate ({pct(prov['rate'].iloc[0])}) "
                          f"and <b>{prov.index[-1]}</b> the lowest ({pct(prov['rate'].iloc[-1])}).")
        if len(rural) >= 30 and len(urban) >= 30:
            points.append(f"Rural children are out of school <b>{pct(rural.mean())}</b> of the time, "
                          f"against <b>{pct(urban.mean())}</b> for urban children.")
        out_d = view.loc[view[TARGET] == 1, "distance_to_school"].median()
        in_d = view.loc[view[TARGET] == 0, "distance_to_school"].median()
        if not (np.isnan(out_d) or np.isnan(in_d)):
            points.append(f"The typical out-of-school child lives <b>{out_d:.1f} km</b> from school, "
                          f"against <b>{in_d:.1f} km</b> for a child in school.")
        if points:
            callout("<b>Key takeaways</b><br>" + "<br>".join("• " + p for p in points))

        c1, c2 = st.columns(2, gap="large")
        with c1:
            chart(chart_province, view, overall_rate, tables=tables, name="Out-of-school rate by province")
        with c2:
            chart(chart_distance, view, tables=tables, name="Distance to school, by status")
        section("Who is most affected?", "Out-of-school rate within each group. Each pair of bars compares two groups.")
        chart(chart_gaps, view, tables=tables, name="Out-of-school rate by group")
        c3, c4 = st.columns(2, gap="large")
        with c3:
            chart(chart_income, view, tables=tables, name="Household income, by status")
        with c4:
            chart(chart_age, view, tables=tables, name="Out-of-school rate by child age")
        table_view(tables)

# ----------------------------------------------------------------------------- Risk factors
with tab_risk:
    if view.empty:
        st.info("Adjust the sidebar filters to see charts.")
    else:
        tables = []
        callout("Darker bars mean a higher position in an ordered scale (farther away, higher income, more schooling). "
                "The height of each bar is the out-of-school rate.")
        c1, c2 = st.columns(2, gap="large")
        with c1:
            chart(chart_ordinal, view, "distance", edu_order, tables=tables, name="Rate by distance to school")
        with c2:
            chart(chart_ordinal, view, "income", edu_order, tables=tables, name="Rate by household income")
        c3, c4 = st.columns(2, gap="large")
        with c3:
            chart(chart_ordinal, view, "mother_education", edu_order, tables=tables, name="Rate by mother's education")
        with c4:
            chart(chart_ordinal, view, "father_education", edu_order, tables=tables, name="Rate by father's education")
        c5, c6 = st.columns(2, gap="large")
        with c5:
            chart(chart_heatmap, view, tables=tables, name="Rate by province and location")
        with c6:
            chart(chart_corr, view, tables=tables, name="Correlation with being out of school")
        callout("<b>Correlation is not causation.</b> For example, children with school transport look <i>more</i> at risk "
                "only because transport mostly exists where schools are far away. The model looks at all factors "
                "together, which helps separate such effects.")
        table_view(tables)

# ----------------------------------------------------------------------------- Model performance
with tab_model:
    tables = []
    cv_raw = meta.get("cv_results")
    section("Why this model?",
            "Three candidates were compared with 5-fold cross-validation on the training data. "
            "The best ROC-AUC was chosen, then tuned, then checked once on the test set.")
    c1, c2 = st.columns([1.1, 1], gap="large")
    with c1:
        if cv_raw:
            cv_df = pd.DataFrame(cv_raw)
            chart(chart_model_comparison, cv_df, model_name, tables=tables, name="Cross-validated scores")
        else:
            st.info("No cross-validation results were saved in the model metadata.")
    with c2:
        callout(
            f"<b>Selected: {model_name}</b><br>"
            "• All candidates scored within about 0.01-0.02 ROC-AUC of each other.<br>"
            "• When models perform about equally, the simplest and most explainable one is the better choice.<br>"
            f"• Settings after tuning: {params_text}.<br>"
            f"• Preprocessing turns the {n_raw_inputs} input columns plus {len(ENGINEERED)} engineered ratios into "
            f"{n_features_out} model features (median or most-frequent imputation, scaling, ordered and one-hot encoding).")
        callout("<b>How to read the scores</b><br>"
                "• <b>Precision</b>: of the children the model flags, how many really are out of school.<br>"
                "• <b>Recall</b>: of the children really out of school, how many the model finds.<br>"
                "• <b>ROC-AUC</b>: how well the model ranks at-risk children above safe ones.")

    section("Try a different decision threshold",
            "A child is flagged when the predicted risk is at least the threshold. Lower it to find more children "
            "(higher recall), raise it to be more selective (higher precision).")
    thr = st.slider("Decision threshold", 0.10, 0.90, 0.50, 0.01, key="perf_threshold")
    mt = metrics_at(y_test_arr, proba, thr)
    kpi_row([
        ("Precision", pct(mt["precision"], 1), f"{mt['tp']:,} of {mt['flagged']:,} flagged are out of school"),
        ("Recall", pct(mt["recall"], 1), f"{mt['tp']:,} of {mt['tp'] + mt['fn']:,} out-of-school children found"),
        ("F1-score", f"{mt['f1']:.3f}", "balance of precision and recall"),
        ("Children flagged", f"{mt['flagged']:,}", f"of {len(y_test_arr):,} in the test set"),
        ("Missed", f"{mt['fn']:,}", "out-of-school children not flagged"),
    ], small=True)

    e1, e2, e3 = st.columns(3, gap="medium")
    with e1:
        chart(chart_confusion, y_test_arr, proba, thr, tables=tables, name="Confusion matrix")
    with e2:
        chart(chart_roc, y_test_arr, proba, thr, tables=tables, name="ROC curve (sampled points)")
    with e3:
        chart(chart_pr, y_test_arr, proba, thr, tables=tables, name="Precision-recall curve (sampled points)")
    f1c, f2c = st.columns(2, gap="large")
    with f1c:
        chart(chart_threshold_sweep, y_test_arr, proba, thr, tables=tables, name="Metrics across thresholds")
    with f2c:
        chart(chart_proba_dist, y_test_arr, proba, thr, tables=tables, name="Predicted risk by actual status")
    table_view(tables)

# ----------------------------------------------------------------------------- Feature importance
with tab_imp:
    tables = []
    section("What drives the predictions?",
            "Two views: how much the model relies on each factor, and which way each factor pushes the risk.")
    imp = perm_importance(model, X_test, y_test)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        chart(chart_perm, imp, tables=tables, name="Permutation importance")
    with c2:
        ctable = coef_table(model, feature_cols)
        if ctable is not None:
            chart(chart_coefs, ctable, tables=tables, name="Coefficients")
        else:
            st.info("Coefficients are only available for linear models such as logistic regression.")
    top3 = ", ".join(nice(c).lower() for c in imp.index[:3])
    callout(f"<b>Reading these charts.</b> The most influential factors are <b>{top3}</b>. "
            "Importance shows how much predictions change when a column is shuffled; a factor that overlaps with others "
            "(for example province and distance) can look less important than it really is. "
            "Coefficients are on a standardised scale: numeric factors are per one standard deviation, "
            "education is per one level, and category labels compare with the reference category. "
            "Overlapping factors can offset each other (for example school type and school fee, or province and "
            "distance), so read a single coefficient with care. "
            "These are associations in the data, not proven causes.")
    table_view(tables)

# ----------------------------------------------------------------------------- Predict a child
with tab_pred:
    section("Estimate the risk for one child",
            "Fill in the child's details and press the button. Education can be set to “Not known”; the model fills gaps the same way it did in training.")
    med = df.median(numeric_only=True)

    def mode_of(col):
        return df[col].mode().iloc[0]

    def idx(options, value):
        return options.index(value) if value in options else 0

    prov_opts = sorted(df["province"].unique())
    school_opts = sorted(df["school_type"].unique())
    edu_opts = edu_order + ["Not known"]

    with st.form("predict_form"):
        fa, fb, fc, fd = st.columns(4, gap="medium")
        with fa:
            st.markdown("**Child**")
            p_age = st.slider("Age", age_min, age_max, int(med["child_age"]))
            p_gender = st.selectbox("Gender", ["Female", "Male"], index=idx(["Female", "Male"], mode_of("gender")))
            p_dis = st.selectbox("Disability", ["No", "Yes"], index=idx(["No", "Yes"], mode_of("disability")))
        with fb:
            st.markdown("**Location**")
            p_prov = st.selectbox("Province", prov_opts, index=idx(prov_opts, mode_of("province")))
            p_loc = st.selectbox("Urban or rural", ["Rural", "Urban"], index=idx(["Rural", "Urban"], mode_of("urban_rural")))
            p_dist = st.number_input("Distance to school (km)", min_value=0.1, max_value=25.0,
                                     value=float(round(med["distance_to_school"], 1)), step=0.5)
            p_trans = st.selectbox("School transport available", ["No", "Yes"], index=idx(["No", "Yes"], mode_of("transport_available")))
        with fc:
            st.markdown("**Household**")
            p_hh = st.slider("Household size", 2, 16, int(med["household_size"]))
            p_kids = st.slider("Number of children", 1, 12, int(med["number_of_children"]))
            p_inc = st.number_input("Household income (PKR per month)", min_value=5000, max_value=1000000,
                                    value=int(round(med["household_income"], -3)), step=1000)
            p_mom = st.selectbox("Mother's education", edu_opts, index=idx(edu_opts, mode_of("mother_education")))
            p_dad = st.selectbox("Father's education", edu_opts, index=idx(edu_opts, mode_of("father_education")))
        with fd:
            st.markdown("**Access and school**")
            p_net = st.selectbox("Internet at home", ["No", "Yes"], index=idx(["No", "Yes"], mode_of("internet_access")))
            p_el = st.selectbox("Electricity at home", ["Yes", "No"], index=idx(["Yes", "No"], mode_of("electricity")))
            p_school = st.selectbox("School type", school_opts, index=idx(school_opts, mode_of("school_type")))
            p_fee = st.number_input("School fee (PKR per month)", min_value=0, max_value=20000,
                                    value=int(round(med["school_fee"], -1)), step=50)
        st.form_submit_button("Estimate risk")

    if p_kids > p_hh:
        st.warning("A household cannot have more children than members, so the number of children was set to the household size.")
        p_kids = p_hh

    child = pd.DataFrame([{
        "child_age": p_age, "gender": p_gender, "disability": p_dis, "province": p_prov, "urban_rural": p_loc,
        "distance_to_school": p_dist, "transport_available": p_trans, "household_size": p_hh,
        "number_of_children": p_kids, "household_income": p_inc,
        "mother_education": np.nan if p_mom == "Not known" else p_mom,
        "father_education": np.nan if p_dad == "Not known" else p_dad,
        "internet_access": p_net, "electricity": p_el, "school_fee": p_fee, "school_type": p_school,
    }])
    child = add_features(child)[feature_cols]
    risk = float(model.predict_proba(child)[0, 1])

    pred_thr = st.slider("Decision threshold for flagging a child", 0.10, 0.90, 0.40, 0.01, key="pred_threshold",
                         help="0.40 finds more at-risk children than 0.50 at the cost of more false alarms.")
    if risk >= pred_thr:
        status, color, text = "critical", STATUS["critical"], "▲ Flag for support"
    elif risk >= pred_thr - 0.15:
        status, color, text = "warning", STATUS["warning"], "! Monitor"
    else:
        status, color, text = "good", STATUS["good"], "✓ Low risk"

    r1, r2 = st.columns([1, 1.2], gap="large")
    with r1:
        st.markdown(
            '<div class="kpi" style="min-height:0"><div class="kpi-label">Estimated risk of being out of school</div>'
            f'<div class="kpi-value" style="font-size:3rem">{pct(risk, 1)}</div>'
            f'<div class="meter"><div class="meter-fill" style="width:{risk * 100:.1f}%"></div>'
            f'<div class="meter-tick" style="left:{pred_thr * 100:.1f}%"></div></div>'
            f'<div class="kpi-sub">The black tick marks your threshold ({pred_thr:.2f}).</div>'
            f'<div style="margin-top:12px"><span class="badge"><span class="dot" style="background:{color}"></span>{text}</span></div>'
            '</div>',
            unsafe_allow_html=True)
        same = df[(df["province"] == p_prov) & (df["urban_rural"] == p_loc)]
        if len(same) >= 30:
            st.caption(f"For comparison, {pct(same[TARGET].mean())} of the {len(same):,} children in the data from "
                       f"{p_prov} ({p_loc.lower()}) are out of school.")
        st.caption("A screening estimate to help prioritise outreach, never a decision about a child.")
    with r2:
        ctable = coef_table(model, feature_cols)
        if ctable is not None:
            means = train_feature_means(model, X_train)
            row = transform_dense(model, child)[0]
            effect = pd.Series(ctable["coef"].to_numpy() * (row - means), index=ctable["column"].to_numpy())
            effect = effect.groupby(level=0).sum()
            png, _ = chart_contrib(effect)
            st.image(png)
        else:
            st.info("The explanation chart is available for linear models such as logistic regression.")

# ----------------------------------------------------------------------------- Data & about
with tab_data:
    section("About this project")
    a1, a2 = st.columns(2, gap="large")
    with a1:
        callout(
            "<b>Problem.</b> Predict whether a child is at risk of being out of school (1) or in school (0) from "
            "household, location and school-access conditions. This is supervised binary classification.<br><br>"
            "<b>Data.</b> 5,000 synthetic children with 16 input columns. Cleaning removed duplicates, capped "
            "extreme values at the 1st and 99th percentile, and left gaps to be imputed inside the model pipeline "
            "so that no information leaks from the test set.")
    with a2:
        callout(
            f"<b>Model.</b> {model_name} ({params_text}). The pipeline imputes, scales or encodes each column group, "
            f"giving {n_features_out} model features, then fits the classifier. "
            f"{len(X_train):,} children were used for training and {len(X_test):,} for testing.<br><br>"
            "<b>Limits.</b> Synthetic data only; about one prediction in four is wrong; feature effects are "
            "associations, not causes. Use gender and disability to direct help, never to deny it.")

    section("Missing values in the cleaned file", "These gaps are filled inside the model pipeline.")
    miss = df.isna().sum()
    miss = miss[miss > 0]
    st.dataframe(pd.DataFrame({"Column": [nice(c) for c in miss.index], "Missing": miss.to_numpy(),
                               "Share (%)": (miss / len(df) * 100).round(1).to_numpy()}), hide_index=True)

    section("Browse the data", f"{len(view):,} children match the sidebar filters.")
    st.dataframe(view, hide_index=True)
    st.download_button("Download filtered data (CSV)", view.to_csv(index=False).encode("utf-8"),
                       file_name="out_of_school_filtered.csv", mime="text/csv")
