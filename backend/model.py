import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def extract_text_from_pdf(file):

    text = ""

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:
            text += page.extract_text()

    return text


def analyze_resume(resume_text, job_description):

    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer(stop_words="english")

    vectors = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]

    resume_words = set(resume_text.lower().split())
    job_words = set(job_description.lower().split())

    missing_skills = list(job_words - resume_words)

    return {
        "match_score": round(similarity * 100,2),
        "missing_skills": missing_skills[:10]
    }