import io

import streamlit as st

from extractor import extract_resume_text, extract_structured_data
from comparator import compare_resume_to_job, extract_required_skills

st.set_page_config(page_title="CV Screener", layout="centered")
st.title("AI Resume Screener")


@st.cache_data(show_spinner=False)
def get_resume_data(file_bytes: bytes, filename: str) -> dict:
    text = extract_resume_text(io.BytesIO(file_bytes), filename)
    return extract_structured_data(text)


uploaded_file = st.file_uploader("Upload resume (PDF or DOCX)", type=["pdf", "docx"])
job_description = st.text_area("Job description", height=200)

if st.button("Analyze"):
    if not uploaded_file or not job_description:
        st.warning("Please fill in all fields.")
    else:
        with st.spinner("Extracting resume data..."):
            resume_data = get_resume_data(uploaded_file.getvalue(), uploaded_file.name)

        with st.spinner("Extracting job requirements..."):
            required_skills = extract_required_skills(job_description)

        with st.spinner("Analyzing match..."):
            result = compare_resume_to_job(resume_data, job_description, required_skills)

        st.subheader("Match Score")
        col1, col2 = st.columns(2)
        col1.metric("Skill Overlap", f"{result['math_overlap_score']}%")
        col2.metric("Final Score", f"{result['final_match_score']}%")

        st.subheader("Matched Skills")
        st.write(", ".join(result["matched_skills"]) or "None")

        st.subheader("Missing Skills")
        st.write(", ".join(result["missing_skills"]) or "None")

        st.subheader("Strengths")
        for s in result["strengths"]:
            st.write(f"- {s}")

        st.subheader("Gaps")
        for g in result["gaps"]:
            st.write(f"- {g}")

        st.subheader("Recommendation")
        st.info(result["recommendation"])

        with st.expander("Extracted Resume Data"):
            st.json(resume_data)

        with st.expander("Extracted Job Requirements"):
            st.json(required_skills)