import streamlit as st
import openai as OpenAI
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import re
import pandas as pd
import json
import plotly.graph_objects as go # <--- New Import for the wheel

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") 

if not api_key:
    st.error("Please configure your OpenAI API Key!")
    st.stop()

client = OpenAI.OpenAI(api_key=api_key)
st.set_page_config(page_title="AI Career Pro Dashboard", page_icon="🚀", layout="wide")

# --- CUSTOM CSS (Refined for "Bubbles" and low contrast) ---
st.markdown("""
<style>
    /* 1. Main Background & Layout */
    .stApp { background: linear-gradient(to bottom, #101014, #181A20); }
    
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #1A1C24;
        border: 1px solid #333;
        border-radius: 16px;
        padding: 2rem;
    }

    /* 2. Text Brightness (Headers & Body) */
    h1, h2, h3 { color: #FFFFFF !important; }
    p, span, label { color: #F0F2F6 !important; }

    /* 3. Metrics & Numbers (The "Gains") */
    [data-testid="stMetricValue"] { color: #00D1FF; font-weight: 800; }
    [data-testid="stMetricLabel"] p { color: #A0AEC0 !important; }

    /* 4. THE BUTTON FIX (Targeting the Upload button) */
    button[data-testid="baseButton-secondary"] {
        background-color: #0E1117 !important; 
        color: #FFFFFF !important; 
        border: 1px solid #444 !important; 
        transition: 0.3s all ease;
    }

    button[data-testid="baseButton-secondary"]:hover {
        border-color: #00D1FF !important; 
        color: #00D1FF !important;
        background-color: #1A1C24 !important;
    }

    /* 5. Fixes the "Drag and drop" text inside the box */
    [data-testid="stFileUploadDropzone"] div div {
        color: #F0F2F6 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# --- UI HEADER ---
st.title("🚀 AI Career Pro: Precision Match")
st.divider()

col_left, col_mid, col_right = st.columns([1, 2, 1], gap="large")

# --- LEFT: METRICS ---
with col_left:
    st.subheader("📊 Performance")
    
    # Check if analysis has been run yet
    if st.session_state.analysis_results:
        res = st.session_state.analysis_results
        total_score = sum(res['scores'].values())
        
        # 1. The Hero Score (Overall)
        with st.container(border=True):
            st.metric(label="Overall Match Score", value=f"{total_score}%", delta="Optimized")
            st.progress(total_score / 100)
            
        # 2. The Suggestions (Moved from Right to Left as requested)
        st.subheader("🛠️ Quick Fixes")
        with st.container(border=True):
            for s in res['suggestions']:
                st.write(f"✅ {s}")
    else:
        # Default state before the button is clicked
        st.info("Upload documents and run analysis to see your score and suggestions.")

# --- MIDDLE: THE WORKSPACE & THE WHEEL ---
# --- MIDDLE: THE WORKSPACE & THE WHEEL ---
with col_mid:
    with st.container(border=True):
        st.subheader("📝 Step 1: Documents")
        uploaded_file = st.file_uploader("Upload Resume", type="pdf")
        job_description = st.text_area("Job Description", height=200)

        if st.button("Run Full Analysis", use_container_width=True, type="primary"):
            if uploaded_file and job_description:
                with st.spinner("Analyzing your documents..."):
                    # 1. EXTRACT & CLEAN TEXT (From your original logic)
                    pdf = PdfReader(uploaded_file)
                    text = ""
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                    text_clean = re.sub(r"(?<!\n)\n(?!\n)", " ", text) #

                    # 2. DYNAMIC OPENAI CALL
                    prompt = f"""
                    Analyze this resume against the job description.
                    Return ONLY a JSON object with these exact keys:
                    "analysis": (2-sentence summary),
                    "suggestions": (list of 3 strings),
                    "scores": {{"Technical": 0-30, "Soft Skills": 0-20, "Experience": 0-25, "Education": 0-10, "Keywords": 0-15}}

                    Resume: {text_clean}
                    Job Description: {job_description}
                    """

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": prompt}],
                        response_format={ "type": "json_object" }
                    )
                    
                    # 3. UPDATE SESSION STATE
                    st.session_state.analysis_results = json.loads(response.choices[0].message.content)
                    st.rerun() # This triggers the Left Column to update
            else:
                st.warning("Please upload a PDF and paste a JD first!")

    # --- THE RADAR CHART (THE WHEEL) ---
    if st.session_state.analysis_results:
        with st.container(border=True):
            st.subheader("🕸️ Skill Overlap Wheel")
            res = st.session_state.analysis_results
            categories = list(res['scores'].keys())
            values = list(res['scores'].values())

            fig = go.Figure(data=go.Scatterpolar(
                r=values + [values[0]], 
                theta=categories + [categories[0]],
                fill='toself',
                line_color='#00D1FF',
                fillcolor='rgba(0, 209, 255, 0.3)'
            ))

            fig.update_layout(
                polar=dict(
                    bgcolor="#1A1C24",
                    radialaxis=dict(visible=True, range=[0, 30], color="#888", gridcolor="#444"),
                    angularaxis=dict(color="#E0E0E0", gridcolor="#444")
                ),
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=40, r=40, t=20, b=20),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

# --- RIGHT: BREAKDOWN ---
with col_right:
    st.subheader("🎯 Top Match Areas")
    if st.session_state.analysis_results:
        res = st.session_state.analysis_results
        with st.container(border=True):
            # Define max values for each category to scale progress bars correctly
            max_vals = {"Technical": 30, "Soft Skills": 20, "Experience": 25, "Education": 10, "Keywords": 15}
            
            for cat, score in res['scores'].items():
                st.write(f"**{cat}**")
                st.progress(score / max_vals.get(cat, 30))
            
            st.divider()
            st.write("**Expert Verdict:**")
            st.caption(res['analysis'])
    else:
        st.info("Awaiting Breakdown")   