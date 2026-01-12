from langchain_groq import ChatGroq
from src.prompt.directorPrompt import DirectorPrompt
from src.state.leadState import LeadState
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile")

def director_agent(state: LeadState):
    query = state["user_query"]
    if "chat_history" not in state:
        state["chat_history"] = []
    
    state["chat_history"].append({
        "role": "user",
        "content": query
    })

    decision = llm.invoke(
        DirectorPrompt + f"\nUser Query:\n{query}"
    ).content.strip()

    state['intent']=decision
    return state


