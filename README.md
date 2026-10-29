# Needle AI on Raspberry Pi Zero 2 W

An ongoing project to run Needle locally on a Raspberry Pi Zero 2 W and connect its tool-calling output to controlled Python functions. New capabilities and experiments will be added incrementally.

## Project Goals

- Run Needle using a compatible ARMv7 runtime.
- Connect model-selected tools to approved Python functions.
- Add hardware and software capabilities through separate, documented tests.

## Hardware and Software

- **Board:** Raspberry Pi Zero 2 W
- **OS:** Raspberry Pi OS, 32-bit (Bookworm / Debian 12 during initial setup)
- **Architecture:** ARMv7 / `armhf`
- **Python:** 3.11.x
- **Needle package:** `cactus-needle` 3.2.8
- **Runtime:** Prebuilt `linux-armv7` executable
- **Model:** `needle3.cact`

## Repository Structure

Keep the core setup and runtime separate from individual tests:

```text
needle-rpi-zero-2w/
├── README.md
├── src/                 # Shared Python integration code
├── config/              # Needle tool schemas and configuration
├── tests/
│   ├── system_status/   # System-status tool experiment
│   ├── gpio/            # GPIO and LED experiments
│   ├── camera/          # Future camera experiments
│   └── ...              # Additional tests
└── docs/                # Setup notes and design documentation
```

Each test folder should contain its own code and, where useful, a short README with wiring, dependencies, commands, expected output, and test status. Add a test to the structure when it is created.

## Setup

The initial runtime is stored on the Raspberry Pi under `~/needle_test/`:

```text
~/needle_test/
├── needle_env/
└── needle_armv7/
    └── linux-armv7/
        ├── needle
        ├── needle3.cact
        ├── libneedle.a
        └── needle.h
```

Activate the existing Python environment and enter the runtime directory:

```bash
source ~/needle_test/needle_env/bin/activate
cd ~/needle_test/needle_armv7/linux-armv7
```

Check that the runtime and model exist, then check the executable:

```bash
ls -lh needle needle3.cact
chmod +x needle
./needle --help
```

The environment was created with `--system-site-packages` to access the system-installed SentencePiece package. The prebuilt ARMv7 runtime was used after the local build path encountered dependency issues.

## How It Works

1. A user request is passed to Needle with the available tool definitions.
2. Needle returns structured output indicating which tool, if any, it selected.
3. A Python handler parses the output.
4. The handler validates the selected function and runs only an explicitly approved implementation.
5. The tool result can then be displayed or used by the surrounding application.

```text
User request
    |
    v
Needle model + tool schema
    |
    v
Structured tool-call output
    |
    v
Python handler
    |
    v
Approved function / hardware interface
```

Needle selects tools; Python performs the actual operations. An empty tool-call result does not mean an action was performed.

## Current Status

- [x] Downloaded and ran the prebuilt ARMv7 Needle runtime.
- [x] Tested selection of a `get_status` tool.
- [x] Connected Needle output to a Python handler for system-status information.
- [ ] Complete and document hardware tests in their respective folders.
- [ ] Add further tools as the project develops.

## Safety

- Execute only predefined, allow-listed functions; do not execute arbitrary model-generated shell commands.
- Raspberry Pi GPIO uses 3.3 V logic. Never apply 5 V directly to a GPIO pin.
- Use a suitable driver circuit for relays, motors, and other loads; do not power them directly from GPIO pins.

## References

- [Needle documentation](https://www.cactuscompute.com/needle)
- [Raspberry Pi documentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html)
- [GPIO Zero documentation](https://gpiozero.readthedocs.io/)
