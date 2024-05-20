import RPi.GPIO as GPIO
import time

# Define the GPIO pins for the LEDs
LED_PIN_1 = 23  # Used when file content is "unlocked"
LED_PIN_2 = 24  # Used when file content is "locked"

# Setup the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_1, GPIO.OUT)
GPIO.setup(LED_PIN_2, GPIO.OUT)

# Initialize PWM on the LEDs at 1000Hz
pwm_led_1 = GPIO.PWM(LED_PIN_1, 1000)
pwm_led_2 = GPIO.PWM(LED_PIN_2, 1000)

pwm_led_1.start(0)
pwm_led_2.start(0)

def breathe_led(pwm_led, duration):
    # Breathing effect
    end_time = time.time() + duration
    while time.time() < end_time:
        for i in range(0, 101):  # Fade in
            pwm_led.ChangeDutyCycle(i)
            time.sleep(0.01)
        for i in range(100, -1, -1):  # Fade out
            pwm_led.ChangeDutyCycle(i)
            time.sleep(0.01)

def turn_on_led(pwm_led):
    pwm_led.ChangeDutyCycle(100)

def turn_off_led(pwm_led):
    pwm_led.ChangeDutyCycle(0)

def read_motor_state():
    try:
        with open("motor-state.txt", "r") as file:
            return file.read().strip().lower()
    except FileNotFoundError:
        return "unknown"

try:
    motor_state = read_motor_state()

    if motor_state == "unlocked":
        breathe_led(pwm_led_1, 5)
        turn_on_led(pwm_led_1)
        turn_off_led(pwm_led_2)
    elif motor_state == "locked":
        breathe_led(pwm_led_2, 5)
        turn_on_led(pwm_led_2)
        turn_off_led(pwm_led_1)
    else:
        # Handle unknown status
        pass

    # Keep LEDs on for a defined period
    # time.sleep(10)

finally:
    # Cleanup
    pwm_led_1.stop()
    pwm_led_2.stop()
    GPIO.cleanup()
