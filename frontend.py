import streamlit as st
import requests
from gtts import gTTS
import speech_recognition as sr
import io
from pydub import AudioSegment
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
# TEXT TO SPEECH
# =========================================================

def speak_question(text):

    tts = gTTS(
        text=text,
        lang="en"
    )

    audio_file = "question_audio.mp3"

    tts.save(audio_file)

    return audio_file


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
    "report": None
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

    name = st.text_input(
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

            if not name or not password:

                st.warning(
                    "Please enter name and password."
                )

            else:

                try:

                    response = requests.post(
                        f"{BACKEND_URL}/auth/login",
                        json={
                            "name": name,
                            "password": password
                        },
                        timeout=60
                    )


                    if response.status_code == 200:

                        data = response.json()

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

            if not name or not password:

                st.warning(
                    "Please enter name and password."
                )

            else:

                try:

                    response = requests.post(
                        f"{BACKEND_URL}/auth/signup",
                        json={
                            "name": name,
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
    "✅ Speech to Text"
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
                        "name": candidate_name,
                        "role": role
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

                    st.session_state.step = (
                        "interview"
                    )


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


        st.subheader(
            f"💬 Interview Question "
            f"{index + 1} / {len(questions)}"
        )


        # =================================================
        # QUESTION
        # =================================================

        st.info(
            current_question
        )


        # =================================================
        # LISTEN QUESTION
        # =================================================

        if st.button(
            "🔊 Listen Question",
            key=f"listen_{index}"
        ):

            try:

                audio_file = speak_question(
                    current_question
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
        # ANSWER KEY
        # =================================================

        answer_key = f"answer_{index}"


        if answer_key not in st.session_state:

            st.session_state[answer_key] = ""


        # =================================================
        # TEXT ANSWER
        # =================================================

        st.subheader(
            "📝 Your Answer"
        )


        st.caption(
            "Type your answer OR use 🎤 voice."
        )


        answer = st.text_area(
            "⌨️ Answer",
            key=answer_key,
            height=150
        )


        st.divider()


        # =================================================
        # VOICE ANSWER
        # =================================================

        st.subheader(
            "🎤 Voice Answer"
        )


        st.caption(
            "Speak your answer. "
            "It will automatically become text."
        )


        audio = mic_recorder(
            start_prompt="🎙️ Start Recording",
            stop_prompt="⏹️ Stop Recording",
            key=f"recorder_{index}"
        )


        if audio:

            st.success(
                "✅ Recording received!"
            )


            st.audio(
                audio["bytes"],
                format="audio/wav"
            )


            try:

                # =========================================
                # CONVERT AUDIO
                # =========================================

                recognizer = sr.Recognizer()


                audio_bytes = audio["bytes"]


                audio_segment = AudioSegment.from_file(
                    io.BytesIO(audio_bytes)
                )


                wav_buffer = io.BytesIO()


                audio_segment.export(
                    wav_buffer,
                    format="wav"
                )


                wav_buffer.seek(0)


                # =========================================
                # SPEECH RECOGNITION
                # =========================================

                with sr.AudioFile(
                    wav_buffer
                ) as source:

                    recorded_audio = recognizer.record(
                        source
                    )


                with st.spinner(
                    "📝 Converting speech to text..."
                ):

                    voice_text = (
                        recognizer.recognize_google(
                            recorded_audio,
                            language="en-IN"
                        )
                    )


                # =========================================
                # STORE TEXT
                # =========================================

                st.session_state[answer_key] = (
                    voice_text
                )


                st.success(
                    "✅ Speech converted to text!"
                )


                # =========================================
                # SHOW RESULT
                # =========================================

                st.write(
                    "📝 Converted Answer:"
                )

                st.write(
                    voice_text
                )


                # =========================================
                # REFRESH ONCE
                # =========================================

                st.rerun()


            except sr.UnknownValueError:

                st.error(
                    "❌ Voice could not be understood."
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
        # NEXT BUTTON
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
            key=f"next_{index}",
            use_container_width=True
        ):


            final_answer = st.session_state.get(
                answer_key,
                ""
            )


            if not final_answer.strip():

                st.warning(
                    "Please type an answer "
                    "or record your voice."
                )

                st.stop()


            # =============================================
            # SAVE ANSWER
            # =============================================

            st.session_state.answers.append(
                {
                    "question": current_question,
                    "answer": final_answer
                }
            )


            # =============================================
            # NEXT QUESTION
            # =============================================

            if index < len(questions) - 1:

                st.session_state.current_q_index += 1

                st.rerun()


            # =============================================
            # SUBMIT INTERVIEW
            # =============================================

            else:

                with st.spinner(
                    "🤖 AI evaluating interview..."
                ):

                    payload = {
                        "name":
                        st.session_state.candidate_name,

                        "role":
                        st.session_state.job_role,

                        "answers":
                        st.session_state.answers
                    }


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
    # FEEDBACK
    # =====================================================

    st.subheader(
        "💡 AI Feedback"
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
                "✅ PDF Generated!"
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


        st.rerun()