from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from model import extract_text_from_pdf, analyze_resume
from database import analysis_collection

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def home():
    return {"message": "AI Resume Analyzer API Running"}


# Resume analysis endpoint
@app.post("/analyze")
async def analyze(resume: UploadFile = File(...), job_description: str = Form(...)):

    # Extract resume text
    resume_text = extract_text_from_pdf(resume.file)

    # Run analysis
    result = analyze_resume(resume_text, job_description)

    # Save result to MongoDB
    record = {
        "match_score": result["match_score"],
        "ats_score": result["ats_score"],
        "resume_skills": result["resume_skills"],
        "missing_skills": result["missing_skills"],
        "strengths": result["strengths"],
        "improvements": result["improvements"]
    }

    analysis_collection.insert_one(record)

    return result


# History endpoint
@app.get("/history")
def history():

    records = list(analysis_collection.find({}, {"_id": 0}))

    return records
