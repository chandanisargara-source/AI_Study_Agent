import streamlit as st
import requests
from gtts import gTTS
import speech_recognition as sr
import io

from report import generate_pdf_report
from streamlit_mic_recorder import mic_recorder


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Job Interview Agent",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# BACKEND
# =========================================================

BACKEND_URL = "https://ai-study-agent-xqis.onrender.com"


# =========================================================
# LANGUAGE SETTINGS
# =========================================================

LANGUAGES = {
    "English": {
        "speech": "en-IN",
        "tts": "en"
    },

    "Hindi": {
        "speech": "hi-IN",
        "tts": "hi"
    },

    "Gujarati": {
        "speech": "gu-IN",
        "tts": "gu"
    },

    "Hinglish": {
        "speech": "en-IN",
        "tts": "en"
    }
}


# =========================================================
# TEXT TO SPEECH
# =========================================================

def speak_question(text, language):

    lang_code = LANGUAGES[
        language
    ]["tts"]

    tts = gTTS(
        text=text,
        lang=lang_code
    )

    audio_file = "question_audio.mp3"

    tts.save(audio_file)

    return audio_file


# =========================================================
# ANSWER COACH
# =========================================================

def get_answer_coach(question):

    q = question.lower()

    if (
        "project" in q
        or "challenge" in q
        or "worked on" in q
    ):

        return [
            "💡 Explain what the project was.",
            "💡 Mention your role and technologies used.",
            "💡 Explain the challenge and how you solved it.",
            "💡 Mention the final result."
        ]


    if (
        "strength" in q
        or "good at" in q
    ):

        return [
            "💡 Mention 1–2 genuine strengths.",
            "💡 Give a short example.",
            "💡 Explain how the strength helps in this role."
        ]


    if (
        "weakness" in q
        or "improve" in q
    ):

        return [
            "💡 Mention one genuine area for improvement.",
            "💡 Explain what you are doing to improve.",
            "💡 Show a positive learning attitude."
        ]


    if (
        "technical" in q
        or "python" in q
        or "fastapi" in q
        or "database" in q
        or "programming" in q
    ):

        return [
            "💡 Start with the basic concept.",
            "💡 Give a practical example.",
            "💡 Explain why you would use it."
        ]


    if (
        "why" in q
        or "fit" in q
        or "hire" in q
    ):

        return [
            "💡 Connect your skills with the job.",
            "💡 Mention your relevant experience or projects.",
            "💡 Explain what value you can bring."
        ]


    if (
        "introduce" in q
        or "tell me about yourself" in q
    ):

        return [
            "💡 Start with your education/background.",
            "💡 Mention important technical skills.",
            "💡 Mention a relevant project.",
            "💡 Finish with your career goal."
        ]


    return [
        "💡 Answer the question directly.",
        "💡 Give a relevant example.",
        "💡 Keep your answer clear and concise."
    ]


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
# LOGIN
# =========================================================

if st.session_state.token is None:

    st.title("🔐 AI Study Agent")

    mode = st.radio(
        "Choose an option",
        ["Login", "Sign Up"],
        horizontal=True
    )

    login_name = st.text_input(
        "Name"
    )

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
                                "Login response does not contain token."
                            )

                            st.stop()


                        st.session_state.token = (
                            data["access_token"]
                        )


                        # ---------------------------------
                        # USER INFORMATION
                        # ---------------------------------

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
# SIDEBAR
# =========================================================

st.sidebar.title(
    "📋 Dashboard"
)

st.sidebar.success(
    "Project Status : Running"
)

st.sidebar.write(
    "✅ Resume Upload"
)

st.sidebar.write(
    "✅ AI Resume Analysis"
)

st.sidebar.write(
    "✅ Mock Interview"
)

st.sidebar.write(
    "✅ Voice Interview"
)

st.sidebar.write(
    "✅ Multi-Language"
)

st.sidebar.write(
    "✅ Speech to Text"
)

st.sidebar.write(
    "✅ AI Answer Coach"
)

st.sidebar.write(
    "✅ AI Evaluation"
)

st.sidebar.write(
    "✅ Performance Report"
)


# =========================================================
# MAIN TITLE
# =========================================================

st.title(
    "🤖 AI Job Interview Agent"
)

st.subheader(
    "AI Powered Resume Analysis & Mock Interview System"
)

st.divider()


# =========================================================
# STEP 1 : RESUME UPLOAD
# =========================================================

if st.session_state.step == "upload":

    st.subheader(
        "📝 Candidate Details"
    )


    candidate_name = st.text_input(
        "Candidate Name"
    )


    role = st.text_input(
        "Job Role"
    )


    company = st.selectbox(
        "Target Company",

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
        "Interview Type",

        [
            "Technical",
            "HR",
            "Behavioral",
            "Mixed"
        ]
    )


    experience = st.selectbox(
        "Experience Level",

        [
            "Fresher",
            "0-2 Years",
            "2-5 Years",
            "5+ Years"
        ]
    )


    # =====================================================
    # LANGUAGE
    # =====================================================

    selected_language = st.selectbox(

        "🌐 Interview Language",

        list(LANGUAGES.keys()),

        index=0
    )


    st.session_state.selected_language = (
        selected_language
    )


    if selected_language == "English":

        st.caption(
            "🇬🇧 Interview will use English speech recognition."
        )

    elif selected_language == "Hindi":

        st.caption(
            "🇮🇳 Interview will use Hindi speech recognition."
        )

    elif selected_language == "Gujarati":

        st.caption(
            "🪔 Interview will use Gujarati speech recognition."
        )

    else:

        st.caption(
            "🗣️ Hinglish uses Indian English speech recognition."
        )


    # =====================================================
    # RESUME
    # =====================================================

    uploaded_file = st.file_uploader(

        "Upload Resume (PDF)",

        type=["pdf"]
    )


    if uploaded_file:

        st.success(
            "✅ Resume Uploaded Successfully"
        )


        col1, col2, col3 = st.columns(3)


        col1.metric(
            "Resume Score",
            "85/100"
        )


        col2.metric(
            "Skills",
            "Python, FastAPI"
        )


        col3.metric(
            "Experience",
            experience
        )


        st.progress(85)


        # =================================================
        # START INTERVIEW
        # =================================================

        if st.button(

            "🚀 Start Interview",

            use_container_width=True
        ):


            if not candidate_name or not role:

                st.error(
                    "Please enter name and role."
                )

                st.stop()


            with st.spinner(

                "🤖 AI generating questions..."
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

                            "Backend returned no questions."
                        )

                        st.stop()


                    # -------------------------------------
                    # SAVE INTERVIEW DATA
                    # -------------------------------------

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

        if st.button(
            "🔄 Back to Upload"
        ):

            st.session_state.step = "upload"

            st.rerun()


    else:

        current_question = questions[index]


        # =================================================
        # PROGRESS
        # =================================================

        progress_value = (

            (index + 1)

            /

            len(questions)
        )


        st.progress(
            progress_value
        )


        st.caption(

            f"Question "
            f"{index + 1} / {len(questions)}"
        )


        # =================================================
        # QUESTION
        # =================================================

        st.subheader(

            f"💬 Interview Question "
            f"{index + 1}"
        )


        st.info(
            current_question
        )


        # =================================================
        # QUESTION VOICE
        # =================================================

        if st.button(

            "🔊 Listen Question",

            key=f"listen_question_{index}"
        ):


            try:

                audio_file = speak_question(

                    current_question,

                    st.session_state.selected_language
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


        # =================================================
        # ANSWER COACH
        # =================================================

        if st.button(

            "💡 Answer Coach",

            key=f"coach_button_{index}"
        ):

            st.session_state.coach_visible = (
                not st.session_state.coach_visible
            )


        if st.session_state.coach_visible:

            st.info(
                "💡 These are hints, not a ready-made answer."
            )


            coach_points = get_answer_coach(

                current_question
            )


            for point in coach_points:

                st.write(
                    point
                )


        st.divider()


        # =================================================
        # ANSWER STATE
        # =================================================

        voice_text_key = (

            f"voice_text_{index}"
        )


        widget_key = (

            f"answer_box_{index}"
        )


        saved_voice_text = (

            st.session_state.voice_text.get(

                index,

                ""
            )
        )


        # =================================================
        # VOICE RECORDING
        # =================================================

        st.subheader(
            "🎤 Voice Answer"
        )


        st.caption(

            "Speak your answer. "
            "It will automatically convert to text."
        )


        audio = mic_recorder(

            start_prompt="🎙️ Start Recording",

            stop_prompt="⏹️ Stop Recording",

            key=f"voice_recorder_{index}"
        )


        # =================================================
        # PROCESS VOICE BEFORE TEXT WIDGET
        # =================================================

        if audio:

            st.success(
                "✅ Recording received!"
            )


            st.audio(

                audio["bytes"],

                format="audio/wav"
            )


            try:

                recognizer = sr.Recognizer()


                audio_bytes = audio["bytes"]


                # -----------------------------------------
                # DIRECT WAV
                # No pydub / ffprobe required
                # -----------------------------------------

                audio_buffer = io.BytesIO(

                    audio_bytes
                )


                with sr.AudioFile(

                    audio_buffer

                ) as source:

                    recorded_audio = (

                        recognizer.record(

                            source
                        )
                    )


                language_code = LANGUAGES[

                    st.session_state.selected_language

                ]["speech"]


                with st.spinner(

                    "📝 Converting voice to text..."
                ):


                    voice_text = (

                        recognizer.recognize_google(

                            recorded_audio,

                            language=language_code
                        )
                    )


                # -----------------------------------------
                # SAVE VOICE TEXT
                # -----------------------------------------

                st.session_state.voice_text[index] = (

                    voice_text
                )


                # -----------------------------------------
                # IMPORTANT
                # Rerun BEFORE text widget is created
                # -----------------------------------------

                st.rerun()


            except sr.UnknownValueError:

                st.error(

                    "❌ Speech could not be understood. "
                    "Please speak clearly and try again."
                )


            except sr.RequestError:

                st.error(

                    "❌ Speech recognition service "
                    "is temporarily unavailable."
                )


            except Exception as e:

                st.error(

                    f"❌ Voice-to-text failed: {e}"
                )


        # =================================================
        # TEXT ANSWER
        # =================================================

        st.subheader(
            "📝 Your Answer"
        )


        st.caption(

            "You can edit the converted text "
            "or type your answer manually."
        )


        answer = st.text_area(

            "⌨️ Answer",

            value=saved_voice_text,

            height=170,

            key=widget_key
        )


        st.divider()


        # =================================================
        # NEXT / SUBMIT
        # =================================================

        if index < len(questions) - 1:

            button_text = (
                "Next Question ➡️"
            )

        else:

            button_text = (
                "Submit Interview 🎓"
            )


        if st.button(

            button_text,

            key=f"next_question_{index}",

            use_container_width=True
        ):


            final_answer = answer.strip()


            if not final_answer:

                st.warning(

                    "Please type an answer "
                    "or record your voice."
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

                    "🤖 AI evaluating interview..."
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
        "📊 Performance Report"
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


    st.divider()


    # =====================================================
    # AI FEEDBACK
    # =====================================================

    st.subheader(
        "💡 AI Feedback"
    )


    st.caption(

        "AI evaluation for each interview answer."
    )


    for item in report[
        "detailed_feedback"
    ]:


        st.markdown(

            f"### ❓ {item['question']}"
        )


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
    # PDF REPORT
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

        "🔄 Restart Interview",

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