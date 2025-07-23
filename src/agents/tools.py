import requests
import os
from pydantic import BaseModel
from jinja2 import Template
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool

from services.vectore_store import retrieve, rerank

TAVILY_API_KEY = os.environ['TAVILY_API_KEY']


@tool
def web_search(query: str) -> list:
    """Search the web for a query"""
    tavily_search = TavilySearchResults(api_key=TAVILY_API_KEY, max_results=5, search_depth='advanced', max_tokens=1000)
    results = tavily_search.invoke(query)
    return results


@tool
def doc_search(query: str) -> dict:
    """Search the IFC's financial report 2024 for a query"""
    retrieved = retrieve(query)
    chunks = rerank(query, retrieved)
    return {"status": "success", "chunks": chunks}


class CanvasInput(BaseModel):
    content_type: str
    data: dict
    template: str

@tool
def canvas_tool(input: dict) -> str:
    """Render a template with data for the canvas tool"""
    canvas_input = CanvasInput(**input)
    tmpl = Template(canvas_input.template)
    return tmpl.render(**canvas_input.data)



MCP_SERVER_URL = "http://localhost:8080/v1/fetch"

FINANCIAL_URLS = {
    "stocks": "https://finance.yahoo.com/markets/stocks/most-active/",
    "crypto": "https://finance.yahoo.com/markets/crypto/all/",
    "currencies": "https://finance.yahoo.com/markets/currencies/"
}

@tool
def financial_data(query: str) -> dict:
    """Fetch financial data (currencies, crypto, stocks) from the MCP server based on the query type in real-time."""
    url = FINANCIAL_URLS.get(query.lower())
    if not url:
        return {"status": "error", "message": f"Unsupported query type '{query}'"}

    try:
        response = requests.post(MCP_SERVER_URL, json={"urls": [url]}, timeout=10)
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.RequestException as e:
        return {"status": "error", "message": str(e)}

