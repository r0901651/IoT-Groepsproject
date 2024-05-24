import time
from smbus2 import SMBus
from bmp280 import BMP280
import paho.mqtt.client as mqtt

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


try:
    bus = SMBus(1)  # 1 indicates /dev/i2c-1
    bmp280 = BMP280(i2c_dev=bus, i2c_addr=0x77)
except:
    print("Error initializing BMP280 sensor")
    exit(1)  # Exit the program if the sensor cannot be initialized

while True:
    temperature = round(bmp280.get_temperature(), 2)
    pressure = round(bmp280.get_pressure(), 2)
    print(f"Temperature: {temperature} C, Pressure: {pressure} hPa")
    time.sleep(5)
    if client.is_connected():
        # Define MQTT_DATA as the total_stock_count variable
        MQTT_DATA = "field4={}&field5={}".format(temperature, pressure)
        client.publish(topic=MQTT_TOPIC, payload=MQTT_DATA, qos=0, retain=False)
    else:
        print("Client is not connected to ThingSpeak. Attempting to connect.")
        client.reconnect()

GPIO.cleanup()