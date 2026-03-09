import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from skills_db import SKILLS_DB, ACTION_VERBS


def extract_text_from_pdf(file):

    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    return text.lower()


def extract_skills(text):

    skills_found = []

    for skill in SKILLS_DB:
        if skill in text:
            skills_found.append(skill)

    return list(set(skills_found))


def compute_similarity(resume, job):

    vectorizer = TfidfVectorizer(stop_words="english")

    vectors = vectorizer.fit_transform([resume, job])

    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]

    return round(similarity * 100, 2)


def analyze_resume(resume_text, job_description):

    resume_skills = extract_skills(resume_text)

    job_skills = extract_skills(job_description)

    missing_skills = list(set(job_skills) - set(resume_skills))

    match_score = compute_similarity(resume_text, job_description)

    improvements = []
    strengths = []

    word_count = len(resume_text.split())

    if word_count < 300:
        improvements.append("Resume is too short. Add more details about projects and experience.")

    if word_count > 1000:
        improvements.append("Resume is too long. Keep it within 1 page.")

    if "-" not in resume_text and "•" not in resume_text:
        improvements.append("Use bullet points in experience section.")

    verb_found = any(v in resume_text for v in ACTION_VERBS)

    if not verb_found:
        improvements.append("Use strong action verbs like developed, built, implemented.")

    if len(resume_skills) > 5:
        strengths.append("Good technical skill coverage")

    if match_score > 70:
        strengths.append("Strong match with job requirements")

    ats_score = round((match_score * 0.6) + ((len(resume_skills)/10)*40),2)

    return {
        "match_score": match_score,
        "ats_score": ats_score,
        "resume_skills": resume_skills,
        "missing_skills": missing_skills,
        "strengths": strengths,
        "improvements": improvements
    }
