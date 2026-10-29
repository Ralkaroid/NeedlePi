# Test: GPIO LED and Needle Control

## Purpose
First test BCM GPIO17 independently, then use Needle to select an approved ON/OFF tool.

## Hardware and wiring
- LED anode (long leg) → 220–330 Ω resistor → physical pin 11 (BCM GPIO17)
- LED cathode (short leg) → physical pin 6 (GND)

Do not connect 5 V to a GPIO pin. Do not connect a motor or relay directly to a GPIO pin.

## Install GPIO Zero

```bash
sudo apt update
sudo apt install -y python3-gpiozero
```

Check the import in the environment you use:

```bash
python3 -c "from gpiozero import LED; print('GPIO Zero ready')"
```

## Step 1 — Test the LED without Needle

From the repository root:

```bash
python3 tests/gpio_control/test_gpio.py
```

The LED should turn on for two seconds, then off for two seconds. Continue only after this works.

## Step 2 — Start Needle GPIO control

```bash
source ~/needle_test/needle_env/bin/activate
python3 tests/gpio_control/gpio_control.py
```

At the `Command>` prompt, try:
- `Turn the LED on using gpio_on`
- `Turn the LED off using gpio_off`
- `exit`

The process keeps the GPIO object open between commands. Ctrl+C or `exit` turns the LED off and releases the GPIO.

## Expected result
Needle should return a `gpio_on` or `gpio_off` function call. The Python handler validates the function name and performs only that approved action. Observe the LED to verify the physical result.

## Troubleshooting
- If the standalone test fails, check wiring, LED polarity, pin numbering, GPIO Zero, and whether another process owns the GPIO.
- If Needle does not select a tool, use a direct prompt naming the intended tool and inspect the returned JSON.
- A message from the model is not proof that the LED changed state.
