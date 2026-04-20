---
name: gamenative-automation
description: Internal execution, auto-launch scripts, and running specific executables.
---

# GameNative Automation Master

Use this skill to configure auto-launch sequences and run arbitrary binaries inside a container.

## Key Tools
- `run_in_container`: Runs any `.exe` or `.bat` inside an existing/new session.
- `setup_autostart_script`: Creates a `.bat` and sets it as the container's default executable.
- `launch_game`: Launches the primary game defined in the container.

## Automation Workflow
1.  **Preparation**: If a tool is missing, use `install_component` first.
2.  **Sequential Execution**: Use `setup_autostart_script` to run multiple tools (e.g., Overlay, Reshade) and then the game.
3.  **Real-time Interaction**: Use `run_in_container` for patching or running configuration utilities without restarting the entire game.
4.  **Verification**: Always use `launch_game` to verify the autostart sequence.
