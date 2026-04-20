---
name: gamenative-fs
description: Manages game files, surgical patching (replace text), and basic file system operations.
---

# GameNative File System Master

Use this skill for direct manipulation of game files, INI/CFG patching, and managing game assets.

## Key Tools
- `read_game_file` / `write_game_file`: Read/write full files in the container's Wine prefix.
- `patch_game_file`: Surgically replaces text (old_string -> new_string), mirroring the Gemini CLI `replace` tool.
- `file_operations`: Provides `cp` (copy), `mv` (move), and `rm` (delete) actions.
- `list_game_files`: Recursively explores game and user folders within the container.

## Patching Best Practices
- **Safety First**: Before using `patch_game_file`, use `file_operations(action="cp", ...)` to back up the original file.
- **Ambiguity**: If `patch_game_file` fails because the string is found multiple times, add more surrounding lines to the `old_string` to make it unique.
- **Pathing**: Use `drive_c/Games/Path/To/Game` for game files, or `drive_c/users/xuser/Documents` for save games and INIs.
