from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import pdfplumber
import certifi
import os

app = FastAPI()

# Allow frontend requests
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


# Extract text from PDF
def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
    return text


# Resume analysis logic
def analyze_resume(resume_text, job_description):

    resume_words = set(resume_text.lower().split())
    job_words = set(job_description.lower().split())

    common_skills = resume_words.intersection(job_words)
    missing_skills = job_words.difference(resume_words)

    if len(job_words) == 0:
        score = 0
    else:
        score = int((len(common_skills) / len(job_words)) * 100)

    strengths = f"Resume matches {len(common_skills)} relevant keywords from the job description."

    improvements = "Consider adding these missing keywords: " + ", ".join(list(missing_skills)[:10])

    return {
        "score": score,
        "skills_found": list(common_skills)[:10],
        "missing_skills": list(missing_skills)[:10],
        "strengths": strengths,
        "improvements": improvements
    }


@app.get("/")
def root():
    return {"message": "AI Resume Analyzer API Running"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...), job_description: str = Form(...)):

    contents = await file.read()

    with open("temp_resume.pdf", "wb") as f:
        f.write(contents)

    resume_text = extract_text_from_pdf("temp_resume.pdf")

    result = analyze_resume(resume_text, job_description)

    analysis_collection.insert_one(result)

    return result


@app.get("/history")
def history():
    records = list(analysis_collection.find({}, {"_id": 0}))
    return records