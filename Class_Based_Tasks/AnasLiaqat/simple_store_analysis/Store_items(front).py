import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(
    page_title="Sales ML Dashboard",
    page_icon="📊",
    layout="wide"
)

df = pd.read_csv("sampledata1.csv")
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }

    h1 {
        font-size: 28px !important;
        margin-bottom: 5px;
    }

    h2 {
        font-size: 20px !important;
    }

    h3 {
        font-size: 15px !important;
    }

    div[data-testid="stMetric"] {
        padding: 8px;
    }

    .stPlotlyChart {
        margin-top: -10px;
    }
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
with col1:
    st.title("Super Store Sales Dashboard")

with col2:
    st.write("Dashboard")

with col3:
    st.write(" Analytics")

with col4:
    st.write(" ML")

with col5:
    st.write(" About")

st.sidebar.title("Filters")

regions = st.sidebar.multiselect(
    "Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

categories = st.sidebar.multiselect(
    "Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

segments = st.sidebar.multiselect(
    "Segment",
    df["Segment"].unique(),
    default=df["Segment"].unique()
)

ship_modes = st.sidebar.multiselect(
    "Ship Mode",
    df["Ship Mode"].unique(),
    default=df["Ship Mode"].unique()
)
filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories)) &
    (df["Segment"].isin(segments)) &
    (df["Ship Mode"].isin(ship_modes))
]
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Sales", f"${filtered_df['Sales'].sum():,.0f}")

with col2:
    st.metric("Profit", f"${filtered_df['Profit'].sum():,.0f}")

with col3:
    st.metric("Quantity", f"{filtered_df['Quantity'].sum():,.0f}")

with col4:
    st.metric("Orders", f"{len(filtered_df):,}")

col1, col2, col3 = st.columns(3)

with col1:
    profit = filtered_df[
        filtered_df["Profit"] > 0
    ]["Profit"].sum()

    loss = abs(
        filtered_df[
            filtered_df["Profit"] < 0
        ]["Profit"].sum()
    )

    data = pd.DataFrame({
        "Type": ["Profit", "Loss"],
        "Amount": [profit, loss]
    })

    fig = px.bar(
        data,
        x="Type",
        y="Amount",
        title="Profit vs Loss"
    )

    fig.update_layout(
        height=250,
        margin=dict(l=10, r=10, t=40, b=10)
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )
with col2:

    data = filtered_df.groupby(
        "Category"
    )[["Sales", "Discount"]].sum().reset_index()

    fig = px.bar(
        data,
        x="Category",
        y=["Sales", "Discount"],
        barmode="group",
        title="Sales vs Discount"
    )

    fig.update_layout(
        height=250,
        margin=dict(l=10, r=10, t=40, b=10)
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

with col3:

    avg_sale = filtered_df.groupby(
        "Category"
    )["Sales"].mean()

    avg_quantity = filtered_df.groupby(
        "Category"
    )["Quantity"].mean()

    data = pd.DataFrame({
        "Category": avg_sale.index,
        "Average Sale": avg_sale.values,
        "Average Quantity": avg_quantity.values
    })

    fig = px.bar(
        data,
        x="Category",
        y=["Average Sale", "Average Quantity"],
        barmode="group",
        title="Average Sale vs Quantity"
    )

    fig.update_layout(
        height=250,
        margin=dict(l=10, r=10, t=40, b=10)
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

col1, col2, col3 = st.columns(3)

with col1:
    data = filtered_df[
        "Segment"
    ].value_counts().reset_index()

    data.columns = ["Segment", "Count"]

    fig = px.pie(
        data,
        names="Segment",
        values="Count",
        title="Customer Segment",
        hole=0.35
    )

    fig.update_layout(
        height=250,
        margin=dict(l=10, r=10, t=40, b=10)
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

with col2:

    data = filtered_df[
        "Ship Mode"
    ].value_counts().reset_index()

    data.columns = ["Ship Mode", "Count"]

    fig = px.pie(
        data,
        names="Ship Mode",
        values="Count",
        title="Ship Modes",
        hole=0.35
    )

    fig.update_layout(
        height=250,
        margin=dict(l=10, r=10, t=40, b=10)
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

with col3:

    data = pd.DataFrame({
        "Type": ["Profit", "Loss"],
        "Amount": [profit, loss]
    })

    fig = px.pie(
        data,
        names="Type",
        values="Amount",
        title="Profit vs Loss",
        hole=0.35
    )

    fig.update_layout(
        height=250,
        margin=dict(l=10, r=10, t=40, b=10)
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )