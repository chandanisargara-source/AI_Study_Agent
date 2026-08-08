import shutil
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List

# આપણી ફાઇલોમાંથી ફંક્શન્સ ઇમ્પોર્ટ કરો
from resume_analyzer import extract_resume_text
from interview import generate_questions
from evaluator import evaluate_answers
from database.database import engine, Base
from auth.router import router as auth_router
from users.router import router as user_router

app = FastAPI(title="AI Interview Agent API")


# Database tables create
Base.metadata.create_all(bind=engine)

# Authentication routes
app.include_router(auth_router)
app.include_router(user_router)

# ટેમ્પરરી સ્ટોરેજ
interview_session = {
    "candidate_name": "",
    "job_role": "",
    "questions": [],
    "answers": []
}

class AnswerInput(BaseModel):
    question: str
    answer: str

class InterviewSubmission(BaseModel):
    name: str
    role: str
    answers: List[AnswerInput]

@app.get("/")
def home():
    return {"message": "AI Interview Agent Backend Running Successfully"}

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...), name: str = "Candidate", role: str = "Developer"):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    file_path = f"temp_{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # ૧. રેઝ્યૂમે ટેક્સ્ટ મેળવો
        resume_text = extract_resume_text(file_path)
        
        # ૨. Gemini પાસે પ્રશ્નો મંગાવો
        raw_questions = generate_questions(resume_text)
        
        # 3. પ્રશ્નોને લિસ્ટમાં કન્વર્ટ કરો (સાફ-સફાઈ લોજિક)
        questions = []
        if raw_questions and isinstance(raw_questions, str):
            questions = [q.strip() for q in raw_questions.strip().split("\n") if q.strip()]
            questions = [q.lstrip("0123456789.- ") for q in questions]
            
        # જો કોઈ કારણસર Gemini પ્રશ્નો ન આપે, તો જ બેકઅપ પ્રશ્નો આવશે
        if not questions:
            questions = [
                f"Tell me about your experience as a {role}.",
                "What are your core technical strengths?",
                "Describe a challenging project you worked on.",
                "How do you keep your technical skills updated?",
                "Why do you think you are a good fit for this role?"
            ]
            
        questions = questions[:5]  # ફક્ત 5 પ્રશ્નો રાખવા
        
        interview_session["candidate_name"] = name
        interview_session["job_role"] = role
        interview_session["questions"] = questions
        
        return {
            "filename": file.filename,
            "candidate_name": name,
            "job_role": role,
            "questions": questions
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@app.post("/submit-interview")
def submit_interview(submission: InterviewSubmission):
    formatted_answers = [
        {
            "question": item.question, 
            "answer": item.answer
        }
         for item in submission.answers
    ]
    evaluation_result = evaluate_answers(formatted_answers)

    total_score = evaluation_result["total_score"]
    max_score = evaluation_result["max_score"]
    percentage = evaluation_result["percentage"]
    recommendation = evaluation_result["recommendation"]
    feedback_report = evaluation_result["feedback_report"]
    
    result_status = recommendation
        
    return {
        "candidate_name": submission.name,
        "job_role": submission.role,

        "total_score": total_score,
        "max_score": max_score,

        "percentage": f"{percentage:.2f}%",

        "status": result_status,

        "recommendation": recommendation,

        "detailed_feedback": feedback_report
    }