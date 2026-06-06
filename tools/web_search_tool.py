from langchain.tools import tool
try:
    from ddgs import DDGS

    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False
@tool
def web_search_tool(query: str) -> str:
    """
    Useful for searching the web for current events, recent news,
    prices, or any information that might not be on Wikipedia.
    Input should be a search query like:
    'latest AI news 2024', 'current weather in Delhi', 'Python 3.12 features'.
    Use this when Wikipedia doesn't have the answer or for recent information.
    """

    # If duckduckgo_search is not installed, give a helpful message
    if not DDGS_AVAILABLE:
        return (
            "⚠️ Web search unavailable. Install it with: pip install duckduckgo-search\n"
            "For now, try the Wikipedia tool instead."
        )

    try:
        query = query.strip().strip("'\"")

        # Use DuckDuckGo to search — no API key required!
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))

        if not results:
            return f"❌ No web results found for '{query}'."

        # Format the results nicely
        output = f"Web search results for '{query}':\n\n"
        for i, result in enumerate(results, 1):
            title = result.get("title", "No title")
            body = result.get("body", "No description")
            href = result.get("href", "")
            output += f"{i}. **{title}**\n   {body}\n   Source: {href}\n\n"

        return output.strip()

    except Exception as e:
        return f"❌ Web search error: {str(e)}. Try the Wikipedia tool instead."