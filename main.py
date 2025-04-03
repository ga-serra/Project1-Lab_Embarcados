from machine import Pin
import time

red_led = Pin(12, Pin.OUT)

while True:
    red_led.value(1)
    time.sleep(1)
    red_led.value(0)
    time.sleep(1)
