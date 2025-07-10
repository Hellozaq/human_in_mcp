# Human-in-MCP

[🇨🇳 中文](README.md) | [🇺🇸 English](README_en.md) 

---

A MCP tool that provides human responses, useful for debugging Agents.

Use case: When building Agents/Workflows, you can debug the Agent/Workflow effects before implementing MCP tools, where humans provide MCP tool return results. After debugging is complete, replace this MCP tool with the implemented tool.

## System Architecture

1. **main.py** - MCP Server, **you can add functions here, remember to complete the function Docstring**
2. **human_api.py** - FastAPI service, handles user interaction (**supports multi-request queue to avoid request overwrite**)
3. **client.py** - Client script for interacting with API, users provide responses here (**supports responding via response.txt file or direct input**)

## Install Dependencies

```bash
uv add fastapi, httpx, loguru, pydantic, uvicorn
```

## Usage

### 1. Start API Service

```bash
uv run human_api.py
```

This will start the API service at `http://127.0.0.1:8000`.

### 2. Start Client (Optional)

Run in another terminal:

```bash
uv run client.py
```

Provides an interactive interface to interact with the API service, where users provide MCP tool call results.

- Supports responding to requests via `response.txt` file or direct input.
- Supports responding to the first request or a specific request ID.

### 3. Run MCP Tool

```bash
uv run main.py
```

## API Endpoints

- `POST /ask` - Send questions to users and wait for responses (**supports multi-request queue**)
- `POST /respond` - Users provide responses (**can specify request_id**)
- `GET /status` - Get current status
- `GET /queue` - View all pending requests

## Workflow

1. When the `human_in_mcp` tool is called, it sends a question to the local API (**each request has a unique ID, supports concurrency**)
2. The API service displays the question and waits for user response, all requests are queued and processed in order
3. Users provide responses through the client (file or input) or by directly calling the API
4. The API returns the response to the `human_in_mcp` tool

## Decorator Usage

You can use the `@auto_human_tool` decorator to quickly define MCP tool functions. See usage example in main.py.

## Usage Example

When the MCP tool calls `human_in_mcp("What is your name?")`:

1. The question will be displayed in the API service console
2. Users can input responses through the client or edit response.txt to reply
3. The response will be returned to the MCP tool

## Notes

- Ensure the API service is started before running the MCP tool
- **Default timeout is 10 minutes**
- API service runs on local 127.0.0.1:8000
