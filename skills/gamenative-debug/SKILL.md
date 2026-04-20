---
name: gamenative-debug
description: Logs (tail/full), Registry, Snapshots, and Process Cleanup.
---

# GameNative Debug Expert

Use this skill to troubleshoot crashes, edit the Wine Registry, and manage container snapshots.

## Key Tools
- `read_log`: Reads the logcat buffer (tail N lines or full). Use `full=True` for comprehensive analysis.
- `manage_wine_registry`: Search for keys/values in `user.reg` and `system.reg`.
- `manage_snapshot`: Save/restore container config and registry state (save before any major registry change).
- `kill_wine_processes`: Cleans up the environment by killing `wineserver`, `explorer.exe`, etc.

## Debugging Workflow
1.  **Cleanup**: Run `kill_wine_processes` to ensure a fresh start.
2.  **Snapshot**: Run `manage_snapshot(action="save", snapshot_name="pre-fix")`.
3.  **Logs**: If the game fails to start, use `read_log(lines=100)` to find the last error messages.
4.  **Registry**: Use `manage_wine_registry` to check if a specific key is set, then use `patch_game_file` on the `.reg` file to change it.
