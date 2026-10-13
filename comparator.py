import json

from llm import generate_json


REQUIRED_SKILLS_SCHEMA = {
    "type": "object",
    "properties": {"required_skills": {"type": "array", "items": {"type": "string"}}},
    "required": ["required_skills"],
}


def extract_required_skills(job_description: str) -> list:
    result = generate_json(
        "Extract only what the candidate must have or be able to do, based on this "
        "job description: technical skills, tools, domain knowledge, qualifications, "
        "and experience level. "
        "Do not include benefits, training, mentorship, rotations, or anything the "
        "employer offers to the candidate. "
        "Use only what is explicitly stated in the text. Do not add examples, "
        "tools, or technologies that are not mentioned. "
        "Exclude soft skills, personality traits, and mindset statements. "
        "Return at most 12 items, each a short keyword or phrase:\n\n"
        f"{job_description}",
        REQUIRED_SKILLS_SCHEMA,
    )
    return result["required_skills"]


MATCH_SCHEMA = {
    "type": "object",
    "properties": {
        "matched": {"type": "array", "items": {"type": "string"}},
        "missing": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["matched", "missing"],
}


def calculate_skill_overlap(resume_data: dict, required_skills: list) -> dict:
    if not required_skills:
        return {"overlap_score": 0, "matched_skills": [], "missing_skills": []}

    evidence = {
        "skills": resume_data.get("skills", []),
        "experience": [
            e.get("description", "") for e in resume_data.get("work_experience", [])
        ],
        "certifications": resume_data.get("certifications", []),
    }

    prompt = f"""
Candidate evidence (JSON):
{json.dumps(evidence, ensure_ascii=False, indent=2)}

Required items:
{json.dumps(required_skills, ensure_ascii=False)}

For each required item, decide whether the candidate's evidence clearly supports it,
either as an explicit skill or through described experience or certifications.
Treat synonyms and abbreviations as the same (for example NLP and Natural Language Processing).
Copy each required item exactly as written into either "matched" or "missing".
Do not add, rename, or omit items.
"""
    result = generate_json(prompt, MATCH_SCHEMA)

    matched_set = {s.strip().lower() for s in result["matched"]}
    matched = [s for s in required_skills if s.strip().lower() in matched_set]
    missing = [s for s in required_skills if s not in matched]
    overlap_score = round(len(matched) / len(required_skills) * 100, 1)

    return {
        "overlap_score": overlap_score,
        "matched_skills": matched,
        "missing_skills": missing,
    }


ANALYSIS_SCHEMA = {
    "type": "object",
    "properties": {
        "final_match_score": {"type": "number"},
        "strengths": {"type": "array", "items": {"type": "string"}},
        "gaps": {"type": "array", "items": {"type": "string"}},
        "recommendation": {"type": "string"},
    },
    "required": ["final_match_score", "strengths", "gaps", "recommendation"],
}


def analyze_match(resume_data: dict, job_description: str, overlap_result: dict) -> dict:
    prompt = f"""
You are a recruiting expert. Given:

Resume data (JSON):
{json.dumps(resume_data, ensure_ascii=False, indent=2)}

Job description:
{job_description}

Preliminary skill match calculation:
- Math overlap score: {overlap_result['overlap_score']}%
- Matched skills: {overlap_result['matched_skills']}
- Missing skills: {overlap_result['missing_skills']}

Use the overlap score as a starting point. Adjust it based on context: relevant
experience or projects that imply a missing skill even if not named directly, and
whether matched skills are core or secondary to the role.

Base your assessment only on what the candidate is required to have. Ignore
benefits or training offered by the employer. Do not infer seniority level or
tools that are not mentioned in the job description.

Return a single final match score (0-100) along with strengths, gaps, and a
recommendation.
"""
    return generate_json(prompt, ANALYSIS_SCHEMA)


def compare_resume_to_job(resume_data: dict, job_description: str, required_skills: list) -> dict:
    overlap_result = calculate_skill_overlap(resume_data, required_skills)
    analysis = analyze_match(resume_data, job_description, overlap_result)

    return {
        "math_overlap_score": overlap_result["overlap_score"],
        "final_match_score": analysis["final_match_score"],
        "matched_skills": overlap_result["matched_skills"],
        "missing_skills": overlap_result["missing_skills"],
        "strengths": analysis["strengths"],
        "gaps": analysis["gaps"],
        "recommendation": analysis["recommendation"],
    }