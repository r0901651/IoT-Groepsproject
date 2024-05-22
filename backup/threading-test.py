import threading
import time
import RPi.GPIO as GPIO

# Assuming BUTTON_PIN is already defined and GPIO is properly set up
BUTTON_PIN = 15  # Example pin number, change as needed

GPIO.setmode(GPIO.BCM)  # Set the GPIO mode
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Setup the pin as input with pull-down resistor

# Global variable for the button state
button_pressed = False

def check_button():
    global button_pressed
    while True:
        button_pressed = False
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
            time.sleep(0.01)  # Debounce delay
            if GPIO.input(BUTTON_PIN) == GPIO.HIGH:  # Check again to confirm
                button_pressed = True
                # Handle button press action here
                while GPIO.input(BUTTON_PIN) == GPIO.HIGH:
                    time.sleep(0.01)  # Wait until the button is released to avoid multiple prints for a single press
        time.sleep(0.1)  # Adjust this delay as needed to avoid busy-waiting

# Create and start the thread
button_thread = threading.Thread(target=check_button)
button_thread.daemon = True  # Optional: makes the thread exit when the main program exits
button_thread.start()
