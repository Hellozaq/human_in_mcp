import sys
import os
# Add the current file's directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp.server.fastmcp import FastMCP
from decorator import auto_human_tool

mcp = FastMCP("human_in_mcp", log_level="ERROR")


# Use decorator to define functions - support multiple parameters
@auto_human_tool(mcp)
async def human_in_loop(question: str) -> str:
    """
    Ask the user a question and return the user's response.
    Args:
        question(str): The question to ask the user.
    Returns:
        str: The user's response.
    """
    pass


# Multiple parameters example
@auto_human_tool(mcp)
async def get_weather(city: str, time: str) -> str:
    """
    Get weather.
    Args:
        city(str): The city to get weather.
        time(str): The time to get weather.
    Returns:
        str: The weather.
    """
    pass


if __name__ == "__main__":
    mcp.run(transport="stdio")
