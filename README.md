
# SpeakSmart India

## Project Overview
SpeakSmart India is a multilingual AI interview
practice assistant designed to help Indian students
improve their interview preparation.

## Problem
Many students struggle with interview confidence,
spoken communication and expressing their answers.

## Solution
The application allows students to listen to interview
questions, record their answers and convert speech
into text for review.

## Technologies
- Python
- Streamlit
- Gnani Prisma v2.5
- Gnani Timbre v2.5
- Speech Recognition
- Text-to-Speech

## Features
1. HR interview questions
2. Technical interview questions
3. English and Telugu speech transcription
4. AI-generated question audio
5. Answer transcript download
6. Structured answer feedback

## Architecture
Student
   |
Streamlit Application
   |
   |---- Gnani Timbre v2.5
   |       Text to Speech
   |
   |---- Gnani Prisma v2.5
   |       Speech to Text
   |
Transcript and Feedback

## Developer Contribution
Individually designed, developed and tested by
the project author.

## Run Instructions

pip install -r requirements.txt

streamlit run app.py

## Security
API credentials are stored in an environment
file and are not included in the repository.

## 🎙️ Voice Recording Duration

- The application currently supports up to **30 seconds of voice recording per answer**.
- Users can record their answers through their device microphone.
- Audio is converted into text using Gnani Prisma Speech-to-Text.

## ⚠️ Current Limitations

- Maximum recording duration: 30 seconds per answer.
- Feedback currently uses rule-based text analysis.
- Advanced AI-based answer evaluation is a future enhancement.

## 🚀 Future Enhancements

- Increase recording duration.
- Add AI-powered answer evaluation.
- Provide grammar, pronunciation, and fluency feedback.