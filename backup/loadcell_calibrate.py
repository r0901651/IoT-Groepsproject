import time
import RPi.GPIO as GPIO
from hx711 import HX711

def clean_and_exit():
    print("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()

GPIO.setmode(GPIO.BOARD)

hx = HX711(29, 31)  # DOUT - Pin 29, PD_SCK - Pin 31

hx.reset()

print("Please remove all weight from scale")
time.sleep(5)
print("Getting zero factor...")
zero_factor = sum([hx._read() for _ in range(10)]) / 10
print("Zero factor: ", zero_factor)

input("Now please place your known weight on the scale and press Enter")
print("Getting known weight factor...")
known_weight_factor = sum([hx._read() for _ in range(10)]) / 10
print("Known weight factor: ", known_weight_factor)

known_weight = 6  # replace with your known weight
conversion_factor = (known_weight_factor - zero_factor) / known_weight
print("Conversion factor: ", conversion_factor)

print("Now measuring weights...")
while True:
    try:
        raw_val = hx._read()
        weight = (raw_val - zero_factor) / conversion_factor
        print(weight)

        time.sleep(0.5)

    except (KeyboardInterrupt, SystemExit):
        clean_and_exit()