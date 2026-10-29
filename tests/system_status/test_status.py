#!/usr/bin/env python3
"""Ask Needle to select get_status, then execute the approved Python function."""

import json
import os
import platform
import subprocess
import sys
from pathlib import Path

NEEDLE_DIR = Path(os.environ.get(
    "NEEDLE_DIR", str(Path.home() / "needle_test/needle_armv7/linux-armv7")
)).expanduser()
NEEDLE_BIN = NEEDLE_DIR / "needle"
MODEL_FILE = NEEDLE_DIR / "needle3.cact"
TOOLS_FILE = Path(__file__).resolve().parents[2] / "config/system_status_tools.json"


def run_needle(prompt):
    for required in (NEEDLE_BIN, MODEL_FILE, TOOLS_FILE):
        if not required.exists():
            raise FileNotFoundError(f"Required file not found: {required}")

    cmd = [
        str(NEEDLE_BIN), "--model", str(MODEL_FILE),
        "--tools", str(TOOLS_FILE), "--prompt", prompt,
        "--max", "96", "--threads", "2"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    output = (result.stdout or "") + "\n" + (result.stderr or "")
    if result.returncode != 0:
        raise RuntimeError(f"Needle exited with code {result.returncode}:\n{output}")

    # The runtime may print diagnostic text around its JSON response.
    decoder = json.JSONDecoder()
    candidates = []
    for i, char in enumerate(output):
        if char == "{":
            try:
                obj, _ = decoder.raw_decode(output[i:])
                if isinstance(obj, dict) and "function_calls" in obj:
                    candidates.append(obj)
            except json.JSONDecodeError:
                pass
    if not candidates:
        raise RuntimeError(f"Could not find Needle JSON response:\n{output}")
    return candidates[-1]


def get_status():
    uptime = "Unavailable"
    try:
        uptime = subprocess.check_output(
            ["uptime", "-p"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    meminfo = {}
    try:
        with open("/proc/meminfo", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 2:
                    meminfo[parts[0].rstrip(":")] = int(parts[1])
    except OSError:
        pass

    total_mb = round(meminfo.get("MemTotal", 0) / 1024)
    available_mb = round(meminfo.get("MemAvailable", 0) / 1024)
    used_mb = max(total_mb - available_mb, 0) if total_mb else None

    return {
        "hostname": platform.node(),
        "uptime": uptime,
        "memory_total_mb": total_mb or None,
        "memory_available_mb": available_mb or None,
        "memory_estimated_used_mb": used_mb,
        "needle_model_exists": MODEL_FILE.is_file(),
        "needle_model_path": str(MODEL_FILE),
    }


def main():
    prompt = "Use get_status to report the Raspberry Pi system status."
    try:
        response = run_needle(prompt)
        calls = response.get("function_calls", [])
        call = next((c for c in calls if c.get("name") == "get_status"), None)
        if not call:
            print("Needle did not select get_status.")
            print(json.dumps(response, indent=2))
            sys.exit(2)

        print("Needle selected: get_status")
        print(json.dumps(get_status(), indent=2))
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
