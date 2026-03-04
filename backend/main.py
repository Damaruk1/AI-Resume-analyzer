from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from model import extract_text_from_pdf, analyze_resume
from database import analysis_collection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Resume Analyzer API running"}


@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    resume_text = extract_text_from_pdf(file.file)

    result = analyze_resume(resume_text, job_description)

    record = {
        "match_score": result["match_score"],
        "missing_skills": result["missing_skills"],
        "created_at": datetime.utcnow()
    }

    analysis_collection.insert_one(record)

    return result


@app.get("/history")
def history():

    records = list(analysis_collection.find({}, {"_id": 0}))

    return records