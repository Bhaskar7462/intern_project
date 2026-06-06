
import wikipedia
from langchain.tools import tool


@tool
def wikipedia_tool(query: str) -> str:
    """
    Useful for looking up factual information about people, places,
    events, concepts, history, science, and general knowledge topics.
    Input should be a search term or topic name like:
    'Albert Einstein', 'Python programming language', 'World War 2'.
    Use this when you need to find facts or summaries about a topic.
    """
    try:
        # Clean the input
        query = query.strip().strip("'\"")

        # Set Wikipedia language to English
        wikipedia.set_lang("en")

        # Search Wikipedia and get a 3-sentence summary
        summary = wikipedia.summary(query, sentences=3, auto_suggest=True)

        return f"Wikipedia result for '{query}':\n{summary}"

    except wikipedia.exceptions.DisambiguationError as e:
        # Multiple results found — return the options
        options = e.options[:5]  # Show top 5 options
        return (
                f"⚠️ '{query}' is ambiguous. Did you mean one of these?\n"
                + "\n".join(f"  - {opt}" for opt in options)
        )

    except wikipedia.exceptions.PageError:
        return f"❌ No Wikipedia page found for '{query}'. Try a different search term."

    except Exception as e:
        return f"❌ Wikipedia search error: {str(e)}"