from langchain.memory import ConversationBufferMemory
class MemoryManager:
    """
    Wraps LangChain's ConversationBufferMemory.

    - 'chat_history' is the key the agent prompt uses to inject history
    - memory_key must match the variable name in the prompt template
    """

    def __init__(self):
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",  # Must match {chat_history} in prompt
            return_messages=False,  # Return as plain text (not message objects)
            human_prefix="You",
            ai_prefix="Assistant",
        )

    def get_memory(self) -> ConversationBufferMemory:
        """Returns the memory object for use in the agent."""
        return self.memory

    def clear_memory(self):
        """Clears all conversation history (fresh start)."""
        self.memory.clear()
        print("🗑️  Memory cleared. Starting fresh conversation.")

    def get_history(self) -> str:
        """Returns the current conversation history as a string."""
        return self.memory.load_memory_variables({}).get("chat_history", "")
