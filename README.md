# 🌿 Rivera AI – Real-Time AI Mental Health Therapist 🕊️

Rivera AI is an AI-powered mental health assistant designed to provide real-time therapeutic support, help users connect with licensed professionals, and simulate emergency interventions when needed.

It aims to make mental health support more accessible, empathetic, and immediate using AI-driven conversations and real-world integrations.

## 💡 Motivation

Mental health support is often difficult to access due to time, cost, or availability barriers. Rivera AI aims to bridge this gap by offering:

Instant emotional support through AI conversations
Guidance similar to a therapeutic interaction
Easy access to mental health resources
Emergency assistance when needed
🔍 Key Features
🧠 AI Therapist

Engages users in empathetic, human-like conversations using LLM-based responses designed for therapeutic support.

## 📍 Find Nearby Therapists

Helps users discover and connect with licensed mental health professionals based on their needs and location.

## 🚨 Emergency Support (Twilio Integration)

Triggers real-time emergency communication using Twilio API for critical situations.

## 💬 Conversational Experience

Maintains natural, supportive, and emotionally aware dialogue to help users feel heard and understood.

## 💻 Interactive UI

Built using Streamlit for a smooth, simple, and user-friendly experience.

## ⚙️ Tech Stack
Python
FastAPI
Streamlit
LangChain
Hugging Face (LLMs)
Twilio API
🚀 Installation Guide
## 1. Clone the repository
git clone https://github.com/Srijamaj10/Rivera_AI_Mental_Health_Therapist.git
cd Rivera_AI_Mental_Health_Therapist
## 2. Create virtual environment (recommended)
python -m venv .venv

Activate it:

Windows

.venv\Scripts\activate

Mac/Linux

source .venv/bin/activate
## 3. Install dependencies
pip install -r requirements.txt
## 4. Set environment variables

Create a .env file:

HUGGINGFACE_API_KEY=your_huggingface_key
TWILIO_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE=your_twilio_number
EMERGENCY_CONTACT=target_number
▶️ Run the Project
## Start backend
uvicorn backend.tools:app --reload
## Start frontend
streamlit run frontend.py

🧠 What I Learned
Building full-stack AI systems with real-time interaction
Working with LLMs using Hugging Face & LangChain
Designing empathetic conversational AI systems
Integrating external APIs like Twilio
Structuring scalable backend + frontend architecture

⚠️ Important Notes
Keep API keys secure (never upload .env to GitHub)
Twilio calls may require verified numbers
Hugging Face API may have rate limits depending on plan

✨ Future Improvements
🎙️ Voice-based therapy support
🌍 Multilingual conversations
📊 Sentiment detection for better responses
👩‍⚕️ Therapist dashboard for real consultations

🤍 Closing Note

Rivera AI is built with a mission to combine technology + empathy, making mental health support more accessible and human-centered.

“Sometimes, being heard is the first step toward healing.” 🕊️
