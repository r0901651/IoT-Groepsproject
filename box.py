# Script to lock the door by rotating the motor clockwise
import RPi.GPIO as GPIO
import time

# Define GPIO pins connected to the ULN2003AN driver board
IN1 = 5
IN2 = 6
IN3 = 13
IN4 = 19

STEPS_DEG = 48

# Define the sequence of steps for rotations clockwise
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

# Define the sequence of steps for rotations counter clockwise
STEP_SEQUENCE_COUNTCLOCKWISE = [
    [0, 0, 0, 1],
    [0, 0, 1, 1],
    [0, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 0],
    [1, 1, 0, 0],
    [1, 0, 0, 0],
    [1, 0, 0, 1]
]

# function for setup of motor pins
def setup_motor():
    GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)

# function to set the steps clockwise
def set_step_clock(step):
    GPIO.output(IN1, STEP_SEQUENCE_CLOCKWISE[step][0])
    GPIO.output(IN2, STEP_SEQUENCE_CLOCKWISE[step][1])
    GPIO.output(IN3, STEP_SEQUENCE_CLOCKWISE[step][2])
    GPIO.output(IN4, STEP_SEQUENCE_CLOCKWISE[step][3])

# function to set the steps counter clockwise
def set_step_countclock(step):
    GPIO.output(IN1, STEP_SEQUENCE_COUNTCLOCKWISE[step][0])
    GPIO.output(IN2, STEP_SEQUENCE_COUNTCLOCKWISE[step][1])
    GPIO.output(IN3, STEP_SEQUENCE_COUNTCLOCKWISE[step][2])
    GPIO.output(IN4, STEP_SEQUENCE_COUNTCLOCKWISE[step][3])

# function to write locked state to state file
def write_motor_state_lock():
    with open('motor-state.txt', 'w') as file:
        file.write("locked")

# function to write unlocked state to state file
def write_motor_state_unlock():
    with open('motor-state.txt', 'w') as file:
        file.write("unlocked")

# function to read state file
def read_motor_state():
    with open('motor-state.txt', 'r') as file:
        motor_state = file.read()
    return motor_state

# function to turn motor clockwise
def rotate_clockwise(degrees):
    write_motor_state_lock()  # Write the motor state to the file
    steps = int(degrees / 30) * STEPS_DEG
    for _ in range(steps):
        for step in range(8):
            set_step_clock(step)
            time.sleep(0.01)

# function to turn motor counter clockwise
def rotate_counterclockwise(degrees):
    write_motor_state_unlock()  # Write the motor state to the file
    steps = int(degrees / 30) * STEPS_DEG
    for _ in range(steps):
        for step in range(8):
            set_step_countclock(step)
            time.sleep(0.01)

# function for GPIO cleanup
def cleanup():
    try:
        GPIO.cleanup()
    except RuntimeWarning as e:
        print("Warning:", e)

# main loop
if __name__ == '__main__':
    try:
        
        if read_motor_state() == "locked":
            setup_motor()
            rotate_counterclockwise(30)

        elif read_motor_state() == "unlocked":
            setup_motor()
            rotate_clockwise(30)

    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
    finally:
        cleanup()