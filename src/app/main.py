import streamlit as st
from PIL import Image
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from src.services.ollama_client import OllamaVLMClient

st.set_page_config(page_title="Image Summarizer", page_icon="", layout="centered")

st.title("Image Summarization with Ollama VLM")

with st.sidebar:
    st.header("Settings")
    model = st.selectbox("Model", ["llava:7b", "llava:13b", "llava-phi3", "bakllava", "minicpm-v", "moondream"], index=0)
    prompt = st.text_area("Prompt", "Describe this image succinctly", height=100)

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded image", use_column_width=True)
    col1, col2 = st.columns(2)
    with col1:
        max_tokens = st.slider("Max tokens", 32, 512, 200, step=16)
    with col2:
        temperature = st.slider("Temperature", 0.0, 1.5, 0.2, step=0.05)
    if st.button("Generate Summary", type="primary"):
        with st.spinner("Generating summary..."):
            try:
                client = OllamaVLMClient()
                summary = client.summarize_image(image, prompt, model, temperature, max_tokens)
                st.subheader("Summary")
                st.write(summary)
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.info("Upload an image to begin.")
