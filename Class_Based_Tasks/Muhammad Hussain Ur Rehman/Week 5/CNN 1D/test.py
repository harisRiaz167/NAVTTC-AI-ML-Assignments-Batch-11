import os
import numpy as np
import streamlit as st
import keras

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="CNN Sentiment AI",
    page_icon="💬",
    layout="wide"
)

MODEL_PATH = "text_cnn.keras"


# ==========================================
# CUSTOM UI DESIGN
# ==========================================

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #101827 0%, #182337 100%);
        color: #F1F5F9;
    }

    .main .block-container {
        max-width: 1050px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    .hero {
        text-align: center;
        padding: 28px 10px 24px 10px;
    }

    .hero-badge {
        display: inline-block;
        padding: 7px 15px;
        border: 1px solid #385477;
        border-radius: 30px;
        background: #1D3048;
        color: #93C5FD;
        font-size: 13px;
        letter-spacing: 1px;
        margin-bottom: 15px;
    }

    .hero h1 {
        color: #FFFFFF;
        font-size: 42px;
        font-weight: 800;
        margin: 0;
    }

    .hero p {
        color: #A9B9CC;
        font-size: 17px;
        margin-top: 12px;
    }

    .section-title {
        color: #E2E8F0;
        font-size: 21px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .info-card {
        background: #1B293D;
        border: 1px solid #32445D;
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 16px;
    }

    .result-positive {
        background: linear-gradient(135deg, #123D35, #174D43);
        border: 1px solid #2D8B70;
        border-radius: 18px;
        padding: 24px;
        text-align: center;
    }

    .result-negative {
        background: linear-gradient(135deg, #48232C, #572833);
        border: 1px solid #A34B5B;
        border-radius: 18px;
        padding: 24px;
        text-align: center;
    }

    .result-label {
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #CBD5E1;
    }

    .result-value {
        font-size: 30px;
        font-weight: 800;
        color: #FFFFFF;
        margin-top: 8px;
    }

    .result-subtitle {
        color: #D1DCE8;
        font-size: 14px;
        margin-top: 8px;
    }

    .footer {
        color: #91A2B8;
        text-align: center;
        font-size: 13px;
        margin-top: 35px;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 3rem;
        font-weight: 700;
    }

    div[data-testid="stTextArea"] textarea {
        background-color: #111D2E;
        color: #F8FAFC;
        border: 1px solid #40536C;
        border-radius: 12px;
    }

    div[data-testid="stMetric"] {
        background: #1B293D;
        padding: 15px;
        border: 1px solid #32445D;
        border-radius: 12px;
    }

    hr {
        border-color: #34445A;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# LOAD TRAINED MODEL
# ==========================================

@st.cache_resource
def load_model():
    return keras.models.load_model(MODEL_PATH)


if not os.path.exists(MODEL_PATH):
    st.error(
        f"Model not found: {MODEL_PATH}. "
        "Place your trained model in the same folder as app.py."
    )
    st.stop()

try:
    model = load_model()
except Exception as error:
    st.error(f"Could not load the model: {error}")
    st.stop()


# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="hero">
    <div class="hero-badge">DEEP LEARNING PROJECT</div>
    <h1>💬 CNN Sentiment Analyzer</h1>
    <p>
        Understand the sentiment behind a review using
        your trained 1D Convolutional Neural Network.
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()


# ==========================================
# REVIEW INPUT
# ==========================================

left, right = st.columns([1.2, 0.8], gap="large")

with left:
    st.markdown(
        '<div class="section-title">✍️ Enter Your Review</div>',
        unsafe_allow_html=True
    )

    with st.form("sentiment_form"):
        review = st.text_area(
            "Review text",
            placeholder=(
                "Example: The product looked promising, "
                "but its performance was disappointing..."
            ),
            height=180,
            label_visibility="collapsed"
        )

        analyze = st.form_submit_button(
            "🔍 Analyze Sentiment",
            type="primary",
            use_container_width=True
        )

    st.caption(
        "Enter a short or long review, then click Analyze Sentiment."
    )


# ==========================================
# MODEL INFORMATION
# ==========================================

with right:
    st.markdown("""
    <div class="info-card">
        <div class="section-title">🧠 Model Information</div>
        <p>Architecture: <b>1D CNN</b></p>
        <p>Task: <b>Binary Sentiment Classification</b></p>
        <p>Output: <b>Positive / Negative</b></p>
        <p>Prediction threshold: <b>0.50</b></p>
        <hr>
        <p style="color:#A9B9CC;font-size:14px;">
            The trained model processes the raw review text
            using its saved TextVectorization layer and learned weights.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# PREDICTION
# ==========================================

if analyze:

    if not review.strip():
        st.warning("Please enter a review before analyzing.")

    else:
        with st.spinner("Analyzing review..."):

            text = np.array([review.strip()], dtype=object)

            probability = float(
                model.predict(text, verbose=0)[0][0]
            )

        negative_probability = 1.0 - probability

        if probability >= 0.5:
            label = "Positive Review"
            result_class = "result-positive"
            icon = "✅"
        else:
            label = "Negative Review"
            result_class = "result-negative"
            icon = "⚠️"

        st.markdown("---")
        st.markdown(
            '<div class="section-title">📊 Analysis Results</div>',
            unsafe_allow_html=True
        )

        st.markdown(f"""
        <div class="{result_class}">
            <div class="result-label">Predicted Sentiment</div>
            <div class="result-value">{icon} {label}</div>
            <div class="result-subtitle">
                Prediction generated by your trained CNN model
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                label="🟢 Positive Probability",
                value=f"{probability * 100:.2f}%"
            )
            st.progress(
                probability,
                text="Positive score"
            )

        with col2:
            st.metric(
                label="🔴 Negative Probability",
                value=f"{negative_probability * 100:.2f}%"
            )
            st.progress(
                negative_probability,
                text="Negative score"
            )

        with st.expander("View submitted review"):
            st.write(review)

        st.caption(
            "Note: These are model output scores, not necessarily "
            "calibrated probabilities of being correct."
        )


# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div class="footer">
    Built with Streamlit, TensorFlow & Keras
    <br>
    Powered by a custom-trained 1D CNN
</div>
""", unsafe_allow_html=True)