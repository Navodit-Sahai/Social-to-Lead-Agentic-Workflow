from src.state.leadState import LeadState
from src.graph import compile_app

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
            result = compile_app.invoke(initial_state)

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