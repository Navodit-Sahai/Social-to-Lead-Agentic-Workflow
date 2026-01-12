# Social-to-Lead Workflow Chatbot

## How to Run the Project Locally

1. **Clone the repository**
```bash
git clone https://github.com/Navodit-Sahai/Social-to-Lead-Agentic-Workflow
cd Social-to-Lead-workflow
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your google_api_key here (if u are using any other LLM by Google)
```

5. **Run the chatbot**
```bash
python -m src.main
```

## Architecture Explanation

I chose **LangGraph** for this project because it provides a clear, graph-based approach to building conversational workflows with multiple agents. LangGraph excels at managing complex state transitions and routing between different agents based on intent classification.

**State Management**: 
- The system uses a centralized `LeadState` TypedDict that tracks user queries, classified intent, chat history, and lead information (name, email, platform)
- State flows through three specialized agents: Director Agent (classifies intent), Retrieval Agent (handles product queries from JSON knowledge base), and Chat Agent (manages casual conversation)
- Each agent directly modifies and returns the state, which is passed to the next node in the graph
- Graph routes based on intent: HIGH_INTENT → human node, INFO_QUERY → retrieval agent, SMALL_TALK → chat agent
- This ensures proper conversation flow and prevents premature lead capture until all required fields are collected

## WhatsApp Deployment with Webhooks

To integrate this agent with WhatsApp:

1. **Set up WhatsApp Business API** through Meta/Twilio and obtain API credentials and webhook verification token.

2. **Create webhook endpoint** (Flask/FastAPI) that receives POST requests from WhatsApp containing user messages in JSON format.

3. **Process incoming messages**: Extract message content and sender ID from the webhook payload, initialize LeadState with the user query, and invoke the LangGraph workflow.

4. **Handle conversation state**: Store conversation history in a database (Redis/PostgreSQL) using sender ID as the key to maintain context across multiple messages.

5. **Send responses back**: Use WhatsApp Business API to send the agent's response back to the user via POST request to WhatsApp's message endpoint.

6. **Handle lead capture**: When HIGH_INTENT is detected, send interactive buttons/list messages to collect name, email, and platform, then call the mock_lead_capture API once all fields are received.

7. **Deploy**: Host the webhook server on a cloud platform (AWS/GCP/Heroku) with HTTPS enabled for security.
