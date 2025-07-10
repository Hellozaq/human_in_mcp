import sys
import os
# Add the current file's directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp.server.fastmcp import FastMCP
from decorator import auto_human_tool

mcp = FastMCP("human_in_mcp", log_level="ERROR")


@auto_human_tool(mcp)
async def getApiDocs(group_id: str, artifact_id: str, version: str, api_sign: str) -> str:
    """
    Get the API documentation.
    Args:
        group_id(str): The group ID of the library.
        artifact_id(str): The artifact ID of the library.
        version(str): The version of the library.
        api_sign(str): The API signature.
    Returns:
        str: The API documentation.
    """
    pass


@auto_human_tool(mcp)
async def getApiUsages(group_id: str, artifact_id: str, version: str, api_sign: str) -> str:
    """
    Get the API usage.
    Args:
        group_id(str): The group ID of the library.
        artifact_id(str): The artifact ID of the library.
        version(str): The version of the library.
        api_sign(str): The API signature.
    Returns:
        str: The API usage examples.
    """
    pass


@auto_human_tool(mcp)
async def getApiCode(group_id: str, artifact_id: str, version: str, api_sign: str) -> str:
    """
    Get the API implementation code.
    Args:
        group_id(str): The group ID of the library.
        artifact_id(str): The artifact ID of the library.
        version(str): The version of the library.
        api_sign(str): The API signature.
    Returns:
        str: The API implementation code.
    """
    pass


@auto_human_tool(mcp)
async def applyResult(res_dict: dict) -> str:
    """
    Apply the result to the client code.
    Args:
        res_dict(dict): res_dict is a dict, the key is the relative path of the file, and the value is the complete code. Return "Apply Success" or the reason for failure.
    Returns:
        str: The result of the application.
    """
    pass


@auto_human_tool(mcp)
async def exeComp() -> str:
    """
    Execute "mvn clean package". Return "Build Success" or the compilation failure information.
    Returns:
        str: The result of the compilation.
    """
    pass


if __name__ == "__main__":
    mcp.run(transport="stdio")
