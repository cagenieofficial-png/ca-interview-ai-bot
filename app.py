import streamlit as st
from openai import OpenAI
import PyPDF2

# ---------------- SESSION STATE ----------------
if "asked_questions" not in st.session_state:
    st.session_state.asked_questions = []

if "mock_step" not in st.session_state:
    st.session_state.mock_step = 0

if "mock_scores" not in st.session_state:
    st.session_state.mock_scores = []

# ---------------- CONFIG ----------------
st.set_page_config(page_title="CA Interview AI Platform", layout="centered")
st.title("🎓 CA Interview AI Platform")

# ---------------- MODE SELECTION ----------------
mode = st.radio(
    "What do you want to do?",
    ["Interview Question Practice", "Live Mock Interview (Voice – 3 Questions)"]
)

# ---------------- API KEY ----------------
api_key = st.text_input("Enter your OpenAI API Key", type="password")
client = OpenAI(api_key=api_key) if api_key else None

# ---------------- COMMON INPUTS ----------------
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

# =========================================================
# 🟢 MODE 1: INTERVIEW QUESTION PRACTICE
# =========================================================
if mode == "Interview Question Practice":

    question_type = st.selectbox(
        "Select Question Type",
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

    st.markdown("### Job Description (optional)")
    jd_text = st.text_area("Paste Job Description")
    jd_file = st.file_uploader("OR upload JD PDF", type=["pdf"])

    def extract_pdf(file):
        text = ""
        if file:
            reader = PyPDF2.PdfReader(file)
            for p in reader.pages:
                text += p.extract_text()
        return text

    jd_final = jd_text if jd_text else extract_pdf(jd_file)

    generate = st.button("Generate Interview Questions")

    if generate and client:
        prompt = f"""
You are a senior Chartered Accountant interviewer in India.

Candidate:
Level: {level}
Domain: {domain}

Question Type: {question_type}

Previously Asked Questions (DO NOT repeat):
{st.session_state.asked_questions}

Job Description:
{jd_final if jd_final else "Not provided"}

Rules:
- Do NOT repeat previous questions
- Use practical CA interview standards
- Avoid textbook questions
- Generate a fresh set every time

Generate 8 interview questions.
{"Provide sample answers." if sample_answers else ""}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9
        )

        output = response.choices[0].message.content
        st.markdown(output)
        st.session_state.asked_questions.append(output)

# =========================================================
# 🔵 MODE 2: LIVE MOCK INTERVIEW (FREE VOICE)
# =========================================================
if mode == "Live Mock Interview (Voice – 3 Questions)" and client:

    questions = [
        "Technical Question",
        "Case / Practical Question",
        "Behavioural / HR Question"
    ]

    if st.session_state.mock_step < 3:
        q_type = questions[st.session_state.mock_step]

        q_prompt = f"""
Ask ONE {q_type} for a {level} candidate in {domain}.
Do not give answer.
"""

        question = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": q_prompt}],
            temperature=0.7
        ).choices[0].message.content

        st.markdown(f"### Question {st.session_state.mock_step + 1}")
        st.markdown(question)

        # -------- FREE BROWSER SPEECH TO TEXT --------
        st.markdown("### 🎙️ Speak Your Answer (Free Voice Mode)")

        speech_html = """
        <script>
        var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-IN';
        recognition.interimResults = false;

        function startDictation() {
            recognition.start();
        }

        recognition.onresult = function(event) {
            document.getElementById("speech_output").value =
            event.results[0][0].transcript;
        }
        </script>

        <button onclick="startDictation()">🎙️ Start Recording</button><br><br>
        <textarea id="speech_output" rows="5" style="width:100%;"></textarea>
        """

        st.components.v1.html(speech_html, height=220)

        user_answer = st.text_area(
            "Captured Answer (you can edit before submitting)",
            placeholder="Your spoken answer will appear here..."
        )

        if st.button("Submit Answer"):
            if not user_answer.strip():
                st.error("Please record or type your answer.")
            else:
                eval_prompt = f"""
You are a senior Chartered Accountant interviewer.

Question:
{question}

Candidate Answer:
{user_answer}

Evaluate and provide:
- Score out of 10
- Strengths
- Gaps
- Improvements
- Sample ideal interview answer
"""

                eval_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": eval_prompt}],
                    temperature=0.3
                )

                st.markdown(eval_response.choices[0].message.content)

                st.session_state.mock_scores.append(7)  # placeholder
                st.session_state.mock_step += 1
                st.rerun()

    else:
        avg_score = sum(st.session_state.mock_scores) / len(st.session_state.mock_scores)
        st.success(f"🎯 Mock Interview Completed – Average Score: {avg_score:.1f} / 10")

        if st.button("Start New Mock Interview"):
            st.session_state.mock_step = 0
            st.session_state.mock_scores = []
            st.rerun()
