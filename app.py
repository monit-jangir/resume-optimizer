import streamlit as st
import fitz  # PyMuPDF
from openai import OpenAI
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# ========== Setup Mistral API ==========
client = OpenAI(
    api_key="CIPZjAc7pvxFnPWXGKV9npDS4jgwNG0x",  # 🔐 Replace with your Mistral API Key
    base_url="https://api.mistral.ai/v1"
)

# ========== Utility Functions ==========

def extract_text_from_pdf(uploaded_file):
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        return "".join([page.get_text() for page in doc])

def generate_pdf_reportlab(text):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(temp_file.name, pagesize=letter)
    text_object = c.beginText(40, 750)
    text_object.setFont("Helvetica", 12)
    for line in text.split("\n"):
        text_object.textLine(line)
    c.drawText(text_object)
    c.save()
    return temp_file.name

# ========== Streamlit UI ==========
st.set_page_config(page_title="Resume Optimizer Agent", layout="wide")
st.title("Resume Optimizer Agent")
st.markdown("Upload your resume and paste a job description to get personalized feedback, score, and interview readiness insights.")

resume_file = st.file_uploader("📄 Upload Resume (PDF)", type="pdf")
jd_text = st.text_area("📝 Paste Job Description")

resume_text = ""
tailored_resume = st.session_state.get("tailored_resume", "")

if resume_file and jd_text:
    resume_text = extract_text_from_pdf(resume_file)

    # ====== Resume Feedback Analysis ======
    prompt_feedback = f"""
You are an expert Resume Evaluator AI.

Compare the resume and job description below:

Resume:
{resume_text}

Job Description:
{jd_text}

Provide:
- ✅ Skills matched
- ❌ Skills missing
- 💡 Suggestions to improve the resume
"""
    # ====== Resume Score Evaluation ======
    prompt_score = f"""
As a resume evaluation AI, score this resume for the job description below.

Give a score from 0 to 100 based on skill match, keywords, experience relevance, and formatting.

Resume:
{resume_text}

Job Description:
{jd_text}

Format:
**Score:** /100
**Reasoning:** ...
"""

    if st.button("🔍 Analyze Resume"):
        with st.spinner("Analyzing using Mistral..."):
            try:
                # Feedback Section
                response = client.chat.completions.create(
                    model="mistral-medium",
                    messages=[
                        {"role": "system", "content": "You are a career expert and resume reviewer."},
                        {"role": "user", "content": prompt_feedback}
                    ],
                    temperature=0.7
                )
                feedback = response.choices[0].message.content

                st.markdown("### Resume Feedback")
                st.write(feedback)

                st.download_button("📥 Download Feedback (TXT)", feedback, file_name="resume_feedback.txt", mime="text/plain")

                # Score Section
                score_response = client.chat.completions.create(
                    model="mistral-medium",
                    messages=[
                        {"role": "system", "content": "You are an expert resume evaluator."},
                        {"role": "user", "content": prompt_score}
                    ],
                    temperature=0.3
                )
                score_output = score_response.choices[0].message.content
                st.markdown("### Resume Score")
                st.markdown(score_output)

            except Exception as e:
                st.error(f"❌ Error: {e}")

    # ====== Tailored Resume Generator ======
    st.markdown("---")
    st.subheader("Generate Tailored Resume")

    if st.button("Create Tailored Resume"):
        with st.spinner("Crafting tailored resume using Mistral..."):
            try:
                tailored_prompt = f"""
You are a professional resume writer.

Using the resume and job description below, rewrite the resume to be tailored for the job.

Resume:
{resume_text}

Job Description:
{jd_text}

Your output should be a complete, improved resume in professional tone and formatting.
Include: Summary, Skills, Experience, Education (based on what you extract from the original).
Use keywords from the JD where appropriate. DO NOT fabricate false information.
"""

                response_tailored = client.chat.completions.create(
                    model="mistral-medium",
                    messages=[
                        {"role": "system", "content": "You are an expert AI resume writer."},
                        {"role": "user", "content": tailored_prompt}
                    ],
                    temperature=0.7
                )

                tailored_resume = response_tailored.choices[0].message.content
                st.session_state["tailored_resume"] = tailored_resume

                st.markdown("### 📄 Tailored Resume")
                st.text_area("📋 View Tailored Resume", tailored_resume, height=400)

                tailored_pdf_path = generate_pdf_reportlab(tailored_resume)
                st.download_button(
                    label="📥 Download Tailored Resume (PDF)",
                    data=open(tailored_pdf_path, "rb"),
                    file_name="Tailored_Resume.pdf",
                    mime="application/pdf"
                )

            except Exception as e:
                st.error(f"❌ Error: {e}")

# ====== Interview Readiness Analyzer ======
st.markdown("---")
st.subheader("Interview Readiness Analyzer")

if st.session_state.get("tailored_resume"):
    if st.button("🎤 Generate Interview Questions"):
        with st.spinner("Generating interview questions..."):
            try:
                interview_prompt = f"""
You are an expert career coach and technical interviewer.

Based on the tailored resume and job description below, generate:
- 5 behavioral interview questions 
- 5 technical interview questions 
that the candidate is likely to be asked.

Tailored Resume:
{st.session_state['tailored_resume']}

Job Description:
{jd_text}

Format your response like:

**Behavioral Questions:**
1. ...
2. ...
...

**Technical Questions:**
1. ...
2. ...
...
"""

                interview_response = client.chat.completions.create(
                    model="mistral-medium",
                    messages=[
                        {"role": "system", "content": "You are a professional interview coach."},
                        {"role": "user", "content": interview_prompt}
                    ],
                    temperature=0.6
                )

                interview_qs = interview_response.choices[0].message.content

                st.markdown("### 📋 Interview Questions")
                st.markdown(interview_qs)

                st.download_button(
                    label="📥 Download Questions (TXT)",
                    data=interview_qs,
                    file_name="Interview_Questions.txt",
                    mime="text/plain"
                )

                pdf_q_path = generate_pdf_reportlab(interview_qs)
                st.download_button(
                    label="📥 Download Questions (PDF)",
                    data=open(pdf_q_path, "rb"),
                    file_name="Interview_Questions.pdf",
                    mime="application/pdf"
                )

            except Exception as e:
                st.error(f"❌ Error generating questions: {e}")
else:
    st.info("⚠️ Generate the tailored resume first to access interview questions.")
