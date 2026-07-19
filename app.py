import streamlit as st
from PyPDF2 import PdfReader
from groq import Groq
from io import BytesIO
from reportlab.pdfgen import canvas
import re
def load_css():
    with open("style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide"
)
# ==========================
# HEADER
# ==========================
# HERO HEADER IMAGE
st.image(
    "assets/hero-banner.png",
    use_container_width=True
)

# Resume Upload
st.markdown("""
<div style="
text-align:center;
margin-bottom:15px;
">

<div style="
font-size:32px;
font-weight:700;
color:white;
">
📄 Upload Your Resume
</div>

<div style="
font-size:15px;
color:#94A3B8;
margin-top:5px;
">
Get ATS analysis, career insights and interview preparation
</div>

</div>
""", unsafe_allow_html=True)

# FIR YE AAYEGA 👇👇👇

resume = st.file_uploader(
    "",
    type=["pdf"],
    label_visibility="collapsed"
)
if resume:

    st.success("✅ Resume Uploaded Successfully")

    reader = PdfReader(resume)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    with st.expander("📋 View Extracted Resume Text"):
        st.text_area(
            "",
            text,
            height=250
        )
    # ==========================
    # SKILLS DETECTION
    # ==========================
    skills = [
        "Python",
        "SQL",
        "Excel",
        "Power BI",
        "Tableau",
        "Pandas",
        "NumPy",
        "Machine Learning",
        "HTML",
        "CSS",
        "JavaScript",
        "Git",
        "MySQL"
    ]

    found_skills = []

    for skill in skills:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    st.subheader(
    f"🎯 Skills Found ({len(found_skills)})"
)

    if found_skills:

        badges = ""

        for skill in found_skills:
            badges += f"""
            <span class="skill-badge">{skill}</span>
            """

        st.markdown(badges, unsafe_allow_html=True)

    else:
        st.warning("No skills detected")
         # ==========================
    # JOB DESCRIPTION MATCHER
    # ==========================

    st.divider()

    st.subheader("💼 Job Description Matcher")

    job_description = st.text_area(
        "Paste Job Description Here",
        height=200
    )

    if job_description:

        matched = []
        missing = []

        for skill in skills:

            if skill.lower() in job_description.lower():

                if skill in found_skills:
                    matched.append(skill)
                else:
                    missing.append(skill)

        total = len(matched) + len(missing)

        match_score = (
            int((len(matched) / total) * 100)
            if total > 0 else 0
        )

        st.subheader("📈 Resume Match Score")

        st.progress(match_score / 100)

        st.metric(
            "Match Score",
            f"{match_score}%"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✅ Matched Skills")

            for skill in matched:
                st.success(skill)

        with col2:
            st.subheader("❌ Missing Skills")

            for skill in missing:
                st.error(skill)
                    # ==========================
    # AI CAREER ADVISOR
    # ==========================

    st.divider()

    st.subheader("🤖 AI Resume Analysis")

    if st.button("🚀 Analyze Resume with AI"):

        try:

            client = Groq(
                api_key=st.secrets["GROQ_API_KEY"]
            )

            prompt = f"""
You are an expert ATS Resume Reviewer and Career Coach.

Analyze the following resume and identify the candidate's domain
(Software Development, Data Analytics, HR, Marketing, Finance,
Mechanical Engineering, Civil Engineering, Healthcare, Education, etc.).

Provide:

1. Candidate Domain
2. Professional Summary
3. Top Strengths
4. Weaknesses
5. Missing Skills relevant to their domain
6. ATS Optimization Suggestions
7. Top 5 Suitable Career Roles
8. Career Growth Recommendations
9. ATS Score (0-100)
10. ATS Score Explanation

Give the response in a professional and structured format.
"""

            with st.spinner("Analyzing Resume..."):

                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

            result = completion.choices[0].message.content

            st.success("Analysis Completed ✅")

            # ATS Score Extract
            ats_score = 0

            match = re.search(
                r'ATS Score[^0-9]*(\d+)',
                result,
                re.IGNORECASE
            )

            if match:
                ats_score = int(match.group(1))

            # ATS Dashboard
            if ats_score > 0:

                st.subheader("📊 ATS Score")

                st.progress(ats_score / 100)

                st.metric(
                    "ATS Score",
                    f"{ats_score}/100"
                )

            st.markdown(result)

            # PDF Report Download
            pdf_buffer = BytesIO()

            p = canvas.Canvas(pdf_buffer)

            y = 800

            for line in result.split("\n"):
                p.drawString(40, y, line[:100])
                y -= 20
                if y < 50:
                    p.showPage()
                    y = 800

            p.save()
            pdf_buffer.seek(0)

            st.download_button(
                label="📄 Download Analysis Report",
                data=pdf_buffer,
                file_name="CareerPilot_Report.pdf",
                mime="application/pdf"
            )

        except Exception as e:

            st.error(f"Error: {e}")

        st.divider()

    st.subheader("🎤 Interview Questions Generator")

    if st.button("Generate Interview Questions"):

        try:

            client = Groq(
                api_key=st.secrets["GROQ_API_KEY"]
            )

            prompt = f"""
Based on this resume:

{text}

Identify the candidate's domain automatically.

Generate:

1. 10 domain-specific technical questions
2. 5 HR interview questions
3. Suggested answers
4. Difficulty level (Easy/Medium/Hard)

Keep questions relevant to the candidate's background.
"""

            with st.spinner("Generating Questions..."):

                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                questions = completion.choices[0].message.content

                st.success("Questions Generated ✅")

                st.markdown(questions)

        except Exception as e:

            st.error(f"Error: {e}")
        st.divider()

    st.subheader("💼 Recommended Job Roles")

col1, col2, col3 = st.columns([3,2,3])

with col2:

    if st.button("🎯 Career Recommendations"):

        try:

            client = Groq(
                api_key=st.secrets["GROQ_API_KEY"]
            )

            prompt = f"""
Analyze this resume:

{text}

Identify the candidate's domain.

Recommend:

1. Top 5 Suitable Job Roles
2. Why each role matches
3. Expected Fresher Salary Range
4. Skills to improve
5. Career Growth Path

Provide realistic recommendations.
"""

            with st.spinner("Finding Best Roles..."):

                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                jobs = completion.choices[0].message.content

                st.success("Recommendations Ready ✅")

                st.markdown(jobs)

        except Exception as e:

            st.error(f"Error: {e}")

st.markdown("---")

# 🔗 LinkedIn Summary Generator

st.subheader("🔗 LinkedIn Summary Generator")

if st.button("Generate LinkedIn Summary"):

    try:

        client = Groq(
            api_key=st.secrets["GROQ_API_KEY"]
        )

        prompt = f"""
Based on this resume:

{text}

Create a professional LinkedIn About section.

Requirements:
- Professional tone
- 150 to 250 words
- Highlight strengths and skills
- Suitable for recruiters
"""

        with st.spinner("Generating LinkedIn Summary..."):

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            linkedin_summary = completion.choices[0].message.content

            st.success("LinkedIn Summary Generated ✅")

            st.markdown(linkedin_summary)

    except Exception as e:

        st.error(f"Error: {e}")
        st.divider()

st.subheader("📄 Cover Letter Generator")

job_role = st.text_input(
    "Enter Target Job Role",
    placeholder="Example: Data Analyst"
)

if st.button("Generate Cover Letter"):

    try:

        client = Groq(
            api_key=st.secrets["GROQ_API_KEY"]
        )

        prompt = f"""
Based on this resume:

{text}

Generate a professional cover letter for the role:

{job_role}

Requirements:
- Professional tone
- Fresher friendly
- 250-350 words
- Ready to send to recruiters
"""

        with st.spinner("Generating Cover Letter..."):

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            cover_letter = completion.choices[0].message.content

            st.success("Cover Letter Generated ✅")

            st.markdown(cover_letter)

    except Exception as e:

        st.error(f"Error: {e}")

st.divider()

if "show_chat" not in st.session_state:
    st.session_state.show_chat = False

if st.button("🤖 AI Assistant"):
    st.session_state.show_chat = not st.session_state.show_chat

if st.session_state.show_chat:

    st.subheader("🤖 Resume AI Assistant")

    user_query = st.text_input(
        "",
        placeholder="💬 Ask anything about your resume..."
    )

    if st.button("🚀 Ask AI"):

        if user_query:

            try:

                client = Groq(
                    api_key=st.secrets["GROQ_API_KEY"]
                )

                prompt = f"""
You are an expert Resume Coach and Career Advisor.

If a resume is uploaded, use it for personalized advice.
If no resume is uploaded, still answer the question professionally.

User Question:

{user_query}

Give practical, detailed and professional guidance.
"""

                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                answer = completion.choices[0].message.content

                st.markdown(answer)

            except Exception as e:

                st.error(f"Error: {e}")
st.markdown("""
<div style="
text-align:center;
color:#94A3B8;
font-size:14px;
padding:10px 0px 5px 0px;
">
CareerPilot AI © 2026 | Developed by Ashutosh Kumar
</div>
""", unsafe_allow_html=True)
