#Step1: Setup FastAPI backend
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from ai_agent import graph, SYSTEM_PROMPT, parse_response
from tools import call_emergency, query_medgemma, lookup_therapists_by_location
import re

app = FastAPI()

CRISIS_KEYWORDS = (
    "suicide",
    "suicidal",
    "kill myself",
    "end my life",
    "want to die",
    "self harm",
    "hurt myself",
    "harm myself",
    "die today",
    "not safe",
    "call emergency",
)


def is_crisis_message(message: str) -> bool:
    normalized = message.lower()
    return any(keyword in normalized for keyword in CRISIS_KEYWORDS)


def is_therapist_search_message(message: str) -> bool:
    normalized = message.lower()
    therapist_keywords = ("therapist", "therapy", "counselor", "psychologist")
    location_keywords = ("near", "nearby", "in ", "live in", "from ")
    return any(keyword in normalized for keyword in therapist_keywords) and any(
        keyword in normalized for keyword in location_keywords
    )


def extract_location(message: str) -> str | None:
    patterns = (
        r"live in\s+([A-Za-z\s]+)",
        r"i am in\s+([A-Za-z\s]+)",
        r"i'm in\s+([A-Za-z\s]+)",
        r"from\s+([A-Za-z\s]+)",
        r"near\s+([A-Za-z\s]+)",
        r"nearby\s+([A-Za-z\s]+)",
        r"in\s+([A-Za-z\s]+)",
    )
    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            location = match.group(1).strip(" .,!?")
            if location:
                return location.title()
    return None

#Step2: Receive and validate request from Frontend
class Query(BaseModel):
    message: str


@app.post("/ask")
async def ask(query: Query):
    if is_crisis_message(query.message):
        try:
            call_emergency()
            return {
                "response": "I have placed an emergency support call for you. Please stay with someone nearby or contact local emergency services right now if you are in immediate danger.",
                "tool_called": "emergency_call_tool",
            }
        except Exception:
            return {
                "response": "I could not place the emergency call right now. Please contact local emergency services or a trusted person immediately.",
                "tool_called": "emergency_call_tool",
            }

    if is_therapist_search_message(query.message):
        location = extract_location(query.message) or "your area"
        return {
            "response": lookup_therapists_by_location(location),
            "tool_called": "find_nearby_therapists_by_location",
        }

    #AI Agent
    #response= ai_agent(query)
    inputs= {"messages": [("system", SYSTEM_PROMPT), ("user",query.message)]}
    try:
        stream= graph.stream(inputs, stream_mode="updates")
        tool_called_name, final_response = parse_response(stream)
    except Exception:
        final_response = query_medgemma(query.message)
        tool_called_name = "None"
    #Step3: Send Response to the frontend
    return {"response": final_response,
            "tool_called":tool_called_name or "None"}

if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
