import streamlit as st
from openai import OpenAI
import PyPDF2
import docx

# ---------------- CONFIG ----------------
st.set_page_config(page_title="CA Interview AI Bot", layout="centered")

st.title("🎓 CA Interview Question Generator")
st.subheader("AI-powered interview prep for CA students & professionals")

# ---------------- API KEY ----------------
api_key = st.text_input(
    "Enter your OpenAI API Key",
    type="password",
    help="Required to generate interview questions"
)

# ---------------- USER INPUTS ----------------
level = st.selectbox(
    "Select Level",
    [
        "CA Articleship",
        "CA Industrial Training",
        "CA Fresher",
        "1–3 Years Experience",
        "3–6 Years Experience",
        "6–9 Years Experience"
    ]
)

domain = st.selectbox(
    "Select Domain",
    [
        "Statutory Audit",
        "Internal Audit",
        "Direct Tax",
        "Indirect Tax",
        "Finance",
        "FP&A",
        "Business Finance",
        "M&A Tax",
        "Private Equity",
        "Consulting",
        "Investment Banking",
        "International Taxation",
        "Overall",
        "Other"
    ]
)

question_type = st.selectbox(
    "Select Type of Questions",
    [
        "Mixed",
        "HR Questions",
        "Behavioural Questions",
        "Straightforward Technical Questions",
        "Case Study / Scenario-Based Questions",
        "CV-Based Questions"
    ]
)

job_description = st.text_area(
    "Paste Job Description (Optional)",
    placeholder="Paste job description here if available"
)

sample_answers = st.checkbox("Provide sample / ideal answers")

# ---------------- CV UPLOAD ----------------
uploaded_cv = st.file_uploader(
    "Upload your CV (PDF or DOCX) – optional",
    type=["pdf", "docx"]
)

def extract_cv_text(file):
    text = ""
    if file is not None:
        if file.type == "application/pdf":
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(file)
            for para in doc.paragraphs:
                text += para.text + "\n"
    return text

cv_text = extract_cv_text(uploaded_cv)

generate = st.button("Generate Interview Questions")

# ---------------- AI LOGIC ----------------
if generate:
    if not api_key:
        st.error("Please enter your OpenAI API key.")
    else:
        client = OpenAI(api_key=api_key)

        prompt = f"""
You are a senior Chartered Accountant and interviewer at a top firm in India.

Candidate Profile:
- Level: {level}
- Domain: {domain}

Job Description:
{job_description if job_description else "Not provided"}

Candidate CV Details:
{cv_text if cv_text else "CV not provided"}

Question Type Selected:
{question_type}

Instructions:
- HR Questions: Ask HR, ethics, communication, motivation, culture-fit questions
- Behavioural Questions: Ask STAR-based questions on past experiences
- Straightforward Technical Questions: Ask direct CA technical questions
- Case Study / Scenario-Based Questions: Ask practical interview case studies
- CV-Based Questions: Ask questions strictly from CV (experience, skills, extracurriculars)
- Mixed: Balanced mix of all types

Structure:
- Generate 10 interview questions aligned to the selected type

Rules:
- Keep questions practical and interview-relevant
- Avoid textbook-style theory
- Use Indian CA interview context

Sample Answers:
{"Provide structured, interview-ready answers after each question." if sample_answers else "Do NOT provide sample answers."}
"""

        with st.spinner("Interview in progress..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )

        st.success("Here are your interview questions 👇")
        st.markdown(response.choices[0].message.content)
