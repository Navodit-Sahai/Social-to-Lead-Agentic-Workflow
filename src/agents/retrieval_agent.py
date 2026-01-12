from langchain_community.document_loaders import JSONLoader
from langchain_groq import ChatGroq
from src.state.leadState import LeadState
from dotenv import load_dotenv
load_dotenv()
import os
from pathlib import Path

class RetrievalAgent:
    def __init__(self, state: LeadState, model="llama-3.3-70b-versatile"):
        self.model = model
        self.llm = ChatGroq(model=self.model)
        self.state = state

    def loadInfo(self):
        
        current_dir = Path(__file__).parent.parent
        data_path = current_dir / "knowledge_base" / "data.json"
        
        loader = JSONLoader(
            file_path=str(data_path),
            jq_schema=".",
            text_content=False
        )
        docs = loader.load()
        info = docs[0].page_content
        print(info)
        return info

    def responder(self, state):
        query = state['user_query']

        if "chat_history" not in state:
            state["chat_history"] = []
        
        info = self.loadInfo()
        
        prompt = f"""
        You are a knowledge retrieval assistant.

        You are given a JSON-based knowledge context about a product.
        Your task is to answer the user's question **using ONLY the information present in the context**.

        User's question:
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
        
        state['response'] = response.content
        return state