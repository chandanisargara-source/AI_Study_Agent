import streamlit as st
import requests
from gtts import gTTS
import speech_recognition as sr
import speech_recognition as sr
import io
from report import generate_pdf_report
from streamlit_mic_recorder import mic_recorder


# ==========================
# STEP 2 : INTERVIEW
# ==========================

elif st.session_state.step == "interview":

    questions = st.session_state.questions

    index = st.session_state.current_q_index

    if not questions:

        st.error(
            "No interview questions available."
        )

        if st.button(
            "🔄 Back to Upload",
            key="back_to_upload"
        ):

            st.session_state.step = "upload"

            st.rerun()

    else:

        current_question = questions[index]

        st.subheader(
            f"💬 Interview Question "
            f"{index + 1}/{len(questions)}"
        )

        # ==========================
        # AI QUESTION
        # ==========================

        st.info(
            current_question
        )

        # ==========================
        # 🔊 LISTEN TO QUESTION
        # ==========================

        if st.button(
            "🔊 Listen Question",
            key=f"listen_question_{index}"
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

        # ==========================
        # 🎤 VOICE ANSWER
        # ==========================

        st.subheader(
            "🎤 Your Answer"
        )

        st.caption(
            "Speak your answer. "
            "You do not need to type anything."
        )

        audio = mic_recorder(
            start_prompt="🎙️ Start Recording",
            stop_prompt="⏹️ Stop Recording",
            key=f"voice_recorder_{index}"
        )

        # Get previous answer if already converted
        answer = st.session_state.get(
            f"voice_answer_{index}",
            ""
        )

        # ==========================
        # VOICE RECORDED
        # ==========================

        if audio:

            st.success(
                "✅ Voice recorded successfully!"
            )

            # Play recorded voice
            st.audio(
                audio["bytes"],
                format="audio/wav"
            )

            try:

                # ==========================
                # SPEECH TO TEXT
                # ==========================

                recognizer = sr.Recognizer()

                audio_file = sr.AudioFile(
                    io.BytesIO(
                        audio["bytes"]
                    )
                )

                with audio_file as source:

                    recorded_audio = recognizer.record(
                        source
                    )

                with st.spinner(
                    "📝 Converting your voice to text..."
                ):

                    answer = recognizer.recognize_google(
                        recorded_audio
                    )

                # Save converted answer
                st.session_state[
                    f"voice_answer_{index}"
                ] = answer

                st.success(
                    "✅ Voice converted to text successfully!"
                )

                # Show automatic transcript
                st.write(
                    "📝 **Your Answer:**"
                )

                st.info(
                    answer
                )

            except sr.UnknownValueError:

                st.error(
                    "❌ I could not understand your voice."
                )

                st.info(
                    "Please record your answer again "
                    "clearly."
                )

            except sr.RequestError as e:

                st.error(
                    "❌ Speech recognition service "
                    "is unavailable."
                )

                st.code(
                    str(e)
                )

            except Exception as e:

                st.error(
                    f"❌ Voice-to-text failed: {e}"
                )

        # ==========================
        # SHOW SAVED ANSWER
        # ==========================

        if answer:

            st.write(
                "📝 **Final Answer:**"
            )

            st.info(
                answer
            )

        # ==========================
        # NEXT / SUBMIT
        # ==========================

        button_text = (
            "Next Question ➡️"
            if index < len(questions) - 1
            else "Submit Interview 🎓"
        )

        if st.button(
            button_text,
            key=f"next_question_{index}"
        ):

            # ==========================
            # CHECK ANSWER
            # ==========================

            if not answer.strip():

                st.warning(
                    "🎤 Please record your answer first."
                )

            else:

                # ==========================
                # SAVE ANSWER
                # ==========================

                st.session_state.answers.append(
                    {
                        "question": current_question,
                        "answer": answer
                    }
                )

                # ==========================
                # NEXT QUESTION
                # ==========================

                if index < len(questions) - 1:

                    st.session_state.current_q_index += 1

                    st.rerun()

                # ==========================
                # SUBMIT INTERVIEW
                # ==========================

                else:

                    with st.spinner(
                        "🤖 AI evaluating answers..."
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

                                try:

                                    st.session_state.report = (
                                        response.json()
                                    )

                                except Exception:

                                    st.error(
                                        "Backend returned invalid report."
                                    )

                                    st.code(
                                        response.text
                                    )

                                    st.stop()

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

    report = st.session_state.report

    if report is None:

        st.error(
            "Report data is not available."
        )

        st.stop()

    # ==========================
    # CANDIDATE INFORMATION
    # ==========================

    st.info(
        f"""
👤 Candidate : {report['candidate_name']}

💼 Job Role : {report['job_role']}
"""
    )

    # ==========================
    # PERFORMANCE REPORT
    # ==========================

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

    # ==========================
    # RECOMMENDATION
    # ==========================

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

    st.markdown(
        "---"
    )

    # ==========================
    # AI FEEDBACK
    # ==========================

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

    st.markdown(
        "---"
    )

    if st.button(
        "📄 Generate PDF Report",
        key="generate_pdf_button"
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
                    mime="application/pdf",
                    key="download_pdf_button"
                )

        except Exception as e:

            st.error(
                f"PDF generation failed: {e}"
            )

    # ==========================
    # RESTART INTERVIEW
    # ==========================

    if st.button(
        "🔄 Restart Interview",
        key="restart_interview_button"
    ):

        st.session_state.step = "upload"

        st.session_state.questions = []

        st.session_state.answers = []

        st.session_state.current_q_index = 0

        st.session_state.candidate_name = ""

        st.session_state.job_role = ""

        st.session_state.report = None

        st.rerun()