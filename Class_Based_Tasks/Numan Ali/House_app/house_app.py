import pandas as pd
import streamlit as st

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


# -------------------------
# PAGE SETTINGS
# -------------------------

st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏠"
)

st.title("🏠 House Price Predictor")
st.write("Enter house details to predict its price.")


# -------------------------
# DATA
# -------------------------

data = {
    "Rooms": [3,4,5,3,6,4,5,7,3,6,
              4,5,6,3,7,5,4,6,8,5],

    "Area_Marla": [5,7,10,6,12,8,9,15,5,11,
                   7,10,13,5,16,9,6,12,18,10],

    "Gas": [1,1,1,0,1,1,0,1,0,1,
            1,0,1,0,1,1,0,1,1,0],

    "Price": [45,65,100,50,125,75,85,160,40,115,
              70,95,135,45,175,90,60,125,200,100]
}

df = pd.DataFrame(data)


# -------------------------
# FEATURES & TARGET
# -------------------------

X = df[["Rooms", "Area_Marla", "Gas"]]

y = df["Price"]


# -------------------------
# TRAIN / TEST SPLIT
# -------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# -------------------------
# TRAIN MODEL
# -------------------------

model = LinearRegression()

model.fit(X_train, y_train)


# -------------------------
# USER INPUT
# -------------------------

rooms = st.number_input(
    "Number of Rooms",
    min_value=1,
    max_value=10,
    value=2
)

area = st.number_input(
    "Land Area (Marla)",
    min_value=2,
    max_value=20,
    value=3
)

gas_option = st.selectbox(
    "Gas Available?",
    ["Yes", "No"]
)


# -------------------------
# CONVERT GAS
# -------------------------

if gas_option == "Yes":
    gas = 1
else:
    gas = 0


# -------------------------
# PREDICT BUTTON
# -------------------------

if st.button("Predict Price"):

    new_house = pd.DataFrame({
        "Rooms": [rooms],
        "Area_Marla": [area],
        "Gas": [gas]
    })

    prediction = model.predict(new_house)

    st.success(
        f"Predicted House Price: {prediction[0]:.0f} Lakh"
    )