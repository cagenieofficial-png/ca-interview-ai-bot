import streamlit as st
import openai

# ---------------- CONFIG ----------------
st.set_page_config(page_title="CA Interview AI Bot", layout="centered")

st.title("🎓 CA Interview Question Generator")
st.subheader("Your personal AI interviewer for CA roles")

# ---------------- API KEY ----------------
api_key = st.text_input(
    "Enter your OpenAI API Key",
    type="password",
    help="This key is required to generate questions"
)

# ---------------- USER INPUTS ----------------
domain = st.selectbox(
    "Select Domain",
    [
        "Statutory Audit",
        "Internal Audit",
        "Direct Tax",
        "GST",
        "Financial Due Diligence (FDD)",
        "FP&A / Corporate Finance",
        "Other"
    ]
)

question_type = st.selectbox(
    "Select Question Type",
    [
        "Mixed",
        "HR Questions",
        "Behavioural Questions",
        "Straightforward Technical Questions",
        "Case Study / Scenario-Based Questions"
    ]
)

level = st.selectbox(
    "Select Level",
    [
        "CA Final Student",
        "Fresher Chartered Accountant",
        "1–3 Years Experience",
        "3–6 Years Experience"
    ]
)

job_description = st.text_area(
    "Paste Job Description (Optional)",
    placeholder="Paste the JD here if you have one..."
)

sample_answers = st.checkbox("Provide sample / ideal answers")

generate = st.button("Generate Interview Questions")

# ---------------- AI LOGIC ----------------
if generate:
    if not api_key:
        st.error("Please enter your OpenAI API key.")
    else:
        openai.api_key = api_key

        prompt = f"""
You are a senior Chartered Accountant and interviewer at a Big 4 firm in India.

Candidate Profile:
- Level: {level}
- Domain: {domain}

Job Description:
{job_description if job_description else "No job description provided. Use domain-based questioning."}

Question Type Selected:
{question_type}

Instructions based on Question Type:
- HR Questions: Ask only HR, personality, ethics, communication, and culture-fit questions.
- Behavioural Questions: Ask STAR-based behavioural questions.
- Straightforward Technical Questions: Ask direct CA technical questions.
- Case Study / Scenario-Based Questions: Ask practical interview case studies.
- Mixed: Balanced mix of HR, technical, behavioural, and case-based questions.

Structure:
- 5 Technical Questions
- 4 Practical / Scenario-Based Questions
- 3 Conceptual or Judgment-Based Questions

Rules:
- Questions must be practical and interview-relevant
- Avoid textbook-style questions
- Match Indian CA interview standards

Sample Answers:
{"Provide structured interview-ready answers after each question." if sample_answers else "Do NOT provide sample answers."}
"""

        with st.spinner("Interview in progress..."):
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )

        st.success("Here are your interview questions 👇")
        st.markdown(response["choices"][0]["message"]["content"])
