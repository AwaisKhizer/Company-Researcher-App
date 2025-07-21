import os
import requests
from dotenv import load_dotenv
from crewai.tools import tool

load_dotenv()

@tool("EnhancedFirecrawlScraper")
def firecrawl_scraper(website_url: str, section: str = "") -> str:
    """
    Scrape and extract meaningful content from a website using the Firecrawl API.
    """
    api_key = os.getenv("FIRECRAWL_API_KEY")
    api_url = "https://api.firecrawl.dev/v1/scrape"
    payload = {"url": website_url, "js_render": False}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": api_key
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        text = data.get("text", "No content found")
        cleaned = " ".join(text.split())
        trimmed = cleaned[:2000]

        if section and section.lower() in trimmed.lower():
            return f"[Filtered Section: {section}]\n\n{trimmed}"
        return trimmed or "No content found."
    except Exception as e:
        print(f"Firecrawl API error: {e}")
        return f"Error scraping site: {e}"
