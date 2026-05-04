import streamlit as st
import tensorflow as tf
from tensorflow.keras.applications.efficientnet import preprocess_input
from PIL import Image
import numpy as np
import json
import os

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Solar Panel Defect Classifier",
    page_icon="☀️",
    layout="centered"
)

st.title("☀️ Solar Panel Defect Classifier")
st.write("Upload a solar panel image to detect defects using EfficientNetB0.")

# ── Load class names from JSON if available ──────────────────────────────────
CLASS_NAMES_FILE = "class_names.json"
DEFAULT_CLASSES  = ["Bird-drop", "Clean", "Dusty",
                    "Electrical-damage", "Physical-damage", "Snow-Covered"]

if os.path.exists(CLASS_NAMES_FILE):
    with open(CLASS_NAMES_FILE) as f:
        CLASSES = json.load(f)
else:
    CLASSES = DEFAULT_CLASSES

# ── Model loading (cached so it only loads once per session) ──────────────────
@st.cache_resource
def load_model(model_path: str = "trained_effnet_finetune.h5"):
    """Load the saved Keras model. Cached to avoid reloading on every rerun."""
    return tf.keras.models.load_model(model_path)

with st.spinner("Loading model..."):
    model = load_model()

# ── Inference helper ──────────────────────────────────────────────────────────
def predict(image: Image.Image) -> np.ndarray:
    """Preprocess a PIL image and return softmax probability array."""
    img      = image.resize((224, 224)).convert("RGB")
    arr      = np.array(img, dtype=np.float32)
    arr      = np.expand_dims(arr, axis=0)   # add batch dimension
    arr      = preprocess_input(arr)         # EfficientNet normalisation
    return model.predict(arr, verbose=0)[0]  # drop batch dimension

# ── UI ────────────────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Upload a solar panel image", type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    with st.spinner("Analysing the panel..."):
        probs = predict(image)

    pred_idx   = int(np.argmax(probs))
    pred_class = CLASSES[pred_idx]
    confidence = probs[pred_idx]

    st.markdown(f"### Prediction: **{pred_class}**")
    st.markdown(f"**Confidence:** {confidence:.1%}")

    if pred_class == "Clean":
        st.success("The panel appears to be in good condition.")
    else:
        st.warning("A defect or contamination has been detected.")

    # Top-3 predictions
    st.write("### Top 3 Predictions")
    top3 = np.argsort(probs)[-3:][::-1]
    medals = ["🥇", "🥈", "🥉"]
    for rank, idx in enumerate(top3):
        st.write(f"{medals[rank]} **{CLASSES[idx]}** — {probs[idx]:.1%}")

    # Full probability table
    with st.expander("View all class probabilities"):
        for cls, prob in zip(CLASSES, probs):
            st.progress(float(prob), text=f"{cls}: {prob:.1%}")