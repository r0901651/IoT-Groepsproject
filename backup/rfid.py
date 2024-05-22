from time import sleep
import time
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import sys
from mfrc522 import SimpleMFRC522
from hx711 import HX711
import subprocess
import sys
import threading

reader = SimpleMFRC522()

# Disable GPIO warnings
GPIO.setwarnings(False)

# MQTT settings
MQTT_HOST = "mqtt3.thingspeak.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_API_KEY = "LCXG16XLWFMWEJIZ"
MQTT_TOPIC = "channels/2552598/publish"
MQTT_CLIENT_ID = "IgImOgklMygBFjUzBhsrIjQ"
MQTT_USER = "IgImOgklMygBFjUzBhsrIjQ"
MQTT_PWD = "D4FAEYlpq8bNhcO2iv7Dq91F"

hx = HX711(29, 31)  # DOUT - Pin 29, PD_SCK - Pin 31
hx.reset()

# Hardcoded calibration data
zero_factor = 622413.7
conversion_factor = 2177.733333333337

# Stock management
stock_weight = 6  # weight of one stock item in grams
max_stock = 8  # maximum number of stock items
stock_total = max_stock  # current number of stock items, start at maximum
last_weight = stock_total * stock_weight  # last measured weight
zero_weight_counter = 0  # counter for how many times the weight has been 0g
print_counter = 0  # counter for printing the current stock

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected OK with result code " + str(rc))
    else:
        print("Bad connection with result code " + str(rc))

def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected result code " + str(rc))

def on_message(client, userdata, msg):
    print("Received a message on topic: " + msg.topic + "; message: " + str(msg.payload))

# Set up a MQTT Client
client = mqtt.Client(client_id=MQTT_CLIENT_ID)
client.username_pw_set(MQTT_USER, MQTT_PWD)

# Connect callback handlers to client
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

print("Attempting to connect to %s" % MQTT_HOST)
client.connect(MQTT_HOST, MQTT_PORT)
client.loop_start()  # start the loop

# Create a dictionary to map RFID IDs to user information
user_dict = {
    584187003279: {'name': 'Jorik'},
    584188061878: {'name': 'Filip'},
    584185031812: {'name': 'Anthony'},
    584153111978: {'name': 'Piet piraat'}
}

# Initialize variables
is_enter_scan = True
current_user = None
total_scans = 0
last_published_stock_total = -1
item2_count = 0
item2_taken = False

# Define the interval between MQTT publish operations
interval = 2

# Wait until the client is connected
while not client.is_connected():
    print("Client is not connected to ThingSpeak. Attempting to connect.")
    sleep(interval)  # Add a delay after each attempt

# Create a dictionary to map each user to a list of items they took
user_items = {}

# Define the GPIO pin that the button is connected to
BUTTON_PIN = 15

# Set up the button pin as an input
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def check_button():
    if GPIO.input(BUTTON_PIN) == GPIO.HIGH: 
        sleep(0.01)  # Debounce delay
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH:  # Check again to confirm
            print("Button pressed!")
            return True
    return False


def check_button_thread():
    global item2_taken
    global item2_count
    global current_user
    while True:
        if current_user is not None:
            button_check = check_button()
            if button_check:
                # Check if item 2 has already been taken
                if not item2_taken:
                    print("Button pressed. Running motor.py script.")
                    subprocess.call([sys.executable, 'motor.py'])
                    item2_count += 1
                    item2_taken = True
                    # Add 'item2' to the list of items for the current user
                    user_items[current_user].append('item2')
                    sleep(1)
                else:
                    print("Item 2 has already been taken during this user session.")
        sleep(0.1)  # Add a short delay to prevent high CPU usage

# Start the button check thread
button_thread = threading.Thread(target=check_button_thread)


# Your main loop
try:
    while True:
        try:
            print("Hold a tag near the reader")
            id, _ = reader.read()
            # Look up the user information in the dictionary
            user_info = user_dict.get(id, {'name': 'Unknown'})
            
            if current_user is None:
                button_thread.start()
                print("ID: %s, User: %s entered" % (id, user_info['name']))
                current_user = user_info['name']
                total_scans += 1
                # Initialize the list of items for the user
                user_items[current_user] = []
                # Record the weight when the user enters
                raw_val = hx._read()
                last_weight = (raw_val - zero_factor) / conversion_factor
                last_weight = round(last_weight, 2)
                # Reset the item2_taken flag when a user badges in
                item2_taken = False
                sleep(1)

            elif current_user == user_info['name']:
                sleep(1)
                print("ID: %s, User: %s left" % (id, user_info['name']))
                # Measure the weight when the user leaves
                raw_val = hx._read()
                weight = (raw_val - zero_factor) / conversion_factor
                weight = round(weight, 2)
                # Calculate the number of items the user took or added
                weight_diff = last_weight - weight
                if weight_diff > 0:  # The user took items
                    stocks_taken = round(weight_diff / stock_weight)
                    user_items[current_user].extend(['item'] * stocks_taken)
                    stock_total -= stocks_taken
                    print("Weight decreased, %s stocks taken, new stock total: %s" % (stocks_taken, stock_total))
                elif weight_diff < 0:  # The user added items
                    stocks_added = round(-weight_diff / stock_weight)
                    stock_total += stocks_added
                    print("Weight increased, %s stocks added, new stock total: %s" % (stocks_added, stock_total))
                print("Items taken: ", user_items[current_user])
                current_user = None
            else:
                print("Error: Another user tried to leave before the current user")

        except Exception as e:
            print("An error occurred while reading the RFID: " + str(e))
            client.reconnect()

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Total scans: %s" % total_scans)
    print("Total item 2 taken: %s" % item2_count)
    raise