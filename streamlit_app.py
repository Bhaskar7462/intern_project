import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set Streamlit page configurations
st.set_page_config(
    page_title="Multi-Tool AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Glassmorphism and Styling
st.markdown("""
    <style>
    /* Gradient Background and overall styling */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(12, 16, 29, 1) 0%, rgba(18, 22, 38, 1) 90.2%);
        color: #e2e8f0;
    }
    
    /* Title Styling */
    .title-text {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 5px;
        font-family: 'Outfit', 'Inter', sans-serif;
    }
    
    .subtitle-text {
        font-size: 1.1rem;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 30px;
    }
    
    /* Metric Cards styling */
    .tool-card {
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    
    .tool-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.4);
    }
    
    .tool-icon {
        font-size: 1.8rem;
        margin-bottom: 8px;
    }
    
    .tool-title {
        font-weight: 700;
        color: #f1f5f9;
        font-size: 1rem;
        margin-bottom: 4px;
    }
    
    .tool-desc {
        font-size: 0.8rem;
        color: #94a3b8;
    }
    </style>
""", unsafe_allow_html=True)

# Main Title & Subtitle
st.markdown("<h1 class='title-text'>🤖 Multi-Tool AI Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle-text'>Powered by Groq Llama-3.3 + LangChain ReAct Agent</p>", unsafe_allow_html=True)

# --- Sidebar Configuration ---
with st.sidebar:
    st.markdown("### ⚙️ Setup & Configuration")
    
    # API Key Handling
    # Automatically check/set key from environment or fallback to the provided one
    env_api_key = os.getenv("GROQ_API_KEY", "")
    
    if not env_api_key:
        # Check Streamlit's secrets manager on deployment
        import streamlit as st
        if "GROQ_API_KEY" in st.secrets:
            env_api_key = st.secrets["GROQ_API_KEY"]
            os.environ["GROQ_API_KEY"] = env_api_key

    if env_api_key:
        st.success("✅ Groq API Connection Configured")
    else:
        st.error("⚠️ GROQ_API_KEY missing! Add it to your .env file or Streamlit Secrets.")

    st.markdown("---")
    st.markdown("### 🧠 Memory Control")
    if st.button("🗑️ Clear Conversation Memory", use_container_width=True):
        if "agent" in st.session_state:
            st.session_state.agent.memory_manager.clear_memory()
        st.session_state.messages = []
        st.success("Memory and chat history cleared!")
        st.rerun()

    st.markdown("---")
    st.markdown("### 💡 Quick Prompt Suggestions")
    
    example_prompts = [
        "Calculate 245 * 78",
        "Who is Alan Turing and what did he invent?",
        "What are the latest features in Python 3.12?",
        "Compare the speed of light vs speed of sound"
    ]
    
    for prompt in example_prompts:
        if st.button(prompt, key=prompt, use_container_width=True):
            st.session_state.user_prompt = prompt

# --- Tool Summary Showcase ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
        <div class="tool-card">
            <div class="tool-icon">🧮</div>
            <div class="tool-title">Calculator Tool</div>
            <div class="tool-desc">Evaluates complex mathematical and algebraic expressions safely using python's math module.</div>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div class="tool-card">
            <div class="tool-icon">📚</div>
            <div class="tool-title">Wikipedia Lookup</div>
            <div class="tool-desc">Searches Wikipedia pages for general knowledge facts, history, science, and biographies.</div>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
        <div class="tool-card">
            <div class="tool-icon">🌐</div>
            <div class="tool-title">Web Search Tool</div>
            <div class="tool-desc">Performs real-time search queries on DuckDuckGo to retrieve current news, weather, or pricing.</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Initialize Agent ---
# Import inside function to make sure GROQ_API_KEY is set before imports run if necessary
import traceback

def get_agent():
    try:
        from agent.assistant_agent import AssistantAgent
        return AssistantAgent()
    except Exception as e:
        st.error(f"Failed to initialize Assistant Agent: {e}")
        st.code(traceback.format_exc())
        return None

if "agent" not in st.session_state:
    if os.getenv("GROQ_API_KEY"):
        st.session_state.agent = get_agent()
    else:
        st.session_state.agent = None

# Re-evaluate agent initialization if API key was updated in sidebar
if st.session_state.agent is None and os.getenv("GROQ_API_KEY"):
    st.session_state.agent = get_agent()

# --- Initialize Messages ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Render Chat History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- Handle User Input ---
# Check if a quick prompt suggestion was clicked
if "user_prompt" in st.session_state and st.session_state.user_prompt:
    user_input = st.session_state.user_prompt
    # Clear the temporary variable
    st.session_state.user_prompt = ""
else:
    user_input = st.chat_input("Ask me anything...")

if user_input:
    # Check if API Key is set
    if not os.getenv("GROQ_API_KEY"):
        st.error("Please provide a GROQ_API_KEY in the sidebar before typing a message.")
    else:
        # Display user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Generate response using ReAct Agent
        with st.chat_message("assistant"):
            with st.spinner("Agent is reasoning and selecting tools..."):
                try:
                    # Initialize agent on first query if not already done
                    if st.session_state.agent is None:
                        st.session_state.agent = get_agent()
                        
                    response = st.session_state.agent.chat(user_input)
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_str = f"An execution error occurred: {e}"
                    st.error(error_str)
                    st.session_state.messages.append({"role": "assistant", "content": error_str})
