#!/usr/bin/env python3

# try to import hx711, first from src dir, second from src dir after adding parent to path, last from pip
try:
    from src.hx711_multi import HX711
except:
    try:

        import sys
        import pathlib
        from os.path import abspath
        sys.path.insert(0, str(pathlib.Path(abspath(__file__)).parents[1]))
        from src.hx711_multi import HX711
    except:
        from hx711_multi import HX711

from time import perf_counter
import RPi.GPIO as GPIO
import json
import os
import threading
import subprocess
import time

# setup MQTT
# MQTT settings
MQTT_HOST ="mqtt3.thingspeak.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL =60
MQTT_API_KEY = yourapikey
MQTT_TOPIC = yourpublishchannel
MQTT_CLIENT_ID = clientid
MQTT_USER = userstring
MQTT_PWD = password


# set GPIO pin mode to BCM numbering
GPIO.setmode(GPIO.BCM)

# Define button pin
BUTTON_PIN = 26

# Define LED pins
LED_PIN_1 = 23
LED_PIN_2 = 24 

# hc-sr04 ultrasonic sensor initial start value
distance = 0.00

# Setup the GPIO for led's
GPIO.setup(LED_PIN_1, GPIO.OUT)
GPIO.setup(LED_PIN_2, GPIO.OUT)

# Initialize PWM on the LEDs at 1000Hz
pwm_led_1 = GPIO.PWM(LED_PIN_1, 1000)
pwm_led_2 = GPIO.PWM(LED_PIN_2, 1000)

pwm_led_1.start(0)
pwm_led_2.start(0)

# Set up the button pin as input with pull-up resistor
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define function for breathing effect for led's with PWM
def breathe_led(pwm_led, duration):
    # Breathing effect
    end_time = time.time() + duration
    while time.time() < end_time:
        for i in range(0, 101):  # Fade in
            pwm_led.ChangeDutyCycle(i)
            time.sleep(0.01)
        for i in range(100, -1, -1):  # Fade out
            pwm_led.ChangeDutyCycle(i)
            time.sleep(0.01)

# Define function to turn on LED to 100%
def turn_on_led(pwm_led):
    pwm_led.ChangeDutyCycle(100)

# Define function to turn off LED (0%)
def turn_off_led(pwm_led):
    pwm_led.ChangeDutyCycle(0)

# Define function to measure distance via the HC-SR04
def measure_distance():
    # Global variable that can be called outside of thread
    global distance
    # Define hc-sr04 ultrasonic sensor pins
    PIN_TRIGGER = 20
    PIN_ECHO = 21
    # Setup pins
    GPIO.setup(PIN_TRIGGER, GPIO.OUT)
    GPIO.setup(PIN_ECHO, GPIO.IN)

    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    time.sleep(0.5)

    GPIO.output(PIN_TRIGGER, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    pulse_start_time = time.time()
    while GPIO.input(PIN_ECHO) == 0:
        pulse_start_time = time.time()

    while GPIO.input(PIN_ECHO) == 1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    time.sleep(3)
    distance = round(pulse_duration * 17150, 2)

# Define thread for measuring distance
def measure_distance_threaded():
    while True:
        measure_distance()
        time.sleep(1)

# Define function to check for button presses
def check_button():
    global button_state
    while True:
        button_state = GPIO.input(BUTTON_PIN)
        time.sleep(0.1)

# Define function to read current motor satte from file
def read_motor_state():
    # open motor state file
    with open('motor-state.txt', 'r') as file:
        # Read contents and save them in a variable
        motor_state = file.read()
    return motor_state

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
box_stock_count = 1

try:
    # Create button thread 
    button_thread = threading.Thread(target=check_button)
    button_thread.daemon = True
    #Start button thread
    button_thread.start()

    # Create distance measure thread 
    thread_measure_distance = threading.Thread(target=measure_distance_threaded)
    thread_measure_distance.daemon = True
    #Start distance measure thread
    thread_measure_distance.start()
    
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
                    'item2': '',
                    'item3': ''
                }
            }

        while True:
            # Save current motor state in variable
            motor_state = read_motor_state()
            # Check if current motor state is unlocked if so turn on Green LED and turn off Red LED
            if motor_state == "unlocked":
                turn_on_led(pwm_led_1)
                turn_off_led(pwm_led_2)
            # Check if current motor state is locked if so turn on Red LED and turn off Green LED
            elif motor_state == "locked":
                turn_on_led(pwm_led_2)
                turn_off_led(pwm_led_1)
            else:
                # Handle unknown status
                pass

            # Check if motor state is unlocked and if distance from HC-SR04 is higher then 60cm
            if read_motor_state() == "unlocked" and distance > 60:
                    # Define thread to create breathing effect via PWM for the Green LED
                    thread = threading.Thread(target=breathe_led, args=(pwm_led_1, 4))
                    # Start the thread
                    thread.start()
                    # Run the script to lock/unlock the box, in this case lock
                    subprocess.run(["python3", "box.py"])
                    # after subprocess is complete turn on Red LED
                    turn_on_led(pwm_led_2)
                    # Finish thread
                    thread.join()

            # Button is pressed
            if button_state == GPIO.LOW:
                # Check if motor state is locked during button press
                if read_motor_state() == "locked":
                    # Define thread to create breathing effect via PWM for the Red LED
                    thread = threading.Thread(target=breathe_led, args=(pwm_led_2, 4))
                    # Start the thread
                    thread.start()
                    # Run the script to lock/unlock the box, in this case unlock
                    subprocess.run(["python3", "box.py"])
                    # after subprocess is complete turn on Green LED
                    turn_on_led(pwm_led_1)
                    # Finish thread
                    thread.join()
                    # Remove item from box from stock
                    box_stock_count -= 1

                    # Read json file and save data in variable
                    with open('items_taken.json', 'r+') as f:
                        data = json.load(f)
                        # If item3 is not in the list create item3 in the json lis/array
                        if 'item3' not in data['items'] or not isinstance(data['items']['item3'], list):
                            data['items']['item3'] = []
                        # add item to items_taken json
                        data['items']['item3'].append('item')
                        f.seek(0)  # Move the cursor to the beginning of the file
                        # Dump data in the file
                        json.dump(data, f, indent=4)
                        f.truncate()  # Remove any remaining part of the file

                # Check if motor state is unlocked during button press        
                elif read_motor_state() == "unlocked":
                    # Create thread to breathe green LED with PWM
                    thread = threading.Thread(target=breathe_led, args=(pwm_led_1, 4))
                    # start the thread
                    thread.start()
                    # Run the script to lock/unlock the box, in this case lock
                    subprocess.run(["python3", "box.py"])
                    # after subprocess is complete turn on Red LED
                    turn_on_led(pwm_led_2)
                    # finish thread
                    thread.join()
                time.sleep(0.5)  # Debounce delay


            # Start a performance counter to measure the time taken for the operation
            start = perf_counter()

            # Perform a read operation on the HX711 load cell, which returns signed integer values as delta from zero
            # The readings are filtered for bad data and then averaged
            raw_vals = hx711.read_raw(readings_to_average=readings_to_average)

            # Request weights using multiples set previously with set_weight_multiples()
            # This function call will not perform a new measurement, it will just use what was acquired during read_raw()
            weights = hx711.get_weight()

            # If a weight is taken, update the JSON file
            if weights != previous_weights:
                # Calculate the number of items taken by subtracting the current weight from the previous weight and dividing by the weight of a single item
                items_taken = [(previous_weights[i] - weights[i]) / item_weight[i] for i in range(len(weights))]
                for i in range(len(items_taken)):
                    # Only append 'item' if an item has been taken
                    if items_taken[i] >= 1:
                        # If the key doesn't exist in the dictionary or isn't a list, initialize it as a list
                        if 'item' + str(i+1) not in data['items'] or not isinstance(data['items']['item' + str(i+1)], list):
                            data['items']['item' + str(i+1)] = []
                        # Add the taken items to the list
                        data['items']['item' + str(i+1)].extend(['item'] * int(items_taken[i]))
                        # Decrease the stock count by the number of items taken
                        total_stock_count[i] -= int(items_taken[i])
                # Open the JSON file and dump the updated data into it
                with open('items_taken.json', 'w') as f:
                    json.dump(data, f)
                # Update the previous_weights with the current weights for the next iteration
                previous_weights = weights

            # Calculate the duration of the read operation
            read_duration = perf_counter() - start
            # Calculate the sample rate as the number of readings divided by the duration
            sample_rate = readings_to_average/read_duration
            # Print the duration and sample rate
            print('\nread duration: {:.3f} seconds, rate: {:.1f} Hz'.format(read_duration, sample_rate))
            # Print the raw values
            print('raw', ['{:.3f}'.format(x) if x is not None else None for x in raw_vals])
            # Print the weights
            print(' wt', ['{:.3f}'.format(x) if x is not None else None for x in weights])
            
            if client.is_connected():
                # Define MQTT_DATA as the total_stock_count variable
                MQTT_DATA = "field2={}&field3={}&field4={}".format(total_stock_count[0], total_stock_count[1], box_stock_count)
                client.publish(topic=MQTT_TOPIC, payload=MQTT_DATA, qos=0, retain=False)
            else:
                print("Client is not connected to ThingSpeak. Attempting to connect.")
                client.reconnect()


# Handle KeyboardInterrupt exception
except KeyboardInterrupt:
    print('Keyboard interrupt..')
# Handle any other exception
except Exception as e:
    print(e)
# Cleanup the GPIO pins regardless of whether an exception was raised or not
finally:
    GPIO.cleanup()
