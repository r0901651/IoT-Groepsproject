# Script to unlock the door by rotating the motor counterclockwise
import RPi.GPIO as GPIO
import time

# Define GPIO pins connected to the ULN2003AN driver board
IN1 = 17
IN2 = 27
IN3 = 22
IN4 = 26

STEPS_DEG = 48

# Define the sequence of steps for counterclockwise rotation (reversed)
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

def setup_motor():
    GPIO.setmode(GPIO.BCM)  # Use BCM numbering
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)

def set_step_countclock(step):
    GPIO.output(IN1, STEP_SEQUENCE_COUNTCLOCKWISE[step][0])
    GPIO.output(IN2, STEP_SEQUENCE_COUNTCLOCKWISE[step][1])
    GPIO.output(IN3, STEP_SEQUENCE_COUNTCLOCKWISE[step][2])
    GPIO.output(IN4, STEP_SEQUENCE_COUNTCLOCKWISE[step][3])

def write_motor_state():
    with open('motor-state.txt', 'w') as file:
        file.write("unlocked")

def rotate_counterclockwise(degrees):
    write_motor_state()  # Write the motor state to the file
    steps = int(degrees / 30) * STEPS_DEG
    for _ in range(steps):
        for step in range(8):
            set_step_countclock(step)
            time.sleep(0.01)

def cleanup():
    GPIO.cleanup()

if __name__ == '__main__':
    try:
        setup_motor()
        rotate_counterclockwise(30)  # Rotate 30 degrees counterclockwise
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
    finally:
        cleanup()
        