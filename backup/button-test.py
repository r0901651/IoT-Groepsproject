import RPi.GPIO as GPIO
import time
import subprocess
import sys

pulse_pin = 16  # Change this to the GPIO pin you are using
button_pin = 15  # Change this to the GPIO pin connected to the button

GPIO.setwarnings(False)  # Ignore warnings for now
GPIO.setmode(GPIO.BCM)  # Use Broadcom GPIO numbering
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pulse_pin, GPIO.OUT)

# Send a single pulse
def send_pulse():
    GPIO.output(pulse_pin, GPIO.HIGH)
    time.sleep(0.1)  # Adjust this delay to match the Pico script
    GPIO.output(pulse_pin, GPIO.LOW)

try:
    while True:
        if GPIO.input(button_pin) == GPIO.HIGH:
            print("Button pressed!")
            send_pulse()
            time.sleep(0.1)  # Adjust this delay to match the Pico script
            time.sleep(0.2)  # Debouncing delay
            print("Button pressed. Running motor.py script.")
            subprocess.call([sys.executable, 'motor.py'])
finally:
    GPIO.cleanup()
    