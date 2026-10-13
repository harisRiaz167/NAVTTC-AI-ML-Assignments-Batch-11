import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="ML Studio",
    page_icon="🤖",
    layout="wide",
)

@st.cache_data
def load_data():
    df = pd.read_csv("daraz.csv")
    df.columns = ["id","url","product_name","price","sold","rating","reviews","province","discount","coins"]

    price = df["price"].astype(str)
    clean_rs = price.str.replace("Rs.", "", regex=False)
    clean_comma = clean_rs.str.replace(",", "", regex=False)
    clean_space = clean_comma.str.strip()
    change_price_to_num = pd.to_numeric(clean_space,errors='coerce')
    df["price"] = change_price_to_num
    df["price"] = df["price"].fillna(df["price"].median())


    def convert_sold(value):
        value = str(value).lower().replace("sold", "").strip()
        if value.endswith("k"):
            value = value[:-1]
            value = float(value) * 1000
            return value
        elif value.endswith("m"):
            value = value[:-1]
            value = float(value) * 1_000_000 
            return value
        else:
            try:
                return float(value)
            except ValueError:
                return np.nan

    df["sold"] = df["sold"].apply(convert_sold)
    df["sold"] = df["sold"].fillna(df["sold"].median())

    df["rating"] = pd.to_numeric(df["rating"],errors="coerce")
    df["rating"] = df["rating"].fillna(df["rating"].median())
    df["reviews"] = pd.to_numeric(df["reviews"],errors="coerce")

    df["discount"] = df["discount"].fillna(0)
    discount = df["discount"].astype(str)
    remove_off = discount.str.replace("% Off", "", regex=False)   
    remove_percent = remove_off.str.replace("%", "", regex=False) 
    remove_space =  remove_percent.str.strip()   
    change_discount_to_num = pd.to_numeric(remove_space,errors="coerce")
    df["discount"] = change_discount_to_num

    df["coins"] = df["coins"].fillna(0)
    coins = df["coins"].astype(str)
    extract_number_str = coins.str.extract(r"(\d+\.?\d*)")
    extract_column = extract_number_str[0]
    coins_to_number = pd.to_numeric(extract_column, errors="coerce")
    df["coins"] = coins_to_number

    return df
df = load_data()

# My Nav
st.html("""
<style>
.custom-navbar {
    height: 64px;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 0 20px;
    box-sizing: border-box;

    background: #111827;
    border: 1px solid #263244;
    border-radius: 14px;

    margin-bottom: 20px;
    margin-top: -35px;
}
.navbar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
}
.logo {
    width: 38px;
    height: 38px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: linear-gradient(
        135deg,
        #6366f1,
        #8b5cf6
    );

    border-radius: 10px;
    font-size: 20px;
}
.brand-name {
    color: white;
    font-size: 17px;
    font-weight: 700;
}
.brand-subtitle {
    color: #94a3b8;
    font-size: 10px;
}
.navbar-links {
    display: flex;
    align-items: center;
    gap: 5px;
}
.nav-link {
    color: #94a3b8;
    text-decoration: none;

    padding: 9px 14px;
    border-radius: 8px;

    font-size: 13px;
}
.nav-link:hover {
    color: white;
    background: #1e293b;
}
.nav-link.active {
    color: white;
    background: #312e81;
}
.navbar-right {
    display: flex;
    align-items: center;
    gap: 12px;
}
.online {
    display: flex;
    align-items: center;
    gap: 6px;

    color: #94a3b8;
    font-size: 12px;
}
.online-dot {
    width: 7px;
    height: 7px;

    border-radius: 50%;
    background: #22c55e;

    box-shadow: 0 0 8px #22c55e;
}
.avatar {
    width: 34px;
    height: 34px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 50%;

    background: #334155;
    color: white;

    font-size: 12px;
    font-weight: 600;
}
</style>
<div class="custom-navbar">
    <div class="navbar-brand">
        <div class="logo">
            🤖
        </div>
        <div>
            <div class="brand-name">
                ML Studio
            </div>
            <div class="brand-subtitle">
                Intelligent Analytics
            </div>
        </div>
    </div>
    <div class="navbar-links">
        <a class="nav-link active" href="#">
            Dashboard
        </a>
        <a class="nav-link" href="#">
            Predictions
        </a>
        <a class="nav-link" href="#">
            Models
        </a>
        <a class="nav-link" href="#">
            Analytics
        </a>
    </div>
    <div class="navbar-right">
        <div class="online">
            <div class="online-dot"></div>
            Online
        </div>
        <div class="avatar">
            MH
        </div>
    </div>
</div>
""")

with st.sidebar:

    st.markdown("ML Studio")
    st.caption("Machine Learning Workspace")
    st.divider()
    st.markdown("Filters")

    search = st.text_input("Search products",placeholder="Search product name...",key="search")

    provinces = df["province"].dropna()
    provinces = provinces.unique()
    provinces = sorted(provinces)
    selected_provinces = st.multiselect("Province",provinces,default=['Punjab'],key="province")

    min_price = int(df["price"].min())
    max_price = int(df["price"].max())

    price_range = st.slider("Price range",min_value=min_price,max_value=max_price,value=(min_price, max_price),key="price")

    rating_range = st.slider("Rating",min_value=0.0,max_value=5.0,value=(0.0, 5.0),step=0.1,key="rating")

    min_sold = df["sold"].min()
    max_sold = df["sold"].max()
    sold_range = st.slider("Products sold",min_value=min_sold,max_value=max_sold,value=(min_sold,max_sold),key="sold")

    min_Review = df["reviews"].min()
    max_Review = df["reviews"].max()
    review_range = st.slider("Reviews",min_value=min_Review,max_value=max_Review,value=(min_Review,max_Review),key="reviews")
   
    discount_range = st.slider("Discount %",min_value=0,max_value=100,value=(0, 100),key="discount")

    def reset_filters():
        st.session_state.search = ""
        st.session_state.province = ["Punjab"]
        st.session_state.price = (min_price, max_price)
        st.session_state.rating = (0.0, 5.0)
        st.session_state.sold = (min_sold, max_sold)
        st.session_state.reviews = (min_Review, max_Review)
        st.session_state.discount = (0, 100)

    st.button("Reset Filters",use_container_width=True,on_click=reset_filters)

# FILTERS
copy_df = df.copy()

if search:
    product_names = copy_df["product_name"]
    matches = product_names.str.contains(search,case=False,na=False)
    copy_df = copy_df[matches]

copy_df = copy_df[copy_df["province"].isin(selected_provinces)]

copy_df = copy_df[copy_df["price"].between(price_range[0],price_range[1])]

copy_df = copy_df[copy_df["rating"].between(rating_range[0],rating_range[1])]

copy_df = copy_df[copy_df["sold"].between(sold_range[0],sold_range[1])]

copy_df = copy_df[copy_df["reviews"].between(review_range[0],review_range[1])]

copy_df = copy_df[copy_df["discount"].between(discount_range[0],discount_range[1])]

# main page header
st.title("📊 E-Commerce Analytics")
st.caption("Interactive analysis of Daraz TOYS dataset")

if not copy_df.empty:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Products",f"{len(copy_df)}") 

    avg_price = copy_df['price'].mean()
    col2.metric("Average Price",f"Rs. {avg_price:.2f}")

    avg_rating = copy_df['rating'].mean()
    col3.metric("Average Rating",f"{avg_rating:.2f}")

    t_sold = copy_df['sold'].sum()
    col4.metric("Total Sold",f"{t_sold}")
else:       
    st.warning("No products matched!")
    st.stop()

st.divider()

col1, col2 = st.columns(2)
# price dist
with col1:

    price_histo = px.histogram(copy_df,x="price",nbins=30,title="Price Distribution",labels={"price": "Price (Rs.)"},marginal="box")

    st.plotly_chart(price_histo,use_container_width=True)

# ratings dist
with col2:

    chart_rating = px.histogram(copy_df,x="rating",nbins=20,title="Rating Distribution",labels={"rating": "Rating",},marginal="box")

    st.plotly_chart(chart_rating,use_container_width=True)

# sales by province

province_sales = copy_df.groupby("province", as_index=False)["sold"].sum().sort_values("sold", ascending=False)

chart_prov = px.bar(province_sales,x="province",y="sold",title="Sales by Province",labels={"province": "Province","sold": "Products Sold"})

st.plotly_chart(chart_prov,use_container_width=True)

# price vs sales

fig_sales = px.scatter(copy_df,x="price",y="sold",size="reviews",color="rating",title="Price vs Sales",labels={"price": "Price","sold": "Products Sold"})

st.plotly_chart(fig_sales,use_container_width=True)

# top products
st.header("Top 10 Products by Sales")
top_products = copy_df.sort_values("sold", ascending=False).head(10).copy()
top_products["short_name"] = top_products["product_name"].str[:20] + "..."
tops = top_products.sort_values("sold")
top_prods = px.bar(tops,x="sold",y="short_name",orientation="h",labels={"sold": "Products Sold","short_name": "Product"})
st.plotly_chart(top_prods,use_container_width=True)

# table
st.header("Filtered Products")

display_columns = [
    "url",
    "product_name",
    "price",
    "sold",
    "rating",
    "reviews",
    "province",
    "discount",
    "coins"
]

df = st.dataframe(copy_df[display_columns].sort_values("sold", ascending=False),use_container_width=True,height=450)
