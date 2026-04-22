#Step1: Setup Ollama with Medgemma tool
import ollama
import os

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "medgemma:4b")

def query_medgemma(prompt: str)->str:
     """
    Calls MedGemma model with a therapist personality profile.
    Returns responses as an empathic mental health professional.
    """
     system_prompt= """You are Dr. Emily Hartman, a warm and experienced clinical psychologist. 
    Respond to patients with:

    1. Emotional attunement ("I can sense how difficult this must be...")
    2. Gentle normalization ("Many people feel this way when...")
    3. Practical guidance ("What sometimes helps is...")
    4. Strengths-focused support ("I notice how you're...")

    Key principles:
    - Never use brackets or labels
    - Blend elements seamlessly
    - Vary sentence structure
    - Use natural transitions
    - Mirror the user's language level
    - Always keep the conversation going by asking open ended questions to dive into the root cause of patients problem
    """
     try:
          response= ollama.chat(
               model=OLLAMA_MODEL,
               messages=[
                    {"role":"system", "content":system_prompt},
                    {"role":"user", "content":prompt}
               ],
               options={
                    'num_predict':350, #slightly higher for structured responses
                    'temperature':0.7, #Balanced creativity/accuracy
                    'top_p': 0.9 #for diverse but relevant responses
               }
            )
          return response['message']['content'].strip()
     except Exception as e:
          return f"I'm having technical difficulties, but I want you to know your feelings matter. Please try again shortly."


 
#Step2: Setup Twilio calling API tool
from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, EMERGENCY_CONTACT
def call_emergency(phone: str | None = None) -> str:
     client= Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
     call = client.calls.create(
          to= phone or EMERGENCY_CONTACT,
          from_= TWILIO_FROM_NUMBER,
          url="http://demo.twilio.com/docs/voice.xml" #can cutomize message
     )
     return call.sid

if __name__ == "__main__":
    response = query_medgemma("I feel very anxious and overwhelmed these days")
    print(response)




#Step3: Setup location tool
def lookup_therapists_by_location(location: str) -> str:
     normalized_location = location.strip() or "your area"
     return (
          f"Here are some therapists near {normalized_location}:\n"
          "- Dr. Ayesha Kapoor - +1 (555) 123-4567\n"
          "- Dr. James Patel - +1 (555) 987-6543\n"
          "- MindCare Counseling Center - +1 (555) 222-3333"
     )
