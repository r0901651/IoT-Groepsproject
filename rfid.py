from time import sleep
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import sys
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

# disable GPIO warnings
GPIO.setwarnings(False)

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

# Create a dictionary to map RFID IDs to user information
user_dict = {
    584187003279: {'name': 'Jorik'},
    584188061878: {'name': 'Filip'},
    584185031812: {'name': 'Anthony'}
}

# Initialize variables
is_enter_scan = True
current_user = None
total_scans = 0

# Define the interval between MQTT publish operations
interval = 5

# Wait until the client is connected
while not client.is_connected():
    print("Client is not connected to ThingSpeak. Attempting to connect.")
    sleep(interval)  # Add a delay after each attempt

# Main loop
try:
    while True:
        try:
            print("Hold a tag near the reader")
            id, _ = reader.read()
            # Look up the user information in the dictionary
            user_info = user_dict.get(id, {'name': 'Unknown'})
            
            if current_user is None:
                print("ID: %s, User: %s entered" % (id, user_info['name']))
                current_user = user_info['name']
                total_scans += 1
            elif current_user == user_info['name']:
                print("ID: %s, User: %s left" % (id, user_info['name']))
                current_user = None
            else:
                print("Error: Another user tried to leave before the current user")

            # Check if the client is connected before publishing
            if client.is_connected():
                # Define MQTT_DATA as the total_scans variable
                MQTT_DATA = "field1={}".format(total_scans)
                client.publish(topic=MQTT_TOPIC, payload=MQTT_DATA, qos=0, retain=False)
            else:
                print("Client is not connected to ThingSpeak. Attempting to connect.")
                client.reconnect()
            sleep(3)
        except Exception as e:
            print("An error occurred while reading the RFID: " + str(e))
            client.reconnect()

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Total scans: %s" % total_scans)
    raise
