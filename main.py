import shutil
import os

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

from pydantic import BaseModel

from typing import List

from resume_analyzer import extract_resume_text

from interview import generate_questions

from evaluator import evaluate_answers

from database.database import (
    engine,
    Base
)

from auth.router import router as auth_router

from users.router import router as user_router


# =========================================================
# APP
# =========================================================

app = FastAPI(
    title="AI Interview Agent API"
)


# =========================================================
# DATABASE
# =========================================================

Base.metadata.create_all(
    bind=engine
)


# =========================================================
# AUTH ROUTES
# =========================================================

app.include_router(
    auth_router
)

app.include_router(
    user_router
)


# =========================================================
# TEMP INTERVIEW SESSION
# =========================================================

interview_session = {

    "candidate_name": "",

    "job_role": "",

    "language": "English",

    "questions": [],

    "answers": []
}


# =========================================================
# MODELS
# =========================================================

class AnswerInput(BaseModel):

    question: str

    answer: str


class InterviewSubmission(BaseModel):

    name: str

    role: str

    answers: List[AnswerInput]


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message":
        "AI Interview Agent Backend Running Successfully"
    }


# =========================================================
# UPLOAD RESUME
# =========================================================

@app.post("/upload-resume")
async def upload_resume(

    file: UploadFile = File(...),

    name: str = "Candidate",

    role: str = "Developer",

    language: str = "English"

):

    # -----------------------------------------------------
    # Validate PDF
    # -----------------------------------------------------

    if not file.filename.lower().endswith(
        ".pdf"
    ):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )


    # -----------------------------------------------------
    # Supported languages
    # -----------------------------------------------------

    supported_languages = [

        "English",

        "Gujarati",

        "Hindi",

        "Marathi",

        "Bengali",

        "Tamil",

        "Telugu"
    ]


    if language not in supported_languages:

        language = "English"


    # -----------------------------------------------------
    # Temporary file
    # -----------------------------------------------------

    file_path = f"temp_{file.filename}"


    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )


    try:

        # =================================================
        # 1. EXTRACT RESUME
        # =================================================

        resume_text = extract_resume_text(
            file_path
        )


        # =================================================
        # 2. GENERATE QUESTIONS
        # =================================================

        raw_questions = generate_questions(

            resume_text,

            language
        )


        # =================================================
        # 3. CLEAN QUESTIONS
        # =================================================

        questions = []


        if (
            raw_questions
            and
            isinstance(
                raw_questions,
                str
            )
        ):

            lines = raw_questions.strip().split(
                "\n"
            )


            for question in lines:

                question = question.strip()


                if not question:

                    continue


                # Remove common numbering

                question = question.lstrip(
                    "0123456789.-) "
                )


                if question:

                    questions.append(
                        question
                    )


        # =================================================
        # FALLBACK QUESTIONS
        # =================================================

        if not questions:

            if language == "Gujarati":

                questions = [

                    f"તમારા {role} સંબંધિત અનુભવ વિશે જણાવો.",

                    "તમારી મુખ્ય ટેકનિકલ કુશળતાઓ કઈ છે?",

                    "તમે કરેલા કોઈ પડકારજનક પ્રોજેક્ટ વિશે જણાવો.",

                    "તમે તમારી ટેકનિકલ કુશળતાઓ કેવી રીતે અપડેટ રાખો છો?",

                    "તમને આ ભૂમિકા માટે યોગ્ય ઉમેદવાર કેમ માનો છો?"
                ]


            elif language == "Hindi":

                questions = [

                    f"अपने {role} से संबंधित अपने अनुभव के बारे में बताइए।",

                    "आपकी मुख्य तकनीकी क्षमताएँ क्या हैं?",

                    "आपने जिस चुनौतीपूर्ण प्रोजेक्ट पर काम किया उसके बारे में बताइए।",

                    "आप अपनी तकनीकी क्षमताओं को कैसे अपडेट रखते हैं?",

                    "आप इस भूमिका के लिए खुद को सही उम्मीदवार क्यों मानते हैं?"
                ]


            else:

                questions = [

                    f"Tell me about your experience as a {role}.",

                    "What are your core technical strengths?",

                    "Describe a challenging project you worked on.",

                    "How do you keep your technical skills updated?",

                    "Why do you think you are a good fit for this role?"
                ]


        # =================================================
        # ONLY 5 QUESTIONS
        # =================================================

        questions = questions[:5]


        # =================================================
        # SAVE SESSION
        # =================================================

        interview_session[
            "candidate_name"
        ] = name


        interview_session[
            "job_role"
        ] = role


        interview_session[
            "language"
        ] = language


        interview_session[
            "questions"
        ] = questions


        # =================================================
        # RESPONSE
        # =================================================

        return {

            "filename":
            file.filename,

            "candidate_name":
            name,

            "job_role":
            role,

            "language":
            language,

            "questions":
            questions
        }


    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)
        )


    finally:

        # -------------------------------------------------
        # Delete temporary PDF
        # -------------------------------------------------

        if os.path.exists(
            file_path
        ):

            os.remove(
                file_path
            )


# =========================================================
# SUBMIT INTERVIEW
# =========================================================

@app.post("/submit-interview")
def submit_interview(
    submission: InterviewSubmission
):

    formatted_answers = [

        {

            "question":
            item.question,

            "answer":
            item.answer

        }

        for item in submission.answers
    ]


    # =====================================================
    # AI EVALUATION
    # =====================================================

    evaluation_result = evaluate_answers(
        formatted_answers
    )


    total_score = evaluation_result[
        "total_score"
    ]


    max_score = evaluation_result[
        "max_score"
    ]


    percentage = evaluation_result[
        "percentage"
    ]


    recommendation = evaluation_result[
        "recommendation"
    ]


    feedback_report = evaluation_result[
        "feedback_report"
    ]


    return {

        "candidate_name":
        submission.name,

        "job_role":
        submission.role,

        "total_score":
        total_score,

        "max_score":
        max_score,

        "percentage":
        f"{percentage:.2f}%",

        "status":
        recommendation,

        "recommendation":
        recommendation,

        "detailed_feedback":
        feedback_report
    }