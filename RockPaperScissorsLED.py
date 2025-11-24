from machine import Pin, UART
import time
import ujson

# UART to Grove Vision
uart = UART(0, baudrate=921600, tx=Pin(0), rx=Pin(1))

# LEDs
led_paper = Pin(2, Pin.OUT)      # Class 0
led_rock = Pin(3, Pin.OUT)       # Class 1
led_scissors = Pin(4, Pin.OUT)   # Class 2

def clear_leds():
    led_paper.low()
    led_rock.low()
    led_scissors.low()

clear_leds()

print("Starting Rock-Paper-Scissors detection...")

while True:

    # Request inference
    uart.write("AT+INVOKE=1,0,0\r")

    # Read UART response
    start = time.ticks_ms()
    raw = b""
    while time.ticks_diff(time.ticks_ms(), start) < 300:
        if uart.any():
            raw += uart.read()

    parts = raw.split(b"\n")

    detected_class = None

    for p in parts:
        p = p.strip()

        if b'"boxes"' in p:
            try:
                msg = ujson.loads(p)
                boxes = msg["data"]["boxes"]

                if len(boxes) > 0:
                    # Only use the first detection
                    detected_class = boxes[0][5]

            except:
                pass

    clear_leds()

    if detected_class == 0:
        print("Detected: PAPER (0)")
        led_paper.high()

    elif detected_class == 1:
        print("Detected: ROCK (1)")
        led_rock.high()

    elif detected_class == 2:
        print("Detected: SCISSORS (2)")
        led_scissors.high()

    else:
        print(raw)

    time.sleep(0.1)
