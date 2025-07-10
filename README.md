# Human-in-MCP

[🇨🇳 中文](README.md) | [🇺🇸 English](README_en.md) 

---

人工提供回复的MCP工具，可以用于调试Agent

应用场景：搭建Agent/WorkFlow时，在尚未实现MCP工具的情况下调试Agent/WorkFlow的效果，即人工提供MCP工具的返回结果，调试完成后将该MCP工具替换为实现好的工具即可


## 系统架构

1. **main.py** - MCP Server，**可以在这里添加函数，注意完善函数的Docstring**
2. **human_api.py** - FastAPI服务，处理用户交互
3. **client.py** - 客户端脚本，用于与API交互，用户在这里提供答复

## 安装依赖

```bash
uv add fastapi, httpx, loguru, pydantic, uvicorn
```

## 使用方法

### 1. 启动API服务

```bash
uv run human_api.py
```

这将在 `http://127.0.0.1:8000` 启动API服务。

### 2. 启动客户端（可选）

在另一个终端中运行：

```bash
uv run client.py
```

提供一个交互式界面来与API服务交互，用户在这里提供MCP工具的调用结果。

### 3. 运行MCP工具

```bash
uv run main.py
```

## API端点

- `POST /ask` - 发送问题给用户并等待回复
- `POST /respond` - 用户提供回复
- `GET /status` - 获取当前状态

## 工作流程

1. 当`human_in_mcp`工具被调用时，它会向本地API发送问题
2. API服务显示问题并等待用户回复
3. 用户通过客户端或直接调用API提供回复
4. API将回复返回给`human_in_mcp`工具

## 示例

当MCP工具调用`human_in_mcp("你的名字是什么？")`时：

1. 问题会显示在API服务控制台
2. 用户可以通过客户端输入回复
3. 回复会返回给MCP工具

## 注意事项

- 确保API服务在MCP工具运行前启动
- 默认超时时间为5分钟
- API服务运行在本地127.0.0.1:8000
