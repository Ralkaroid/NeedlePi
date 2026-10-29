#!/usr/bin/env python3
"""Interactive Needle tool-calling loop for GPIO17 LED control.

The LED object remains open between prompts so the requested state can persist
until the next command. Ctrl+C turns the LED off before exiting.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from gpiozero import LED

NEEDLE_DIR = Path(os.environ.get(
    "NEEDLE_DIR", str(Path.home() / "needle_test/needle_armv7/linux-armv7")
)).expanduser()
NEEDLE_BIN = NEEDLE_DIR / "needle"
MODEL_FILE = NEEDLE_DIR / "needle3.cact"
TOOLS_FILE = Path(__file__).resolve().parents[2] / "config/gpio_tools.json"


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


def main():
    for required in (NEEDLE_BIN, MODEL_FILE, TOOLS_FILE):
        if not required.exists():
            print(f"ERROR: Required file not found: {required}", file=sys.stderr)
            sys.exit(1)

    led = LED(17)
    led.off()  # Start in a known safe state.
    print("Needle GPIO control ready (BCM GPIO17).")
    print("Enter: turn the LED on / turn the LED off / exit")

    try:
        while True:
            prompt = input("\nCommand> ").strip()
            if prompt.lower() in {"exit", "quit"}:
                break
            if not prompt:
                continue

            try:
                response = run_needle(prompt)
                calls = response.get("function_calls", [])
                call = next(
                    (c for c in calls if c.get("name") in {"gpio_on", "gpio_off"}),
                    None
                )
                if call is None:
                    print("No approved GPIO tool selected. No hardware action taken.")
                    print(json.dumps(response, indent=2))
                    continue

                name = call["name"]
                if name == "gpio_on":
                    led.on()
                    print("Executed gpio_on. LED should now be ON.")
                elif name == "gpio_off":
                    led.off()
                    print("Executed gpio_off. LED should now be OFF.")
            except Exception as exc:
                print(f"Command failed: {exc}", file=sys.stderr)
    except KeyboardInterrupt:
        print("\nInterrupted.")
    finally:
        led.off()
        led.close()
        print("GPIO released; LED set OFF.")


if __name__ == "__main__":
    main()
