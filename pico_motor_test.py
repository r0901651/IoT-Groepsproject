import RPi.GPIO as GPIO
import time

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for sending the pulse
pulse_pin = 16  # Change this to the GPIO pin you are using

# Set up the pulse pin as an output
GPIO.setup(pulse_pin, GPIO.OUT)

# Send a single pulse
def send_pulse():
    GPIO.output(pulse_pin, GPIO.HIGH)
    time.sleep(0.1)  # Adjust this delay to match the Pico script
    GPIO.output(pulse_pin, GPIO.LOW)

try:
    send_pulse()
    time.sleep(0.1)  # Adjust this delay to match the Pico script
    GPIO.cleanup()
except KeyboardInterrupt:
    GPIO.cleanup()
    