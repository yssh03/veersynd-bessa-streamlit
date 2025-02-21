import streamlit as st
import pandas as pd
from resume_tailor import ResumeTailor
import os
from dotenv import load_dotenv
import time
load_dotenv()
st.set_page_config(
    page_title="Veersynd Bessa", 
    layout="wide",  
    initial_sidebar_state="expanded",  
)
st.title("Veersynd Bessa")

st.write("## Job Description")

toggle_button = st.toggle("Is Job Description a file?")

if toggle_button:
    uploaded_file = st.file_uploader(
        "Choose a file", type=["pdf", "docx", "doc", "txt"])
else:
    uploaded_jd = st.text_area("Enter Job Description:")

resume = st.text_area("Enter Resume Bullet Points:",)

button = st.button("Customize")
loading = False
if button:
    if toggle_button and not uploaded_file:
        st.warning("Please upload or enter job description!")
    elif not toggle_button and not uploaded_jd:
        st.warning("Please upload or enter job description!")
    elif not resume:
        st.warning("Please enter resume bullet points!")
    else:
        jd_data = ""
        if toggle_button and uploaded_file:
            jd_data = uploaded_file.read().decode('utf-8')
        else:
            jd_data = uploaded_jd
        api_key = os.getenv("api_key")
        resume_tailor = ResumeTailor(api_key, resume, jd_data)
        flag = resume_tailor.validate_jd()
        
        if not flag:
            st.warning("Are you sure this resume point is relevant to the JD? Consider removing it from your resume or be a little more specific.")
        else:    
            resume_tailored = resume_tailor.customize_resume()
            st.write("## Customized Bullet Points!!")
            st.write(str(resume_tailored))
        
