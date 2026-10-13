import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)

# ------------------------------------------------------------
# Page configuration
# ------------------------------------------------------------
st.set_page_config(
    page_title="Student Outcome ML Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------
# Styling
# ------------------------------------------------------------
st.markdown("""
<style>
    .main { padding-top: 1rem; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    .hero {
        padding: 1.5rem 1.8rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #111827, #1f2937);
        border: 1px solid #374151;
        margin-bottom: 1.2rem;
    }
    .hero h1 { margin: 0; font-size: 2.25rem; }
    .hero p { margin: .5rem 0 0; color: #cbd5e1; }
    .metric-card {
        padding: 1rem;
        border-radius: 14px;
        background: #111827;
        border: 1px solid #374151;
        text-align: center;
    }
    .metric-value { font-size: 1.65rem; font-weight: 700; }
    .metric-label { color: #94a3b8; font-size: .85rem; }
    div[data-testid="stMetric"] {
        background: #111827;
        border: 1px solid #374151;
        padding: 12px;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Constants
# ------------------------------------------------------------
DEFAULT_CATEGORICAL = [
    "Marital Status",
    "Application mode",
    "Course",
    "Previous qualification",
    "Nacionality",
    "Mother's qualification",
    "Father's qualification",
    "Mother's occupation",
    "Father's occupation",
]

RANDOM_STATE = 22

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
@st.cache_data
def load_data(uploaded_file):
    return pd.read_csv(uploaded_file)


def build_preprocessor(X):
    categorical_features = [
        c for c in DEFAULT_CATEGORICAL if c in X.columns
    ]

    # Treat any remaining object/category columns as categorical too.
    extra_categorical = X.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    categorical_features = list(dict.fromkeys(
        categorical_features + extra_categorical
    ))

    numeric_features = [
        c for c in X.columns if c not in categorical_features
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_features,
            ),
            ("numerical", StandardScaler(), numeric_features),
        ],
        remainder="drop",
    )

    return preprocessor, categorical_features, numeric_features


def make_pipeline(model, X):
    preprocessor, categorical_features, numeric_features = build_preprocessor(X)
    pipe = Pipeline([
        ("preprocessor", preprocessor),
        ("model", model),
    ])
    return pipe, categorical_features, numeric_features


@st.cache_resource
def train_models(X, y, test_size=0.20):
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    model_defs = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "K-Nearest Neighbors": KNeighborsClassifier(),
        "Decision Tree": DecisionTreeClassifier(random_state=RANDOM_STATE),
        "Random Forest": RandomForestClassifier(
            random_state=RANDOM_STATE,
            n_estimators=200,
            n_jobs=-1,
        ),
    }

    results = []
    trained = {}
    reports = {}

    for name, model in model_defs.items():
        pipe, _, _ = make_pipeline(model, X_train)
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)

        results.append({
            "Model": name,
            "Accuracy": accuracy_score(y_test, pred),
            "Precision (Macro)": precision_score(
                y_test, pred, average="macro", zero_division=0
            ),
            "Recall (Macro)": recall_score(
                y_test, pred, average="macro", zero_division=0
            ),
            "F1 (Macro)": f1_score(
                y_test, pred, average="macro", zero_division=0
            ),
        })

        trained[name] = pipe
        reports[name] = {
            "y_test": y_test,
            "pred": pred,
            "confusion_matrix": confusion_matrix(y_test, pred),
            "classification_report": classification_report(
                y_test, pred, output_dict=True, zero_division=0
            ),
        }

    return pd.DataFrame(results), trained, reports, X_train, X_test, y_train, y_test


@st.cache_resource
def tune_logistic_regression(X_train, y_train):
    pipe, _, _ = make_pipeline(
        LogisticRegression(max_iter=2000),
        X_train
    )

    param_grid = {
        "model__C": [0.01, 0.1, 1, 10, 100],
        "model__class_weight": [None, "balanced"],
    }

    grid = GridSearchCV(
        estimator=pipe,
        param_grid=param_grid,
        scoring="f1_macro",
        cv=5,
        n_jobs=-1,
        return_train_score=False,
    )
    grid.fit(X_train, y_train)

    return grid


# ------------------------------------------------------------
# Header
# ------------------------------------------------------------
st.markdown("""
<div class="hero">
    <h1>🎓 Student Outcome ML Dashboard</h1>
    <p>End-to-end data understanding, preprocessing, model comparison,
    hyperparameter tuning and prediction using scikit-learn.</p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuration")
    uploaded_file = st.file_uploader(
        "Upload student outcome CSV",
        type=["csv"],
        help="Upload the student_outcome.csv dataset."
    )

    test_size = st.slider(
        "Test set size",
        min_value=0.10,
        max_value=0.40,
        value=0.20,
        step=0.05,
    )

    st.divider()
    st.caption("Random state")
    st.code(str(RANDOM_STATE))

if uploaded_file is None:
    st.info("👈 Upload `student_outcome.csv` from the sidebar to start.")
    st.stop()

# ------------------------------------------------------------
# Load and validate
# ------------------------------------------------------------
try:
    df = load_data(uploaded_file)
except Exception as e:
    st.error(f"Could not read the CSV file: {e}")
    st.stop()

target_candidates = [c for c in df.columns if c.lower() == "target"]

with st.sidebar:
    target_col = st.selectbox(
        "Target column",
        options=df.columns.tolist(),
        index=df.columns.get_loc(target_candidates[0])
        if target_candidates else len(df.columns) - 1,
    )

X = df.drop(columns=[target_col])
y = df[target_col]

missing_count = int(df.isna().sum().sum())
duplicate_count = int(df.duplicated().sum())
class_count = int(y.nunique())

# ------------------------------------------------------------
# KPI row
# ------------------------------------------------------------
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Rows", f"{len(df):,}")
k2.metric("Features", f"{X.shape[1]:,}")
k3.metric("Classes", f"{class_count:,}")
k4.metric("Missing values", f"{missing_count:,}")
k5.metric("Duplicates", f"{duplicate_count:,}")

# ------------------------------------------------------------
# Tabs
# ------------------------------------------------------------
tabs = st.tabs([
    "📊 Data Understanding",
    "🔎 Exploratory Analysis",
    "🤖 Model Comparison",
    "🎯 Hyperparameter Tuning",
    "🧪 Prediction",
])

# ============================================================
# 1. Data Understanding
# ============================================================
with tabs[0]:
    st.subheader("Dataset Overview")

    c1, c2 = st.columns([1.25, 1])

    with c1:
        st.markdown("#### Data Preview")
        st.dataframe(df.head(10), use_container_width=True)

    with c2:
        st.markdown("#### Dataset Information")
        info_df = pd.DataFrame({
            "Metric": [
                "Rows",
                "Columns",
                "Target",
                "Target dtype",
                "Missing values",
                "Duplicate rows",
            ],
            "Value": [
                len(df),
                len(df.columns),
                target_col,
                str(y.dtype),
                missing_count,
                duplicate_count,
            ],
        })
        st.dataframe(info_df, hide_index=True, use_container_width=True)

    st.markdown("#### Data Types")
    dtype_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing": df.isna().sum().values,
        "Unique Values": [df[c].nunique(dropna=True) for c in df.columns],
    })
    st.dataframe(dtype_df, hide_index=True, use_container_width=True)

    st.markdown("#### Descriptive Statistics")
    st.dataframe(
        df.describe(include="all").transpose(),
        use_container_width=True,
    )

# ============================================================
# 2. Exploratory Analysis
# ============================================================
with tabs[1]:
    st.subheader("Exploratory Data Analysis")

    left, right = st.columns(2)

    with left:
        st.markdown("#### Target Distribution")
        target_counts = y.value_counts().reset_index()
        target_counts.columns = ["Target", "Count"]
        fig = px.bar(
            target_counts,
            x="Target",
            y="Count",
            text="Count",
            title="Student Outcome Distribution",
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("#### Target Percentage")
        target_pct = (
            y.value_counts(normalize=True)
            .mul(100)
            .round(2)
            .reset_index()
        )
        target_pct.columns = ["Target", "Percentage"]
        fig2 = px.pie(
            target_pct,
            names="Target",
            values="Percentage",
            hole=0.45,
            title="Target Class Share",
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("#### Numeric Feature Distribution")
    numeric_cols = X.select_dtypes(include=np.number).columns.tolist()

    if numeric_cols:
        selected_num = st.selectbox(
            "Select a numeric feature",
            numeric_cols,
            index=0,
        )
        hist = px.histogram(
            df,
            x=selected_num,
            color=target_col,
            marginal="box",
            title=f"{selected_num} by Student Outcome",
            barmode="overlay",
        )
        st.plotly_chart(hist, use_container_width=True)

    st.markdown("#### Correlation Heatmap")
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr()
        heat = px.imshow(
            corr,
            text_auto=False,
            aspect="auto",
            title="Numeric Feature Correlation",
        )
        st.plotly_chart(heat, use_container_width=True)

# ============================================================
# 3. Model Comparison
# ============================================================
with tabs[2]:
    st.subheader("Machine Learning Model Comparison")

    with st.spinner("Training models..."):
        (
            results_df,
            trained_models,
            reports,
            X_train,
            X_test,
            y_train,
            y_test,
        ) = train_models(X, y, test_size)

    display_df = results_df.copy()
    metric_cols = [
        "Accuracy",
        "Precision (Macro)",
        "Recall (Macro)",
        "F1 (Macro)",
    ]
    display_df[metric_cols] = display_df[metric_cols].round(4)

    st.markdown("#### Performance Summary")
    st.dataframe(
        display_df.sort_values("F1 (Macro)", ascending=False),
        hide_index=True,
        use_container_width=True,
    )

    chart_df = results_df.melt(
        id_vars="Model",
        value_vars=metric_cols,
        var_name="Metric",
        value_name="Score",
    )
    fig = px.bar(
        chart_df,
        x="Model",
        y="Score",
        color="Metric",
        barmode="group",
        range_y=[0, 1],
        title="Model Performance",
    )
    st.plotly_chart(fig, use_container_width=True)

    best_model_name = results_df.loc[
        results_df["F1 (Macro)"].idxmax(), "Model"
    ]
    st.success(
        f"Best model by Macro F1 on the held-out test set: **{best_model_name}**"
    )

    st.markdown("#### Detailed Evaluation")
    selected_model = st.selectbox(
        "Select a model",
        list(trained_models.keys()),
        index=list(trained_models.keys()).index(best_model_name),
    )

    report_data = reports[selected_model]
    cm = report_data["confusion_matrix"]
    labels = trained_models[selected_model].classes_

    cm_fig = px.imshow(
        cm,
        x=list(labels),
        y=list(labels),
        text_auto=True,
        aspect="auto",
        labels={
            "x": "Predicted",
            "y": "Actual",
            "color": "Count",
        },
        title=f"Confusion Matrix — {selected_model}",
    )
    cm_fig.update_xaxes(side="bottom")
    st.plotly_chart(cm_fig, use_container_width=True)

    report_df = pd.DataFrame(report_data["classification_report"]).transpose()
    st.dataframe(
        report_df.round(4),
        use_container_width=True,
    )

# ============================================================
# 4. Hyperparameter Tuning
# ============================================================
with tabs[3]:
    st.subheader("Logistic Regression — GridSearchCV")

    (
        results_df,
        trained_models,
        reports,
        X_train,
        X_test,
        y_train,
        y_test,
    ) = train_models(X, y, test_size)

    st.write(
        "The tuning objective is **Macro F1**, using 5-fold cross-validation."
    )

    with st.spinner("Running GridSearchCV..."):
        grid = tune_logistic_regression(X_train, y_train)

    c1, c2 = st.columns(2)
    c1.metric("Best CV Macro F1", f"{grid.best_score_:.4f}")
    c2.metric("Best Parameters", str(grid.best_params_))

    tuned_pred = grid.best_estimator_.predict(X_test)

    tuned_metrics = pd.DataFrame([{
        "Accuracy": accuracy_score(y_test, tuned_pred),
        "Precision (Macro)": precision_score(
            y_test, tuned_pred, average="macro", zero_division=0
        ),
        "Recall (Macro)": recall_score(
            y_test, tuned_pred, average="macro", zero_division=0
        ),
        "F1 (Macro)": f1_score(
            y_test, tuned_pred, average="macro", zero_division=0
        ),
    }]).T
    tuned_metrics.columns = ["Test Score"]

    st.markdown("#### Tuned Model — Test Performance")
    st.dataframe(
        tuned_metrics.round(4),
        use_container_width=True,
    )

    st.markdown("#### Grid Search Results")
    cv_results = pd.DataFrame(grid.cv_results_)[[
        "param_model__C",
        "param_model__class_weight",
        "mean_test_score",
        "std_test_score",
        "rank_test_score",
    ]].sort_values("rank_test_score")

    st.dataframe(
        cv_results.round(5),
        hide_index=True,
        use_container_width=True,
    )

# ============================================================
# 5. Prediction
# ============================================================
with tabs[4]:
    st.subheader("Predict Student Outcome")

    st.caption(
        "Enter the student's feature values. The model uses the same "
        "preprocessing pipeline as training."
    )

    (
        results_df,
        trained_models,
        reports,
        X_train,
        X_test,
        y_train,
        y_test,
    ) = train_models(X, y, test_size)

    best_model_name = results_df.loc[
        results_df["F1 (Macro)"].idxmax(), "Model"
    ]

    model_choice = st.selectbox(
        "Prediction model",
        list(trained_models.keys()),
        index=list(trained_models.keys()).index(best_model_name),
    )

    prediction_model = trained_models[model_choice]

    categorical_features = [
        c for c in DEFAULT_CATEGORICAL if c in X.columns
    ]
    categorical_features += [
        c for c in X.select_dtypes(
            include=["object", "category", "bool"]
        ).columns
        if c not in categorical_features
    ]
    categorical_features = list(dict.fromkeys(categorical_features))

    numeric_features = [
        c for c in X.columns if c not in categorical_features
    ]

    input_data = {}

    with st.form("prediction_form"):
        cols = st.columns(3)

        for i, col in enumerate(categorical_features):
            with cols[i % 3]:
                values = X[col].dropna().unique().tolist()
                values = sorted(values, key=lambda v: str(v))
                if values:
                    input_data[col] = st.selectbox(
                        col,
                        values,
                        key=f"cat_{col}",
                    )

        for i, col in enumerate(numeric_features):
            with cols[i % 3]:
                series = pd.to_numeric(X[col], errors="coerce")
                median = float(series.median()) if not series.dropna().empty else 0.0
                minimum = float(series.min()) if not series.dropna().empty else 0.0
                maximum = float(series.max()) if not series.dropna().empty else 1.0

                if minimum == maximum:
                    input_data[col] = st.number_input(
                        col,
                        value=median,
                        key=f"num_{col}",
                    )
                else:
                    input_data[col] = st.number_input(
                        col,
                        min_value=minimum,
                        max_value=maximum,
                        value=min(max(median, minimum), maximum),
                        key=f"num_{col}",
                    )

        submitted = st.form_submit_button(
            "🚀 Predict Student Outcome",
            use_container_width=True,
        )

    if submitted:
        input_df = pd.DataFrame([input_data])

        try:
            prediction = prediction_model.predict(input_df)[0]

            st.success(f"### Predicted Outcome: **{prediction}**")

            if hasattr(prediction_model, "predict_proba"):
                probabilities = prediction_model.predict_proba(input_df)[0]
                classes = prediction_model.classes_

                probability_df = pd.DataFrame({
                    "Outcome": classes,
                    "Probability": probabilities,
                }).sort_values("Probability", ascending=False)

                fig = px.bar(
                    probability_df,
                    x="Outcome",
                    y="Probability",
                    text=probability_df["Probability"].map(
                        lambda x: f"{x:.1%}"
                    ),
                    range_y=[0, 1],
                    title="Prediction Probabilities",
                )
                st.plotly_chart(fig, use_container_width=True)

                st.dataframe(
                    probability_df.assign(
                        Probability=probability_df["Probability"].map(
                            lambda x: f"{x:.2%}"
                        )
                    ),
                    hide_index=True,
                    use_container_width=True,
                )

        except Exception as e:
            st.error(f"Prediction failed: {e}")

# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------
st.divider()
st.caption(
    "Student Outcome ML Dashboard • scikit-learn Pipeline • "
    "Random State = 22"
)
