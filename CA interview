import streamlit as st
from openai import OpenAI

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
        client = OpenAI(api_key=api_key)

        prompt = f"""
You are a senior Chartered Accountant and interviewer at a Big 4 firm in India.

Candidate Profile:
- Level: {level}
- Domain: {domain}

Job Description:
{job_description if job_description else "No job description provided. Use domain-based questioning."}

Task:
Generate interview questions relevant to Indian CA interviews.

Structure:
1. 5 technical questions
2. 3 practical / scenario-based questions
3. 2 conceptual or judgment-based questions

Rules:
- Questions must be practical and interview-relevant
- Avoid generic textbook questions
- Focus on real-world CA exposure

Sample Answers:
{"Provide structured, interview-ready sample answers after each question." if sample_answers else "Do NOT provide sample answers."}
"""

        with st.spinner("Interview in progress..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

        st.success("Here are your interview questions 👇")
        st.markdown(response.choices[0].message.content)
