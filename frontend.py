import streamlit as st
import requests
from gtts import gTTS
import speech_recognition as sr
from pydub import AudioSegment
import io

from report import generate_pdf_report
from streamlit_mic_recorder import mic_recorder


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Job Interview Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
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

        "subtitle":
        "AI Powered Resume Analysis & Mock Interview System",

        "candidate":
        "Candidate Name",

        "role":
        "Job Role",

        "company":
        "Target Company",

        "interview_type":
        "Interview Type",

        "experience":
        "Experience Level",

        "language":
        "Interview Language",

        "upload_resume":
        "Upload Resume (PDF)",

        "start":
        "🚀 Start Interview",

        "question":
        "Interview Question",

        "listen":
        "🔊 Listen Question",

        "voice_answer":
        "🎤 Your Voice Answer",

        "voice_help":
        "Speak your answer. It will automatically convert to text.",

        "text_answer":
        "📝 Your Answer",

        "text_help":
        "You can edit the converted text or type manually.",

        "coach":
        "💡 Answer Tips",

        "coach_help":
        "Use these hints to structure your answer.",

        "next":
        "Next Question ➜",

        "submit":
        "Submit Interview 🎓",

        "recorded":
        "✅ Voice recorded successfully!",

        "converting":
        "📝 Converting voice to text...",

        "empty":
        "Please type an answer or record your voice.",

        "back":
        "← Back",

        "report":
        "📊 Performance Report",

        "feedback":
        "💡 AI Feedback",

        "restart":
        "🔄 Restart Interview"
    },


    "Gujarati": {
        "speech": "gu-IN",
        "tts": "gu",

        "title":
        "AI જોબ ઇન્ટરવ્યૂ એજન્ટ",

        "subtitle":
        "AI આધારિત Resume Analysis અને Mock Interview System",

        "candidate":
        "ઉમેદવારનું નામ",

        "role":
        "જોબ રોલ",

        "company":
        "Target Company",

        "interview_type":
        "ઇન્ટરવ્યૂ પ્રકાર",

        "experience":
        "અનુભવનું સ્તર",

        "language":
        "ઇન્ટરવ્યૂ ભાષા",

        "upload_resume":
        "Resume Upload કરો (PDF)",

        "start":
        "🚀 ઇન્ટરવ્યૂ શરૂ કરો",

        "question":
        "ઇન્ટરવ્યૂ પ્રશ્ન",

        "listen":
        "🔊 પ્રશ્ન સાંભળો",

        "voice_answer":
        "🎤 તમારો Voice Answer",

        "voice_help":
        "તમારો જવાબ બોલો. તે આપમેળે Textમાં convert થશે.",

        "text_answer":
        "📝 તમારો જવાબ",

        "text_help":
        "Voiceમાંથી આવેલ જવાબ edit કરી શકો છો અથવા manually લખી શકો છો.",

        "coach":
        "💡 Answer Tips",

        "coach_help":
        "તમારા જવાબને સારી રીતે structure કરવા માટે આ hints ઉપયોગ કરો.",

        "next":
        "આગળનો પ્રશ્ન ➜",

        "submit":
        "ઇન્ટરવ્યૂ Submit કરો 🎓",

        "recorded":
        "✅ Voice સફળતાપૂર્વક record થયો!",

        "converting":
        "📝 Voice ને Textમાં convert કરી રહ્યા છીએ...",

        "empty":
        "કૃપા કરીને જવાબ લખો અથવા voice record કરો.",

        "back":
        "← પાછા જાઓ",

        "report":
        "📊 Performance Report",

        "feedback":
        "💡 AI Feedback",

        "restart":
        "🔄 ઇન્ટરવ્યૂ ફરી શરૂ કરો"
    },


    "Hindi": {
        "speech": "hi-IN",
        "tts": "hi",

        "title":
        "AI जॉब इंटरव्यू एजेंट",

        "subtitle":
        "AI आधारित Resume Analysis और Mock Interview System",

        "candidate":
        "उम्मीदवार का नाम",

        "role":
        "जॉब रोल",

        "company":
        "Target Company",

        "interview_type":
        "इंटरव्यू प्रकार",

        "experience":
        "अनुभव स्तर",

        "language":
        "इंटरव्यू भाषा",

        "upload_resume":
        "Resume Upload करें (PDF)",

        "start":
        "🚀 इंटरव्यू शुरू करें",

        "question":
        "इंटरव्यू प्रश्न",

        "listen":
        "🔊 प्रश्न सुनें",

        "voice_answer":
        "🎤 आपका Voice Answer",

        "voice_help":
        "अपना जवाब बोलें। यह अपने आप Text में convert होगा।",

        "text_answer":
        "📝 आपका जवाब",

        "text_help":
        "Voice से आए जवाब को edit कर सकते हैं या manually लिख सकते हैं।",

        "coach":
        "💡 Answer Tips",

        "coach_help":
        "अपने जवाब को बेहतर बनाने के लिए इन hints का उपयोग करें।",

        "next":
        "अगला प्रश्न ➜",

        "submit":
        "इंटरव्यू Submit करें 🎓",

        "recorded":
        "✅ Voice सफलतापूर्वक record हुई!",

        "converting":
        "📝 Voice को Text में convert किया जा रहा है...",

        "empty":
        "कृपया जवाब लिखें या voice record करें।",

        "back":
        "← वापस",

        "report":
        "📊 Performance Report",

        "feedback":
        "💡 AI Feedback",

        "restart":
        "🔄 इंटरव्यू फिर से शुरू करें"
    },


    "Hinglish": {
        "speech": "en-IN",
        "tts": "en",

        "title":
        "AI Job Interview Agent",

        "subtitle":
        "AI Powered Resume Analysis & Mock Interview System",

        "candidate":
        "Candidate Name",

        "role":
        "Job Role",

        "company":
        "Target Company",

        "interview_type":
        "Interview Type",

        "experience":
        "Experience Level",

        "language":
        "Interview Language",

        "upload_resume":
        "Upload Resume (PDF)",

        "start":
        "🚀 Start Interview",

        "question":
        "Interview Question",

        "listen":
        "🔊 Listen Question",

        "voice_answer":
        "🎤 Your Voice Answer",

        "voice_help":
        "Apna answer bolo. Ye automatically Text mein convert hoga.",

        "text_answer":
        "📝 Your Answer",

        "text_help":
        "Converted text ko edit kar sakte ho ya manually type kar sakte ho.",

        "coach":
        "💡 Answer Tips",

        "coach_help":
        "Answer ko better structure karne ke liye ye hints use karo.",

        "next":
        "Next Question ➜",

        "submit":
        "Submit Interview 🎓",

        "recorded":
        "✅ Voice successfully recorded!",

        "converting":
        "📝 Voice ko Text mein convert kar rahe hain...",

        "empty":
        "Please answer type karo ya voice record karo.",

        "back":
        "← Back",

        "report":
        "📊 Performance Report",

        "feedback":
        "💡 AI Feedback",

        "restart":
        "🔄 Restart Interview"
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

    lang_code = LANGUAGE_DATA[language]["tts"]

    tts = gTTS(
        text=text,
        lang=lang_code
    )

    audio_file = "question_audio.mp3"

    tts.save(audio_file)

    return audio_file


# =========================================================
# ANSWER TIPS
# =========================================================

def get_answer_tips(question, language):

    q = question.lower()

    if language == "Gujarati":

        if "project" in q or "challenge" in q:

            return [
                "💡 Project શું હતું તે જણાવો.",
                "💡 તમારો role અને technologies જણાવો.",
                "💡 કયો challenge આવ્યો તે જણાવો.",
                "💡 તમે તેને કેવી રીતે solve કર્યો તે સમજાવો.",
                "💡 અંતે result જણાવો."
            ]

        if "strength" in q:

            return [
                "💡 તમારી 1-2 strengths જણાવો.",
                "💡 એક practical example આપો.",
                "💡 આ strength jobમાં કેવી રીતે મદદ કરશે તે કહો."
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

        return [
            "💡 Questionનો direct જવાબ આપો.",
            "💡 Relevant example આપો.",
            "💡 Answer clear અને concise રાખો."
        ]


    if language == "Hindi":

        if "project" in q or "challenge" in q:

            return [
                "💡 Project क्या था बताएं।",
                "💡 अपना role और technologies बताएं।",
                "💡 कौन सा challenge आया बताएं।",
                "💡 आपने उसे कैसे solve किया बताएं।",
                "💡 अंत में result बताएं।"
            ]

        if "strength" in q:

            return [
                "💡 अपनी 1-2 strengths बताएं।",
                "💡 एक practical example दें।",
                "💡 यह strength job में कैसे मदद करेगी बताएं।"
            ]

        if "weakness" in q:

            return [
                "💡 एक genuine weakness बताएं।",
                "💡 उसे improve करने के लिए क्या कर रहे हैं बताएं।",
                "💡 Learning attitude दिखाएं।"
            ]

        return [
            "💡 Question का direct answer दें।",
            "💡 Relevant example दें।",
            "💡 Answer clear और concise रखें।"
        ]


    if language == "Hinglish":

        return [
            "💡 Question ka direct answer do.",
            "💡 Relevant example do.",
            "💡 Apni skills ko role ke saath connect karo.",
            "💡 Answer short aur clear rakho."
        ]


    return [
        "💡 Answer the question directly.",
        "💡 Give a relevant example.",
        "💡 Connect your answer with the job.",
        "💡 Keep your answer clear and concise."
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

    selected_language = st.selectbox(

        "🌐 Interview Language",

        list(LANGUAGE_DATA.keys()),

        index=list(
            LANGUAGE_DATA.keys()
        ).index(
            st.session_state.selected_language
        )
    )


    st.session_state.selected_language = (
        selected_language
    )


language = st.session_state.selected_language

T = LANGUAGE_DATA[language]


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title(
    "📋 Dashboard"
)

st.sidebar.success(
    "🟢 Project Running"
)

st.sidebar.write(
    "✅ Resume Upload"
)

st.sidebar.write(
    "✅ AI Question Generation"
)

st.sidebar.write(
    "✅ Voice Interview"
)

st.sidebar.write(
    "✅ Speech to Text"
)

st.sidebar.write(
    "✅ Multi-Language"
)

st.sidebar.write(
    "✅ Answer Tips"
)

st.sidebar.write(
    "✅ AI Evaluation"
)

st.sidebar.write(
    "✅ Performance Report"
)

st.sidebar.divider()

st.sidebar.info(
    f"🌐 Language\n\n{language}"
)


# =========================================================
# MAIN HEADER
# =========================================================

if st.session_state.step == "upload":

    st.title(
        f"🤖 {T['title']}"
    )

    st.caption(
        T["subtitle"]
    )

    st.divider()


# =========================================================
# STEP 1 : RESUME UPLOAD
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


                    # IMPORTANT:
                    # Language is sent to backend
                    # so questions can be generated
                    # in selected language.

                    params = {

                        "name":
                        candidate_name,

                        "role":
                        role,

                        "language":
                        language
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
# STEP 2 : CLEAN INTERVIEW PAGE
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
    # TOP HEADER
    # =====================================================

    st.markdown(
        "## 🤖 AI MOCK INTERVIEW"
    )


    st.caption(

        f"{T['question']} "
        f"{index + 1} / {len(questions)}"
    )


    progress = (

        (index + 1)

        /

        len(questions)
    )


    st.progress(
        progress
    )


    st.divider()


    # =====================================================
    # QUESTION
    # =====================================================

    st.markdown(
        f"### 💬 {T['question']}"
    )


    st.markdown(
        f"""
        <div style="
            padding:22px;
            border-radius:15px;
            border:1px solid rgba(128,128,128,0.25);
            margin-bottom:15px;
        ">
        <h3>{current_question}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # LISTEN QUESTION
    # =====================================================

    if st.button(

        T["listen"],

        key=f"listen_question_{index}"
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
    # ANSWER SECTION
    # =====================================================

    st.markdown(
        f"### {T['voice_answer']}"
    )


    st.caption(
        T["voice_help"]
    )


    # =====================================================
    # VOICE RECORDER
    # =====================================================

    audio = mic_recorder(

        start_prompt="🎙️ Start Recording",

        stop_prompt="⏹️ Stop Recording",

        key=f"voice_recorder_{index}"
    )


    # =====================================================
    # PROCESS AUDIO
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

            raw_audio = audio["bytes"]


            # ---------------------------------------------
            # AUDIO CONVERSION
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


            speech_language = (

                LANGUAGE_DATA[language]["speech"]
            )


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
            # SAVE CONVERTED TEXT
            # ---------------------------------------------

            st.session_state.voice_text[index] = (

                converted_text
            )


            st.success(
                "📝 Voice converted successfully!"
            )


        except sr.UnknownValueError:

            st.error(
                "❌ Speech could not be understood. "
                "Please speak clearly and try again."
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


    answer_key = f"answer_box_{index}"


    # IMPORTANT:
    # If voice text is available and widget does not exist,
    # initialize it before creating widget.

    if answer_key not in st.session_state:

        st.session_state[answer_key] = (

            st.session_state.voice_text.get(
                index,
                ""
            )
        )


    answer = st.text_area(

        T["text_answer"],

        height=160,

        key=answer_key
    )


    st.divider()


    # =====================================================
    # ANSWER TIPS
    # =====================================================

    if st.button(

        T["coach"],

        key=f"coach_button_{index}"
    ):

        st.session_state.coach_visible = (

            not st.session_state.coach_visible
        )


    if st.session_state.coach_visible:

        st.info(
            T["coach_help"]
        )


        tips = get_answer_tips(

            current_question,

            language
        )


        for tip in tips:

            st.write(
                tip
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

        key=f"next_question_{index}",

        use_container_width=True
    ):


        final_answer = answer.strip()


        if not final_answer:

            st.warning(
                T["empty"]
            )

            st.stop()


        st.session_state.answers.append(

            {
                "question":
                current_question,

                "answer":
                final_answer
            }
        )


        # =================================================
        # NEXT QUESTION
        # =================================================

        if index < len(questions) - 1:

            st.session_state.current_q_index += 1

            st.session_state.coach_visible = False

            st.rerun()


        # =================================================
        # FINAL SUBMIT
        # =================================================

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


    st.divider()


    # =====================================================
    # AI FEEDBACK
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
                "✅ PDF Report Generated Successfully!"
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


    st.divider()


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


        # Remove old answer widgets

        keys_to_remove = [

            key

            for key in st.session_state.keys()

            if key.startswith("answer_box_")
        ]


        for key in keys_to_remove:

            del st.session_state[key]


        st.rerun()