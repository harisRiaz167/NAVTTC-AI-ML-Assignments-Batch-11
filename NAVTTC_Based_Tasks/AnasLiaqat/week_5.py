"""
Credit Card Default Risk - Streamlit Dashboard
==============================================
Converted from the notebook `Default_of_Credit.ipynb`.

Run it with:
    streamlit run app.py

Needs `UCI_Credit_Card.csv` in the same folder as this file
(or upload it from the sidebar).
"""

import os

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import StratifiedKFold, cross_val_predict, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# ----------------------------------------------------------------------------
# Page setup and style
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Credit Default Risk",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

NAVY = "#0F172A"
TEAL = "#0F766E"
BLUE = "#2563EB"
CORAL = "#E4572E"
GOLD = "#F59E0B"
SLATE = "#64748B"
LIGHT = "#F1F5F9"

st.markdown(
    """
    <style>
        .block-container {padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1280px;}
        footer {visibility: hidden;}
        .hero {
            background: linear-gradient(120deg, #0F172A 0%, #0F766E 100%);
            padding: 26px 32px; border-radius: 16px; margin-bottom: 22px;
        }
        .hero h1 {color: #FFFFFF; margin: 0; font-size: 2rem; font-weight: 700;}
        .hero p {color: #CBD5E1; margin: 6px 0 0 0; font-size: 1.02rem;}
        .kpi {
            background: #FFFFFF; border: 1px solid #E2E8F0; border-left: 5px solid #0F766E;
            border-radius: 12px; padding: 14px 18px; box-shadow: 0 1px 3px rgba(15,23,42,0.06);
            margin-bottom: 10px;
        }
        .kpi-label {color: #64748B; font-size: 0.78rem; font-weight: 600;
                    text-transform: uppercase; letter-spacing: 0.04em;}
        .kpi-value {color: #0F172A; font-size: 1.75rem; font-weight: 700; line-height: 1.25;}
        .kpi-sub {color: #64748B; font-size: 0.8rem;}
        .callout {
            background: #F1F5F9; border-radius: 12px; padding: 14px 18px;
            border-left: 5px solid #2563EB; color: #0F172A; margin: 8px 0 14px 0;
        }
        .result-high {background:#FEE2E2; border-left:6px solid #DC2626; color:#7F1D1D;
                      padding:16px 20px; border-radius:12px; font-size:1.1rem; font-weight:600;}
        .result-low {background:#DCFCE7; border-left:6px solid #16A34A; color:#14532D;
                     padding:16px 20px; border-radius:12px; font-size:1.1rem; font-weight:600;}
        h2, h3 {color: #0F172A;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------
DATA_FILE = "UCI_Credit_Card.csv"
PAY_COLS = [f"PAY_{i}" for i in range(1, 7)]
BILL_COLS = [f"BILL_AMT{i}" for i in range(1, 7)]
PAY_AMT_COLS = [f"PAY_AMT{i}" for i in range(1, 7)]
CATEGORICAL = ["SEX", "EDUCATION", "MARRIAGE"]
MONTHS = ["September", "August", "July", "June", "May", "April"]

SEX_MAP = {1: "Male", 2: "Female"}
EDU_MAP = {1: "Graduate school", 2: "University", 3: "High school", 4: "Others"}
MAR_MAP = {1: "Married", 2: "Single", 3: "Others"}
DEFAULT_LABEL = {0: "No default", 1: "Default"}
COLOR_MAP = {"No default": TEAL, "Default": CORAL}

NEW_FEATURES = {
    "AVG_DELAY": "Average payment status over 6 months",
    "MAX_DELAY": "Worst payment status in 6 months",
    "MONTHS_LATE": "Number of months with a late payment",
    "AVG_BILL": "Average bill amount over 6 months",
    "TOTAL_PAID": "Total amount paid over 6 months",
    "PAY_RATIO": "Share of the bills that was actually paid (0 to 1)",
    "UTILIZATION": "Latest bill divided by the credit limit",
    "BILL_TREND": "Latest bill minus the oldest bill (growing or shrinking)",
}


def pay_label(v):
    if v == -2:
        return "-2  No consumption"
    if v == -1:
        return "-1  Paid in full"
    if v == 0:
        return " 0  Revolving credit"
    return f"{v}  month(s) late"


# ----------------------------------------------------------------------------
# Data preparation (same steps as the notebook)
# ----------------------------------------------------------------------------
def add_features(d):
    """Fix category codes and add the 8 engineered columns (row by row)."""
    d = d.copy()
    d["EDUCATION"] = d["EDUCATION"].replace({0: 4, 5: 4, 6: 4})
    d["MARRIAGE"] = d["MARRIAGE"].replace({0: 3})
    d["AVG_DELAY"] = d[PAY_COLS].mean(axis=1)
    d["MAX_DELAY"] = d[PAY_COLS].max(axis=1)
    d["MONTHS_LATE"] = (d[PAY_COLS] > 0).sum(axis=1)
    d["AVG_BILL"] = d[BILL_COLS].mean(axis=1)
    d["TOTAL_PAID"] = d[PAY_AMT_COLS].sum(axis=1)
    total_bills = d[BILL_COLS].clip(lower=0).sum(axis=1).replace(0, np.nan)
    d["PAY_RATIO"] = (d["TOTAL_PAID"] / total_bills).fillna(1).clip(0, 1)
    d["UTILIZATION"] = (d["BILL_AMT1"] / d["LIMIT_BAL"]).clip(-1, 2)
    d["BILL_TREND"] = d["BILL_AMT1"] - d["BILL_AMT6"]
    return d


@st.cache_data(show_spinner=False)
def load_raw(path):
    return pd.read_csv(path)


@st.cache_data(show_spinner="Preparing the data...")
def prepare(raw):
    report = {
        "rows": int(raw.shape[0]),
        "raw_cols": int(raw.shape[1]),
        "nulls": int(raw.isnull().sum().sum()),
        "duplicates": int(raw.duplicated().sum()),
    }
    df = raw.rename(columns={"PAY_0": "PAY_1", "default.payment.next.month": "DEFAULT"})
    df = df.drop(columns=["ID"], errors="ignore")
    report["edu_fixed"] = int(df["EDUCATION"].isin([0, 5, 6]).sum())
    report["mar_fixed"] = int((df["MARRIAGE"] == 0).sum())
    report["neg_bills"] = int((df[BILL_COLS] < 0).sum().sum())
    report["edu_before"] = df["EDUCATION"].value_counts().sort_index().to_dict()
    report["mar_before"] = df["MARRIAGE"].value_counts().sort_index().to_dict()
    return add_features(df), report


@st.cache_resource(show_spinner="Training the model...")
def train(df):
    X = df.drop(columns=["DEFAULT"])
    y = df["DEFAULT"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    num_cols = [c for c in X.columns if c not in CATEGORICAL]
    pre = ColumnTransformer(
        [
            ("num", StandardScaler(), num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
        ]
    )
    model = Pipeline(
        [("preprocess", pre), ("classifier", LogisticRegression(max_iter=1000, random_state=42))]
    )
    model.fit(X_train, y_train)

    # Tuned threshold: chosen on TRAINING data only (cross-validated probabilities)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    oof = cross_val_predict(model, X_train, y_train, cv=cv, method="predict_proba")[:, 1]
    grid = np.arange(0.10, 0.70, 0.02)
    best_t = float(round(grid[int(np.argmax([f1_score(y_train, oof >= t) for t in grid]))], 2))

    probs_test = model.predict_proba(X_test)[:, 1]
    dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
    names = [n.split("__", 1)[-1] for n in model.named_steps["preprocess"].get_feature_names_out()]

    return {
        "model": model,
        "columns": list(X.columns),
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "probs_test": probs_test,
        "best_t": best_t,
        "train_acc": accuracy_score(y_train, model.predict(X_train)),
        "test_acc": accuracy_score(y_test, model.predict(X_test)),
        "baseline_acc": accuracy_score(y_test, dummy.predict(X_test)),
        "auc": roc_auc_score(y_test, probs_test),
        "feat_names": names,
        "coefs": model.named_steps["classifier"].coef_[0],
    }


def metrics_at(y_true, probs, t):
    pred = (probs >= t).astype(int)
    return {
        "accuracy": accuracy_score(y_true, pred),
        "precision": precision_score(y_true, pred, zero_division=0),
        "recall": recall_score(y_true, pred, zero_division=0),
        "f1": f1_score(y_true, pred, zero_division=0),
        "cm": confusion_matrix(y_true, pred, labels=[0, 1]),
        "pred": pred,
    }


# ----------------------------------------------------------------------------
# UI helpers
# ----------------------------------------------------------------------------
def hero(title, subtitle):
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)


def kpi(label, value, sub="", color=TEAL):
    st.markdown(
        f'<div class="kpi" style="border-left-color:{color}">'
        f'<div class="kpi-label">{label}</div><div class="kpi-value">{value}</div>'
        f'<div class="kpi-sub">{sub}</div></div>',
        unsafe_allow_html=True,
    )


def callout(text):
    st.markdown(f'<div class="callout">{text}</div>', unsafe_allow_html=True)


def style(fig, height=380, title=None):
    fig.update_layout(
        template="plotly_white",
        height=height,
        title=dict(text=title, font=dict(size=16, color=NAVY)) if title else None,
        margin=dict(l=10, r=10, t=50 if title else 20, b=10),
        font=dict(family="Inter, Segoe UI, sans-serif", size=13, color=NAVY),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    )
    return fig


def rate_bar(df, group, title, ytitle="Default rate"):
    g = df.groupby(group, observed=True)["DEFAULT"].agg(["mean", "size"]).reset_index()
    g[group] = g[group].astype(str)
    fig = go.Figure(
        go.Bar(
            x=g[group],
            y=g["mean"],
            marker_color=CORAL,
            text=[f"{v:.0%}" for v in g["mean"]],
            textposition="outside",
            customdata=g["size"],
            hovertemplate="%{x}<br>Default rate: %{y:.1%}<br>Clients: %{customdata:,}<extra></extra>",
        )
    )
    overall = df["DEFAULT"].mean()
    fig.add_hline(
        y=overall,
        line_dash="dash",
        line_color=NAVY,
        annotation_text=f"Overall {overall:.1%}",
        annotation_position="top left",
    )
    fig.update_yaxes(tickformat=".0%", title=ytitle, range=[0, min(1, g["mean"].max() + 0.15)])
    return style(fig, 390, title)


# ----------------------------------------------------------------------------
# Pages
# ----------------------------------------------------------------------------
def page_overview(df, report, M):
    hero(
        "Credit Card Default Risk",
        "Predicting which clients will fail to pay next month's bill, from 6 months of payment history.",
    )
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi("Clients analysed", f"{len(df):,}", "Taiwan bank, Apr-Sep 2005", BLUE)
    with c2:
        kpi("Default rate", f"{df['DEFAULT'].mean():.1%}", "Share of clients who defaulted", CORAL)
    with c3:
        kpi("Features used", f"{df.shape[1] - 1}", "23 original + 8 engineered", GOLD)
    with c4:
        kpi("Test accuracy", f"{M['test_acc']:.1%}", f"Baseline {M['baseline_acc']:.1%}", TEAL)

    st.markdown("### The business problem")
    callout(
        "A bank loses money when a client cannot pay the credit card bill (a <b>default</b>). "
        "If the bank can flag risky clients early, it can lower their limit, call them, or offer a payment plan. "
        "This app trains a <b>Logistic Regression</b> model on 30,000 real clients and lets you explore the data, "
        "judge the model, and score a new client."
    )

    late = df[df["PAY_1"] >= 2]["DEFAULT"].mean()
    ontime = df[df["PAY_1"] <= 0]["DEFAULT"].mean()
    st.markdown("### Key findings")
    k1, k2, k3 = st.columns(3)
    with k1:
        kpi("2+ months late (last month)", f"{late:.0%}", "of these clients default", CORAL)
    with k2:
        kpi("Paid on time or revolving", f"{ontime:.0%}", "of these clients default", TEAL)
    with k3:
        top = df.corr(numeric_only=True)["DEFAULT"].drop("DEFAULT").abs().idxmax()
        kpi("Strongest signal", top, "Highest correlation with default", BLUE)

    st.markdown("### Workflow")
    steps = [
        ("1. Clean", "Rename columns, drop ID, fix unknown category codes."),
        ("2. Engineer", "Create 8 new columns from the payment history."),
        ("3. Train", "Scale + encode + Logistic Regression in one pipeline."),
        ("4. Evaluate", "Accuracy, recall, F1, ROC-AUC and a tuned threshold."),
    ]
    for col, (t, d) in zip(st.columns(4), steps):
        with col:
            callout(f"<b>{t}</b><br>{d}")

    with st.expander("Preview the prepared data"):
        st.dataframe(df.head(100))


def page_quality(df, report, M):
    hero("Data Quality", "What we checked and what we fixed before modelling.")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        kpi("Rows", f"{report['rows']:,}", f"{report['raw_cols']} raw columns", BLUE)
    with c2:
        kpi("Null values", f"{report['nulls']}", "Nothing to fill", TEAL)
    with c3:
        kpi("Duplicate rows", f"{report['duplicates']}", "Nothing to remove", TEAL)
    with c4:
        kpi("Codes fixed", f"{report['edu_fixed'] + report['mar_fixed']:,}", "Unknown EDUCATION/MARRIAGE", GOLD)
    with c5:
        kpi("Negative bills", f"{report['neg_bills']:,}", "Kept: client overpaid", SLATE)

    left, right = st.columns(2)
    with left:
        st.markdown("#### EDUCATION: before and after")
        before = pd.DataFrame(
            {"Code": [str(k) for k in report["edu_before"]], "Clients": list(report["edu_before"].values()), "Stage": "Before"}
        )
        after_counts = df["EDUCATION"].value_counts().sort_index()
        after = pd.DataFrame({"Code": [str(k) for k in after_counts.index], "Clients": after_counts.values, "Stage": "After"})
        fig = px.bar(
            pd.concat([before, after]),
            x="Code",
            y="Clients",
            color="Stage",
            barmode="group",
            color_discrete_map={"Before": SLATE, "After": TEAL},
        )
        st.plotly_chart(style(fig, 340))
        st.caption("Codes 0, 5 and 6 are undocumented, so they are merged into 4 (Others).")
    with right:
        st.markdown("#### MARRIAGE: before and after")
        before = pd.DataFrame(
            {"Code": [str(k) for k in report["mar_before"]], "Clients": list(report["mar_before"].values()), "Stage": "Before"}
        )
        after_counts = df["MARRIAGE"].value_counts().sort_index()
        after = pd.DataFrame({"Code": [str(k) for k in after_counts.index], "Clients": after_counts.values, "Stage": "After"})
        fig = px.bar(
            pd.concat([before, after]),
            x="Code",
            y="Clients",
            color="Stage",
            barmode="group",
            color_discrete_map={"Before": SLATE, "After": TEAL},
        )
        st.plotly_chart(style(fig, 340))
        st.caption("Code 0 is undocumented, so it is merged into 3 (Others).")

    st.markdown("#### What the coded columns mean")
    a, b, c = st.columns(3)
    with a:
        st.dataframe(pd.DataFrame({"Code": list(SEX_MAP), "SEX": list(SEX_MAP.values())}), hide_index=True)
    with b:
        st.dataframe(pd.DataFrame({"Code": list(EDU_MAP), "EDUCATION": list(EDU_MAP.values())}), hide_index=True)
    with c:
        st.dataframe(pd.DataFrame({"Code": list(MAR_MAP), "MARRIAGE": list(MAR_MAP.values())}), hide_index=True)

    st.markdown("#### Payment status columns (PAY_1 to PAY_6)")
    callout(
        "<b>-2</b> no credit use &nbsp;|&nbsp; <b>-1</b> paid in full &nbsp;|&nbsp; <b>0</b> revolving credit "
        "&nbsp;|&nbsp; <b>1, 2, 3...</b> months the payment is late. A bigger number is a worse sign."
    )
    with st.expander("Summary statistics"):
        st.dataframe(df.describe().T.round(2))


def page_explore(df, report, M):
    hero("Exploration", "Which columns relate to default? Hover over any chart for details.")
    labeled = df.assign(Status=df["DEFAULT"].map(DEFAULT_LABEL))

    c1, c2 = st.columns([1, 2])
    with c1:
        counts = labeled["Status"].value_counts()
        fig = go.Figure(
            go.Pie(
                labels=counts.index,
                values=counts.values,
                hole=0.62,
                marker=dict(colors=[COLOR_MAP[l] for l in counts.index]),
                textinfo="percent",
            )
        )
        st.plotly_chart(style(fig, 390, "Target balance"))
    with c2:
        st.plotly_chart(rate_bar(df, "PAY_1", "Default rate by last month's payment status (PAY_1)"))
    callout(
        "Clients with no delay default about 13-17% of the time, but at <b>2 months late</b> the rate jumps above 60%. "
        "Very late groups (6+ months) have few clients, so read their bars carefully (see the hover text)."
    )

    c3, c4 = st.columns(2)
    with c3:
        grp = pd.qcut(df["LIMIT_BAL"], 5, labels=["Q1 lowest", "Q2", "Q3", "Q4", "Q5 highest"])
        tmp = df.assign(LimitGroup=grp)
        st.plotly_chart(rate_bar(tmp, "LimitGroup", "Default rate by credit limit group"))
    with c4:
        choice = st.selectbox("Compare default rate by", ["Sex", "Education", "Marital status", "Age group"])
        if choice == "Sex":
            tmp = df.assign(Group=df["SEX"].map(SEX_MAP))
        elif choice == "Education":
            tmp = df.assign(Group=df["EDUCATION"].map(EDU_MAP))
        elif choice == "Marital status":
            tmp = df.assign(Group=df["MARRIAGE"].map(MAR_MAP))
        else:
            tmp = df.assign(Group=pd.cut(df["AGE"], [20, 30, 40, 50, 60, 80], labels=["21-30", "31-40", "41-50", "51-60", "61+"]))
        st.plotly_chart(rate_bar(tmp, "Group", f"Default rate by {choice.lower()}"))

    st.markdown("### Correlation with default")
    corr = df.corr(numeric_only=True)["DEFAULT"].drop("DEFAULT").sort_values()
    fig = go.Figure(
        go.Bar(
            x=corr.values,
            y=corr.index,
            orientation="h",
            marker_color=[CORAL if v > 0 else BLUE for v in corr.values],
            hovertemplate="%{y}: %{x:.3f}<extra></extra>",
        )
    )
    fig.update_xaxes(title="Correlation with DEFAULT")
    st.plotly_chart(style(fig, 640))

    st.markdown("### Distribution explorer")
    numeric = [c for c in df.columns if c not in CATEGORICAL + ["DEFAULT"]]
    col = st.selectbox("Choose a column", numeric, index=numeric.index("LIMIT_BAL"))
    fig = px.histogram(
        labeled,
        x=col,
        color="Status",
        nbins=50,
        barmode="overlay",
        opacity=0.65,
        histnorm="percent",
        marginal="box",
        color_discrete_map=COLOR_MAP,
    )
    st.plotly_chart(style(fig, 440))

    with st.expander("Full correlation matrix"):
        m = df.corr(numeric_only=True)
        fig = px.imshow(m, color_continuous_scale="RdBu_r", zmin=-1, zmax=1, aspect="auto")
        st.plotly_chart(style(fig, 760))


def page_features(df, report, M):
    hero("Feature Engineering", "8 new columns built from each client's own payment history.")
    corr = df[list(NEW_FEATURES) + ["DEFAULT"]].corr()["DEFAULT"].drop("DEFAULT")
    table = pd.DataFrame(
        {"Feature": list(NEW_FEATURES), "What it means": list(NEW_FEATURES.values()), "Correlation with default": corr.round(3).values}
    )
    left, right = st.columns([3, 2])
    with left:
        st.dataframe(table, hide_index=True)
        callout(
            "Each new value uses only the <b>same row</b>, so creating these columns before the train/test split "
            "does not leak any test information."
        )
    with right:
        s = corr.sort_values()
        fig = go.Figure(
            go.Bar(x=s.values, y=s.index, orientation="h", marker_color=[CORAL if v > 0 else BLUE for v in s.values])
        )
        st.plotly_chart(style(fig, 360, "Correlation with DEFAULT"))

    feat = st.selectbox("Inspect a new feature", list(NEW_FEATURES), index=2)
    labeled = df.assign(Status=df["DEFAULT"].map(DEFAULT_LABEL))
    fig = px.box(labeled, x="Status", y=feat, color="Status", color_discrete_map=COLOR_MAP, points=False)
    fig.update_layout(showlegend=False)
    st.plotly_chart(style(fig, 420, f"{feat} for clients who default vs do not"))


def page_model(df, report, M):
    hero("Model Performance", "Logistic Regression in a scikit-learn Pipeline, tested on 6,000 unseen clients.")
    thr = st.session_state["thr"]
    y_test, probs = M["y_test"], M["probs_test"]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi("Test accuracy (0.50)", f"{M['test_acc']:.1%}", f"Train {M['train_acc']:.1%}: no overfitting", TEAL)
    with c2:
        kpi("Baseline", f"{M['baseline_acc']:.1%}", "Always guess 'no default'", SLATE)
    with c3:
        kpi("ROC-AUC", f"{M['auc']:.3f}", "Ranking quality (0.5 = random)", BLUE)
    with c4:
        kpi("Tuned threshold", f"{M['best_t']:.2f}", "Best F1 on training data", GOLD)

    r = metrics_at(y_test, probs, thr)
    st.markdown(f"### Results at the current decision threshold: **{thr:.2f}**")
    st.caption("Change the threshold in the sidebar. A lower threshold flags more clients as risky.")
    a, b, c, d = st.columns(4)
    with a:
        kpi("Accuracy", f"{r['accuracy']:.1%}", "", TEAL)
    with b:
        kpi("Precision", f"{r['precision']:.1%}", "Flagged clients who really default", BLUE)
    with c:
        kpi("Recall", f"{r['recall']:.1%}", "Real defaulters we catch", CORAL)
    with d:
        kpi("F1 score", f"{r['f1']:.3f}", "Balance of precision and recall", GOLD)

    left, right = st.columns(2)
    with left:
        fig = px.imshow(
            r["cm"],
            x=["Predicted: no default", "Predicted: default"],
            y=["Actual: no default", "Actual: default"],
            text_auto=True,
            color_continuous_scale=["#F1F5F9", TEAL],
        )
        fig.update_coloraxes(showscale=False)
        fig.update_traces(textfont_size=20)
        st.plotly_chart(style(fig, 380, "Confusion matrix"))
        st.caption("Bottom-left = real defaulters the model missed. Top-right = false alarms.")
    with right:
        fpr, tpr, ths = roc_curve(y_test, probs)
        idx = int(np.argmin(np.abs(ths - thr)))
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines", name="Model", line=dict(color=TEAL, width=3)))
        fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Random", line=dict(color=SLATE, dash="dash")))
        fig.add_trace(
            go.Scatter(x=[fpr[idx]], y=[tpr[idx]], mode="markers", name="Current threshold", marker=dict(size=13, color=CORAL))
        )
        fig.update_xaxes(title="False positive rate")
        fig.update_yaxes(title="True positive rate (recall)")
        st.plotly_chart(style(fig, 380, f"ROC curve (AUC = {M['auc']:.3f})"))

    grid = np.linspace(0.05, 0.90, 86)
    rows = [metrics_at(y_test, probs, t) for t in grid]
    fig = go.Figure()
    for key, color in [("accuracy", TEAL), ("precision", BLUE), ("recall", CORAL), ("f1", GOLD)]:
        fig.add_trace(go.Scatter(x=grid, y=[x[key] for x in rows], mode="lines", name=key.capitalize(), line=dict(color=color, width=3)))
    fig.add_vline(x=thr, line_dash="dash", line_color=NAVY)
    fig.update_xaxes(title="Decision threshold")
    fig.update_yaxes(title="Score", tickformat=".0%")
    st.plotly_chart(style(fig, 400, "The trade-off: accuracy vs recall"))
    callout(
        "Lowering the threshold finds more real defaulters (recall goes up) but accuracy falls, and can drop below the "
        "78% baseline. For a bank, <b>missing a defaulter costs more than a false alarm</b>, so the tuned threshold is a "
        "sensible choice even with lower accuracy."
    )

    coef = pd.DataFrame({"Feature": M["feat_names"], "Coefficient": M["coefs"]})
    coef = coef.reindex(coef["Coefficient"].abs().sort_values(ascending=False).index).head(14).iloc[::-1]
    fig = go.Figure(
        go.Bar(
            x=coef["Coefficient"],
            y=coef["Feature"],
            orientation="h",
            marker_color=[CORAL if v > 0 else BLUE for v in coef["Coefficient"]],
        )
    )
    fig.update_xaxes(title="Coefficient (positive = pushes toward default)")
    st.plotly_chart(style(fig, 460, "What the model learned: top 14 features"))

    with st.expander("Classification report at the current threshold"):
        rep = classification_report(y_test, r["pred"], target_names=["No default", "Default"], output_dict=True, zero_division=0)
        st.dataframe(pd.DataFrame(rep).T.round(3))


def page_predict(df, report, M):
    hero("Predict Risk", "Enter a client's profile and payment history to get a default probability.")
    thr = st.session_state["thr"]

    with st.form("client_form"):
        st.markdown("#### Profile")
        a, b, c, d, e = st.columns(5)
        limit = a.number_input("Credit limit", 10000, 1000000, 50000, 5000)
        age = b.number_input("Age", 21, 79, 35)
        sex = c.selectbox("Sex", list(SEX_MAP), index=1, format_func=SEX_MAP.get)
        edu = d.selectbox("Education", list(EDU_MAP), index=1, format_func=EDU_MAP.get)
        mar = e.selectbox("Marital status", list(MAR_MAP), index=0, format_func=MAR_MAP.get)

        st.markdown("#### Payment status (latest month first)")
        defaults_pay = [2, 2, 2, 1, 0, 0]
        pay = []
        cols = st.columns(6)
        for i, col in enumerate(cols):
            pay.append(col.selectbox(f"{MONTHS[i]} (PAY_{i + 1})", list(range(-2, 9)), index=defaults_pay[i] + 2, format_func=pay_label))

        st.markdown("#### Bill amounts")
        defaults_bill = [48000, 47000, 46000, 45000, 44000, 43000]
        bills = []
        cols = st.columns(6)
        for i, col in enumerate(cols):
            bills.append(col.number_input(f"{MONTHS[i]}", -200000, 1000000, defaults_bill[i], 1000, key=f"bill{i}"))

        st.markdown("#### Payments made")
        defaults_amt = [0, 0, 1500, 1500, 1500, 1500]
        paid = []
        cols = st.columns(6)
        for i, col in enumerate(cols):
            paid.append(col.number_input(f"{MONTHS[i]} ", 0, 1000000, defaults_amt[i], 500, key=f"paid{i}"))

        submitted = st.form_submit_button("Assess risk", type="primary")

    if not submitted:
        st.info("Fill in the form and press **Assess risk**. The example values describe a high-risk client.")
        return

    record = {"LIMIT_BAL": limit, "SEX": sex, "EDUCATION": edu, "MARRIAGE": mar, "AGE": age}
    for i in range(6):
        record[f"PAY_{i + 1}"] = pay[i]
        record[f"BILL_AMT{i + 1}"] = bills[i]
        record[f"PAY_AMT{i + 1}"] = paid[i]
    row = add_features(pd.DataFrame([record]))[M["columns"]]
    prob = float(M["model"].predict_proba(row)[0, 1])
    high = prob >= thr

    left, right = st.columns([1, 1])
    with left:
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=prob * 100,
                number=dict(suffix="%", font=dict(size=46, color=NAVY)),
                gauge=dict(
                    axis=dict(range=[0, 100]),
                    bar=dict(color=CORAL if high else TEAL),
                    steps=[dict(range=[0, thr * 100], color="#DCFCE7"), dict(range=[thr * 100, 100], color="#FEE2E2")],
                    threshold=dict(line=dict(color=NAVY, width=4), thickness=0.8, value=thr * 100),
                ),
                title=dict(text="Probability of default"),
            )
        )
        st.plotly_chart(style(fig, 330))
    with right:
        st.markdown("&nbsp;", unsafe_allow_html=True)
        if high:
            st.markdown(
                f'<div class="result-high">HIGH RISK: flag this client for review.<br>'
                f'<span style="font-weight:400">Probability {prob:.1%} is above the threshold {thr:.2f}.</span></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="result-low">LOWER RISK: no action needed.<br>'
                f'<span style="font-weight:400">Probability {prob:.1%} is below the threshold {thr:.2f}.</span></div>',
                unsafe_allow_html=True,
            )
        st.markdown("&nbsp;", unsafe_allow_html=True)
        avg = df["DEFAULT"].mean()
        callout(f"The average client in the data has a default rate of <b>{avg:.1%}</b>. This client is at <b>{prob:.1%}</b>.")

    # Why: contribution of each feature relative to an average client
    pre = M["model"].named_steps["preprocess"]
    xt = pre.transform(row)
    xt = xt.toarray() if hasattr(xt, "toarray") else np.asarray(xt)
    contrib = pd.Series(xt[0] * M["coefs"], index=M["feat_names"])
    top = contrib.reindex(contrib.abs().sort_values(ascending=False).head(10).index).iloc[::-1]
    fig = go.Figure(
        go.Bar(x=top.values, y=top.index, orientation="h", marker_color=[CORAL if v > 0 else BLUE for v in top.values])
    )
    fig.update_xaxes(title="Push toward default (red) or toward paying (blue)")
    st.plotly_chart(style(fig, 420, "Why this score? Top 10 factors for this client"))


# ----------------------------------------------------------------------------
# App entry
# ----------------------------------------------------------------------------
def main():
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [os.path.join(here, DATA_FILE), DATA_FILE]
    path = next((p for p in candidates if os.path.exists(p)), None)

    st.sidebar.markdown("## 💳 Credit Risk")
    if path is not None:
        raw = load_raw(path)
    else:
        up = st.sidebar.file_uploader("Upload UCI_Credit_Card.csv", type="csv")
        if up is None:
            hero("Credit Card Default Risk", "Upload the dataset to start.")
            st.info(f"Put **{DATA_FILE}** next to app.py, or upload it in the sidebar.")
            st.stop()
        raw = pd.read_csv(up)

    if not {"PAY_0", "default.payment.next.month", "LIMIT_BAL"}.issubset(raw.columns):
        st.error("This does not look like UCI_Credit_Card.csv (expected columns are missing).")
        st.stop()

    df, report = prepare(raw)
    M = train(df)

    if "thr" not in st.session_state:
        st.session_state["thr"] = M["best_t"]

    pages = {
        "📊 Overview": page_overview,
        "🧹 Data Quality": page_quality,
        "🔍 Exploration": page_explore,
        "🛠️ Feature Engineering": page_features,
        "🤖 Model Performance": page_model,
        "🎯 Predict Risk": page_predict,
    }
    choice = st.sidebar.radio("Navigation", list(pages), label_visibility="collapsed")

    st.sidebar.divider()
    st.sidebar.markdown("**Decision threshold**")
    st.sidebar.slider("Flag a client as risky above", 0.05, 0.90, step=0.01, key="thr", label_visibility="collapsed")
    b1, b2 = st.sidebar.columns(2)
    b1.button("Tuned", on_click=lambda: st.session_state.update(thr=M["best_t"]), help="Threshold tuned on training data")
    b2.button("Default 0.50", on_click=lambda: st.session_state.update(thr=0.50))
    st.sidebar.caption("Used by the Model Performance and Predict Risk pages.")
    st.sidebar.divider()
    st.sidebar.caption(
        "Educational project. Data: Taiwan credit card clients, 2005 (UCI). "
        "Not for real lending decisions."
    )

    pages[choice](df, report, M)


main()
