#!/usr/bin/env python3
"""Standalone GPIO test. This test does not use Needle."""

from time import sleep
from gpiozero import LED

led = LED(17)  # BCM GPIO17, physical pin 11

try:
    print("LED ON for 2 seconds")
    led.on()
    sleep(2)

    print("LED OFF for 2 seconds")
    led.off()
    sleep(2)
finally:
    led.off()
    led.close()
    print("GPIO test finished; LED set OFF.")
