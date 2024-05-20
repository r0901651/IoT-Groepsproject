from machine import Pin
import time

# Define the pin for the internal LED
led_pin = Pin(25, Pin.OUT)

# Toggle the LED state
led_pin.value(not led_pin.value())

# Define physical GPIO pins connected to the ULN2003AN driver board
IN1 = 10
IN2 = 11
IN3 = 12
IN4 = 13

STEPS_DEG = 48

# Define the sequence of steps for clockwise rotation
STEP_SEQUENCE_CLOCKWISE = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]

# Setup the motor pins
stepper_pins = [Pin(IN1, Pin.OUT), Pin(IN2, Pin.OUT), Pin(IN3, Pin.OUT), Pin(IN4, Pin.OUT)]

def set_step_clock(step):
    for pin_index in range(4):
        stepper_pins[pin_index].value(STEP_SEQUENCE_CLOCKWISE[step][pin_index])

def rotate_clockwise(degrees):
    write_motor_state()  # Write the motor state to the file
    steps = int(degrees / 30) * STEPS_DEG
    for _ in range(steps):
        for step in range(8):
            set_step_clock(step)
            time.sleep(0.01)

def write_motor_state():
    with open('motor-state.txt', 'w') as file:
        file.write("locked")

def cleanup():
    for pin in stepper_pins:
        pin.low()

# Function to be called when a pulse is detected on GPIO 22
def pulse_detected(pin):
    rotate_clockwise(30)  # Rotate 30 degrees clockwise
    cleanup()  # Cleanup GPIO pins used for the motor

# Set up GPIO 22 as an input with pull-up resistor
gpio22 = Pin(22, Pin.IN, Pin.PULL_UP)
# Attach an interrupt to GPIO 22 that calls pulse_detected function on rising edge
gpio22.irq(trigger=Pin.IRQ_RISING, handler=pulse_detected)

# Infinite loop to keep the program running
while True:
    time.sleep(0.5)
