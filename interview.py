import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(
    api_key=api_key
)


def generate_questions(
    resume_text,
    language="English"
):
    """
    Resume પરથી exactly 5 interview questions બનાવે છે.
    Questions selected languageમાં જ આવશે.
    """

    prompt = f"""
You are an expert HR and technical interviewer.

Read the candidate's resume below.

Generate exactly 5 interview questions based on
the candidate's skills, education, projects and experience.

IMPORTANT LANGUAGE RULE:
The interview language is: {language}

ALL 5 QUESTIONS MUST BE WRITTEN ENTIRELY IN {language}.

Do not use English unless the selected language is English.

Provide ONLY the questions.
Do not provide numbering.
Do not provide bullet points.
Do not provide explanations.
Each question must be on a new line.

Resume:
{resume_text}
"""

    try:

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        return response.text

    except Exception as e:

        print(
            f"Error generating questions: {e}"
        )

        return ""