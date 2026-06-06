import warnings

warnings.simplefilter("ignore")
warnings.filterwarnings("ignore")

from pydantic.warnings import PydanticDeprecatedSince20
warnings.filterwarnings("ignore", category=PydanticDeprecatedSince20)
from agent.assistant_agent import AssistantAgent


def main():
    print("=" * 60)
    print("   🤖  Multi-Tool AI Assistant (Powered by Groq + LangChain)")
    print("=" * 60)
    print("Tools available: Calculator | Wikipedia | Web Search")
    print("Type 'quit' or 'exit' to stop the assistant.\n")

    # Create the agent (loads tools + memory automatically)
    agent = AssistantAgent()
    while True:
        try:
            user_input = input("You: ").strip()

            # Allow user to exit cleanly
            if user_input.lower() in ["quit", "exit", "q"]:
                print("\nAssistant: Goodbye! ")
                break

            # Skip empty input
            if not user_input:
                continue

            # Get response from agent
            response = agent.chat(user_input)
            print(f"\nAssistant: {response}\n")

        except KeyboardInterrupt:
            print("\n\nAssistant: Goodbye! ")
            break


if __name__ == "__main__":
    main()