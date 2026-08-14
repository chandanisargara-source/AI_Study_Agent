import streamlit as st
import requests
from gtts import gTTS
import speech_recognition as sr
from pydub import AudioSegment
import io
import os

from report import generate_pdf_report
from streamlit_mic_recorder import mic_recorder


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Job Interview Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# BACKEND
# =========================================================

BACKEND_URL = "https://ai-study-agent-xqis.onrender.com"


# =========================================================
# LANGUAGE DATA
# =========================================================

LANGUAGE_DATA = {

    "English": {
        "speech": "en-IN",
        "tts": "en",

        "title": "AI Job Interview Agent",
        "subtitle": "AI Powered Resume Analysis & Mock Interview System",

        "candidate": "Candidate Name",
        "role": "Job Role",
        "company": "Target Company",
        "interview_type": "Interview Type",
        "experience": "Experience Level",

        "language": "Interview Language",

        "upload_resume": "Upload Resume (PDF)",
        "start": "🚀 Start Interview",

        "question": "Interview Question",
        "listen": "🔊 Listen Question",

        "voice_answer": "🎤 Voice Answer",
        "voice_help": "Speak your answer. It will automatically convert to text.",

        "text_answer": "📝 Your Answer",
        "text_help": "You can edit the converted text or type manually.",

        "coach": "💡 Answer Coach",
        "coach_help": "These are hints, not a ready-made answer.",

        "next": "Next Question ➡️",
        "submit": "Submit Interview 🎓",

        "recorded": "✅ Voice recorded successfully!",
        "converting": "📝 Converting voice to text...",

        "empty_answer": "Please type an answer or record your voice.",

        "report": "📊 Performance Report",
        "feedback": "💡 AI Feedback",
        "restart": "🔄 Restart Interview"
    },


    "Gujarati": {
        "speech": "gu-IN",
        "tts": "gu",

        "title": "AI જોબ ઇન્ટરવ્યૂ એજન્ટ",
        "subtitle": "AI આધારિત Resume Analysis અને Mock Interview System",

        "candidate": "ઉમેદવારનું નામ",
        "role": "જોબ રોલ",
        "company": "Target Company",
        "interview_type": "ઇન્ટરવ્યૂ પ્રકાર",
        "experience": "અનુભવનું સ્તર",

        "language": "ઇન્ટરવ્યૂ ભાષા",

        "upload_resume": "Resume Upload કરો (PDF)",
        "start": "🚀 ઇન્ટરવ્યૂ શરૂ કરો",

        "question": "ઇન્ટરવ્યૂ પ્રશ્ન",
        "listen": "🔊 પ્રશ્ન સાંભળો",

        "voice_answer": "🎤 Voice Answer",
        "voice_help": "તમારો જવાબ બોલો. તે આપમેળે Textમાં બદલાશે.",

        "text_answer": "📝 તમારો જવાબ",
        "text_help": "Voiceમાંથી આવેલ જવાબ edit કરી શકો છો અથવા manually લખી શકો છો.",

        "coach": "💡 Answer Coach",
        "coach_help": "આ માત્ર hints છે, ready-made answer નથી.",

        "next": "આગળનો પ્રશ્ન ➡️",
        "submit": "ઇન્ટરવ્યૂ Submit કરો 🎓",

        "recorded": "✅ Voice સફળતાપૂર્વક record થયો!",
        "converting": "📝 Voice ને Textમાં convert કરી રહ્યા છીએ...",

        "empty_answer": "કૃપા કરીને જવાબ લખો અથવા voice record કરો.",

        "report": "📊 Performance Report",
        "feedback": "💡 AI Feedback",
        "restart": "🔄 ઇન્ટરવ્યૂ ફરી શરૂ કરો"
    },


    "Hindi": {
        "speech": "hi-IN",
        "tts": "hi",

        "title": "AI जॉब इंटरव्यू एजेंट",
        "subtitle": "AI आधारित Resume Analysis और Mock Interview System",

        "candidate": "उम्मीदवार का नाम",
        "role": "जॉब रोल",
        "company": "Target Company",
        "interview_type": "इंटरव्यू प्रकार",
        "experience": "अनुभव स्तर",

        "language": "इंटरव्यू भाषा",

        "upload_resume": "Resume Upload करें (PDF)",
        "start": "🚀 इंटरव्यू शुरू करें",

        "question": "इंटरव्यू प्रश्न",
        "listen": "🔊 प्रश्न सुनें",

        "voice_answer": "🎤 Voice Answer",
        "voice_help": "अपना जवाब बोलें। यह अपने आप Text में बदल जाएगा।",

        "text_answer": "📝 आपका जवाब",
        "text_help": "Voice से आए जवाब को edit कर सकते हैं या manually लिख सकते हैं।",

        "coach": "💡 Answer Coach",
        "coach_help": "ये केवल hints हैं, ready-made answer नहीं।",

        "next": "अगला प्रश्न ➡️",
        "submit": "इंटरव्यू Submit करें 🎓",

        "recorded": "✅ Voice सफलतापूर्वक record हुई!",
        "converting": "📝 Voice को Text में convert किया जा रहा है...",

        "empty_answer": "कृपया जवाब लिखें या voice record करें।",

        "report": "📊 Performance Report",
        "feedback": "💡 AI Feedback",
        "restart": "🔄 इंटरव्यू फिर से शुरू करें"
    },


    "Hinglish": {
        "speech": "en-IN",
        "tts": "en",

        "title": "AI Job Interview Agent",
        "subtitle": "AI Powered Resume Analysis & Mock Interview System",

        "candidate": "Candidate Name",
        "role": "Job Role",
        "company": "Target Company",
        "interview_type": "Interview Type",
        "experience": "Experience Level",

        "language": "Interview Language",

        "upload_resume": "Upload Resume (PDF)",
        "start": "🚀 Start Interview",

        "question": "Interview Question",
        "listen": "🔊 Listen Question",

        "voice_answer": "🎤 Voice Answer",
        "voice_help": "Apna answer bolo. Ye automatically Text mein convert hoga.",

        "text_answer": "📝 Your Answer",
        "text_help": "Converted text ko edit kar sakte ho ya manually type kar sakte ho.",

        "coach": "💡 Answer Coach",
        "coach_help": "Ye hints hain, ready-made answer nahi.",

        "next": "Next Question ➡️",
        "submit": "Submit Interview 🎓",

        "recorded": "✅ Voice successfully recorded!",
        "converting": "📝 Voice ko Text mein convert kar rahe hain...",

        "empty_answer": "Please answer type karo ya voice record karo.",

        "report": "📊 Performance Report",
        "feedback": "💡 AI Feedback",
        "restart": "🔄 Restart Interview"
    }
}


# =========================================================
# SESSION STATE
# =========================================================

defaults = {

    "token": None,

    "user": None,

    "step": "upload",

    "questions": [],

    "answers": [],

    "current_q_index": 0,

    "candidate_name": "",

    "job_role": "",

    "report": None,

    "selected_language": "English",

    "voice_text": {},

    "coach_visible": False
}


for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# =========================================================
# TEXT TO SPEECH
# =========================================================

def speak_question(text, language):

    lang = LANGUAGE_DATA[language]["tts"]

    tts = gTTS(
        text=text,
        lang=lang
    )

    filename = "question_audio.mp3"

    tts.save(filename)

    return filename


# =========================================================
# ANSWER COACH
# =========================================================

def get_answer_coach(question):

    q = question.lower()

    if "project" in q or "challenge" in q:

        return [
            "💡 Project શું હતું તે જણાવો.",
            "💡 તમારો role અને technology જણાવો.",
            "💡 કયો challenge આવ્યો અને કેવી રીતે solve કર્યો તે કહો.",
            "💡 Final result જણાવો."
        ]

    if "strength" in q:

        return [
            "💡 તમારી 1-2 genuine strengths જણાવો.",
            "💡 એક practical example આપો.",
            "💡 આ strength jobમાં કેવી રીતે મદદ કરશે તે સમજાવો."
        ]

    if "weakness" in q:

        return [
            "💡 એક genuine weakness જણાવો.",
            "💡 તેને improve કરવા શું કરો છો તે કહો.",
            "💡 Learning attitude બતાવો."
        ]

    if "why" in q or "fit" in q or "hire" in q:

        return [
            "💡 તમારી skills ને job સાથે connect કરો.",
            "💡 Relevant project અથવા experience જણાવો.",
            "💡 Company માટે તમે શું value લાવી શકો તે કહો."
        ]

    if "introduce" in q or "yourself" in q:

        return [
            "💡 Education/backgroundથી શરૂઆત કરો.",
            "💡 Important technical skills જણાવો.",
            "💡 Relevant project જણાવો.",
            "💡 Career goal સાથે answer finish કરો."
        ]

    return [
        "💡 Questionનો direct જવાબ આપો.",
        "💡 Relevant example આપો.",
        "💡 Answer clear અને concise રાખો."
    ]


# =========================================================
# LOGIN
# =========================================================

if st.session_state.token is None:

    st.title("🔐 AI Study Agent")

    mode = st.radio(
        "Choose an option",
        ["Login", "Sign Up"],
        horizontal=True
    )

    login_name = st.text_input("Name")

    password = st.text_input(
        "Password",
        type="password"
    )


    # =====================================================
    # LOGIN
    # =====================================================

    if mode == "Login":

        if st.button(
            "Login",
            use_container_width=True
        ):

            if not login_name or not password:

                st.warning(
                    "Please enter name and password."
                )

            else:

                try:

                    response = requests.post(

                        f"{BACKEND_URL}/auth/login",

                        json={
                            "name": login_name,
                            "password": password
                        },

                        timeout=60
                    )


                    if response.status_code == 200:

                        data = response.json()

                        if "access_token" not in data:

                            st.error(
                                "Login token not received."
                            )

                            st.stop()


                        st.session_state.token = (
                            data["access_token"]
                        )


                        try:

                            headers = {
                                "Authorization":
                                f"Bearer {st.session_state.token}"
                            }

                            user_response = requests.get(

                                f"{BACKEND_URL}/users/me",

                                headers=headers,

                                timeout=30
                            )


                            if user_response.status_code == 200:

                                st.session_state.user = (
                                    user_response.json()
                                )

                        except Exception:

                            pass


                        st.session_state.step = "upload"

                        st.rerun()


                    else:

                        try:

                            st.error(
                                response.json()
                            )

                        except Exception:

                            st.error(
                                f"Login failed: "
                                f"{response.status_code}"
                            )


                except Exception as e:

                    st.error(
                        f"Connection error: {e}"
                    )


    # =====================================================
    # SIGN UP
    # =====================================================

    else:

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            if not login_name or not password:

                st.warning(
                    "Please enter name and password."
                )

            else:

                try:

                    response = requests.post(

                        f"{BACKEND_URL}/auth/signup",

                        json={
                            "name": login_name,
                            "password": password
                        },

                        timeout=60
                    )


                    if response.status_code in [200, 201]:

                        st.success(
                            "Account created successfully! 🎉"
                        )

                        st.info(
                            "Now select Login."
                        )

                    else:

                        try:

                            st.error(
                                response.json()
                            )

                        except Exception:

                            st.error(
                                f"Sign Up failed: "
                                f"{response.status_code}"
                            )


                except Exception as e:

                    st.error(
                        f"Connection error: {e}"
                    )


    st.stop()


# =========================================================
# LANGUAGE
# =========================================================

if st.session_state.step == "upload":

    language = st.selectbox(
        "🌐 Interview Language",
        list(LANGUAGE_DATA.keys())
    )

    st.session_state.selected_language = language


else:

    language = st.session_state.selected_language


T = LANGUAGE_DATA[language]


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📋 Dashboard")

st.sidebar.success(
    "🟢 Project Running"
)

st.sidebar.write("✅ Resume Upload")
st.sidebar.write("✅ AI Questions")
st.sidebar.write("✅ Voice Interview")
st.sidebar.write("✅ Speech to Text")
st.sidebar.write("✅ Multi Language")
st.sidebar.write("✅ Answer Coach")
st.sidebar.write("✅ AI Evaluation")
st.sidebar.write("✅ Performance Report")

st.sidebar.divider()

st.sidebar.info(
    f"🌐 Language\n\n{language}"
)


# =========================================================
# MAIN HEADER
# =========================================================

st.title(
    f"🤖 {T['title']}"
)

st.caption(
    T["subtitle"]
)

st.divider()


# =========================================================
# STEP 1 : UPLOAD
# =========================================================

if st.session_state.step == "upload":

    st.subheader(
        "📝 Candidate Details"
    )


    col1, col2 = st.columns(2)


    with col1:

        candidate_name = st.text_input(
            T["candidate"]
        )


        role = st.text_input(
            T["role"]
        )


    with col2:

        company = st.selectbox(
            T["company"],

            [
                "Google",
                "Microsoft",
                "Amazon",
                "Infosys",
                "TCS",
                "Wipro",
                "Accenture",
                "Other"
            ]
        )


        interview_type = st.selectbox(
            T["interview_type"],

            [
                "Technical",
                "HR",
                "Behavioral",
                "Mixed"
            ]
        )


    experience = st.selectbox(

        T["experience"],

        [
            "Fresher",
            "0-2 Years",
            "2-5 Years",
            "5+ Years"
        ]
    )


    uploaded_file = st.file_uploader(

        T["upload_resume"],

        type=["pdf"]
    )


    if uploaded_file:

        st.success(
            "✅ Resume Uploaded Successfully!"
        )


        c1, c2, c3 = st.columns(3)


        c1.metric(
            "Resume Score",
            "85/100"
        )


        c2.metric(
            "Skills",
            "Python, FastAPI"
        )


        c3.metric(
            "Experience",
            experience
        )


        st.progress(85)


        st.divider()


        if st.button(

            T["start"],

            use_container_width=True
        ):


            if not candidate_name or not role:

                st.error(
                    "Please enter candidate name and job role."
                )

                st.stop()


            with st.spinner(
                "🤖 AI generating interview questions..."
            ):

                try:

                    files = {

                        "file": (

                            uploaded_file.name,

                            uploaded_file.getvalue(),

                            "application/pdf"
                        )
                    }


                    params = {

                        "name":
                        candidate_name,

                        "role":
                        role
                    }


                    response = requests.post(

                        f"{BACKEND_URL}/upload-resume",

                        files=files,

                        params=params,

                        timeout=120
                    )


                    if response.status_code != 200:

                        st.error(
                            f"Backend Error: "
                            f"{response.status_code}"
                        )

                        st.code(
                            response.text
                        )

                        st.stop()


                    data = response.json()

                    questions = data.get(
                        "questions",
                        []
                    )


                    if not questions:

                        st.error(
                            "No interview questions received."
                        )

                        st.stop()


                    st.session_state.questions = (
                        questions
                    )

                    st.session_state.candidate_name = (
                        candidate_name
                    )

                    st.session_state.job_role = (
                        role
                    )

                    st.session_state.answers = []

                    st.session_state.current_q_index = 0

                    st.session_state.voice_text = {}

                    st.session_state.coach_visible = False

                    st.session_state.step = "interview"

                    st.rerun()


                except Exception as e:

                    st.error(
                        f"Error: {e}"
                    )


# =========================================================
# STEP 2 : INTERVIEW
# =========================================================

elif st.session_state.step == "interview":

    questions = st.session_state.questions

    index = st.session_state.current_q_index


    if not questions:

        st.error(
            "No interview questions available."
        )

        st.stop()


    current_question = questions[index]


    # =====================================================
    # PROGRESS
    # =====================================================

    progress = (

        (index + 1)

        /

        len(questions)
    )


    st.progress(
        progress
    )


    st.caption(
        f"🎯 {T['question']} "
        f"{index + 1} / {len(questions)}"
    )


    # =====================================================
    # QUESTION CARD
    # =====================================================

    st.markdown(
        "### 💬 Question"
    )

    st.info(
        current_question
    )


    # =====================================================
    # LISTEN
    # =====================================================

    if st.button(

        T["listen"],

        key=f"listen_{index}"
    ):

        try:

            audio_file = speak_question(

                current_question,

                language
            )


            with open(
                audio_file,
                "rb"
            ) as audio:

                st.audio(
                    audio.read(),
                    format="audio/mp3"
                )


        except Exception as e:

            st.error(
                f"Voice generation failed: {e}"
            )


    st.divider()


    # =====================================================
    # ANSWER COACH
    # =====================================================

    coach_col1, coach_col2 = st.columns(
        [1, 4]
    )


    with coach_col1:

        coach_clicked = st.button(

            T["coach"],

            key=f"coach_{index}"
        )


    if coach_clicked:

        st.session_state.coach_visible = (
            not st.session_state.coach_visible
        )


    if st.session_state.coach_visible:

        st.info(
            T["coach_help"]
        )


        coach_points = get_answer_coach(

            current_question
        )


        for point in coach_points:

            st.write(
                point
            )


    st.divider()


    # =====================================================
    # VOICE ANSWER
    # =====================================================

    st.markdown(
        f"### {T['voice_answer']}"
    )


    st.caption(
        T["voice_help"]
    )


    audio = mic_recorder(

        start_prompt="🎙️ Start Recording",

        stop_prompt="⏹️ Stop Recording",

        key=f"voice_recorder_{index}"
    )


    # =====================================================
    # VOICE PROCESSING
    # =====================================================

    if audio:

        st.success(
            T["recorded"]
        )


        st.audio(
            audio["bytes"],
            format="audio/wav"
        )


        try:

            # ---------------------------------------------
            # GET AUDIO
            # ---------------------------------------------

            raw_audio = audio["bytes"]


            # ---------------------------------------------
            # CONVERT TO WAV USING PYDUB
            # ---------------------------------------------

            audio_segment = AudioSegment.from_file(

                io.BytesIO(raw_audio)
            )


            wav_buffer = io.BytesIO()


            audio_segment.export(

                wav_buffer,

                format="wav"
            )


            wav_buffer.seek(0)


            # ---------------------------------------------
            # SPEECH RECOGNITION
            # ---------------------------------------------

            recognizer = sr.Recognizer()


            with sr.AudioFile(

                wav_buffer

            ) as source:

                recorded_audio = recognizer.record(
                    source
                )


            speech_language = LANGUAGE_DATA[

                language

            ]["speech"]


            with st.spinner(
                T["converting"]
            ):

                converted_text = (

                    recognizer.recognize_google(

                        recorded_audio,

                        language=speech_language
                    )
                )


            # ---------------------------------------------
            # SAVE TEXT
            # ---------------------------------------------

            st.session_state.voice_text[index] = (
                converted_text
            )


            st.success(
                "📝 Voice converted successfully!"
            )


        except sr.UnknownValueError:

            st.error(
                "❌ Voice samajh nahi aavi. "
                "Please clearly speak and try again."
            )


        except sr.RequestError:

            st.error(
                "❌ Speech recognition service unavailable."
            )


        except Exception as e:

            st.error(
                f"❌ Voice-to-text failed: {e}"
            )


    # =====================================================
    # TEXT ANSWER
    # =====================================================

    st.markdown(
        f"### {T['text_answer']}"
    )


    st.caption(
        T["text_help"]
    )


    existing_text = (

        st.session_state.voice_text.get(

            index,

            ""
        )
    )


    # IMPORTANT:
    # We use value= instead of modifying widget state.
    # This avoids:
    # st.session_state.answer_0 cannot be modified
    #

    answer = st.text_area(

        T["text_answer"],

        value=existing_text,

        height=170,

        key=f"answer_box_{index}"
    )


    st.divider()


    # =====================================================
    # NEXT / SUBMIT
    # =====================================================

    if index < len(questions) - 1:

        button_text = T["next"]

    else:

        button_text = T["submit"]


    if st.button(

        button_text,

        key=f"next_{index}",

        use_container_width=True
    ):


        final_answer = answer.strip()


        if not final_answer:

            st.warning(
                T["empty_answer"]
            )

            st.stop()


        # ---------------------------------------------
        # SAVE ANSWER
        # ---------------------------------------------

        st.session_state.answers.append(

            {
                "question":
                current_question,

                "answer":
                final_answer
            }
        )


        # ---------------------------------------------
        # NEXT QUESTION
        # ---------------------------------------------

        if index < len(questions) - 1:

            st.session_state.current_q_index += 1

            st.session_state.coach_visible = False

            st.rerun()


        # ---------------------------------------------
        # FINAL SUBMIT
        # ---------------------------------------------

        else:

            payload = {

                "name":
                st.session_state.candidate_name,

                "role":
                st.session_state.job_role,

                "answers":
                st.session_state.answers
            }


            with st.spinner(
                "🤖 AI evaluating your interview..."
            ):

                try:

                    response = requests.post(

                        f"{BACKEND_URL}/submit-interview",

                        json=payload,

                        timeout=120
                    )


                    if response.status_code == 200:

                        st.session_state.report = (
                            response.json()
                        )

                        st.session_state.step = (
                            "report"
                        )

                        st.rerun()


                    else:

                        st.error(
                            "Report generation failed."
                        )

                        st.code(
                            response.text
                        )


                except Exception as e:

                    st.error(
                        f"Connection error: {e}"
                    )


# =========================================================
# STEP 3 : REPORT
# =========================================================

elif st.session_state.step == "report":

    st.balloons()


    st.success(
        "🎉 Interview Completed Successfully!"
    )


    report = st.session_state.report


    if not report:

        st.error(
            "Report data is not available."
        )

        st.stop()


    # =====================================================
    # CANDIDATE
    # =====================================================

    st.info(

        f"""
👤 Candidate : {report['candidate_name']}

💼 Job Role : {report['job_role']}
"""
    )


    # =====================================================
    # PERFORMANCE
    # =====================================================

    st.subheader(
        T["report"]
    )


    percentage = float(

        str(
            report["percentage"]
        ).replace(
            "%",
            ""
        )
    )


    st.progress(
        int(percentage)
    )


    col1, col2, col3 = st.columns(3)


    col1.metric(

        "Questions",

        len(
            report["detailed_feedback"]
        )
    )


    col2.metric(

        "Score",

        f"{report['total_score']} / "
        f"{report['max_score']}"
    )


    col3.metric(

        "Percentage",

        report["percentage"]
    )


    st.divider()


    # =====================================================
    # RECOMMENDATION
    # =====================================================

    recommendation = report[
        "recommendation"
    ]


    if recommendation == (

        "Excellent Candidate - Recommended"
    ):

        st.success(
            f"🏆 {recommendation}"
        )


    elif recommendation == (

        "Good Candidate - Can Be Considered"
    ):

        st.info(
            f"👍 {recommendation}"
        )


    elif recommendation == (

        "Average - Needs Improvement"
    ):

        st.warning(
            f"⚠️ {recommendation}"
        )


    else:

        st.error(
            f"❌ {recommendation}"
        )


    # =====================================================
    # FEEDBACK
    # =====================================================

    st.subheader(
        T["feedback"]
    )


    for item in report[
        "detailed_feedback"
    ]:

        with st.expander(
            f"❓ {item['question']}"
        ):

            st.write(
                "📝 **Your Answer:**"
            )

            st.write(
                item["answer"]
            )


            st.write(
                f"⭐ **Score:** "
                f"{item['score']} / 5"
            )


            st.success(
                item["feedback"]
            )


    st.divider()


    # =====================================================
    # PDF
    # =====================================================

    if st.button(
        "📄 Generate PDF Report",
        use_container_width=True
    ):

        try:

            pdf_file = generate_pdf_report(

                filename="Interview_Report.pdf",

                candidate_name=report[
                    "candidate_name"
                ],

                job_role=report[
                    "job_role"
                ],

                total_score=report[
                    "total_score"
                ],

                max_score=report[
                    "max_score"
                ],

                percentage=report[
                    "percentage"
                ],

                recommendation=report[
                    "recommendation"
                ],

                feedback_report=report[
                    "detailed_feedback"
                ]
            )


            st.success(
                "✅ PDF Report Generated!"
            )


            with open(
                pdf_file,
                "rb"
            ) as file:

                st.download_button(

                    "⬇️ Download PDF",

                    data=file,

                    file_name="Interview_Report.pdf",

                    mime="application/pdf"
                )


        except Exception as e:

            st.error(
                f"PDF generation failed: {e}"
            )


    # =====================================================
    # RESTART
    # =====================================================

    if st.button(

        T["restart"],

        use_container_width=True
    ):

        st.session_state.step = "upload"

        st.session_state.questions = []

        st.session_state.answers = []

        st.session_state.current_q_index = 0

        st.session_state.candidate_name = ""

        st.session_state.job_role = ""

        st.session_state.report = None

        st.session_state.voice_text = {}

        st.session_state.coach_visible = False

        st.rerun()