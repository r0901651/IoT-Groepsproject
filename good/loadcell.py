#!/usr/bin/env python3

# try to import hx711, first from src dir, second from src dir after adding parent to path, last from pip
try:
    from src.hx711_multi import HX711
except:
    try:
        # try after inserting parent folder in path
        import sys
        import pathlib
        from os.path import abspath
        sys.path.insert(0, str(pathlib.Path(abspath(__file__)).parents[1]))
        from src.hx711_multi import HX711
    except:
        from hx711_multi import HX711

from time import perf_counter
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO  # import GPIO
import json
import os

# init GPIO (should be done outside HX711 module in case you are using other GPIO functionality)
GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering

readings_to_average = 10
sck_pin = 17
dout_pins = [27, 22]
weight_multiples = [1861.2, 332.8]

# create hx711 instance
hx711 = HX711(dout_pins=dout_pins,
              sck_pin=sck_pin,
              channel_A_gain=128,
              channel_select='A',
              all_or_nothing=False,
              log_level='CRITICAL')
# reset ADC, zero it
hx711.reset()
try:
    hx711.zero(readings_to_average=readings_to_average*3)
except Exception as e:
    print(e)
# uncomment below loop to see raw 2's complement and read integers
# for adc in hx711._adcs:
#     print(adc.raw_reads)  # these are the 2's complemented values read bitwise from the hx711
#     print(adc.reads)  # these are the raw values after being converted to signed integers


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

hx711.set_weight_multiples(weight_multiples=weight_multiples)

# Assuming the weight of a single item for each load cell
item_weight = [5.7, 5.7]  # Replace with actual weights

# Add a total stock count variable
total_stock_count = [4, 4]  # Replace with actual stock counts


try:
    previous_weights = [0, 0]  # Initialize previous weights for each load cell
    with open('user_badges.json', 'r') as user_file:
        user_data = json.load(user_file)
        user_id = user_data['id']
        user_name = user_data['name']

       # Load existing data or initialize new data
        if os.path.exists('items_taken.json') and os.path.getsize('items_taken.json') > 0:
            with open('items_taken.json', 'r') as f:
                data = json.load(f)
        else:
            data = {
                'id': user_id,
                'name': user_name,
                'items': {
                    'item1': '',
                    'item2': ''
                }
            }

        while True:
            start = perf_counter()

            # perform read operation, returns signed integer values as delta from zero()
            # readings are filtered for bad data and then averaged
            raw_vals = hx711.read_raw(readings_to_average=readings_to_average)

            # request weights using multiples set previously with set_weight_multiples()
            # This function call will not perform a new measurement, it will just use what was acquired during read_raw()
            weights = hx711.get_weight()

            # If a weight is taken, update the JSON file
            if weights != previous_weights:
                # Calculate the number of items taken
                items_taken = [(previous_weights[i] - weights[i]) / item_weight[i] for i in range(len(weights))]
                for i in range(len(items_taken)):
                    # Only append 'item' if an item has been taken
                    if items_taken[i] >= 1:
                        # If the key doesn't exist in the dictionary or isn't a list, initialize it as a list
                        if 'item' + str(i+1) not in data['items'] or not isinstance(data['items']['item' + str(i+1)], list):
                            data['items']['item' + str(i+1)] = []
                        data['items']['item' + str(i+1)].extend(['item'] * int(items_taken[i]))
                        # Decrease the stock count
                        total_stock_count[i] -= int(items_taken[i])
                with open('items_taken.json', 'w') as f:
                    json.dump(data, f)
                previous_weights = weights

            read_duration = perf_counter() - start
            sample_rate = readings_to_average/read_duration
            print('\nread duration: {:.3f} seconds, rate: {:.1f} Hz'.format(read_duration, sample_rate))
            print(
                'raw',
                ['{:.3f}'.format(x) if x is not None else None for x in raw_vals])
            print(' wt',
                ['{:.3f}'.format(x) if x is not None else None for x in weights])
            
            if client.is_connected():
                # Define MQTT_DATA as the total_stock_count variable
                MQTT_DATA = "field2={}&field3={}".format(total_stock_count[0], total_stock_count[1])
                client.publish(topic=MQTT_TOPIC, payload=MQTT_DATA, qos=0, retain=False)
            else:
                print("Client is not connected to ThingSpeak. Attempting to connect.")
                client.reconnect()
except KeyboardInterrupt:
    print('Keyboard interrupt..')
    GPIO.cleanup()
except Exception as e:
    print(e)

# cleanup GPIO
GPIO.cleanup()