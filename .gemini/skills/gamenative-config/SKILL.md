---
name: gamenative-config
description: Manages container settings, driver versions, DXVK/Wine components, and queries the knowledge base.
---

# GameNative Configuration Expert

Use this skill to update container parameters or install new compatibility layers.

## Key Tools
- `list_containers`: Lists current game containers and their configurations.
- `update_container_config`: Modifies container JSON (graphicsDriver, dxwrapper, etc.).
- `install_component`: Pushes `.wcp` or `.zip` components to the container environment.
- `query_knowledge_base`: Searches EmuReady for the best settings for a specific SoC/Game.

## Configuration Strategy
- **Drivers**: Try **Turnip** for Adreno, **VirGL** for older chips.
- **DXVK**: GPLAsync (2.3/2.4) is usually better for stability; 2.6/2.7 for newer games.
- **Wine**: Proton (9.0/10.0) for Steam games; Wine 9.2 for generic apps.
- **Check EmuReady**: Always use `query_knowledge_base` before trying a random driver.
