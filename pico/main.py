from machine import Pin
from time import sleep


# Define the pin for the internal LED
led_pin = Pin(25, Pin.OUT)

# Toggle the LED state
led_pin.value(not led_pin.value())

# Define the pins for stepper motor 1
IN1_M1 = 2
IN2_M1 = 3
IN3_M1 = 4
IN4_M1 = 5

# Define the pins for stepper motor 2
IN1_M2 = 6
IN2_M2 = 7
IN3_M2 = 8
IN4_M2 = 9

# Define the input pin for the signal to start the motor
input_pin = Pin(16, Pin.IN)

# Define the pins for the stepper motor for setup
pins_M1 = [Pin(IN1_M1, Pin.OUT), Pin(IN2_M1, Pin.OUT), Pin(IN3_M1, Pin.OUT), Pin(IN4_M1, Pin.OUT)]
pins_M2 = [Pin(IN1_M2, Pin.OUT), Pin(IN2_M2, Pin.OUT), Pin(IN3_M2, Pin.OUT), Pin(IN4_M2, Pin.OUT)]

# Define the sequence for the stepper motor
sequence_clockwise = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
sequence_counter_clockwise = [[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]

# Define the functions to rotate the 1st stepper motor clockwise
def rotate_M1_clockwise():
    for _ in range(130):
        for step in sequence_clockwise:
            for i in range(len(pins_M1)):
                pins_M1[i].value(step[i])
                sleep(0.001)

# Define the functions to rotate the 1st stepper motor counter-clockwise
def rotate_M1_counter_clockwise():
    for _ in range(130):
        for step in sequence_counter_clockwise:
            for i in range(len(pins_M1)):
                pins_M1[i].value(step[i])
                sleep(0.001)

# Define the functions to rotate the 2nd stepper motor clockwise
def rotate_M2_clockwise():
    for _ in range(130):
        for step in sequence_clockwise:
            for i in range(len(pins_M2)):
                pins_M2[i].value(step[i])
                sleep(0.001)

# Define the functions to rotate the 2nd stepper motor counter-clockwise
def rotate_M2_counter_clockwise():
    for _ in range(130):
        for step in sequence_counter_clockwise:
            for i in range(len(pins_M2)):
                pins_M2[i].value(step[i])
                sleep(0.001)
                

# Define the functions to rotate both motors clockwise
def rotate_both_motors_clockwise():
    for _ in range(130):
        for step in sequence_clockwise:
            for i in range(len(pins_M1)):
                pins_M1[i].value(step[i])
                pins_M2[i].value(step[i])
            sleep(0.001)

# Define the functions to rotate both motors counter-clockwise
def rotate_both_motors_counter_clockwise():
    for _ in range(130):
        for step in sequence_counter_clockwise:
            for i in range(len(pins_M1)):
                pins_M1[i].value(step[i])
                pins_M2[i].value(step[i])
            sleep(0.001)


# Define the functions to write the motor state to a file
def write_motor_state_closed():
    with open('motor-state.txt', 'w') as file:
        file.write("closed")
        
def write_motor_state_open():
    with open('motor-state.txt', 'w') as file:
        file.write("open")

# Define the functions to read the motor state from a file        
def read_motor_state():
    with open('motor-state.txt', 'r') as file:
        motor_state = file.read()
    return motor_state

# Define the functions to open the gate
def open_gate():
    rotate_M1_clockwise()
    rotate_M2_counter_clockwise()
    write_motor_state_open()

# Define the functions to close the gate
def close_gate():
    rotate_M2_clockwise()
    rotate_M1_counter_clockwise()
    write_motor_state_closed()
    


# Define a function to start rotation when input signal is received
def start_door(pin):
    open_gate()
    sleep(2)
    close_gate()
    cleanup_motors()
        
# Define a function to cleanup the pins for motor 1
def cleanup_M1():
    for i in pins_M1:
        pin.low()

# Define a function to cleanup the pins for motor 2  
def cleanup_M2():
    for i in pins_M2:
        pin.low()

# Define a function to cleanup the pins for both motors        
def cleanup_motors():
    for pin in pins_M1:
        pin.low()
    for pin in pins_M2:
        pin.low()

# Set up an interrupt on the input pin to call start_rotation function
input_pin.irq(trigger=Pin.IRQ_RISING, handler=start_door)
