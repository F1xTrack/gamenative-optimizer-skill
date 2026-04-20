---
name: gamenative-subagents
description: Dispatches parallel or independent tasks (like multi-container benchmarking) to the 'generalist' sub-agent.
---

# GameNative Subagent Orchestrator

Use this skill when you have multiple independent tasks to perform (e.g., "Fix all 10 containers," "Benchmark 3 drivers in parallel").

## Strategic Delegation

1.  **Identify Independence**: Ensure the tasks do not modify the same file or resource at the same time. 
    *   *Safe*: Benchmarking different games on separate containers.
    *   *Unsafe*: Updating the same `mcp_server.py` from multiple agents.
2.  **Dispatch**: Use the `generalist` tool to delegate each task.
3.  **Synthesize**: Collect the results from all sub-agents and provide a unified report.

## When to use Subagents
- **Batch Processing**: "Apply this .ini tweak to all Fallout containers."
- **Speculative Research**: "Check EmuReady for 5 different games and summarize."
- **High-Volume Output**: "Run a 5-minute benchmark and parse the full log."

## Example Directive
> "I'm delegating the benchmarking of Container_A to a generalist sub-agent while I analyze the logs for Container_B."
