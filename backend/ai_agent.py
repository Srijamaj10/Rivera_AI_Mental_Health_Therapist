from langchain_core.tools import tool
from tools import query_medgemma, call_emergency, lookup_therapists_by_location

@tool
def ask_mental_health_specialist(query:str)->str:
      
    """
    Generate a therapeutic response using the MedGemma model.
    Use this for all general user queries, mental health questions, emotional concerns,
    or to offer empathetic, evidence-based guidance in a conversational tone.
    """
    return query_medgemma(query)


@tool
def emergency_call_tool(phone: str = "") -> str:
    """
    Place an emergency call to the safety helpline's phone number via Twilio.    
    Use this only if the user expresses sucidal ideation, intent to self-harm,
    or describes a mental health emergency requiring immediate help.
    """
    try:
        call_sid = call_emergency(phone.strip() or None)
        return f"Emergency call placed successfully. Call SID: {call_sid}"
    except Exception:
        return "I could not place the emergency call right now. Please contact local emergency services or a trusted person immediately."

@tool
def find_nearby_therapists_by_location(location: str) -> str:
    """
    Finds and returns a list of licensed therapists near the specified location.

    Args:
        location (str): The name of the city or area in which the user is seeking therapy support.

    Returns:
        str: A newline-separated string containing therapist names and contact info.
    """
    return lookup_therapists_by_location(location)
#Step 1: create an AI agent & Link to backend
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain.agents import create_agent
from dotenv import load_dotenv
import os

load_dotenv()
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")


tools = [ask_mental_health_specialist, emergency_call_tool, find_nearby_therapists_by_location]

llm= HuggingFaceEndpoint(
    repo_id="google/gemma-2b-it",
    task= "text-generation",
    temperature= 0.2,
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN
)
model = ChatHuggingFace(llm=llm)

SYSTEM_PROMPT = """
You are an emphathetic AI therapist assistant supporting mental health conversations with warmth and clinical accuracy.
You have access to three tools:

1. `ask_mental_health_specialist`: Use this tool to answer all emotional or psychological queries with therapeutic guidance.
2. `find_nearby_therapists_by_location`: Use this tool if the user asks about nearby therapists or if recommending local professional help would be beneficial.
3. `emergency_call_tool`: Use this immediately if the user expresses suicidal thoughts, self-harm intentions, or is in crisis.If you use `emergency_call_tool`, always follow up with a short, calming confirmation message to the user.

Always prioritize user safety, validation and helpful action. Respond kindly, clearly, and supportively.

Keep your responses short and easy to read: aim for 3–4 sentences maximum unless the user specifically asks for more detail.
Avoid long lists unless explicitly requested. 
Focus on one practical suggestion or comfort at a time.
"""

graph = create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)

def parse_response(stream):
    tool_called_name = "None"
    final_response = None

    for s in stream:
        # Check if a tool was called
        tool_data = s.get('tools')
        if tool_data:
            tool_messages = tool_data.get('messages')
            if tool_messages and isinstance(tool_messages, list):
                for msg in tool_messages:
                    tool_called_name = getattr(msg, 'name', 'None')

        # Check if agent returned a message
        agent_data = s.get('agent')
        if agent_data:
            messages = agent_data.get('messages')
            if messages and isinstance(messages, list):
                for msg in messages:
                    if msg.content:
                        final_response = msg.content

    return tool_called_name, final_response


if __name__ == "__main__":
    print("AI therapist agent is running. Type 'exit' to quit.")
    while True:
        user_input = input("User: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Session closed.")
            break
        if not user_input:
            continue

        inputs = {"messages": [("system", SYSTEM_PROMPT), ("user", user_input)]}
        try:
            stream = graph.stream(inputs, stream_mode="updates")
            tool_called_name, final_response = parse_response(stream)
        except Exception:
            final_response = query_medgemma(user_input)
            tool_called_name = "None"

        print("TOOL CALLED:", tool_called_name)
        print("ANSWER:", final_response)
