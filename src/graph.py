from langgraph.graph import StateGraph, END
from src.state.leadState import LeadState
from src.agents.direct_agent import director_agent
from src.agents.retrieval_agent import RetrievalAgent
from langchain_groq import ChatGroq
from langgraph.prebuilt import interrupt
from dotenv import load_dotenv
load_dotenv()


def human_node(state: LeadState):
    interrupt({
        "message": "High intent detected. Please provide your name and email.",
        "required_fields": ["name", "email"]
    })
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
retrieval_agent = RetrievalAgent(state=LeadState(), model="llama-3.3-70b-versatile")

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

app = graph.compile()



def main():
    print("=" * 50)
    print("Social-to-Lead Workflow Chatbot")
    print("=" * 50)
    print("Type 'quit' or 'exit' to end the conversation\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue

            initial_state = LeadState(
                user_query=user_input,
                intent=None,
                name=None,
                email=None,
                response="",
                chat_history=[]
            )
            result = app.invoke(initial_state)

            if result.get('response'):
                print(f"\nBot: {result['response']}\n")
            
            if result.get('intent') == 'HIGH_INTENT':
                print("\n High intent detected!")
                name = input("Please enter your name: ").strip()
                email = input("Please enter your email: ").strip()
                print(f"\n Thank you, {name}! We'll contact you at {email}\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n Error: {str(e)}\n")
            print("Please try again.\n")


if __name__ == "__main__":
    main()