import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain import hub

# Import our custom tools
from tools.calculator_tool import calculator_tool
from tools.wikipedia_tool import wikipedia_tool
from tools.web_search_tool import web_search_tool

# Import our memory manager
from memory.memory_manager import MemoryManager

# Load environment variables from .env file
load_dotenv()
class AssistantAgent:
    """
    AssistantAgent wraps a LangChain ReAct agent with:
    - Groq LLM (llama3-8b-8192)
    - 3 tools: calculator, wikipedia, web_search
    - ConversationBufferMemory for multi-turn chat
    """

    def __init__(self):
        # Load Groq API key
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found! Please add it to your .env file.\n"
                "Get your free key at: https://console.groq.com"
            )

        # Set up the Groq LLM
        # We use llama-3.3-70b-versatile fast and free on Groq
        self.llm = ChatGroq(
            api_key=api_key,
            model_name="llama-3.3-70b-versatile",  # You can also use "mixtral-8x7b-32768"
            temperature=0.6,              # 0 = deterministic, 1 = creative
            max_tokens=1024,
        )

        # Register tools
        self.tools = [
            calculator_tool,
            wikipedia_tool,
            web_search_tool,
        ]

        # Set up memory
        self.memory_manager = MemoryManager()
        self.memory = self.memory_manager.get_memory()

        #  Build the agent
        self.agent_executor = self._build_agent()

    def _build_agent(self) -> AgentExecutor:
        """Creates and returns the LangChain ReAct agent executor."""

        # The ReAct prompt tells the agent HOW to think step-by-step
        # and when to call a tool vs when to answer directly
        prompt = PromptTemplate.from_template("""
You are a helpful AI assistant with access to tools.
Use tools when needed, but answer directly if you already know the answer.

You have access to the following tools:
{tools}

Use the following format STRICTLY:

Question: the input question you must answer
Thought: think about what to do
Action: the action to take, must be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (repeat Thought/Action/Action Input/Observation as needed)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Previous conversation history:
{chat_history}

Question: {input}
Thought: {agent_scratchpad}
""")

        # Create the ReAct agent
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt,
        )

        # Wrap in AgentExecutor (handles the loop + error catching)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=False,          # Set to False to hide tool call logs
            handle_parsing_errors=True,   # Don't crash on bad LLM output
            max_iterations=10,      # Prevent infinite loops
        )

        return agent_executor

    def chat(self, user_input: str) -> str:
        """
        Send a message to the agent and get a response.
        Memory is automatically managed by LangChain.
        """
        try:
            result = self.agent_executor.invoke({"input": user_input})
            return result.get("output", "I could not generate a response.")

        except Exception as e:
            # Friendly error message instead of a raw Python traceback
            error_msg = str(e)
            if "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
                return "❌ API key error. Please check your GROQ_API_KEY in the .env file."
            elif "rate_limit" in error_msg.lower():
                return "⚠️ Rate limit reached. Please wait a moment and try again."
            elif "timeout" in error_msg.lower():
                return "⏱️ Request timed out. Please try again."
            else:
                return f"❌ An error occurred: {error_msg}"