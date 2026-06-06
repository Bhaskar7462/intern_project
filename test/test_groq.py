import os
import sys

# Add parent directory to path so we can import from project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()


def test_groq_connection():
    """Test that the Groq API key is set and working."""
    print("Testing Groq API connection...\n")

    # Check if API key exists
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ FAIL: GROQ_API_KEY not found in .env file")
        print("   Add this line to your .env file:")
        print("   GROQ_API_KEY=your_key_here")
        return False

    print(f"✅ API key found: {api_key[:8]}...{api_key[-4:]}")

    # Try making a real API call
    try:
        from langchain_groq import ChatGroq
        from langchain.schema import HumanMessage

        llm = ChatGroq(
            api_key=api_key,
            model_name="llama-3.3-70b-versatile",
            max_tokens=50,
        )

        response = llm.invoke([HumanMessage(content="Say 'Hello, I am working!' in exactly those words.")])
        print(f"✅ API call successful!")
        print(f"   Response: {response.content}")
        return True

    except Exception as e:
        print(f"❌ FAIL: API call failed — {str(e)}")
        return False


def test_calculator():
    """Test the calculator tool works."""
    print("\nTesting Calculator tool...")
    from tools.calculator_tool import calculator_tool
    result = calculator_tool.invoke("25 * 48")
    print(f"✅ Calculator: 25 * 48 = {result}")


def test_wikipedia():
    """Test Wikipedia tool works."""
    print("\nTesting Wikipedia tool...")
    from tools.wikipedia_tool import wikipedia_tool
    result = wikipedia_tool.invoke("Python programming language")
    print(f"✅ Wikipedia: {result[:100]}...")


def test_memory():
    """Test memory manager works."""
    print("\nTesting Memory Manager...")
    from memory.memory_manager import MemoryManager
    mem = MemoryManager()
    mem.memory.save_context({"input": "My name is Rahul"}, {"output": "Hello Rahul!"})
    history = mem.get_history()
    print(f"✅ Memory works: {history[:80]}...")


if __name__ == "__main__":
    print("=" * 50)
    print("  Running All Tests")
    print("=" * 50)

    groq_ok = test_groq_connection()

    if groq_ok:
        test_calculator()
        test_wikipedia()
        test_memory()
        print("\n" + "=" * 50)
        print("✅ All tests passed! Run: python app.py")
        print("=" * 50)
    else:
        print("\n❌ Fix your Groq API key first, then re-run tests.")

