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

resume = st.text_area("Enter Resume Bullet Points:")

#Adithya Arya changes --> If multiple bullet points, create multiple objects and run the customize routine for each point separately.

resume = resume.split("\n")

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
        resume_tailor = []
        for bullet_point in resume:
            resume_tailor.append(ResumeTailor(api_key, bullet_point, jd_data))
        
        flags = []
        for index in range(len(resume_tailor)):
            flags.append(resume_tailor[index].validate_jd())
        
        st.write("## Customized Bullet Points!!")
        for flag,bullet_point in zip(flags,resume_tailor):
            if not flag:
                st.warning(str("Are you sure resume point # "+str(resume_tailor.index(bullet_point)+1)+" is relevant to the JD? Consider removing it from your resume or be a little more specific."))
            else:    
                resume_tailored = bullet_point.customize_resume()
                #st.write("## Customized Bullet Points!!")
                st.write(str("- "+resume_tailored))
        
