
# agents/researcher.py

import logging
from typing import List, Dict, Any, Optional
import json

# Initialize Logger
logger = logging.getLogger(__name__)

class ResearchAgent:
    def __init__(self):
        self.enabled = False
        try:
            from duckduckgo_search import DDGS
            self.ddgs = DDGS()
            self.enabled = True
            logger.info("🦆 DuckDuckGo Search initialized successfully.")
        except ImportError:
            logger.warning("❌ duckduckgo_search not installed. Research Agent disabled. Run `pip install duckduckgo-search`.")
            self.ddgs = None
        except Exception as e:
            logger.error(f"❌ Failed to initialize Research Agent: {e}")
            self.ddgs = None

    def perform_research(self, query: str, max_results: int = 5) -> str:
        """
        Executes a web search and returns a summarized string of results.
        """
        if not self.enabled or not self.ddgs:
            return "Research Agent is disabled. Please install `duckduckgo-search`."

        print(f"\n🔎 RESEARCHING: {query} ...\n")
        
        try:
            results = list(self.ddgs.text(query, max_results=max_results))
            
            if not results:
                return f"No results found for '{query}'."

            summary = f"### Research Results for '{query}':\n\n"
            
            for i, r in enumerate(results):
                title = r.get('title', 'No Title')
                href = r.get('href', '#')
                body = r.get('body', 'No Content')
                
                summary += f"**{i+1}. [{title}]({href})**\n{body}\n\n"
            
            return summary

        except Exception as e:
            error_msg = f"Search failed: {e}"
            logger.error(error_msg)
            return error_msg

# Singleton Instance
researcher = ResearchAgent()

def perform_research(query: str) -> str:
    """Helper function to call the singleton."""
    return researcher.perform_research(query)
