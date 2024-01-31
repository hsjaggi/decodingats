from pathlib import Path

import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

from dotenv import load_dotenv

## load all the environment variables
load_dotenv()

##API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

##Gemini Pro Response
def get_gemini_response(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

## Prompt Template
input_prompt="""
Het Act Like a skilled or very experienced ATS(Application Tracking System)
with a deep understanding of tech field, software engineering, data science, data analyst, and data engineer. 
You task is to evaluate the resume based on the given job description. 
You must consider the job market is very competitive and you should provide best assistance for improving 
the resumes. Assign the percentage Matching based on jd and add the missing 
keywrods with high accuracy. 
resume:{text}
description:{jd}

I want the response on one single string having the structure 
{{"JD Match":"%","Missing Keywords:[]","Profile Summary":""}}
"""

#streamlit app
st.title("Cracking ATS")
st.text("Beat the ATS by improving your Resume score")

jd=st.text_area("Paste the JD")
uploaded_file=st.file_uploader("Upload your Resume", type="pdf",help="Please upload the pdf")


submit=st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_prompt)
        st.subheader(response)