# GameNative Optimizer Context

This extension provides tools to optimize games running in GameNative (an Android translation layer for Windows games).

## Core Directives
- Always check the Android device connection via ADB before suggesting optimizations.
- Use the 'gamenative-config' skill to query the EmuReady knowledge base for specific games.
- Prioritize stability over raw FPS; 30-60 FPS with no graphical glitches is the goal.
- When patching files, always use 'gamenative-fs' Master to create a backup first.
- If a game crashes, use 'gamenative-debug' Expert to analyze logcat and the Wine registry.

## Security
- Do not attempt to access files outside the GameNative /data/data/ or /sdcard/ paths unless explicitly requested.
- Warn the user before disabling thermal throttling.
