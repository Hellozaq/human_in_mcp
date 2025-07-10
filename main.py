from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from loguru import logger


mcp = FastMCP("human_in_mcp", log_level="ERROR")


@mcp.tool()
async def human_in_loop(question: str) -> str:
    """Ask the user a question and return the user's response.

    Args:
        question(str): The question to ask the user.

    Returns:
        str: The user's response.
    """
    logger.info(f"***Getting user response for question: human_in_loop({str(question)})***")
    api_url = "http://127.0.0.1:8000/ask"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                api_url,
                json={"question": f"human_in_loop({str(question)})"},
                timeout=300.0  # 5 minutes timeout
            )
            response.raise_for_status()
            result = response.json()
            return result["response"]
        except Exception as e:
            logger.error(f"Failed to get user response: {e}")
            return f"Error getting user response: {e}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
