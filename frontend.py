# Step1: Setup Streamlit
import streamlit as st
import requests
from requests import RequestException

BACKEND_URL= "http://localhost:8000/ask"

st.set_page_config(page_title= "AI Mental Health Therapist", layout= "wide")
#st.title("🕊️ Rivera – Flow Into Peace | AI Mental Health Therapist")

st.markdown(
    """
    <h2 style='text-align: center; font-size: 26px;'>
        🕊️ Rivera – Flow Into Peace | AI Mental Health Therapist
    </h2>
    """,
    unsafe_allow_html=True
)

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history= []

# Step2: User is able to ask question
#chat input
user_input= st.chat_input("What's on your mind today?")
if user_input:
    #Append user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})

     #AI Agent exists here
    try:
        response = requests.post(BACKEND_URL, json={"message": user_input}, timeout=30)
        response.raise_for_status()
        payload = response.json()
        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": payload.get("response", "I could not generate a response right now."),
            }
        )
    except RequestException:
        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": "The backend is not reachable right now. Please start `uv run backend/main.py` in another terminal and try again.",
            }
        )

# Step3: Show response from backend
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
