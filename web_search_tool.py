import os
import requests
from dotenv import load_dotenv
from crewai.tools import tool

load_dotenv()

@tool("RankedSerperSearch")
def serper_web_search(query: str, date_range: str = "") -> str:
    """
    Search the web using Serper API and return top results.
    """
    api_key = os.getenv("SERPER_API_KEY")
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    payload = {"q": query, "num": 3}
    if date_range:
        payload["when"] = date_range

    try:
        res = requests.post(url, json=payload, headers=headers, timeout=10)
        res.raise_for_status()
        data = res.json()
        results = ""
        for i, item in enumerate(data.get("organic", []), 1):
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            link = item.get("link", "")
            results += f"{i}. **{title}**\n   {snippet}\n   ({link})\n\n"
        return results or "No results found."
    except Exception as e:
        print(f"Serper API error: {e}")
        return f"Error searching web: {e}"
