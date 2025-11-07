import streamlit as st
from utils import generate_test_script
import time

st.set_page_config(
    page_title="Figma Test Generator",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar: Instructions and branding
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/5968/5968705.png", width=80)
    st.title("Figma Test Generator")
    st.markdown("""
    <div style='font-size:16px;line-height:1.6;'>
    <b>How to use:</b><br>
    <ol>
    <li>Select your target framework</li>
    <li>Upload a Figma screen (PNG/JPG/SVG)</li>
    <li>Enter Base URL for the application under test</li>
    <li>Click <b>Generate Test Script</b> to auto-generate test cases</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
    st.info("Set your GEMINI API key in the .env file for real LLM generation.")
    st.markdown("---")
    st.caption("Made for Hackathon 2025 · Powered by Streamlit & AI Café")

# Main header
st.markdown("""
<h1 style='background: linear-gradient(90deg,#4F8BF9,#6DD5FA,#43E97B);color:white;padding:20px;border-radius:12px;text-align:center;'>
🧪 Figma → Automated Test Generator
</h1>
""", unsafe_allow_html=True)

# Framework selection
st.markdown("""
<div style='background:#f7fafd;border-radius:12px;padding:24px;margin-bottom:16px;'>
<h3 style='color:#4F8BF9;'>1. Select Target Framework</h3>
""", unsafe_allow_html=True)
framework = st.selectbox("Target framework", ["Playwright", "Selenium"], index=0)
st.markdown("</div>", unsafe_allow_html=True)

# Base URL input
st.markdown("""
<div style='background:#f7fafd;border-radius:12px;padding:24px;margin-bottom:16px;'>
<h3 style='color:#4F8BF9;'>2. Enter Base URL</h3>
""", unsafe_allow_html=True)
base_url = st.text_input("Base URL (e.g., https://opensource-demo.orangehrmlive.com/)", "")
st.markdown("</div>", unsafe_allow_html=True)

# Image upload
st.markdown("""
<div style='background:#f7fafd;border-radius:12px;padding:24px;margin-bottom:16px;'>
<h3 style='color:#4F8BF9;'>3. Upload Figma Screen</h3>
""", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload PNG, JPG, or SVG", type=["png", "jpg", "jpeg", "svg"])
if uploaded_file:
    st.image(uploaded_file, width=320)
st.markdown("</div>", unsafe_allow_html=True)

# Buttons
col1, col2 = st.columns([2, 1])
with col1:
    generate = st.button("🚀 Generate Test Script", use_container_width=True)
with col2:
    clear = st.button("🧹 Clear Output", use_container_width=True)

if clear:
    st.session_state.clear()  # clear stored states
    st.stop()  # stop execution to refresh

# Output area
st.markdown("---")
output_container = st.container()

with output_container:
    if generate:
        if uploaded_file is None:
            st.warning("Please upload a Figma screen image.")
        elif not base_url:
            st.warning("Please enter a Base URL.")
        else:
            with st.spinner("Generating test script — calling the LLM..."):
                image_bytes = uploaded_file.read()
                try:
                    result = generate_test_script("", image_bytes, framework, page_header=None, base_url=base_url)
                except Exception as e:
                    result = {"error": f"Exception calling generate_test_script: {e}"}

            if not result:
                st.error("❌ No response received from generate_test_script. Check logs or API connectivity.")
            elif isinstance(result, dict) and result.get("error"):
                st.error(f"❌ {result['error']}")
                st.info("Check your API key and endpoint in .env.")
            elif isinstance(result, dict) and result.get("script"):
                st.success("✅ Generated test script successfully!")
                st.markdown("#### Preview (combined):")
                st.code(result["script"], language="python")

                try:
                    with open(result["filename"], "w", encoding="utf-8") as f:
                        f.write(result["script"])
                except Exception as e:
                    st.warning(f"Could not save file: {e}")

                st.download_button(
                    "⬇️ Download test script",
                    data=result["script"],
                    file_name=result["filename"],
                    mime="text/x-python"
                )
                st.info(f"Saved file: {result['filename']}")

# Footer note
st.markdown("---")
st.caption("Set your GEMINI API key and endpoint in .env before running. Large image uploads may exceed prompt size; keep images reasonable.")
