from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
from pymongo import MongoClient
import certifi
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client["resume_analyzer"]
analysis_collection = db["analysis"]


def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def analyze_resume(resume_text, job_description):

    skills = [
        "python",
        "sql",
        "machine learning",
        "deep learning",
        "data analysis",
        "pandas",
        "numpy",
        "tensorflow",
        "docker",
        "aws",
    ]

    found = []
    missing = []

    for skill in skills:
        if skill in resume_text.lower():
            found.append(skill)
        else:
            missing.append(skill)

    score = int((len(found) / len(skills)) * 100)

    strengths = "Good alignment with technical skills."
    improvements = "Add missing skills and quantify achievements."

    return {
        "score": score,
        "skills_found": found,
        "missing_skills": missing,
        "strengths": strengths,
        "improvements": improvements,
    }


@app.get("/")
def root():
    return {"message": "AI Resume Analyzer API Running"}


@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    contents = await file.read()

    with open("temp.pdf", "wb") as f:
        f.write(contents)

    resume_text = extract_text_from_pdf("temp.pdf")

    result = analyze_resume(resume_text, job_description)

    record = {
        "score": result["score"],
        "skills_found": result["skills_found"],
        "missing_skills": result["missing_skills"],
        "strengths": result["strengths"],
        "improvements": result["improvements"],
    }

    analysis_collection.insert_one(record)

    return result


@app.get("/history")
def history():
    records = list(analysis_collection.find({}, {"_id": 0}))
    return records