import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import sys
import os
import json
import datetime
import zipfile
import io
import base64
from typing import List, Dict, Any
import time
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from src.services.ollama_client import OllamaVLMClient

st.set_page_config(
    page_title="Drishti AI - Vision Intelligence", 
    page_icon="👁️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FF9933 0%, #F0F0F0 50%, #138808 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: #000080;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        font-family: 'Arial', sans-serif;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #FF9933;
        margin: 1rem 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .metric-card {
        background: #f5f5f5;
        padding: 1.2rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        border-bottom: 3px solid #138808;
    }
    .sidebar-section {
        background: #f1f3f4;
        padding: 1.2rem;
        border-radius: 8px;
        margin: 1.2rem 0;
        border-top: 2px solid #FF9933;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #FF9933 0%, #138808 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        opacity: 0.9;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .success-box {
        background: #2c3e50; /* Dark background */
        border: 1px solid #34495e; /* Slightly lighter border */
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #ecf0f1; /* White text for contrast */
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #e0e0e0;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
        border: none;
        color: #333333;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF9933 !important;
        color: white !important;
    }
    .upload-section {
        border: 2px dashed #138808;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
        background-color: rgba(19, 136, 8, 0.05);
    }
    .footer {
        text-align: center;
        padding: 1rem;
        font-size: 0.8rem;
        color: #6c757d;
        margin-top: 2rem;
        border-top: 1px solid #dee2e6;
    }
    .result-container {
        border-left: 4px solid #138808;
        padding-left: 1rem;
        margin: 1rem 0;
    }
    /* Additional styles for better contrast */
    .batch-result {
        background-color: #f5f7f9;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        border-left: 3px solid #FF9933;
    }
    .batch-result-header {
        font-weight: bold;
        color: #333;
        margin-bottom: 8px;
    }
    .batch-result-content {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 6px;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'current_images' not in st.session_state:
    st.session_state.current_images = []
if 'processing_stats' not in st.session_state:
    st.session_state.processing_stats = {'total_processed': 0, 'total_time': 0}

def save_analysis_to_history(image_name: str, prompt: str, model: str, result: str, processing_time: float):
    analysis = {
        'timestamp': datetime.datetime.now().isoformat(),
        'image_name': image_name,
        'prompt': prompt,
        'model': model,
        'result': result,
        'processing_time': processing_time
    }
    st.session_state.analysis_history.append(analysis)
    st.session_state.processing_stats['total_processed'] += 1
    st.session_state.processing_stats['total_time'] += processing_time

def export_results_as_json():
    return json.dumps(st.session_state.analysis_history, indent=2)

def create_zip_export():
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        json_data = export_results_as_json()
        zip_file.writestr('analysis_results.json', json_data)
        
        for i, analysis in enumerate(st.session_state.analysis_history):
            filename = f"analysis_{i+1}_{analysis['timestamp'].replace(':', '-')}.txt"
            content = f"Image: {analysis['image_name']}\nModel: {analysis['model']}\nPrompt: {analysis['prompt']}\nProcessing Time: {analysis['processing_time']:.2f}s\n\nResult:\n{analysis['result']}"
            zip_file.writestr(filename, content)
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

def apply_image_enhancements(image: Image.Image, brightness: float, contrast: float, saturation: float, blur: float) -> Image.Image:
    if brightness != 1.0:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(brightness)
    
    if contrast != 1.0:
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(contrast)
    
    if saturation != 1.0:
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(saturation)
    
    if blur > 0:
        image = image.filter(ImageFilter.GaussianBlur(radius=blur))
    
    return image

st.markdown("""
<div class="main-header">
    <h1>🪔 Drishti AI - Vision Intelligence</h1>
    <p>Advanced Image Analysis with Vision Language Models</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🛠️ Configuration")
    
    with st.expander("🤖 Model Settings", expanded=True):
        model = st.selectbox(
            "Vision Model", 
            ["llava:7b", "llava:13b", "llava:phi3", "bakllava", "minicpm-v", "moondream", "llava:34b"], 
            index=0,
            help="Choose the vision language model for analysis"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            max_tokens = st.slider("Max Tokens", 32, 1024, 300, step=16)
        with col2:
            temperature = st.slider("Temperature", 0.0, 2.0, 0.2, step=0.05)
    
    with st.expander("✨ Image Enhancement", expanded=False):
        brightness = st.slider("Brightness", 0.5, 2.0, 1.0, step=0.1)
        contrast = st.slider("Contrast", 0.5, 2.0, 1.0, step=0.1)
        saturation = st.slider("Saturation", 0.0, 2.0, 1.0, step=0.1)
        blur = st.slider("Blur", 0.0, 5.0, 0.0, step=0.1)
    
    with st.expander(" Prompt Templates", expanded=True):
        prompt_templates = {
            "General Description": "Describe this image in detail, including objects, people, setting, and overall composition.",
            "Technical Analysis": "Provide a technical analysis of this image including composition, lighting, colors, and photographic elements.",
            "Creative Writing": "Write a creative story or narrative inspired by this image.",
            "Accessibility": "Describe this image for someone who cannot see it, focusing on important visual elements.",
            "Educational": "Explain what can be learned from this image from an educational perspective.",
            "Marketing": "Analyze this image from a marketing and branding perspective.",
            "Art Critique": "Provide an art critique of this image, discussing style, technique, and artistic elements.",
            "OCR": "Extract and transcribe any text visible in this image.",
            "Object Detection": "Identify and list all objects, people, and items visible in this image.",
            "Scene Understanding": "Analyze the scene, setting, and context of this image.",
            "Color Analysis": "Describe the color palette, lighting, and visual mood of this image.",
            "Composition": "Analyze the composition, framing, and visual structure of this image.",
            "Custom": ""
        }
        
        selected_template = st.selectbox("Choose Template", list(prompt_templates.keys()))
        
        if selected_template == "Custom":
            prompt = st.text_area("Custom Prompt", height=100, placeholder="Enter your custom prompt here...")
        else:
            prompt = st.text_area("Prompt", value=prompt_templates[selected_template], height=100)
    
    st.markdown("---")
    
    if st.session_state.analysis_history:
        st.markdown("### 📊 Session Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Processed", st.session_state.processing_stats['total_processed'])
        with col2:
            avg_time = st.session_state.processing_stats['total_time'] / max(1, st.session_state.processing_stats['total_processed'])
            st.metric("Avg Time", f"{avg_time:.1f}s")
        
        if st.button("📥 Export Results"):
            zip_data = create_zip_export()
            st.download_button(
                label="Download ZIP",
                data=zip_data,
                file_name=f"analysis_results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                mime="application/zip"
            )
        
        if st.button("️ Clear History"):
            st.session_state.analysis_history = []
            st.session_state.processing_stats = {'total_processed': 0, 'total_time': 0}
            st.rerun()

tab1, tab2, tab3, tab4 = st.tabs(["🖼️ Single Image", "📊 Batch Processing", "🔍 Compare Images", "📜 History"])

with tab1:
    st.markdown("### Upload and Analyze Single Image")
    
    uploaded_file = st.file_uploader(
        "Choose an image file", 
        type=["png", "jpg", "jpeg", "webp", "bmp", "tiff"],
        help="Supported formats: PNG, JPG, JPEG, WebP, BMP, TIFF"
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        
        enhanced_image = apply_image_enhancements(image, brightness, contrast, saturation, blur)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### Original Image")
            st.image(image, caption=f"Original: {uploaded_file.name}", use_container_width=True)
            
            st.markdown("#### Image Information")
            st.info(f"""
            **Filename:** {uploaded_file.name}
            **Size:** {image.size[0]} × {image.size[1]} pixels
            **Format:** {image.format}
            **Mode:** {image.mode}
            **File Size:** {len(uploaded_file.getvalue()) / 1024:.1f} KB
            """)
        
        with col2:
            st.markdown("#### Enhanced Image")
            st.image(enhanced_image, caption="Enhanced version", use_container_width=True)
            
            if st.button("🚀 Analyze Image", type="primary"):
                if not prompt.strip():
                    st.error("Please enter a prompt for analysis.")
                else:
                    with st.spinner(f"Analyzing with {model}..."):
                        try:
                            start_time = time.time()
                            client = OllamaVLMClient()
                            
                            progress_bar = st.progress(0)
                            for i in range(100):
                                time.sleep(0.01)
                                progress_bar.progress(i + 1)
                            
                            summary = client.summarize_image(enhanced_image, prompt, model, temperature, max_tokens)
                            processing_time = time.time() - start_time
                            
                            st.markdown("####  Analysis Result")
                            st.markdown(f"""
                            <div class="success-box">
                                <strong>Model:</strong> {model}<br>
                                <strong>Processing Time:</strong> {processing_time:.2f} seconds<br>
                                <strong>Tokens:</strong> ~{len(summary.split()) * 1.3:.0f}
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown(summary)
                            
                            save_analysis_to_history(uploaded_file.name, prompt, model, summary, processing_time)
                            
                            col_export1, col_export2 = st.columns(2)
                            with col_export1:
                                st.download_button(
                                    "📄 Download as Text",
                                    data=f"Image: {uploaded_file.name}\nModel: {model}\nPrompt: {prompt}\n\nResult:\n{summary}",
                                    file_name=f"analysis_{uploaded_file.name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                    mime="text/plain"
                                )
                            with col_export2:
                                analysis_json = {
                                    'image_name': uploaded_file.name,
                                    'model': model,
                                    'prompt': prompt,
                                    'result': summary,
                                    'processing_time': processing_time,
                                    'timestamp': datetime.datetime.now().isoformat()
                                }
                                st.download_button(
                                    "📊 Download as JSON",
                                    data=json.dumps(analysis_json, indent=2),
                                    file_name=f"analysis_{uploaded_file.name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                    mime="application/json"
                                )
                            
                        except Exception as e:
                            st.error(f"Analysis failed: {str(e)}")
                            st.info("Make sure Ollama is running and the selected model is available.")

with tab2:
    st.markdown("### Batch Image Processing")
    
    uploaded_files = st.file_uploader(
        "Choose multiple image files", 
        type=["png", "jpg", "jpeg", "webp", "bmp", "tiff"],
        accept_multiple_files=True,
        help="Upload multiple images for batch processing"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} images uploaded")
        
        batch_prompt = st.text_area(
            "Batch Processing Prompt", 
            value="Describe this image briefly and identify key elements.",
            height=80
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            batch_model = st.selectbox("Batch Model", ["llava:7b", "llava:13b", "llava:phi3", "bakllava"], key="batch_model")
        with col2:
            batch_max_tokens = st.slider("Batch Max Tokens", 32, 512, 150, key="batch_tokens")
        with col3:
            batch_temperature = st.slider("Batch Temperature", 0.0, 1.5, 0.2, key="batch_temp")
        
        if st.button(" Process All Images", type="primary"):
            if not batch_prompt.strip():
                st.error("Please enter a prompt for batch processing.")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()
                results_container = st.container()
                
                batch_results = []
                
                for i, uploaded_file in enumerate(uploaded_files):
                    status_text.text(f"Processing {uploaded_file.name} ({i+1}/{len(uploaded_files)})")
                    
                    try:
                        image = Image.open(uploaded_file).convert("RGB")
                        enhanced_image = apply_image_enhancements(image, brightness, contrast, saturation, blur)
                        
                        start_time = time.time()
                        client = OllamaVLMClient()
                        summary = client.summarize_image(enhanced_image, batch_prompt, batch_model, batch_temperature, batch_max_tokens)
                        processing_time = time.time() - start_time
                        
                        result = {
                            'filename': uploaded_file.name,
                            'summary': summary,
                            'processing_time': processing_time,
                            'image': enhanced_image
                        }
                        batch_results.append(result)
                        
                        save_analysis_to_history(uploaded_file.name, batch_prompt, batch_model, summary, processing_time)
                        
                    except Exception as e:
                        st.error(f"Failed to process {uploaded_file.name}: {str(e)}")
                    
                    progress_bar.progress((i + 1) / len(uploaded_files))
                
                status_text.text("✅ Batch processing complete!")
                
                with results_container:
                    st.markdown("#### Batch Results")
                    for result in batch_results:
                        with st.expander(f"📄 {result['filename']} ({result['processing_time']:.2f}s)"):
                            col1, col2 = st.columns([1, 2])
                            with col1:
                                st.image(result['image'], caption=result['filename'], use_container_width=True)
                            with col2:
                                st.markdown(f"""
                                <div class="batch-result">
                                    <div class="batch-result-header">Analysis Result:</div>
                                    <div class="batch-result-content">{result['summary']}</div>
                                </div>
                                """, unsafe_allow_html=True)
                    
                    batch_export_data = []
                    for result in batch_results:
                        batch_export_data.append({
                            'filename': result['filename'],
                            'model': batch_model,
                            'prompt': batch_prompt,
                            'result': result['summary'],
                            'processing_time': result['processing_time'],
                            'timestamp': datetime.datetime.now().isoformat()
                        })
                    
                    st.download_button(
                        "📥 Download Batch Results",
                        data=json.dumps(batch_export_data, indent=2),
                        file_name=f"batch_results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )

with tab3:
    st.markdown("### Compare Multiple Images")
    
    compare_files = st.file_uploader(
        "Upload 2-4 images to compare", 
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=True,
        key="compare_uploader"
    )
    
    if compare_files and len(compare_files) >= 2:
        if len(compare_files) > 4:
            st.warning("Only the first 4 images will be used for comparison.")
            compare_files = compare_files[:4]
        
        st.markdown(f"#### Comparing {len(compare_files)} Images")
        
        cols = st.columns(len(compare_files))
        images = []
        
        for i, (col, file) in enumerate(zip(cols, compare_files)):
            with col:
                image = Image.open(file).convert("RGB")
                enhanced_image = apply_image_enhancements(image, brightness, contrast, saturation, blur)
                images.append((file.name, enhanced_image))
                st.image(enhanced_image, caption=f"{i+1}. {file.name}", use_column_width=True)
        
        comparison_prompt = st.text_area(
            "Comparison Prompt", 
            value="Compare these images, highlighting similarities and differences in composition, style, content, and quality.",
            height=100
        )
        
        if st.button("🔍 Compare Images", type="primary"):
            if not comparison_prompt.strip():
                st.error("Please enter a comparison prompt.")
            else:
                with st.spinner("Analyzing and comparing images..."):
                    try:
                        client = OllamaVLMClient()
                        comparisons = []
                        
                        for name, image in images:
                            start_time = time.time()
                            individual_analysis = client.summarize_image(
                                image, 
                                f"Analyze this image ({name}) in detail: {comparison_prompt}", 
                                model, 
                                temperature, 
                                max_tokens
                            )
                            processing_time = time.time() - start_time
                            comparisons.append({
                                'name': name,
                                'analysis': individual_analysis,
                                'processing_time': processing_time
                            })
                        
                        st.markdown("#### 🔍 Individual Analysis")
                        for comp in comparisons:
                            with st.expander(f"Analysis: {comp['name']} ({comp['processing_time']:.2f}s)"):
                                st.markdown(comp['analysis'])
                        
                        st.markdown("####  Comparison Summary")
                        summary_prompt = f"Based on these analyses, provide a comparative summary: {' | '.join([comp['analysis'] for comp in comparisons])}"
                        
                        if len(summary_prompt) > 8000:
                            summary_prompt = summary_prompt[:8000] + "..."
                        
                        comparison_summary = client.summarize_image(
                            images[0][1], 
                            "Provide a comparative analysis summary of the previously analyzed images, focusing on key similarities and differences.",
                            model,
                            temperature,
                            max_tokens
                        )
                        
                        st.markdown(comparison_summary)
                        
                        comparison_data = {
                            'images': [comp['name'] for comp in comparisons],
                            'individual_analyses': comparisons,
                            'comparison_summary': comparison_summary,
                            'model': model,
                            'timestamp': datetime.datetime.now().isoformat()
                        }
                        
                        st.download_button(
                            "📥 Download Comparison",
                            data=json.dumps(comparison_data, indent=2),
                            file_name=f"image_comparison_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
                        
                    except Exception as e:
                        st.error(f"Comparison failed: {str(e)}")

with tab4:
    st.markdown("### 📜 Analysis History")
    
    if not st.session_state.analysis_history:
        st.info("No analysis history yet. Start by analyzing some images!")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Analyses", len(st.session_state.analysis_history))
        with col2:
            total_time = sum(analysis['processing_time'] for analysis in st.session_state.analysis_history)
            st.metric("Total Time", f"{total_time:.1f}s")
        with col3:
            avg_time = total_time / len(st.session_state.analysis_history)
            st.metric("Average Time", f"{avg_time:.1f}s")
        
        st.markdown("#### Recent Analyses")
        
        for i, analysis in enumerate(reversed(st.session_state.analysis_history[-10:])):
            with st.expander(f"🖼️ {analysis['image_name']} - {analysis['timestamp'][:19]}"):
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.markdown(f"""
                    **Model:** {analysis['model']}  
                    **Time:** {analysis['processing_time']:.2f}s  
                    **Date:** {analysis['timestamp'][:10]}
                    """)
                with col2:
                    st.markdown("**Prompt:**")
                    st.text(analysis['prompt'])
                    st.markdown("**Result:**")
                    st.markdown(analysis['result'])

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p> AI Vision Studio - Powered by Ollama Vision Language Models</p>
    <p>Built with Streamlit • Enhanced with advanced image processing capabilities</p>
</div>
""", unsafe_allow_html=True)
