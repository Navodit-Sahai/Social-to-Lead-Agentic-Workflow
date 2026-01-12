from src.state.leadState import LeadState
from src.graph import compile_app
from src.tools.mock_api_tool import mock_lead_capture

def get_lead_info():
    """
    Collect all three required fields before calling the API.
    Ensures no premature API calls.
    """
    print("\n")
    print("Please provide your information:")
    
    while True:
        name = input("Name: ").strip()
        if name:
            break
        print("name cannot be empty")
    while True:
        email = input("Email: ").strip()
        if email :
            break
        print("email cannot be empty")

    platforms = ["YouTube", "Instagram", "TikTok", "Twitter", "Facebook", "LinkedIn", "Other"]
    print(f"\nAvailable platforms: {', '.join(platforms)}")
    while True:
        platform = input("Creator Platform: ").strip()
        if platform:
            break
        print(" Platform cannot be empty. Please try again.")
    
    return name, email, platform




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
                platform=None,
                response="",
                chat_history=[],
                lead_captured=None
            )
            result = compile_app.invoke(initial_state)

            if result.get('response'):
                print(f"\nBot: {result['response']}\n")
            
            if result.get('intent') == 'HIGH_INTENT':
                print("\n High intent detected!")
                name,email,platform=get_lead_info()
                mock_lead_capture(name, email, platform)
                print(f"\n Thank you, {name}! We'll contact you at {email}\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n Error: {str(e)}\n")
            print("Please try again.\n")


if __name__ == "__main__":
    main()