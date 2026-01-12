from langgraph.graph import StateGraph, END
from src.state.leadState import LeadState
from src.agents.direct_agent import director_agent
from src.agents.retrieval_agent import RetrievalAgent
from langchain_groq import ChatGroq
from langgraph.types import interrupt
from dotenv import load_dotenv
load_dotenv()


def human_node(state: LeadState):
    print("human node")
    value = interrupt({
        "message": "High intent detected. Please provide your name and email.",
        "required_fields": ["name", "email"]
    })
    if value:
        state["name"] = value.get("name")
        state["email"] = value.get("email")
    
    return state


def chat(state: LeadState):
    llm = ChatGroq(model="llama-3.3-70b-versatile")
    response = llm.invoke(state['user_query'])
    if "chat_history" not in state:
        state["chat_history"] = []
    
    state["chat_history"].append({
        "role": "assistant",
        "content": response.content
    })

    if len(state["chat_history"]) > 12:
        state["chat_history"] = state["chat_history"][-12:]
    
    state['response'] = response.content
    return state


graph = StateGraph(LeadState)
retrieval_agent = RetrievalAgent(model="llama-3.3-70b-versatile")

graph.add_node("director", director_agent)
graph.add_node("human", human_node)
graph.add_node("retrieval", retrieval_agent.responder)
graph.add_node("chat", chat)

graph.set_entry_point("director")

graph.add_conditional_edges(
    "director",
    lambda state: state["intent"],
    {
        "HIGH_INTENT": "human",
        "INFO_QUERY": "retrieval",
        "SMALL_TALK": "chat"
    }
)

graph.add_edge("human", END)
graph.add_edge("retrieval", END)
graph.add_edge("chat", END)

compile_app = graph.compile()