# Human-in-MCP

[🇨🇳 中文](README.md) | [🇺🇸 English](README_en.md) 

---

A MCP tool that provides human responses, useful for debugging Agents.

Use case: When building Agents/Workflows, you can debug the Agent/Workflow effects before implementing MCP tools, where humans provide MCP tool return results. After debugging is complete, replace this MCP tool with the implemented tool.

## System Architecture

1. **main.py** - MCP Server, **you can add functions here, remember to complete the function Docstring**
2. **human_api.py** - FastAPI service, handles user interaction
3. **client.py** - Client script for interacting with API, users provide responses here

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

### 3. Run MCP Tool

```bash
uv run main.py
```

## API Endpoints

- `POST /ask` - Send questions to users and wait for responses
- `POST /respond` - Users provide responses
- `GET /status` - Get current status

## Workflow

1. When the `human_in_mcp` tool is called, it sends a question to the local API
2. The API service displays the question and waits for user response
3. Users provide responses through the client or by directly calling the API
4. The API returns the response to the `human_in_mcp` tool

## Example

When the MCP tool calls `human_in_mcp("What is your name?")`:

1. The question will be displayed in the API service console
2. Users can input responses through the client
3. The response will be returned to the MCP tool

## Notes

- Ensure the API service is started before running the MCP tool
- Default timeout is 5 minutes
- API service runs on local 127.0.0.1:8000
