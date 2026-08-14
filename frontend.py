import streamlit as st
import requests
import tempfile
import os
import speech_recognition as sr

from gtts import gTTS
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

LANGUAGE_CODES = {
    "English": "en",
    "Gujarati": "gu",
    "Hindi": "hi",
    "Marathi": "mr",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te"
}


SPEECH_CODES = {
    "English": "en-IN",
    "Gujarati": "gu-IN",
    "Hindi": "hi-IN",
    "Marathi": "mr-IN",
    "Bengali": "bn-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN"
}


# =========================================================
# TEXT TO SPEECH
# =========================================================

def speak_question(text, language):

    language_code = LANGUAGE_CODES.get(
        language,
        "en"
    )

    tts = gTTS(
        text=text,
        lang=language_code
    )

    audio_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    ).name

    tts.save(audio_file)

    return audio_file


# =========================================================
# SPEECH TO TEXT
# =========================================================

def convert_voice_to_text(audio_bytes, language):

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    )

    try:

        temp_file.write(audio_bytes)
        temp_file.close()

        recognizer = sr.Recognizer()

        with sr.AudioFile(
            temp_file.name
        ) as source:

            audio_data = recognizer.record(
                source
            )

        speech_language = SPEECH_CODES.get(
            language,
            "en-IN"
        )

        text = recognizer.recognize_google(
            audio_data,
            language=speech_language
        )

        return text

    finally:

        if os.path.exists(
            temp_file.name
        ):

            os.remove(
                temp_file.name
            )


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

    "answer_values": {}
}


for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# =========================================================
# LOGIN / SIGNUP
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

                        timeout=120
                    )


                    if response.status_code == 200:

                        data = response.json()

                        if "access_token" not in data:

                            st.error(
                                "Invalid login response."
                            )

                            st.stop()


                        st.session_state.token = (
                            data["access_token"]
                        )


                        headers = {
                            "Authorization":
                            f"Bearer {st.session_state.token}"
                        }


                        try:

                            user_response = requests.get(

                                f"{BACKEND_URL}/users/me",

                                headers=headers,

                                timeout=120
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
                                response.text
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

                        timeout=120
                    )


                    if response.status_code in [200, 201]:

                        st.success(
                            "Account created successfully! 🎉"
                        )

                        st.info(
                            "Now select Login and sign in."
                        )

                    else:

                        try:

                            st.error(
                                response.json()
                            )

                        except Exception:

                            st.error(
                                response.text
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
    "Project Status: Running"
)

st.sidebar.write(
    "✅ Resume Upload"
)

st.sidebar.write(
    "✅ Multilingual Interview"
)

st.sidebar.write(
    "✅ Voice Answer"
)

st.sidebar.write(
    "✅ Speech to Text"
)

st.sidebar.write(
    "✅ AI Evaluation"
)

st.sidebar.write(
    "✅ PDF Report"
)


# =========================================================
# MAIN TITLE
# =========================================================

st.title(
    "🤖 AI Job Interview Agent"
)

st.caption(
    "AI Powered Resume Analysis & Mock Interview System"
)


# =========================================================
# STEP 1 : RESUME UPLOAD
# =========================================================

if st.session_state.step == "upload":

    st.subheader(
        "📝 Candidate Details"
    )


    col1, col2 = st.columns(2)


    with col1:

        candidate_name_input = st.text_input(
            "Candidate Name",
            key="candidate_name_input"
        )


    with col2:

        role_input = st.text_input(
            "Job Role",
            key="job_role_input"
        )


    col1, col2, col3 = st.columns(3)


    with col1:

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


    with col2:

        interview_type = st.selectbox(
            "Interview Type",
            [
                "Technical",
                "HR",
                "Behavioral",
                "Mixed"
            ]
        )


    with col3:

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

        [
            "English",
            "Gujarati",
            "Hindi",
            "Marathi",
            "Bengali",
            "Tamil",
            "Telugu"
        ],

        key="selected_language"
    )


    uploaded_file = st.file_uploader(
        "📄 Upload Resume",
        type=["pdf"]
    )


    if uploaded_file is not None:

        st.success(
            "✅ Resume Uploaded Successfully"
        )


        if st.button(
            "🚀 Start Interview",
            use_container_width=True
        ):

            if not candidate_name_input:

                st.error(
                    "Please enter candidate name."
                )

                st.stop()


            if not role_input:

                st.error(
                    "Please enter job role."
                )

                st.stop()


            with st.spinner(
                f"🤖 Generating {selected_language} interview questions..."
            ):

                files = {

                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/pdf"
                    )
                }


                params = {

                    "name":
                    candidate_name_input,

                    "role":
                    role_input,

                    "language":
                    selected_language
                }


                try:

                    response = requests.post(

                        f"{BACKEND_URL}/upload-resume",

                        files=files,

                        params=params,

                        timeout=120
                    )


                    if response.status_code == 200:

                        data = response.json()


                        questions = data.get(
                            "questions",
                            []
                        )


                        if not questions:

                            st.error(
                                "Backend returned no questions."
                            )

                        else:

                            st.session_state.questions = (
                                questions
                            )

                            st.session_state.answers = []

                            st.session_state.current_q_index = 0

                            st.session_state.candidate_name = (
                                candidate_name_input
                            )

                            st.session_state.job_role = (
                                role_input
                            )

                            st.session_state.selected_language = (
                                selected_language
                            )

                            st.session_state.voice_text = {}

                            st.session_state.answer_values = {}

                            st.session_state.step = "interview"

                            st.rerun()


                    else:

                        st.error(
                            f"Backend Error: "
                            f"{response.status_code}"
                        )

                        st.code(
                            response.text
                        )


                except Exception as e:

                    st.error(
                        f"Connection Error: {e}"
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

    language = st.session_state.selected_language


    # =====================================================
    # HEADER
    # =====================================================

    col1, col2 = st.columns([4, 1])


    with col1:

        st.subheader(
            "🎤 AI Mock Interview"
        )

        st.caption(
            f"🌐 Language: {language}"
        )


    with col2:

        st.metric(
            "Question",
            f"{index + 1}/{len(questions)}"
        )


    # =====================================================
    # QUESTION
    # =====================================================

    st.info(
        f"❓ {current_question}"
    )


    # =====================================================
    # QUESTION VOICE
    # =====================================================

    if st.button(
        "🔊 Listen Question",
        use_container_width=True
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


            os.remove(
                audio_file
            )


        except Exception as e:

            st.error(
                f"Voice generation failed: {e}"
            )


    st.divider()


    # =====================================================
    # CURRENT ANSWER VALUE
    # =====================================================

    current_answer = st.session_state.answer_values.get(
        index,
        ""
    )


    # =====================================================
    # ANSWER BOX
    # =====================================================

    st.markdown(
        "### 📝 Your Answer"
    )


    answer = st.text_area(

        "Type your answer or use microphone",

        value=current_answer,

        height=130,

        key=f"answer_box_{index}"
    )


    # Save manually typed answer

    st.session_state.answer_values[index] = answer


    # =====================================================
    # VOICE RECORDER
    # =====================================================

    st.caption(
        "🎙️ Or speak your answer"
    )


    audio = mic_recorder(

        start_prompt="🎙️ Start Recording",

        stop_prompt="⏹️ Stop Recording",

        just_once=True,

        format="wav",

        key=f"voice_recorder_{index}"
    )


    # =====================================================
    # VOICE → TEXT
    # =====================================================

    if audio:

        st.success(
            "🎤 Voice recorded successfully!"
        )


        st.audio(
            audio["bytes"],
            format="audio/wav"
        )


        with st.spinner(
            "🎧 Converting voice to text..."
        ):

            try:

                converted_text = convert_voice_to_text(

                    audio["bytes"],

                    language
                )


                # ------------------------------------------------
                # STORE CONVERTED TEXT
                # ------------------------------------------------

                st.session_state.voice_text[index] = (
                    converted_text
                )


                # ------------------------------------------------
                # IMPORTANT:
                # Store it BEFORE widget is created
                # on next rerun.
                # ------------------------------------------------

                st.session_state.answer_values[index] = (
                    converted_text
                )


                st.success(
                    "✅ Speech converted successfully!"
                )


                st.rerun()


            except sr.UnknownValueError:

                st.error(
                    "❌ Voice સમજાઈ નથી. "
                    "Please speak clearly and try again."
                )


            except sr.RequestError:

                st.error(
                    "❌ Speech recognition service unavailable."
                )


            except Exception as e:

                st.error(
                    f"Voice-to-text failed: {e}"
                )


    # =====================================================
    # SHOW CONVERTED TEXT
    # =====================================================

    if index in st.session_state.voice_text:

        st.success(
            "📝 Voice converted to text and added to Answer box."
        )


    # =====================================================
    # NEXT / SUBMIT
    # =====================================================

    if index < len(questions) - 1:

        button_text = (
            "➡️ Next Question"
        )

    else:

        button_text = (
            "🎓 Submit Interview"
        )


    if st.button(
        button_text,
        use_container_width=True
    ):

        final_answer = st.session_state.answer_values.get(
            index,
            ""
        )


        if not final_answer.strip():

            st.warning(
                "⚠️ Please type an answer or record your voice."
            )

            st.stop()


        # -----------------------------------------------------
        # SAVE ANSWER
        # -----------------------------------------------------

        st.session_state.answers.append(

            {
                "question":
                current_question,

                "answer":
                final_answer
            }
        )


        # =====================================================
        # NEXT QUESTION
        # =====================================================

        if index < len(questions) - 1:

            next_index = index + 1


            st.session_state.current_q_index = (
                next_index
            )


            st.rerun()


        # =====================================================
        # SUBMIT
        # =====================================================

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
                "🤖 AI evaluating your answers..."
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

                        st.session_state.step = "report"

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
                        f"Connection Error: {e}"
                    )


# =========================================================
# STEP 3 : REPORT
# =========================================================

elif st.session_state.step == "report":

    st.balloons()


    st.success(
        "🎉 Interview Completed Successfully"
    )


    report = st.session_state.report


    if report is None:

        st.error(
            "Report data is not available."
        )

        st.stop()


    # =====================================================
    # CANDIDATE
    # =====================================================

    col1, col2 = st.columns(2)


    with col1:

        st.info(
            f"👤 Candidate\n\n"
            f"{report['candidate_name']}"
        )


    with col2:

        st.info(
            f"💼 Job Role\n\n"
            f"{report['job_role']}"
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


    # =====================================================
    # AI FEEDBACK
    # =====================================================

    st.subheader(
        "💡 AI Feedback"
    )


    for item in report[
        "detailed_feedback"
    ]:

        with st.expander(
            f"❓ {item['question']}"
        ):

            st.write(
                "📝 Your Answer:"
            )

            st.write(
                item["answer"]
            )

            st.write(
                f"⭐ Score: "
                f"{item['score']} / 5"
            )

            st.success(
                item["feedback"]
            )


    # =====================================================
    # PDF
    # =====================================================

    st.divider()


    if st.button(
        "📄 Generate PDF Report",
        use_container_width=True
    ):

        try:

            pdf_file = generate_pdf_report(

                filename="Interview_Report.pdf",

                candidate_name=
                report["candidate_name"],

                job_role=
                report["job_role"],

                total_score=
                report["total_score"],

                max_score=
                report["max_score"],

                percentage=
                report["percentage"],

                recommendation=
                report["recommendation"],

                feedback_report=
                report["detailed_feedback"]
            )


            with open(
                pdf_file,
                "rb"
            ) as file:

                st.download_button(

                    label="⬇️ Download PDF",

                    data=file,

                    file_name="Interview_Report.pdf",

                    mime="application/pdf",

                    use_container_width=True
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

        st.session_state.answer_values = {}

        st.session_state.selected_language = "English"

        st.rerun()