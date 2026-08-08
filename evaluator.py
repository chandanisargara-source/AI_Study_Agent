import os
from google import genai
from dotenv import load_dotenv

# .env ફાઇલ લોડ કરો
load_dotenv()

# Gemini Client તૈયાર કરો
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def evaluate_answers(answers_list):
    """
    answers_list: [{'question': '...', 'answer': '...'}, ...]
    આ ફંક્શન દરેક જવાબને Gemini API વડે ચેક કરશે અને સ્કોર આપશે.
    """
    total_score = 0
    max_score = len(answers_list) * 5  # દરેક પ્રશ્નના મહત્તમ 5 માર્ક્સ
    feedback_report = []

    for item in answers_list:
        q = item['question']
        a = item['answer']
        
        # Gemini ને પ્રશ્ન અને જવાબ મૂલ્યાંકન કરવા માટે પ્રોમ્પ્ટ
        prompt = f"""
        You are an expert technical interviewer. Evaluate the candidate's answer for the given question.
        
        Question: {q}
        Candidate's Answer: {a}
        
        Provide the result strictly in this format:
        Score: [Give a integer score from 1 to 5]
        Feedback: [Write 1-2 lines of constructive feedback in English]
        """
        
        try:
            response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=prompt
            )
            res_text = response.text.strip()
            
            # Gemini ના રિસ્પોન્સમાંથી Score અને Feedback અલગ તારવો
            lines = res_text.split("\n")
            score = 1
            feedback = "No feedback generated."
            
            for line in lines:
                if line.startswith("Score:"):
                    score = int(line.replace("Score:", "").strip())
                elif line.startswith("Feedback:"):
                    feedback = line.replace("Feedback:", "").strip()
            
        except Exception as e:
            # જો API માં કોઈ ભૂલ આવે તો સેફ્ટી માટે ડિફોલ્ટ સ્કોર
            score = 1
            feedback = f"Error evaluating answer: {str(e)}"
            
        total_score += score
        feedback_report.append({
            "question": q,
            "answer": a,
            "score": score,
            "feedback": feedback
        })
        
    percentage = round((total_score / max_score) * 100, 2)

    if percentage >= 80:
        recommendation = "Excellent Candidate - Recommended"

    elif percentage >= 60:
        recommendation = "Good Candidate - Can Be Considered"

    elif percentage >= 40:
        recommendation = "Average - Needs Improvement"

    else:
        recommendation = "Not Ready"

    return {
        "total_score": total_score,
        "max_score": max_score,
        "percentage": percentage,
        "recommendation": recommendation,
        "feedback_report": feedback_report
    }