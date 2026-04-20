# GameNative Optimizer Deployment Guide

This guide describes how to use the newly created Skill and MCP server to optimize your games in GameNative.

## 1. Prerequisites
- **ADB**: Ensure `adb` is in your PATH and your Android device is connected.
- **Python**: Python 3.10+ is required for the MCP server.
- **Dependencies**: The `mcp` library must be installed in a virtual environment.

## 2. Setting Up the MCP Server
The server is located in `./gamenative-mcp/mcp_server.py`.

To run it:
```sh
# Create virtual environment if not already done
python3 -m venv venv
./venv/bin/pip install mcp

# Run the server
./venv/bin/python gamenative-mcp/mcp_server.py
```

To register it with Gemini CLI, add this to your `~/.gemini/settings.json`:
```json
{
  "mcpServers": {
    "gamenative": {
      "command": "/path/to/project/venv/bin/python",
      "args": ["/path/to/project/gamenative-mcp/mcp_server.py"]
    }
  }
}
```

## 3. Using the Skill
Once registered, you can activate the skill by saying:
> "Help me optimize [Game Name] in GameNative"

The skill will:
1.  **Scan**: Use `list_containers` to find your game.
2.  **Config**: Use `update_container_config` to try different drivers/DXVK versions.
3.  **Run**: Use `launch_game` and `execute_actions` to test performance.
4.  **Analyze**: Review `fps_session.json` and logs to find the best configuration.

## 4. Action Chain Example (JSON)
You can provide complex testing runs via the `execute_actions` tool:
```json
{
  "actions": [
    { "type": "wait", "ms": 10000 },
    { "type": "click", "x": 540, "y": 1200 },
    { "type": "wait", "ms": 5000 },
    { "type": "key", "name": "ENTER", "action": "press" },
    { "type": "collect_fps", "id": "load_save", "duration_s": 20 },
    { "type": "screenshot", "name": "ingame_look" }
  ]
}
```

## 5. Advanced: Performance Intervals
If you need real-time FPS intervals (1s, 10s, etc.), ensure you are using a GameNative build that logs FPS to logcat. The MCP server's `get_logs` tool can be used by the skill to parse these values.
