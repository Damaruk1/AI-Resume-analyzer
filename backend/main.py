from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import pdfplumber
import certifi
import os

app = FastAPI()

# Allow frontend access
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

    common = resume_words.intersection(job_words)
    missing = job_words.difference(resume_words)

    if len(job_words) == 0:
        score = 0
    else:
        score = int((len(common) / len(job_words)) * 100)

    return {
        "score": score,
        "skills_found": list(common)[:10],
        "missing_skills": list(missing)[:10],
        "strengths": f"Resume matches {len(common)} relevant keywords.",
        "improvements": "Add more keywords from the job description."
    }


@app.get("/")
def root():
    return {"message": "AI Resume Analyzer API Running"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...), job_description: str = Form(...)):

    contents = await file.read()

    with open("temp.pdf", "wb") as f:
        f.write(contents)

    resume_text = extract_text_from_pdf("temp.pdf")

    result = analyze_resume(resume_text, job_description)

    # store in MongoDB
    analysis_collection.insert_one(result)

    # IMPORTANT: return only the result (no ObjectId)
    return result


@app.get("/history")
def history():

    records = list(analysis_collection.find({}, {"_id": 0}))
    return records