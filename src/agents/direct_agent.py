from langchain_groq import ChatGroq
from src.prompt.directorPrompt import DirectorPrompt
from src.state.leadState import LeadState

llm = ChatGroq(model="llama3-70b-8192")

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


