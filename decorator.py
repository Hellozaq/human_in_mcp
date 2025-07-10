import functools
import inspect
import httpx
from loguru import logger
from mcp.server.fastmcp import FastMCP
from typing import Callable


def auto_human_tool(
    mcp_instance: FastMCP,
    api_url: str = "http://127.0.0.1:8000/ask",
    timeout: float = 300.0
):
    """
    Decorator to automatically extract function information.
    
    Usage example:
    @auto_human_tool(mcp)
    async def ask_user(question: str) -> str:
        '''Ask the user a question and return the user's response.'''
        pass
    """
    def decorator(func: Callable) -> Callable:
        function_name = func.__name__
        docstring = func.__doc__ or f"Call {function_name} with user interaction"
        
        # Get function type hints
        type_hints = func.__annotations__
        # Remove return type
        parameters = {k: v for k, v in type_hints.items() if k != 'return'}
        sig = inspect.signature(func)

        @mcp_instance.tool()
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            # Build parameter string
            param_str = ", ".join([f"{k}=\"{v}\"" for k, v in bound.arguments.items()])
            full_call = f"{function_name}({param_str})"
            
            logger.info(f"***Getting user response for question: {full_call}***")
            
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.post(
                        api_url,
                        json={"question": full_call},
                        timeout=timeout
                    )
                    response.raise_for_status()
                    result = response.json()
                    return result["response"]
                except Exception as e:
                    logger.error(f"Failed to get user response: {e}")
                    return f"Error getting user response: {e}"
        
        # Set function attributes
        wrapper.__name__ = function_name
        wrapper.__doc__ = docstring
        wrapper.__annotations__ = parameters
        wrapper.__signature__ = sig  # Make the signature visible to the outside
        return wrapper
    
    return decorator
