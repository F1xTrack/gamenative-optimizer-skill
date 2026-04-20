import os
import subprocess
import json
import time
import tempfile
import threading
from typing import List, Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

# Configuration
PACKAGE_NAME = "app.gamenative"
IMAGEFS_PATH = f"/data/data/{PACKAGE_NAME}/files/imagefs"
CONTAINERS_PATH = f"{IMAGEFS_PATH}/home/xuser/.winlator/containers"

mcp = FastMCP("GameNative Optimizer")

class ADB:
    @staticmethod
    def run_command(args: List[str], use_root: bool = False, use_run_as: bool = False) -> str:
        cmd = ["adb", "shell"]
        
        prefix = ""
        if use_root:
            prefix = "su -c "
        elif use_run_as:
            prefix = f"run-as {PACKAGE_NAME} "
            
        full_command = prefix + " ".join(args)
        cmd.append(full_command)
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"ADB command failed: {result.stderr}")
        return result.stdout.strip()

    @staticmethod
    def push_file(local_path: str, remote_path: str):
        subprocess.run(["adb", "push", local_path, remote_path], check=True)

    @staticmethod
    def pull_file(remote_path: str, local_path: str):
        subprocess.run(["adb", "pull", remote_path, local_path], check=True)

    @staticmethod
    def shell_input(command: str):
        subprocess.run(["adb", "shell", "input", command], check=True)

@mcp.tool()
def list_containers(use_root: bool = False) -> List[Dict[str, Any]]:
    """List all containers and their basic info."""
    try:
        # We need to find directories in CONTAINERS_PATH
        cmd = [f"ls -1 {CONTAINERS_PATH}"]
        output = ADB.run_command(cmd, use_root=use_root, use_run_as=not use_root)
        container_ids = output.split("\n")
        
        containers = []
        for cid in container_ids:
            if not cid: continue
            try:
                config_path = f"{CONTAINERS_PATH}/{cid}/.container"
                config_json = ADB.run_command([f"cat {config_path}"], use_root=use_root, use_run_as=not use_root)
                data = json.loads(config_json)
                containers.append(data)
            except:
                pass
        return containers
    except Exception as e:
        return [{"error": str(e)}]

@mcp.tool()
def update_container_config(container_id: str, updates: Dict[str, Any], use_root: bool = False) -> str:
    """Update a container's configuration."""
    try:
        config_path = f"{CONTAINERS_PATH}/{container_id}/.container"
        config_json = ADB.run_command([f"cat {config_path}"], use_root=use_root, use_run_as=not use_root)
        data = json.loads(config_json)
        data.update(updates)
        
        new_config = json.dumps(data)
        
        # Write to temp file and push
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write(new_config)
            temp_local = f.name
            
        temp_remote = f"/data/local/tmp/container_{container_id}.json"
        ADB.push_file(temp_local, temp_remote)
        
        # Move to target location
        mv_cmd = [f"cp {temp_remote} {config_path}"]
        ADB.run_command(mv_cmd, use_root=use_root, use_run_as=not use_root)
        
        os.unlink(temp_local)
        return "Success"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def launch_game(container_id: str) -> str:
    """Launch a container by ID."""
    # This might vary based on how GameNative handles intents.
    # Usually: am start -n app.gamenative/app.gamenative.ui.MainActivity --ei container_id <ID>
    # Checking XServerScreen.kt might reveal more.
    try:
        cmd = ["am", "start", "-n", f"{PACKAGE_NAME}/com.winlator.MainActivity", "--ei", "container_id", container_id]
        subprocess.run(["adb", "shell"] + cmd, check=True)
        return "Game launched"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def list_game_files(container_id: str, sub_path: str = "", use_root: bool = False) -> List[str]:
    """List files within a container's Wine prefix (e.g., '.wine/drive_c/Games/')."""
    try:
        remote_path = f"{CONTAINERS_PATH}/{container_id}/.wine/{sub_path}"
        output = ADB.run_command([f"ls -R {remote_path}"], use_root=use_root, use_run_as=not use_root)
        return output.split("\n")
    except Exception as e:
        return [f"Error: {str(e)}"]

@mcp.tool()
def read_game_file(container_id: str, sub_path: str, use_root: bool = False) -> str:
    """Read a file from the container's Wine prefix."""
    try:
        remote_path = f"{CONTAINERS_PATH}/{container_id}/.wine/{sub_path}"
        return ADB.run_command([f"cat {remote_path}"], use_root=use_root, use_run_as=not use_root)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def write_game_file(container_id: str, sub_path: str, content: str, use_root: bool = False) -> str:
    """Write or update a file in the container's Wine prefix."""
    try:
        remote_path = f"{CONTAINERS_PATH}/{container_id}/.wine/{sub_path}"
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write(content)
            temp_local = f.name
            
        temp_remote = f"/data/local/tmp/game_file_{int(time.time())}.tmp"
        ADB.push_file(temp_local, temp_remote)
        
        # Move to final location
        mv_cmd = [f"cp {temp_remote} {remote_path}"]
        ADB.run_command(mv_cmd, use_root=use_root, use_run_as=not use_root)
        
        os.unlink(temp_local)
        return "Success"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def run_in_container(container_id: str, exe_path: str, args: str = "") -> str:
    """Run an executable or script inside an active container using winhandler."""
    try:
        # We can use 'am start' with specific extras to run a file in an existing/new session
        # Based on Winlator/GameNative code, usually there's a 'winhandler' intent
        cmd = [
            "am", "start", "-n", f"{PACKAGE_NAME}/com.winlator.MainActivity",
            "--ei", "container_id", container_id,
            "--es", "executable_path", exe_path,
            "--es", "exec_args", args
        ]
        subprocess.run(["adb", "shell"] + cmd, check=True)
        return f"Execution requested for {exe_path}"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_hardware_vitals(use_root: bool = False) -> Dict[str, Any]:
    """Get current hardware telemetry (thermal, frequencies, memory, battery)."""
    try:
        vitals = {}
        
        # Thermals (might need root or specific paths)
        try:
            thermal_cmd = ["cat /sys/class/thermal/thermal_zone*/temp"]
            temps = ADB.run_command(thermal_cmd, use_root=use_root).split("\n")
            vitals["thermals"] = [float(t)/1000.0 if t.isdigit() else t for t in temps if t]
        except: vitals["thermals"] = "Error collecting thermals"

        # CPU Frequencies
        try:
            freq_cmd = ["cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq"]
            freqs = ADB.run_command(freq_cmd, use_root=use_root).split("\n")
            vitals["cpu_freqs_mhz"] = [int(f)/1000.0 if f.isdigit() else f for f in freqs if f]
        except: vitals["cpu_freqs_mhz"] = "Error collecting CPU freqs"

        # GPU Frequency (Snapdragon specific)
        try:
            gpu_cmd = ["cat /sys/class/kgsl/kgsl-3d0/gpuclk"]
            gpu_clk = ADB.run_command(gpu_cmd, use_root=use_root)
            vitals["gpu_clk_mhz"] = int(gpu_clk)/1000000.0 if gpu_clk.isdigit() else gpu_clk
        except: vitals["gpu_clk_mhz"] = "N/A"

        # Memory
        try:
            mem_cmd = ["cat /proc/meminfo"]
            mem_info = ADB.run_command(mem_cmd, use_root=use_root)
            vitals["mem_info"] = mem_info.split("\n")[:10] # Top 10 lines
        except: vitals["mem_info"] = "Error collecting memory info"

        # Battery/Power
        try:
            bat_cmd = ["dumpsys battery"]
            bat_info = ADB.run_command(bat_cmd, use_root=use_root)
            vitals["battery"] = bat_info
        except: vitals["battery"] = "Error collecting battery info"

        return vitals
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def optimize_system_performance(use_root: bool = True) -> str:
    """Optimize Android system for gaming (Root required).
    Sets CPU/GPU governors to performance, clears background tasks.
    """
    if not use_root:
        return "Error: Root is required for system optimization."
    
    try:
        # 1. Set CPU Governor to performance
        ADB.run_command(["for i in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do echo performance > $i; done"], use_root=True)
        
        # 2. Set GPU Governor to performance (Snapdragon)
        ADB.run_command(["echo performance > /sys/class/kgsl/kgsl-3d0/devfreq/governor"], use_root=True)
        
        # 3. Clear background processes (aggressive)
        ADB.run_command(["am kill-all"], use_root=True)
        
        # 4. Disable thermal throttling (DANGEROUS, but requested for 'testing')
        # ADB.run_command(["stop thermald"], use_root=True) 
        
        return "System optimized for performance (Governors set, background apps killed)."
    except Exception as e:
        return f"Error during optimization: {str(e)}"

@mcp.tool()
def read_log(lines: int = 100, full: bool = False) -> str:
    """Read logcat logs. Set full=True to get the complete log buffer."""
    try:
        cmd = ["logcat", "-d"]
        if not full:
            cmd.extend(["-t", str(lines)])
        return ADB.run_command(cmd)
    except Exception as e:
        return f"Error reading logs: {str(e)}"

@mcp.tool()
def patch_game_file(container_id: str, sub_path: str, old_string: str, new_string: str, use_root: bool = False) -> str:
    """Surgically replace text in a game file (similar to Gemini CLI 'replace' tool).
    Requires exact match for 'old_string'.
    """
    try:
        content = read_game_file(container_id, sub_path, use_root=use_root)
        if "Error:" in content: return content
        
        if old_string not in content:
            return f"Error: 'old_string' not found in {sub_path}"
        
        if content.count(old_string) > 1:
             return f"Error: 'old_string' is ambiguous (found multiple occurrences) in {sub_path}"
             
        new_content = content.replace(old_string, new_string)
        return write_game_file(container_id, sub_path, new_content, use_root=use_root)
    except Exception as e:
        return f"Error patching file: {str(e)}"

@mcp.tool()
def file_operations(container_id: str, action: str, src_sub_path: str, dst_sub_path: str = "", use_root: bool = False) -> str:
    """Perform file operations (copy, move, delete) within the container's Wine prefix.
    Actions: 'cp', 'mv', 'rm'.
    """
    try:
        src = f"{CONTAINERS_PATH}/{container_id}/.wine/{src_sub_path}"
        dst = f"{CONTAINERS_PATH}/{container_id}/.wine/{dst_sub_path}" if dst_sub_path else ""
        
        if action == "cp":
            cmd = [f"cp -r {src} {dst}"]
        elif action == "mv":
            cmd = [f"mv {src} {dst}"]
        elif action == "rm":
            cmd = [f"rm -rf {src}"]
        else:
            return "Error: Invalid action. Use 'cp', 'mv', or 'rm'."
            
        ADB.run_command(cmd, use_root=use_root, use_run_as=not use_root)
        return f"Action '{action}' successful."
    except Exception as e:
        return f"Error during file operation: {str(e)}"

@mcp.tool()
def kill_wine_processes(use_root: bool = False) -> str:
    """Forcefully kill all Wine-related processes (wineserver, explorer, etc.) to clean the environment."""
    try:
        processes = ["wineserver", "explorer.exe", "winhandler", "services.exe", "plugplay.exe"]
        for p in processes:
            try:
                ADB.run_command([f"pkill -9 {p}"], use_root=use_root)
            except: pass
        return "Wine processes killed."
    except Exception as e:
        return f"Error killing processes: {str(e)}"

@mcp.tool()
def manage_wine_registry(container_id: str, reg_file: str, key: str, value: str = None, action: str = "get", use_root: bool = False) -> str:
    """Read or modify the Wine registry (user.reg, system.reg).
    Actions: 'get' (returns the line containing the key), 'set' (adds/updates the key - use with caution).
    """
    # Note: Proper .reg parsing is complex; for now we use grep/sed style for simple keys.
    try:
        path = f"drive_c/windows/{reg_file}" # Simplified path, actual is usually in the prefix root
        if "user.reg" in reg_file or "system.reg" in reg_file:
            path = reg_file # Root of prefix
            
        if action == "get":
            content = read_game_file(container_id, path, use_root=use_root)
            lines = [line for line in content.split("\n") if key in line]
            return "\n".join(lines) if lines else "Key not found."
        elif action == "set" and value is not None:
            # This is a placeholder for more complex registry manipulation.
            # Realistically, models should use 'patch_game_file' on .reg files for precision.
            return "For 'set', please use the 'patch_game_file' tool directly on the .reg file to ensure correct formatting."
        return "Invalid action or missing value."
    except Exception as e:
        return f"Error managing registry: {str(e)}"

@mcp.tool()
def manage_snapshot(container_id: str, action: str = "save", snapshot_name: str = "default", use_root: bool = False) -> str:
    """Save or restore a container's configuration and prefix state.
    Actions: 'save', 'restore'.
    """
    try:
        backup_path = f"{IMAGEFS_PATH}/home/xuser/.winlator/backups/{container_id}_{snapshot_name}"
        container_src = f"{CONTAINERS_PATH}/{container_id}"
        
        if action == "save":
            ADB.run_command([f"mkdir -p {backup_path}"], use_root=use_root, use_run_as=not use_root)
            ADB.run_command([f"cp -r {container_src}/.container {backup_path}/"], use_root=use_root, use_run_as=not use_root)
            # Only backup important config files from prefix to save space/time
            ADB.run_command([f"cp {container_src}/.wine/*.reg {backup_path}/"], use_root=use_root, use_run_as=not use_root)
            return f"Snapshot '{snapshot_name}' saved to {backup_path}"
        elif action == "restore":
            ADB.run_command([f"cp {backup_path}/.container {container_src}/"], use_root=use_root, use_run_as=not use_root)
            ADB.run_command([f"cp {backup_path}/*.reg {container_src}/.wine/"], use_root=use_root, use_run_as=not use_root)
            return f"Snapshot '{snapshot_name}' restored."
        return "Invalid action."
    except Exception as e:
        return f"Error managing snapshot: {str(e)}"

@mcp.tool()
def execute_actions(chain_json: str, use_root: bool = False) -> Dict[str, Any]:
    """Execute a chain of actions and collect results.
    Supports complex intervals and gamepad inputs (simulated).
    """
    try:
        chain = json.loads(chain_json)
        results = {"events": [], "screenshots": [], "performance": {}}
        
        start_time = time.time()
        
        for action in chain.get("actions", []):
            atype = action.get("type")
            if atype == "wait":
                time.sleep(action.get("ms", 1000) / 1000.0)
            elif atype == "click":
                ADB.shell_input(f"tap {action['x']} {action['y']}")
            elif atype == "key":
                name = action.get("name")
                act = action.get("action", "press")
                if act == "press":
                    ADB.shell_input(f"keyevent {name}")
            elif atype == "gamepad":
                # Placeholder for complex gamepad events via sendevent
                btn = action.get("button")
                axis = action.get("axis")
                val = action.get("value")
                duration = action.get("ms", 100)
                results["events"].append(f"Gamepad: {btn or axis} = {val} for {duration}ms")
                # Implementation would involve mapping axes to /dev/input/eventX
            elif atype == "collect_fps":
                # Collect session summary
                summary = get_performance_summary(use_root=use_root)
                results["performance"][action.get("id", "test")] = summary
            elif atype == "screenshot":
                name = action.get("name", f"scr_{int(time.time())}")
                temp_remote = f"/data/local/tmp/{name}.png"
                ADB.run_command([f"screencap -p {temp_remote}"])
                with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
                    temp_local = f.name
                ADB.pull_file(temp_remote, temp_local)
                results["screenshots"].append({"name": name, "local_path": temp_local})
        
        return results
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_performance_summary(use_root: bool = False) -> Dict[str, Any]:
    """Get the current FPS summary from the last session."""
    fps_log_path = f"{IMAGEFS_PATH}/tmp/fps_session.json"
    try:
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_local = f.name
        ADB.pull_file(fps_log_path, temp_local)
        with open(temp_local, 'r') as f:
            data = json.load(f)
        os.unlink(temp_local)
        return data
    except Exception as e:
        return {"error": f"Could not read FPS log: {str(e)}"}

@mcp.tool()
def get_logs(lines: int = 100) -> str:
    """Get the last N lines of logcat."""
    try:
        return ADB.run_command([f"logcat -d -t {lines}"])
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
