import streamlit as st
import requests
from report import generate_pdf_report
from streamlit_mic_recorder import mic_recorder


# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="AI Job Interview Agent",
    page_icon="🤖",
    layout="wide"
)


BACKEND_URL = "https://ai-study-agent-xqis.onrender.com"


# ==========================
# SESSION STATE
# ==========================

if "token" not in st.session_state:
    st.session_state.token = None

if "user" not in st.session_state:
    st.session_state.user = None

if "step" not in st.session_state:
    st.session_state.step = "upload"

if "questions" not in st.session_state:
    st.session_state.questions = []

if "answers" not in st.session_state:
    st.session_state.answers = []

if "current_q_index" not in st.session_state:
    st.session_state.current_q_index = 0

if "candidate_name" not in st.session_state:
    st.session_state.candidate_name = ""

if "job_role" not in st.session_state:
    st.session_state.job_role = ""

if "report" not in st.session_state:
    st.session_state.report = None

 # ==========================
# LOGIN SYSTEM
# ==========================

if st.session_state.token is None:

    st.title("🔐 AI Study Agent")

    mode = st.radio(
        "Choose an option",
        ["Login", "Sign Up"],
        horizontal=True,
        key="login_mode"
    )

    login_name = st.text_input(
        "Name",
        key="login_name"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    # ==========================
    # LOGIN
    # ==========================

    if mode == "Login":

        if st.button(
            "Login",
            key="login_button"
        ):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/auth/login",
                    json={
                        "name": login_name,
                        "password": password
                    },
                    timeout=30
                )

                if response.status_code != 200:

                    try:

                        error_data = response.json()

                        st.error(
                            f"Login failed: {error_data}"
                        )

                    except Exception:

                        st.error(
                            f"Login failed "
                            f"({response.status_code}): "
                            f"{response.text}"
                        )

                else:

                    try:

                        data = response.json()

                    except Exception:

                        st.error(
                            "Backend did not return valid JSON."
                        )

                        st.code(
                            response.text
                        )

                        st.stop()

                    if "access_token" not in data:

                        st.error(
                            f"Login response: {data}"
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
                            timeout=30
                        )

                        if user_response.status_code == 200:

                            st.session_state.user = (
                                user_response.json()
                            )

                        else:

                            st.session_state.user = None

                    except Exception:

                        st.session_state.user = None

                    st.session_state.step = "upload"

                    st.success(
                        "Login Successful 🎉"
                    )

                    st.rerun()
                    
            except requests.exceptions.RequestException as e:

                st.error(
                    f"Connection error: {e}"
                )

            except Exception as e:

                st.error(
                    f"Unexpected error: {e}"
                )

    # ==========================
    # SIGN UP
    # ==========================

    else:

        if st.button(
            "Create Account",
            key="signup_button"
        ):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/auth/signup",
                    json={
                        "name": login_name,
                        "password": password
                    },
                    timeout=30
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

                        error_data = response.json()

                        st.error(
                            f"Sign Up failed: {error_data}"
                        )

                    except Exception:

                        st.error(
                            f"Sign Up failed "
                            f"({response.status_code}): "
                            f"{response.text}"
                        )

            except requests.exceptions.RequestException as e:

                st.error(
                    f"Connection error: {e}"
                )

            except Exception as e:

                st.error(
                    f"Unexpected error: {e}"
                )

    st.stop()


# ==========================
# MAIN DASHBOARD
# ==========================

st.success("✅ MAIN DASHBOARD LOADED")

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
    "✅ AI Evaluation"
)

st.sidebar.write(
    "✅ Performance Report"
)

st.title(
    "🤖 AI Job Interview Agent"
)

st.subheader(
    "AI Powered Resume Analysis & Mock Interview System"
)

st.divider()

# ==========================
# STEP 1 : RESUME UPLOAD
# ==========================

if st.session_state.step == "upload":

    st.subheader(
        "📝 Candidate Details"
    )


    name = st.text_input(
        "Candidate Name",
        key="candidate_name_input"
    )


    role = st.text_input(
        "Job Role",
        key="job_role_input"
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
        ],
        key="company_input"
    )


    interview_type = st.selectbox(
        "Interview Type",
        [
            "Technical",
            "HR",
            "Behavioral",
            "Mixed"
        ],
        key="interview_type_input"
    )


    experience = st.selectbox(
        "Experience Level",
        [
            "Fresher",
            "0-2 Years",
            "2-5 Years",
            "5+ Years"
        ],
        key="experience_input"
    )


    uploaded_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"],
        key="resume_upload"
    )


    if uploaded_file is not None:

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
            "Fresher"
        )


        st.progress(85)


        if st.button(
            "🚀 Start Interview"
        ):

            if not name or not role:

                st.error(
                    "Please enter name and role"
                )


            else:

                with st.spinner(
                    "AI generating questions..."
                ):

                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf"
                        )
                    }


                    params = {
                        "name": name,
                        "role": role
                    }


                    try:

                        response = requests.post(
                            f"{BACKEND_URL}/upload-resume",
                            files=files,
                            params=params,
                            timeout=60
                        )


                        if response.status_code == 200:

                            data = response.json()


                            questions = data.get(
                                "questions",
                                []
                            )


                            if not questions:

                                st.error(
                                    "Backend returned no interview questions."
                                )


                            else:

                                st.session_state.questions = (
                                    questions
                                )

                                st.session_state.candidate_name = (
                                    name
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


                        else:

                            st.error(
                                f"Backend Error: "
                                f"{response.status_code}"
                            )

                            st.code(
                                response.text
                            )


                    except requests.exceptions.RequestException as e:

                        st.error(
                            f"Connection Error: {e}"
                        )


                    except Exception as e:

                        st.error(
                            f"Unexpected Error: {e}"
                        )


# ==========================
# STEP 2 : INTERVIEW
# ==========================

elif st.session_state.step == "interview":

    questions = (
        st.session_state.questions
    )

    index = (
        st.session_state.current_q_index
    )


    if not questions:

        st.error(
            "No interview questions found."
        )

        if st.button(
            "🔄 Back to Upload"
        ):

            st.session_state.step = "upload"

            st.rerun()


    else:

        st.subheader(
            f"💬 Interview Question "
            f"{index + 1}/{len(questions)}"
        )


        st.info(
            questions[index]
        )


        answer = st.text_area(
            "Your Answer:",
            height=150,
            key=f"answer_{index}"
        )


        st.write(
            "🎤 Or answer using your voice"
        )


        audio = mic_recorder(
            start_prompt="🎙️ Start Recording",
            stop_prompt="⏹️ Stop Recording",
            key=f"voice_recorder_{index}"
        )


        if audio:

            st.success(
                "Voice recorded successfully!"
            )


        if index < len(questions) - 1:

            button_text = (
                "Next Question ➡️"
            )

        else:

            button_text = (
                "Submit Interview 🎓"
            )


        if st.button(
            button_text
        ):

            if not answer.strip():

                st.warning(
                    "કૃપા કરીને જવાબ લખો"
                )


            else:

                st.session_state.answers.append(
                    {
                        "question":
                        questions[index],

                        "answer":
                        answer
                    }
                )


                if index < len(questions) - 1:

                    st.session_state.current_q_index += 1

                    st.rerun()


                else:

                    with st.spinner(
                        "AI evaluating answers..."
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
                                timeout=60
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


                        except requests.exceptions.RequestException as e:

                            st.error(
                                f"Connection Error: {e}"
                            )


                        except Exception as e:

                            st.error(
                                f"Unexpected Error: {e}"
                            )


# ==========================
# STEP 3 : REPORT
# ==========================

elif st.session_state.step == "report":

    st.balloons()


    st.success(
        "🎉 Interview Completed Successfully"
    )


    report = (
        st.session_state.report
    )


    st.info(
        f"""
👤 Candidate : {report['candidate_name']}

💼 Job Role : {report['job_role']}
"""
    )


    st.subheader(
        "📊 Performance Report"
    )


    percentage = float(
        str(
            report["percentage"]
        ).replace("%", "")
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


    recommendation = (
        report["recommendation"]
    )


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


    st.markdown("---")


    st.subheader(
        "💡 AI Feedback"
    )


    st.caption(
        "AI evaluation for each interview answer"
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


    # ==========================
    # PDF REPORT
    # ==========================

    if st.button(
        "📄 Generate PDF Report"
    ):

        try:

            pdf_file = generate_pdf_report(
                filename="Interview_Report.pdf",

                candidate_name=(
                    report["candidate_name"]
                ),

                job_role=(
                    report["job_role"]
                ),

                total_score=(
                    report["total_score"]
                ),

                max_score=(
                    report["max_score"]
                ),

                percentage=(
                    report["percentage"]
                ),

                recommendation=(
                    report["recommendation"]
                ),

                feedback_report=(
                    report["detailed_feedback"]
                )
            )


            st.success(
                "✅ PDF Report Generated Successfully!"
            )


            with open(
                pdf_file,
                "rb"
            ) as file:

                st.download_button(
                    label="⬇️ Download PDF",
                    data=file,
                    file_name="Interview_Report.pdf",
                    mime="application/pdf"
                )


        except Exception as e:

            st.error(
                f"PDF generation failed: {e}"
            )


    # ==========================
    # RESTART
    # ==========================

    if st.button(
        "🔄 Restart Interview"
    ):

        st.session_state.step = "upload"

        st.session_state.questions = []

        st.session_state.answers = []

        st.session_state.current_q_index = 0

        st.session_state.candidate_name = ""

        st.session_state.job_role = ""

        st.session_state.report = None

        st.rerun()