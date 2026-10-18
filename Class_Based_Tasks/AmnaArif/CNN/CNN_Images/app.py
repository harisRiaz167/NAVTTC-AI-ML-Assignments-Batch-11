import json
import os

import numpy as np
import streamlit as st
from PIL import Image, ImageOps

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
MODEL_PATH = "cat_dog_horse_model.keras"
CLASSES_PATH = "class_names.json"
IMG_SIZE = 128
LOW_CONFIDENCE = 0.60

OFFWHITE = "#FAF6EF"
OFFWHITE_DARK = "#F0E9DD"
PURPLE = "#3D1A5B"
PURPLE_MID = "#6B3FA0"
PURPLE_LIGHT = "#C9B5DE"

st.set_page_config(
    page_title="Animal Image Classifier",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {OFFWHITE};
        color: {PURPLE};
    }}
    header[data-testid="stHeader"] {{
        background: transparent;
    }}
    .block-container {{
        padding-top: 2rem;
        max-width: 1150px;
    }}

    h1, h2, h3, h4, p, label, span, li {{
        color: {PURPLE};
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: {PURPLE};
    }}
    section[data-testid="stSidebar"] * {{
        color: {OFFWHITE} !important;
    }}
    section[data-testid="stSidebar"] hr {{
        border-color: {PURPLE_MID};
    }}

    /* Hero banner */
    .hero {{
        background: {PURPLE};
        padding: 2rem 2.2rem;
        border-radius: 14px;
        margin-bottom: 1.8rem;
    }}
    .hero h1 {{
        color: {OFFWHITE};
        font-size: 2.1rem;
        margin: 0 0 0.35rem 0;
        letter-spacing: 0.3px;
    }}
    .hero p {{
        color: {PURPLE_LIGHT};
        margin: 0;
        font-size: 1.02rem;
    }}

    /* Cards */
    .card {{
        background: {OFFWHITE_DARK};
        border: 1px solid {PURPLE_LIGHT};
        border-radius: 14px;
        padding: 1.4rem 1.5rem;
    }}
    .card-title {{
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 1.4px;
        color: {PURPLE_MID};
        margin-bottom: 0.6rem;
        font-weight: 600;
    }}

    /* Prediction result */
    .result-label {{
        font-size: 3rem;
        font-weight: 700;
        color: {PURPLE};
        line-height: 1.1;
        margin: 0.2rem 0 0.3rem 0;
        text-transform: capitalize;
    }}
    .result-conf {{
        font-size: 1.1rem;
        color: {PURPLE_MID};
        margin-bottom: 1.2rem;
    }}

    /* Probability bars */
    .bar-row {{
        margin-bottom: 0.9rem;
    }}
    .bar-head {{
        display: flex;
        justify-content: space-between;
        font-size: 0.95rem;
        margin-bottom: 0.3rem;
        text-transform: capitalize;
        color: {PURPLE};
    }}
    .bar-track {{
        background: {OFFWHITE};
        border: 1px solid {PURPLE_LIGHT};
        border-radius: 8px;
        height: 14px;
        overflow: hidden;
    }}
    .bar-fill {{
        height: 100%;
        border-radius: 8px;
    }}

    /* File uploader */
    div[data-testid="stFileUploader"] section {{
        background-color: {OFFWHITE_DARK};
        border: 2px dashed {PURPLE_MID};
        border-radius: 14px;
    }}
    div[data-testid="stFileUploader"] section * {{
        color: {PURPLE} !important;
    }}
    div[data-testid="stFileUploader"] button {{
        background-color: {PURPLE};
        color: {OFFWHITE} !important;
        border: none;
        border-radius: 8px;
    }}
    div[data-testid="stFileUploader"] button * {{
        color: {OFFWHITE} !important;
    }}
    div[data-testid="stFileUploader"] button:hover {{
        background-color: {PURPLE_MID};
    }}

    /* Images */
    div[data-testid="stImage"] img {{
        border-radius: 12px;
        border: 1px solid {PURPLE_LIGHT};
    }}

    /* Notices */
    .note {{
        background: {OFFWHITE};
        border-left: 4px solid {PURPLE};
        padding: 0.8rem 1rem;
        border-radius: 6px;
        font-size: 0.95rem;
        margin-top: 0.6rem;
        color: {PURPLE};
    }}
    .placeholder {{
        text-align: center;
        padding: 3.5rem 1rem;
        color: {PURPLE_MID};
    }}
    .placeholder h3 {{
        color: {PURPLE};
        margin-bottom: 0.4rem;
    }}

    footer {{visibility: hidden;}}
    #MainMenu {{visibility: hidden;}}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Model loading and prediction
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner="Loading model")
def load_assets():
    import tensorflow as tf

    model = tf.keras.models.load_model(MODEL_PATH)
    with open(CLASSES_PATH, "r") as f:
        class_names = json.load(f)
    return model, class_names


def preprocess(pil_img):
    pil_img = ImageOps.exif_transpose(pil_img).convert("RGB")
    pil_img = pil_img.resize((IMG_SIZE, IMG_SIZE))
    arr = np.asarray(pil_img, dtype="float32")
    return np.expand_dims(arr, axis=0)


def predict(model, class_names, pil_img):
    probs = model.predict(preprocess(pil_img), verbose=0)[0]
    order = np.argsort(probs)[::-1]
    return [(class_names[i], float(probs[i])) for i in order]


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### About this app")
    st.write(
        "A convolutional neural network trained to recognise three "
        "categories of animal: cat, dog and horse."
    )
    st.markdown("---")
    st.markdown("### How to use")
    st.write("1. Upload a clear photo of a single animal.")
    st.write("2. Wait a moment for the model to run.")
    st.write("3. Read the predicted category and confidence scores.")
    st.markdown("---")
    st.markdown("### Model details")
    st.write(f"Input size: {IMG_SIZE} x {IMG_SIZE} pixels")
    st.write("Classes: cat, dog, horse")
    st.write("Accepted files: JPG, JPEG, PNG, WEBP")

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>Animal Image Classifier</h1>
        <p>Upload an image and the model will tell you whether it shows a cat, a dog or a horse.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if not (os.path.exists(MODEL_PATH) and os.path.exists(CLASSES_PATH)):
    st.error(
        f"Could not find {MODEL_PATH} or {CLASSES_PATH}. Run the notebook first and "
        "place both saved files in the same folder as this app."
    )
    st.stop()

model, class_names = load_assets()

# ---------------------------------------------------------------------------
# Main layout
# ---------------------------------------------------------------------------
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown('<div class="card-title">Step 1 - Upload an image</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed",
    )

    if uploaded is not None:
        image = Image.open(uploaded)
        st.image(image, caption=uploaded.name, use_container_width=True)

with right:
    st.markdown('<div class="card-title">Step 2 - Prediction</div>', unsafe_allow_html=True)

    if uploaded is None:
        st.markdown(
            """
            <div class="card placeholder">
                <h3>No image yet</h3>
                <p>Upload a photo on the left to see the prediction here.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        with st.spinner("Analysing image"):
            results = predict(model, class_names, image)

        top_label, top_conf = results[0]

        bars = ""
        for name, p in results:
            color = PURPLE if name == top_label else PURPLE_LIGHT
            bars += f"""
            <div class="bar-row">
                <div class="bar-head"><span>{name}</span><span>{p * 100:.1f}%</span></div>
                <div class="bar-track">
                    <div class="bar-fill" style="width:{p * 100:.1f}%; background:{color};"></div>
                </div>
            </div>
            """

        note = ""
        if top_conf < LOW_CONFIDENCE:
            note = (
                '<div class="note">The model is not very confident about this image. '
                "It may not show a cat, dog or horse, or the animal may be hard to see.</div>"
            )

        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">Predicted category</div>
                <div class="result-label">{top_label}</div>
                <div class="result-conf">Confidence: {top_conf * 100:.1f}%</div>
                <div class="card-title">Confidence by class</div>
                {bars}
                {note}
            </div>
            """,
            unsafe_allow_html=True,
        )
