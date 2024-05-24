# Necessary imports
import json
from time import sleep
import sys
import paho.mqtt.client as mqtt
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
from rpi_lcd import LCD

# setup MQTT
# MQTT settings
MQTT_HOST ="mqtt3.thingspeak.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL =60
MQTT_API_KEY = "LCXG16XLWFMWEJIZ"
MQTT_TOPIC = "channels/2552598/publish"
MQTT_CLIENT_ID = "IgImOgklMygBFjUzBhsrIjQ"
MQTT_USER = "IgImOgklMygBFjUzBhsrIjQ"
MQTT_PWD = "D4FAEYlpq8bNhcO2iv7Dq91F"

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Connected OK with result code "+str(rc))
    else:
        print("Bad connection with result code "+str(rc))

def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected result code "+str(rc))

def on_message(client,userdata,msg):
    print("Received a message on topic: " + msg.topic + "; message: " + msg.payload)

# Set up a MQTT Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, MQTT_CLIENT_ID)
client.username_pw_set(MQTT_USER, MQTT_PWD)

# Connect callback handlers to client
client.on_connect= on_connect
client.on_disconnect= on_disconnect
client.on_message= on_message

print("Attempting to connect to %s" % MQTT_HOST)
client.connect(MQTT_HOST, MQTT_PORT)
client.loop_start() #start the loop

# Suppress GPIO warnings
GPIO.setwarnings(False)

# Initialize the RFID reader
reader = SimpleMFRC522()

# Initialize the LCD screen
lcd = LCD()

# Initialize total_scans variable
total_scans = 0

# Create a dictionary to map RFID IDs to user information
user_dict = {
    584187003279: {'name': 'Jorik Goris'},
    584188061878: {'name': 'Filip Kolb'},
    584185031812: {'name': 'Anthony V.Roy'},
    584153111978: {'name': 'Piet piraat'},
    5412957131: {'name': 'Patrick Dielens'}
}

# Wait until the client is connected
while not client.is_connected():
    print("Client is not connected to ThingSpeak. Attempting to connect.")
    sleep(1)  # Add a delay after each attempt

# Function to update the JSON file with badge data
def update_json_file(data, filename='user_badges.json'):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


try:
    last_scanned_user = None
    while True:
        print("Hold a tag near the reader")
        id, _ = reader.read()
        
        if last_scanned_user is None:
            if id in user_dict:
                user_info = user_dict[id]
                badge_data = {
                    'id': id,
                    'name': user_info['name']
                }
                update_json_file(badge_data)
                welcome_message = "Welcome, " + user_info['name'] + "\n"
                lcd.text(welcome_message, 1)
                print(json.dumps(badge_data))
                last_scanned_user = id
                total_scans += 1  # Increment total_scans
                sleep(1)
                # Do not exit here. Continue running and wait for a leave scan.
            else:
                print(f"Unknown user: {id}")
                sys.exit(1)  # Exit with status code 1 to indicate failure
        else:
            if id == last_scanned_user:
                user_info = user_dict[id]
                leave_message = "Goodbye, " + user_info['name'] + "\n"
                lcd.text(leave_message, 1)
                print(f"{user_info['name']} has left.")
                last_scanned_user = None
                sleep(5)
                sys.exit(0)  # Exit with status code 0 to indicate success
            else:
                print(f"Unknown user: {id}")
                sys.exit(1)  # Exit with status code 1 to indicate failure
                
        # Check if the client is connected before publishing
        if client.is_connected():
            # Define MQTT_DATA as the total_scans variable
            MQTT_DATA = "field1={}".format(total_scans)
            client.publish(topic=MQTT_TOPIC, payload=MQTT_DATA, qos=0, retain=False)
        else:
            print("Client is not connected to ThingSpeak. Attempting to connect.")
            client.reconnect()
        sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()
    raise
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
finally:
    GPIO.cleanup()