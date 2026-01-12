from langchain_community.document_loaders import JSONLoader
from langchain_groq import ChatGroq
from src.state.leadState import LeadState

class RetrievalAgent:
    def __init__(self,state:LeadState,model="llama3-70b-8192"):
        self.model = model
        self.llm = ChatGroq(model=self.model)
        self.state=state

    def loadInfo(self):
        loader = JSONLoader(
            file_path=r"C:\Users\sahai\OneDrive\Desktop\Social-to-Lead-workflow\src\knowledge_base\data.json",
            jq_schema=".",
            text_content=False
        )
        docs = loader.load()
        info=docs[0].page_content
        print(info)
        return info

    def responder(self,state):
        query=state['user_query']
        info=self.loadInfo()
        prompt = f"""
        You are a knowledge retrieval assistant.

        You are given a JSON-based knowledge context about a product.
        Your task is to answer the user's question **using ONLY the information present in the context**.

        user's question:
        {query}

        Rules:
        - Do NOT hallucinate or assume anything not in the context.
        - If the information is not available, say: "The requested information is not available in the knowledge base."
        - Be precise and concise.
        - If pricing is requested, clearly mention the plan name, price, and key features.

        Knowledge Context:
        {info}

        Answer:
        """
        response = self.llm.invoke(prompt)
        state["chat_history"].append({
            "role": "assistant", 
            "content": response.content
        })

        if len(state["chat_history"]) > 12:  
            state["chat_history"] = state["chat_history"][-12:]
        state['response']= response.content
        return state

