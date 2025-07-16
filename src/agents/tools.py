import logging
import requests
from google.adk.tools.tool_context import ToolContext
from pydantic import BaseModel
from jinja2 import Template, TemplateError

from services.vectore_store import retrieve, rerank


def doc_search(query: str) -> dict:
    """
    Search internal document "IFC Annual Report 2024 financials" semantically for relevant content.

    Args:
        query (str): What the user is looking for.

    Returns:
        dict: List of chunks and status.
    """
    retrieved = retrieve(query)
    chunks = rerank(query, retrieved)
    return {"status": "success", "chunks": chunks}


class CanvasInput(BaseModel):
    content_type: str
    data: dict
    template: str


def canvas_tool(input: dict) -> str:
    """
    Generate structured outputs like reports, docs or code using Jinja2 templates. Use this tool when the user expects a specific format or wants a long-form answer.

    Args:
        input (CanvasInput):
            - content_type (str): Type of content to generate (e.g., "report", "doc", "code").
            - data (dict): Data to be rendered in the template.
            - template (str): Jinja2 template string to render.

    Returns:
        str: Rendered output from the Jinja2 template.
    """
    canvas_input = CanvasInput(**input)
    try:
        tmpl = Template(canvas_input.template)
        rendered = tmpl.render(**canvas_input.data)
        logging.info(f"Rendered {canvas_input.content_type} output successfully.")
        return rendered
    except TemplateError as e:
        logging.error(f"Jinja2 template rendering failed: {str(e)}")
        return (
            f"[CanvasTool Error] Failed to render the {canvas_input.content_type} output due to template error: {str(e)}"
        )

def exit_loop(tool_context: ToolContext):
    """
    Call this function ONLY when the critique indicates no further changes 
    are needed, signaling the iterative process should end.
    """
    tool_context.actions.escalate = True

    return {}  


import logging
import requests
from pydantic import BaseModel
from google.adk.tools.tool_context import ToolContext

logger = logging.getLogger(__name__)

MCP_SERVER_URL = "http://localhost:8080/v1/fetch"

FINANCIAL_URLS = {
    "stocks": "https://finance.yahoo.com/markets/stocks/most-active/",
    "crypto": "https://finance.yahoo.com/markets/crypto/all/",
    "currencies": "https://finance.yahoo.com/markets/currencies/"
}

class FinancialQuery(BaseModel):
    type: str  # "stocks", "crypto", "currencies"

def financial_data(query: str) -> dict:
    """
    Fetches structured financial data through the MCP server for a given type.

    Args:
        query (str): One of "stocks", "crypto", or "currencies".

    Returns:
        dict: Structured result or error.
    """
    logger.info(f"FinancialDataTool: received query '{query}'")

    url = FINANCIAL_URLS.get(query.lower())
    if not url:
        logger.warning(f"Unsupported financial query type: {query}")
        return {"status": "error", "message": f"Unsupported query type '{query}'"}

    try:
        response = requests.post(MCP_SERVER_URL, json={"urls": [url]}, timeout=10)
        response.raise_for_status()
        logger.info("Data successfully fetched from MCP server")
        return {"status": "success", "data": response.json()}
    except requests.RequestException as e:
        logger.error(f"Failed to fetch financial data: {e}")
        return {"status": "error", "message": str(e)}
