from langgraph.graph import StateGraph, END
from src.state.leadState import LeadState
from src.agents.direct_agent import director_agent
from src.agents.retrieval_agent import RetrievalAgent
from langchain_groq import ChatGroq
from langgraph.prebuilt import interrupt


def human_node(state: LeadState):
    interrupt({
        "message": "High intent detected. Please provide your name and email.",
        "required_fields": ["name", "email"]
    })

def chat(state:LeadState):
    llm = ChatGroq(model="llama3-70b-8192")
    state['response']=llm.invoke(state['user_query'])
    


graph = StateGraph(LeadState)
retrieval_agent = RetrievalAgent(state=LeadState())

graph.add_node("director", director_agent)
graph.add_node("human", human_node)
graph.add_node("retrieval", retrieval_agent.responder)
graph.add_node("chat",chat)
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
graph.add_edge("chat",END)

app = graph.compile()


