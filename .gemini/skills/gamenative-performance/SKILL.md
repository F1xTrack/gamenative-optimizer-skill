---
name: gamenative-performance
description: Monitors FPS, GPU/CPU vitals, and optimizes system-level performance (Governors/Root).
---

# GameNative Performance Skill

Use this skill when you need to benchmark a game, monitor hardware health, or optimize the Android system.

## Key Tools
- `get_performance_summary`: Fetches AVG/MIN/MAX FPS from the last session.
- `get_hardware_vitals`: Checks thermals, CPU/GPU frequencies, and memory pressure.
- `optimize_system_performance`: Sets performance governors (Requires Root).
- `execute_actions`: Used with `collect_fps` to run timed performance tests.

## Optimization Advice
- **FPS Dips**: If FPS drops but frequencies are stable, the bottleneck is in the compatibility layer (DXVK/Wine).
- **Throttling**: If temperatures exceed 70-80°C and frequencies drop, recommend a cooling pad or reducing resolution.
- **Root Performance**: Always suggest running `optimize_system_performance` before a serious benchmark.
