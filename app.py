import os
import streamlit as st
from dotenv import load_dotenv

from gnani.stt import GnaniSTTClient
from gnani.tts import GnaniTTSClient, AudioConfig


# -------------------------------
# 1. LOAD API KEY
# -------------------------------

load_dotenv()
API_KEY = os.getenv("GNANI_API_KEY")


# -------------------------------
# 2. STREAMLIT PAGE SETTINGS
# -------------------------------

st.set_page_config(
    page_title="SpeakSmart India",
    page_icon="🎤",
    layout="centered"
)

st.title("🎤 SpeakSmart India")
st.subheader("Your Multilingual AI Interview Partner")

st.write(
    "Practice interview questions, record your answers, "
    "convert your speech into text, and receive feedback."
)

if not API_KEY:
    st.error("API key missing. Please check your .env file.")
    st.stop()


# -------------------------------
# 3. INITIALIZE GNANI CLIENTS
# -------------------------------

@st.cache_resource
def get_clients(api_key):
    stt = GnaniSTTClient(api_key=api_key)
    tts = GnaniTTSClient(api_key=api_key)
    return stt, tts


try:
    stt_client, tts_client = get_clients(API_KEY)

except Exception as e:
    st.error(f"Could not initialize Gnani clients: {e}")
    st.stop()


# -------------------------------
# 4. INTERVIEW QUESTIONS
# -------------------------------

questions = {
    "HR Interview": [
        "Tell me about yourself.",
        "What are your strengths and weaknesses?",
        "Why should we hire you?",
        "Where do you see yourself in five years?"
    ],

    "Technical Interview": [
        "Explain the concept of object-oriented programming.",
        "What is the difference between a list and a tuple in Python?",
        "What is a database?",
        "Explain the concept of machine learning."
    ]
}


category = st.selectbox(
    "Choose interview category",
    list(questions.keys())
)

question = st.selectbox(
    "Choose your interview question",
    questions[category]
)


# -------------------------------
# 5. SELECT LANGUAGE
# -------------------------------

language = st.selectbox(
    "Choose your answer language",
    ["English", "Telugu"]
)

language_code = (
    "en-IN" if language == "English" else "te-IN"
)


# -------------------------------
# 6. TEXT TO SPEECH
# -------------------------------

st.divider()
st.header("🔊 Listen to the Interview Question")

if st.button("Listen to Question", key="listen_question"):

    try:
        with st.spinner("Generating question audio..."):

            audio = tts_client.synthesize(
                question,
                voice="Nalini",
                model="timbre-v2.5",
                language="en-IN",
                audio_config=AudioConfig(
                    sample_rate=48000,
                    encoding="linear_pcm",
                    container="wav"
                )
            )

        st.audio(audio, format="audio/wav")
        st.success("Question audio generated successfully!")

    except Exception as e:
        st.error(f"Text-to-speech error: {e}")


# -------------------------------
# 7. RECORD YOUR ANSWER
# -------------------------------

st.divider()
st.header("🎙️ Record Your Answer")

st.write(
    "Allow microphone access in your browser. "
    "Click the microphone button, speak your answer, "
    "and stop recording when finished."
)

recording = st.audio_input(
    "Click here to record your interview answer",
    sample_rate=16000,
    key="answer_recording"
)


# -------------------------------
# 8. PLAY AND TRANSCRIBE AUDIO
# -------------------------------

if recording is not None:

    audio_bytes = recording.getvalue()

    if len(audio_bytes) == 0:
        st.warning("No audio was captured. Please record again.")

    else:
        st.success("Recording captured successfully!")

        st.write("Recording size:", len(audio_bytes), "bytes")

        # Play recorded audio
        st.audio(audio_bytes, format="audio/wav")

        if st.button(
            "Convert Speech to Text",
            key="convert_speech"
        ):

            try:
                with st.spinner("Gnani Prisma is transcribing your answer..."):

                    result = stt_client.transcribe_bytes(
                        audio_bytes,
                        filename="interview_answer.wav",
                        language_code=language_code
                    )

                    transcript = result.get("transcript", "").strip()

                    if not transcript:
                        st.warning(
                            "No speech was detected. "
                            "Please record your answer again."
                        )

                    else:
                        st.session_state["transcript"] = transcript
                        st.success("Speech-to-text completed!")

            except Exception as e:
                st.error(f"Speech-to-text error: {e}")


# -------------------------------
# 9. DISPLAY TRANSCRIPT
# -------------------------------

if st.session_state.get("transcript"):

    transcript = st.session_state["transcript"]

    st.divider()
    st.header("📝 Your Answer")

    st.text_area(
        "Transcribed answer",
        value=transcript,
        height=180
    )

    st.download_button(
        label="Download Transcript",
        data=transcript,
        file_name="interview_answer.txt",
        mime="text/plain"
    )


    # -------------------------------
    # 10. BASIC ANSWER FEEDBACK
    # -------------------------------

    st.header("📊 Answer Feedback")

    words = transcript.split()
    word_count = len(words)

    st.metric("Word Count", word_count)

    if word_count < 20:

        st.warning(
            "Your answer is short. Add more explanation "
            "and one relevant example."
        )

    elif word_count <= 120:

        st.success(
            "Good answer length. Check whether your "
            "answer directly addresses the question."
        )

    else:

        st.info(
            "Your answer is detailed. Try to keep it "
            "focused and avoid repetition."
        )


    st.subheader("Improvement Checklist")

    if word_count >= 20:
        st.write("✅ Your answer has sufficient length.")
    else:
        st.write("❌ Add more details to your answer.")

    example_words = [
        "because", "example", "result", "achieved"
    ]

    if any(word in transcript.lower() for word in example_words):
        st.write("✅ You included an explanation or example.")
    else:
        st.write("💡 Include a specific example or result.")

    personal_words = ["i", "my", "we", "our"]

    if any(word in transcript.lower().split() for word in personal_words):
        st.write("✅ You referred to your own experience.")
    else:
        st.write("💡 Explain your personal contribution.")

    st.caption(
        "Note: This feedback uses simple text-based rules. "
        "It is not an independent AI assessment of answer quality."
    )


# -------------------------------
# 11. ABOUT THE PROJECT
# -------------------------------

st.divider()
st.header("ℹ️ About SpeakSmart India")

st.write("""
SpeakSmart India is a multilingual AI interview practice
application designed to help students improve their
interview communication skills.

**Technologies used:**

- Gnani Prisma: Speech-to-Text
- Gnani Timbre: Text-to-Speech
- Python
- Streamlit

Developed as an individual project for the
Great Indian AI Internship Challenge 2026.
""")

st.success("Thank you for using SpeakSmart India! 🎤")