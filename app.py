import streamlit as st
from openai import OpenAI
import PyPDF2

# ---------------- SESSION MEMORY ----------------
if "asked_questions" not in st.session_state:
    st.session_state.asked_questions = []

# ---------------- CONFIG ----------------
st.set_page_config(page_title="CA Interview AI Bot", layout="centered")

st.title("🎓 CA Interview Question Generator")
st.subheader("AI-powered interview prep for CA students & professionals")

# ---------------- API KEY ----------------
api_key = st.text_input(
    "Enter your OpenAI API Key",
    type="password"
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

sample_answers = st.checkbox("Provide sample / ideal answers")

# ---------------- JOB DESCRIPTION INPUT ----------------
st.markdown("### Job Description (choose one)")

jd_text = st.text_area(
    "Paste Job Description (optional)",
    placeholder="Paste job description here"
)

jd_file = st.file_uploader(
    "OR upload Job Description PDF (optional)",
    type=["pdf"]
)

def extract_pdf_text(file):
    text = ""
    if file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

jd_final = jd_text if jd_text else extract_pdf_text(jd_file)

# ---------------- CV UPLOAD ----------------
uploaded_cv = st.file_uploader(
    "Upload your CV (PDF – optional)",
    type=["pdf"]
)

def extract_cv_text(file):
    text = ""
    if file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
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
{jd_final if jd_final else "Not provided"}

Candidate CV:
{cv_text if cv_text else "Not provided"}

Question Type Selected:
{question_type}

Previously Asked Questions (DO NOT repeat these):
{st.session_state.asked_questions}

Instructions:
- HR Questions: HR, ethics, communication, motivation
- Behavioural Questions: STAR-based experience questions
- Straightforward Technical Questions: Direct CA technical questions
- Case Study Questions: Practical real-life scenarios
- CV-Based Questions: Ask strictly from CV (work, skills, activities)
- Mixed: Balanced mix of all types

Rules:
- Do NOT repeat any previously asked question
- Keep questions interview-relevant and practical
- Use Indian CA interview context
- Generate a fresh set every time

Structure:
- Generate 8 interview questions

Sample Answers:
{"Provide interview-ready sample answers." if sample_answers else "Do NOT provide sample answers."}
"""

        with st.spinner("Interview in progress..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.9
            )

        output = response.choices[0].message.content
        st.success("Here are your interview questions 👇")
        st.markdown(output)

        # store asked questions
        st.session_state.asked_questions.append(output)
