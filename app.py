import os
from interview import generate_questions
from evaluator import evaluate_answers
from report import generate_report

def start_terminal_interview():
    print("\n================🤖 AI Job Interview Agent 🤖================")
    print("------------------------------------------------------------")
    
    name = input("Candidate name: ")
    role = input("Job role you are applying for: ")
    
    # 1. રેઝ્યૂમે ટેક્સ્ટ (ટેસ્ટિંગ માટે અત્યારે મેન્યુઅલ ટેક્સ્ટ આપી છે)
    # પાછળથી આને આપણે FastAPI માં અપલોડ થતી PDF સાથે જોડી દઈશું
    print("\n[Processing...] Analyzing your profile and generating questions...")
    mock_resume_text = f"Candidate Name: {name}. Applying for: {role}. Experienced in Python, basic coding, and system design."
    
    # interview.py માંથી Gemini વડે પ્રશ્નો જનરેટ કરો
    raw_questions = generate_questions(mock_resume_text)
    
    # Gemini નો રિસ્પોન્સ જો સ્ટ્રિંગ હોય તો તેને લિસ્ટમાં કન્વર્ટ કરો
    # (જો પ્રશ્નો ન્યૂ લાઈનથી અલગ પડતા હોય તો)
    if isinstance(raw_questions, str):
        questions = [q.strip() for q in raw_questions.strip().split("\n") if q.strip()]
        # જો લિસ્ટમાં પ્રશ્ન નંબર (1., 2.) આવતા હોય તો તેને પણ ક્લીન કરી શકાય
    else:
        # સેફ્ટી માટે જો કોઈ પ્રશ્ન ન મળે તો ડિફોલ્ટ પ્રશ્નો
        questions = [
            "Tell me about yourself.",
            f"Why do you want to join as a {role}?",
            "Describe a challenging technical problem you solved.",
            "What are your core strengths?",
            "Do you have any questions for us?"
        ]
        
    # ફક્ત પહેલા 5 પ્રશ્નો જ પૂછવા માટે
    questions = questions[:5]
    
    print(f"\nWelcome {name}! AI Interviewer has generated {len(questions)} questions for you.")
    print("------------------------------------------------------------")
    
    answers_list = []
    
    # 2. ઇન્ટરવ્યૂ રાઉન્ડ શરૂ કરો
    for i, q in enumerate(questions, 1):
        print(f"\nInterviewer (Q{i}): {q}")
        user_answer = input("Your answer: ")
        
        # ઇવેલ્યુએટર માટે પ્રશ્ન અને જવાબ પેર (dict) બનાવો
        answers_list.append({
            "question": q,
            "answer": user_answer
        })
        
    print("\n[Processing...] Evaluating your answers with Gemini AI...")
    
    # 3. evaluator.py નો ઉપયોગ કરીને Gemini વડે સ્કોર મેળવો
    total_score, max_score, feedback_report = evaluate_answers(answers_list)
    
    # 4. report.py ના ફંક્શન વડે ફાઇનલ રિપોર્ટ પ્રિન્ટ કરો
    generate_report(name, role, total_score, max_score)
    
    # દરેક પ્રશ્નનો વિગતવાર ફીડબેક પ્રિન્ટ કરો
    print("\nDetailed AI Feedback:")
    for item in feedback_report:
        print(f"\n📌 Q: {item['question']}")
        print(f"   A: {item['answer']}")
        print(f"   ⭐ Score: {item['score']}/5")
        print(f"   💡 Feedback: {item['feedback']}")
        
    print("\n============================================================")

if __name__ == "__main__":
    start_terminal_interview()