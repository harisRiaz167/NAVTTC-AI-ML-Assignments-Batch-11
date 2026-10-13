from pathlib import Path

import streamlit as st
import tensorflow as tf
import keras.utils as utils
from PIL import Image
import tensorflow.keras as keras


st.set_page_config(
    page_title="Animal Vision | CNN Classifier",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded",
)

MODEL_PATH = Path("saved_model/cnn2d.keras")
TEST_IMAGE_PATH = Path("dataset/test/dog/dog_0010.png")
IMAGE_SIZE = (32, 32)

# Keep this order identical to the class order used during training.
CLASS_NAMES = ["cat", "dog", "horse"]


st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #f6f8fc 0%, #eef3fb 100%);
        }
        [data-testid="stHeader"] {
            background: rgba(246, 248, 252, 0.9);
        }
        .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        .hero {
            padding: 1.8rem 2rem;
            border-radius: 24px;
            background: linear-gradient(115deg, #182848 0%, #315b96 100%);
            color: #ffffff;
            margin-bottom: 1.5rem;
            box-shadow: 0 12px 32px rgba(24, 40, 72, 0.16);
        }
        .hero h1 {
            color: #ffffff;
            font-size: clamp(2rem, 4vw, 3rem);
            margin: 0 0 0.4rem 0;
            letter-spacing: -0.04em;
        }
        .hero p {
            color: #e4edff;
            font-size: 1.05rem;
            margin: 0;
        }
        .section-title {
            font-size: 1.2rem;
            font-weight: 700;
            color: #182848;
            margin: 0.3rem 0 0.8rem 0;
        }
        .panel {
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid #e0e7f1;
            border-radius: 20px;
            padding: 1.25rem;
            box-shadow: 0 8px 24px rgba(31, 51, 81, 0.06);
        }
        .prediction-label {
            color: #52647d;
            font-size: 0.9rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        .prediction-value {
            color: #18345e;
            font-size: 2.4rem;
            line-height: 1.2;
            font-weight: 800;
            margin: 0.25rem 0 0.8rem 0;
        }
        .small-note {
            color: #607089;
            font-size: 0.9rem;
        }
        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #e0e7f1;
            padding: 1rem;
            border-radius: 16px;
        }
        div.stButton > button[kind="primary"] {
            border-radius: 12px;
            min-height: 3rem;
            font-weight: 700;
        }
        section[data-testid="stSidebar"] {
            background: #f0f4fa;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner="Loading your trained CNN model...")
def load_model(model_path: str):
    return tf.keras.models.load_model(model_path)

st.markdown(
    """
    <div class="hero">
        <h1>🐾 Animal Vision</h1>
        <p>A 2D CNN that predicts whether an image contains a cat, dog, or horse.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## About this demo")
    st.write(
        "This application loads a previously trained TensorFlow/Keras CNN and "
        "uses it to classify one image into one of three animal categories."
    )
    st.markdown("---")
    st.markdown("**Model input**")
    st.write("180 × 180 pixels · 3 RGB channels")
    st.markdown("**Classes**")
    st.write("🐱 Cat · 🐶 Dog · 🐴 Horse")
    st.markdown("**Prediction flow**")
    st.caption("Load image → Resize → CNN prediction → Display class probabilities")


left_col, right_col = st.columns([1, 1.15], gap="large")

with left_col:
    st.markdown('<div class="section-title">1. Choose an image</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload a cat, dog, or horse image",
        type=["png", "jpg", "jpeg", "webp"],
        help="Upload an image to classify it, or use the sample image below.",
    )

    image = None
    image_label = ""

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file).convert("RGB")
            image_label = uploaded_file.name
        except Exception as error:
            st.error(f"Could not open this image: {error}")
    elif TEST_IMAGE_PATH.exists():
        try:
            image = Image.open(TEST_IMAGE_PATH).convert("RGB")
            image_label = str(TEST_IMAGE_PATH)
            st.info("Using the sample test image. Upload another image above to try it instead.")
        except Exception as error:
            st.error(f"Could not open the sample image: {error}")
    else:
        st.info("Upload an image to begin. The default sample image was not found.")

    if image is not None:
        st.image(image, caption=image_label, use_container_width=True)
        st.caption(f"Original image size: {image.width} × {image.height} pixels")

with right_col:
    st.markdown('<div class="section-title">2. Prediction results</div>', unsafe_allow_html=True)

    if not MODEL_PATH.exists():
        st.error(
            f"Model not found at `{MODEL_PATH}`. Train and save your model first, "
            "then run this app from your project root directory."
        )
    elif image is None:
        st.markdown(
            '<div class="panel"><p class="small-note">Your prediction will appear here after you provide an image.</p></div>',
            unsafe_allow_html=True,
        )
    else:
        try:
            with st.spinner("Analyzing the image..."):
                model = load_model(str(MODEL_PATH))

                # Resize and convert the image to a numeric array.
                resized_image = image.resize(IMAGE_SIZE)
                image_array = utils.img_to_array(resized_image)
                image_batch = tf.expand_dims(image_array, axis=0)

                # The model's Rescaling layer already scales pixels to 0–1.
                probabilities = model.predict(image_batch, verbose=0)[0]

            if len(probabilities) != len(CLASS_NAMES):
                st.error(
                    f"The model returned {len(probabilities)} class scores, but "
                    f"CLASS_NAMES contains {len(CLASS_NAMES)} names. Update CLASS_NAMES "
                    "to match the model used during training."
                )
            else:
                predicted_index = int(tf.argmax(probabilities).numpy())
                predicted_class = CLASS_NAMES[predicted_index]
                confidence = float(probabilities[predicted_index])

                st.markdown('<div class="panel">', unsafe_allow_html=True)
                st.markdown('<div class="prediction-label">Predicted animal</div>', unsafe_allow_html=True)
                emoji = {"cat": "🐱", "dog": "🐶", "horse": "🐴"}.get(predicted_class, "🐾")
                st.markdown(
                    f'<div class="prediction-value">{emoji} {predicted_class.title()}</div>',
                    unsafe_allow_html=True,
                )
                st.progress(confidence, text=f"Model score: {confidence * 100:.2f}%")
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("### Probability by class")
                for name, probability in zip(CLASS_NAMES, probabilities):
                    score = float(probability)
                    class_emoji = {"cat": "🐱", "dog": "🐶", "horse": "🐴"}.get(name, "🐾")
                    st.markdown(f"**{class_emoji} {name.title()}** — {score * 100:.2f}%")
                    st.progress(score)

                st.caption(
                    "These are the model's softmax scores. A high score is not a guarantee "
                    "that the prediction is correct."
                )
        except Exception as error:
            st.error(f"Prediction failed: {error}")

st.markdown("---")
st.caption("Built with Streamlit, TensorFlow, and Keras · CNN image classification demo")
