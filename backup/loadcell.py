import time
import RPi.GPIO as GPIO
from hx711 import HX711

def clean_and_exit():
    print("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()

GPIO.setmode(GPIO.BOARD)

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


print("Now measuring weights...")
while True:
    try:
        raw_val = hx._read()
        weight = (raw_val - zero_factor) / conversion_factor

        # Round weight to 2 decimal places
        weight = round(weight, 2)

        # Ignore negative weights
        if weight < 0:
            continue

        print(f"Current weight: {weight}g")
        time.sleep(5)  # print the current weight

        # Print current stock every 5 seconds
        print_counter += 1
        if print_counter >= 1:
            print(f"Current stock: {stock_total}")
            print_counter = 0

        # Check if weight is 0g
        if 0 <= weight < 1:
            zero_weight_counter += 1
            if zero_weight_counter >= 1:  # if weight has been 0g for approximately 5 seconds
                print("Item out of stock")
                zero_weight_counter = 0  # reset the counter
        else:
            zero_weight_counter = 0  # reset the counter if weight is not 0g
        # Check if weight has decreased by the weight of one or more stock items
        weight_diff = last_weight - weight
        if weight_diff >= stock_weight * 0.95:
            stocks_taken = round(weight_diff / stock_weight)
            stock_total -= stocks_taken
            # Ensure stock doesn't go below zero
            if stock_total < 0:
                stock_total = 0
            last_weight = weight
            print(f"Weight decreased, {stocks_taken} stocks taken, new stock total: {stock_total}")

        # Check if weight has increased by the weight of one or more stock items
        weight_diff = weight - last_weight
        if weight_diff >= stock_weight * 0.95:
            stocks_added = round(weight_diff / stock_weight)
            stock_total += stocks_added
            last_weight = weight
            print(f"Weight increased, {stocks_added} stocks added, new stock total: {stock_total}")

    except (KeyboardInterrupt, SystemExit):
        clean_and_exit()