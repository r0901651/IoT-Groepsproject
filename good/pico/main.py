from machine import Pin
from time import sleep


# Define the pin for the internal LED
led_pin = Pin(25, Pin.OUT)

# Toggle the LED state
led_pin.value(not led_pin.value())


IN1_M1 = 2
IN2_M1 = 3
IN3_M1 = 4
IN4_M1 = 5

IN1_M2 = 6
IN2_M2 = 7
IN3_M2 = 8
IN4_M2 = 9

input_pin = Pin(16, Pin.IN)  # Change 10 to the GPIO pin number you're using

#pins_M1 = [IN1_M1, IN2_M1, IN3_M1, IN4_M1]
#pins_M2 = [IN1_M2, IN2_M2, IN3_M2, IN4_M2]

pins_M1 = [Pin(IN1_M1, Pin.OUT), Pin(IN2_M1, Pin.OUT), Pin(IN3_M1, Pin.OUT), Pin(IN4_M1, Pin.OUT)]
pins_M2 = [Pin(IN1_M2, Pin.OUT), Pin(IN2_M2, Pin.OUT), Pin(IN3_M2, Pin.OUT), Pin(IN4_M2, Pin.OUT)]

sequence_clockwise = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
sequence_counter_clockwise = [[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]

def rotate_M1_clockwise():
    for _ in range(130):
        for step in sequence_clockwise:
            for i in range(len(pins_M1)):
                pins_M1[i].value(step[i])
                sleep(0.001)

def rotate_M1_counter_clockwise():
    for _ in range(130):
        for step in sequence_counter_clockwise:
            for i in range(len(pins_M1)):
                pins_M1[i].value(step[i])
                sleep(0.001)

def rotate_M2_clockwise():
    for _ in range(130):
        for step in sequence_clockwise:
            for i in range(len(pins_M2)):
                pins_M2[i].value(step[i])
                sleep(0.001)

def rotate_M2_counter_clockwise():
    for _ in range(130):
        for step in sequence_counter_clockwise:
            for i in range(len(pins_M2)):
                pins_M2[i].value(step[i])
                sleep(0.001)
                


def rotate_both_motors_clockwise():
    for _ in range(130):
        for step in sequence_clockwise:
            for i in range(len(pins_M1)):
                pins_M1[i].value(step[i])
                pins_M2[i].value(step[i])
            sleep(0.001)

def rotate_both_motors_counter_clockwise():
    for _ in range(130):
        for step in sequence_counter_clockwise:
            for i in range(len(pins_M1)):
                pins_M1[i].value(step[i])
                pins_M2[i].value(step[i])
            sleep(0.001)



def write_motor_state_closed():
    with open('motor-state.txt', 'w') as file:
        file.write("closed")
        
def write_motor_state_open():
    with open('motor-state.txt', 'w') as file:
        file.write("open")
        
def read_motor_state():
    with open('motor-state.txt', 'r') as file:
        motor_state = file.read()
    return motor_state


def open_gate():
    rotate_M1_clockwise()
    rotate_M2_clockwise()
    #rotate_both_motors_counter_clockwise()
    write_motor_state_open()
    
def close_gate():
    rotate_M2_counter_clockwise()
    rotate_M1_counter_clockwise()
    #rotate_both_motors_counter_clockwise()
    write_motor_state_closed()
    


# Define a function to start rotation when input signal is received
def start_door(pin):
    #if read_motor_state() == "closed":
    #    open_gate()
    #elif read_motor_state() == "open":
    #    close_gate()
    open_gate()
    sleep(1)
    close_gate()
    cleanup_motors()
        

def cleanup_M1():
    for i in pins_M1:
        pin.low()
        
def cleanup_M2():
    for i in pins_M2:
        pin.low()
        
def cleanup_motors():
    for pin in pins_M1:
        pin.low()
    for pin in pins_M2:
        pin.low()

# Set up an interrupt on the input pin to call start_rotation function
input_pin.irq(trigger=Pin.IRQ_RISING, handler=start_door)
