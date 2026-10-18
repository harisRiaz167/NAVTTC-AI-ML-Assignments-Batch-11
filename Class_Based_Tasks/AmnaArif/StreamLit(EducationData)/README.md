# Out-of-School Risk Dashboard

A Streamlit dashboard (maroon and off-white theme) for the out-of-school prediction project.

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

The browser opens at http://localhost:8501.

## Files

| File | Purpose |
|---|---|
| `app.py` | The dashboard |
| `.streamlit/config.toml` | Maroon and off-white theme colours (keep this folder next to `app.py`) |
| `out_of_school_model.joblib` | Trained scikit-learn pipeline (from notebook section 15) |
| `model_metadata.joblib` | Model name, tuned settings, cross-validation scores |
| `out_of_school_clean.csv` | Cleaned data used for the charts |
| `requirements.txt` | Python libraries |

## If the model will not load

The `.joblib` files were saved with scikit-learn 1.9.1. If your scikit-learn is a different version, the app shows
a message instead of crashing. Fix it by running the notebook (`out_of_school_ml_notebook.ipynb`) through
section 15 on your own computer, then copy the three new files (`out_of_school_model.joblib`,
`model_metadata.joblib`, `out_of_school_clean.csv`) into this folder and restart the app.

## Tabs

1. **Overview**: headline KPI cards, province, distance, group gaps, income and age charts
2. **Risk factors**: out-of-school rate by distance, income, parents' education, province and location
3. **Model performance**: model comparison, adjustable threshold, confusion matrix, ROC, precision-recall
4. **Feature importance**: what the model relies on and which way each factor pushes the risk
5. **Predict a child**: enter one child's details and get a risk estimate with an explanation
6. **Data & about**: project summary, missing values, filtered data table and CSV download

The sidebar filters (province, location, gender, age) apply to the Overview, Risk factors and Data tabs.
The data is synthetic, so the numbers show how the method works and do not describe a real country.
