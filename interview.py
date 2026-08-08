import os
from dotenv import load_dotenv
from google import genai

# .env ફાઇલ લોડ કરો
load_dotenv()

# Gemini Client તૈયાર કરો
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_questions(resume_text):
    """
    આ ફંક્શન રેઝ્યૂમે વાંચીને Gemini API દ્વારા 5 અલગ-અલગ પ્રશ્નો બનાવશે.
    """
    prompt = f"""
    You are an expert HR interviewer. Read the candidate's resume below and generate exactly 5 interview questions based on their skills and experience.
    Provide only the questions, each on a new line, without any numbering, bullet points, or introductory text.

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
        print(f"Error generating questions: {e}")
        return ""