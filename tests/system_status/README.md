# Test: Get System Status

## Purpose
Ask Needle to select `get_status`. The Python script then returns the Raspberry Pi hostname, uptime, memory information, and whether the Needle model exists.

## Files
- `test_status.py` — invokes Needle and executes the approved status function.
- `../../config/system_status_tools.json` — tool schema provided to Needle.

## Run
From the repository root on the Pi:

```bash
source ~/needle_test/needle_env/bin/activate
python3 tests/system_status/test_status.py
```

If your Needle runtime is in a different location, set it before running:

```bash
export NEEDLE_DIR="$HOME/needle_test/needle_armv7/linux-armv7"
```

## Expected result
The output should state that Needle selected `get_status`, followed by JSON with the hostname, uptime, memory values, and model-file status.

## Notes
This test reads system information; it does not change hardware. A model file can exist while model inference still fails, so inspect any runtime errors separately.
