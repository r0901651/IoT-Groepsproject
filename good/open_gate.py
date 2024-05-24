import RPi.GPIO as GPIO
import time

# Set up GPIO using BCM numbering if not set in different scripts
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for sending the pulse
pulse_pin = 25  # Change this to the GPIO pin you are using

# Set up the pulse pin as an output
GPIO.setup(pulse_pin, GPIO.OUT)

# Send a single pulse
def send_pulse():
    GPIO.output(pulse_pin, GPIO.HIGH)
    time.sleep(0.01)  # Adjust this delay to match the Pico script
    GPIO.output(pulse_pin, GPIO.LOW)

try:
    send_pulse()
    time.sleep(0.5)  # Adjust this delay to match the Pico script
except KeyboardInterrupt:
    GPIO.cleanup()
finally:
    GPIO.cleanup()

