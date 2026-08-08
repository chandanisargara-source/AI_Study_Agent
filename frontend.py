import streamlit as st
import requests
from report import generate_pdf_report
from streamlit_mic_recorder import mic_recorder

st.set_page_config(
    page_title="AI Job Interview Agent",
    page_icon="🤖",
    layout="wide"
)

BACKEND_URL = "http://127.0.0.1:8000"


if "token" not in st.session_state:
    st.session_state.token = None

if "user" not in st.session_state:
    st.session_state.user = None

# Session State
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

    st.title("🔐 AI Study Agent Login")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )


    if st.button("Login"):

        try:

            response = requests.post(
                f"{BACKEND_URL}/auth/login",
                json={
                    "email": email,
                    "password": password
                }
            )

            if response.status_code == 200:

                data = response.json()

                st.session_state.token = data["access_token"]

                headers = {
                    "Authorization": f"Bearer {st.session_state.token}"
                }

                user_response = requests.get(
                    f"{BACKEND_URL}/users/me",
                    headers=headers
                )

                if user_response.status_code == 200:
                    st.session_state.user = user_response.json()

                st.success("Login Successful 🎉")
                st.rerun()

            else:
                st.error("Invalid Email or Password")


        except Exception as e:
            st.error(str(e))


    st.stop()

# Sidebar
st.sidebar.title("📋 Dashboard")
st.sidebar.success("Project Status : Running")

st.sidebar.write("✅ Resume Upload")
st.sidebar.write("✅ AI Resume Analysis")
st.sidebar.write("✅ Mock Interview")
st.sidebar.write("✅ AI Evaluation")
st.sidebar.write("✅ Performance Report")


st.title("🤖 AI Job Interview Agent")
st.subheader("AI Powered Resume Analysis & Mock Interview System")

st.divider()


# ==========================
# STEP 1 : UPLOAD
# ==========================

if st.session_state.step == "upload":

    st.subheader("📝 Candidate Details")

    name = st.text_input(
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


    if uploaded_file is not None:

        st.success("✅ Resume Uploaded Successfully")


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


        if st.button("🚀 Start Interview"):

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
                            params=params
                        )


                        if response.status_code == 200:

                            data = response.json()

                            st.session_state.questions = data["questions"]

                            st.session_state.candidate_name = name

                            st.session_state.job_role = role

                            st.session_state.answers = []

                            st.session_state.current_q_index = 0

                            st.session_state.step = "interview"

                            st.rerun()


                        else:

                            st.error(
                                "Backend Error"
                            )


                    except Exception as e:

                        st.error(
                            str(e)
                        )
                        # ==========================
# STEP 2 : INTERVIEW
# ==========================

elif st.session_state.step == "interview":

    questions = st.session_state.questions
    index = st.session_state.current_q_index


    st.subheader(
        f"💬 Interview Question {index + 1}/{len(questions)}"
    )


    st.info(
        questions[index]
    )


    answer = st.text_area(
        "Your Answer:",
        height=150
    )

    st.write("🎤 Or answer using your voice")

    audio = mic_recorder(
        start_prompt="🎙️ Start Recording",
        stop_prompt="⏹️ Stop Recording",
        key="voice_recorder"
    )

    if audio:
        st.success("Voice recorded successfully!")


    if st.button(
        "Next Question ➡️"
        if index < len(questions)-1
        else
        "Submit Interview 🎓"
    ):


        if not answer.strip():

            st.warning(
                "કૃપા કરીને જવાબ લખો"
            )


        else:

            st.session_state.answers.append(
                {
                    "question": questions[index],
                    "answer": answer
                }
            )


            if index < len(questions)-1:

                st.session_state.current_q_index += 1

                st.rerun()


            else:

                with st.spinner(
                    "AI evaluating answers..."
                ):

                    payload = {

                        "name": st.session_state.candidate_name,

                        "role": st.session_state.job_role,

                        "answers": st.session_state.answers
                    }


                    try:

                        response = requests.post(
                            f"{BACKEND_URL}/submit-interview",
                            json=payload
                        )


                        if response.status_code == 200:

                            st.session_state.report = response.json()

                            st.session_state.step = "report"

                            st.rerun()


                        else:

                            st.error(
                                "Report generation failed"
                            )


                    except Exception as e:

                        st.error(
                            str(e)
                        )



# ==========================
# STEP 3 : REPORT
# ==========================

elif st.session_state.step == "report":

    st.balloons()

    st.success("🎉 Interview Completed Successfully")

    report = st.session_state.report

    st.info(
        f"""
    👤 Candidate : {report['candidate_name']}

    💼 Job Role : {report['job_role']}
    """
    )

    st.subheader(
        "📊 Performance Report"
    )

    st.progress(int(float(report["percentage"].replace("%", ""))) / 100)

    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Questions",
        len(report["detailed_feedback"])
    )

    
    col2.metric(
        "Score",
        f"{report['total_score']} / {report['max_score']}"
    )


    col3.metric(
        "Percentage",
        report["percentage"]
    )


    if report["recommendation"] == "Excellent Candidate - Recommended":
        st.success(f"🏆 {report['recommendation']}")

    elif report["recommendation"] == "Good Candidate - Can Be Considered":
        st.info(f"👍 {report['recommendation']}")

    elif report["recommendation"] == "Average - Needs Improvement":
        st.warning(f"⚠️ {report['recommendation']}")

    else:
        st.error(f"❌ {report['recommendation']}")
    
    st.markdown("---")

    st.subheader("💡 AI Feedback")
    st.caption("AI evaluation for each interview answer")
    
    for item in report["detailed_feedback"]:

            st.markdown(f"### ❓ {item['question']}")

            st.write("📝 **Your Answer:**")
            st.write(item["answer"])

            st.write(f"⭐ **Score:** {item['score']} / 5")

            st.success(item["feedback"])

            st.markdown("### 📝 Your Answer")
            st.write(item["answer"])

            st.markdown(f"### ⭐ Score : {item['score']} / 5")

            st.markdown("### 💡 AI Feedback")
            st.success(item["feedback"])
   
    if st.button("📄 Generate PDF Report"):

        pdf_file = generate_pdf_report(
            filename="Interview_Report.pdf",
            candidate_name=report["candidate_name"],
            job_role=report["job_role"],
            total_score=report["total_score"],
            max_score=report["max_score"],
            percentage=report["percentage"],
            recommendation=report["recommendation"],
            feedback_report=report["detailed_feedback"]
        )

        st.success("✅ PDF Report Generated Successfully!")

        with open(pdf_file, "rb") as file:
            st.download_button(
                label="⬇️ Download PDF",
                data=file,
                file_name="Interview_Report.pdf",
                mime="application/pdf"
        )
    
    if st.button("🔄 Restart Interview"):

        st.session_state.step = "upload"
        st.session_state.questions = []
        st.session_state.answers = []

        st.rerun()