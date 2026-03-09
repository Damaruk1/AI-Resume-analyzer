from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import pdfplumber
import certifi
import os

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())

db = client["resume_analyzer"]
analysis_collection = db["analysis"]


def extract_text_from_pdf(file_path):

    text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    return text


def analyze_resume(resume_text, job_description):

    resume_words = set(resume_text.lower().split())
    job_words = set(job_description.lower().split())

    matched = resume_words.intersection(job_words)
    missing = job_words.difference(resume_words)

    score = 0
    if len(job_words) > 0:
        score = int((len(matched) / len(job_words)) * 100)

    return {
        "score": score,
        "skills_found": list(matched)[:10],
        "missing_skills": list(missing)[:10],
        "strengths": f"Resume matches {len(matched)} keywords from job description.",
        "improvements": "Add more relevant skills from the job description."
    }


@app.get("/")
def home():
    return {"message": "AI Resume Analyzer API Running"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...), job_description: str = Form(...)):

    contents = await file.read()

    with open("temp_resume.pdf", "wb") as f:
        f.write(contents)

    resume_text = extract_text_from_pdf("temp_resume.pdf")

    result = analyze_resume(resume_text, job_description)

    # Save to MongoDB
    analysis_collection.insert_one(result)

    # IMPORTANT: return only the clean result dictionary
    return {
        "score": result["score"],
        "skills_found": result["skills_found"],
        "missing_skills": result["missing_skills"],
        "strengths": result["strengths"],
        "improvements": result["improvements"]
    }


@app.get("/history")
def history():

    records = list(analysis_collection.find({}, {"_id": 0}))

    return records