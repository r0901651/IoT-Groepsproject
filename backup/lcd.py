import spidev
import RPi.GPIO as GPIO
import time

# Define GPIO pins
RST = 20
DC = 21
SPI_PORT = 0
SPI_DEVICE = 0

# Initialize SPI and GPIO
spi = spidev.SpiDev()
spi.open(SPI_PORT, SPI_DEVICE)
GPIO.setmode(GPIO.BCM)
GPIO.setup(RST, GPIO.OUT)
GPIO.setup(DC, GPIO.OUT)

# Reset the LCD
GPIO.output(RST, GPIO.LOW)
time.sleep(0.1)
GPIO.output(RST, GPIO.HIGH)

# Send a command to the LCD
def send_command(command):
    GPIO.output(DC, GPIO.LOW)
    spi.xfer([command])

# Send data to the LCD
def send_data(data):
    GPIO.output(DC, GPIO.HIGH)
    spi.xfer([data])

# Initialize the LCD
def init_lcd():
    send_command(0x21)  # Extended command mode
    send_command(0xB8)  # Set Vop
    send_command(0x04)  # Set Temp coefficent
    send_command(0x14)  # LCD bias mode 1:48
    send_command(0x20)  # Standard command mode
    send_command(0x0C)  # Normal mode

# Clear the LCD
def clear_lcd():
    for i in range(6):
        send_command(0x80 | i)  # Set Y address
        send_command(0x80)  # Set X address
        for j in range(84):
            send_data(0x00)

# Write a character to the LCD
def write_char(char):
    for i in range(5):
        send_data(char[i])
    send_data(0x00)

# ASCII to LCD character mapping
CHAR_MAP = {
    'H': [0x7C, 0x12, 0x12, 0x12, 0x7C],
    'E': [0x7E, 0x4A, 0x4A, 0x4A, 0x3A],
    'L': [0x7E, 0x40, 0x40, 0x40, 0x40],
    'O': [0x3C, 0x42, 0x42, 0x42, 0x3C],
}

# Write a word to the LCD
def write_word(word):
    for char in word:
        write_char(CHAR_MAP[char])

# Initialize and clear the LCD
init_lcd()
clear_lcd()

# Write "HELLO" to the LCD
write_word('HELLO')

# Cleanup GPIO
GPIO.cleanup()