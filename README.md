# IoT-Groepsproject

# Pinout Wiring
Below are the pinout wiring details for the RFID-RC522, HX711, and 28BYJ Driver. Ensure that you connect each component to the correct GPIO pins of the Raspberry Pi 4 as specified to avoid any issues.
## RFID-RC522

| Pin   | Color   | Connection (Pi) |
|-------|---------|-----------------|
| VCC   | Red     | 3.3V            |
| RST   | Orange  | GPIO16          |
| GND   | Blue    | GND             |
| MISO  | Black   | GPIO9           |
| MOSI  | White   | GPIO10          |
| SCK   | Yellow  | GPIO11          |
| SDA   | Green   | GPIO8           |

## HX711 (1)

| Pin   | Color   | Connection (Pi) |
|-------|---------|-----------------|
| VCC   | Red     | 3.3V            |
| GND   | Blue    | GND             |
| DT    | Black   | GPIO27          |
| SCK   | White   | GPIO17          |

## HX711 (2)

| Pin   | Color   | Connection (Pi) |
|-------|---------|-----------------|
| VCC   | Red     | 3.3V            |
| GND   | Blue    | GND             |
| DT    | Black   | GPIO22          |
| SCK   | White   | GPIO17          |

## 28BYJ Driver (box)

| Pin    | Color  | Connection (Pi) |
|--------|--------|-----------------|
| 5-12V+ | Red    | 5V              |
| 5-12V- | Blue   | GND             |
| IN1    | Yellow | GPIO5           |
| IN2    | Green  | GPIO6           |
| IN3    | Purple | GPIO13          |
| IN4    | Black  | GPIO19          |

## Green LED (box)
LED's are wired with a 220Ω resistor.
| Pin    | Color  | Connection (Pi) |
|--------|--------|-----------------|
|   +    | Green  |     GPIO23      |

## Red LED (box)
LED's are wired with a 220Ω resistor.
| Pin    | Color  | Connection (Pi) |
|--------|--------|-----------------|
|   +    |  Red   |     GPIO24      |

## HC-SR04 (box)
The HC-SR04 needs a voltage divider between the Echo pin the GPIO input of your raspberry pi and the GND following one 1KΩ resistor and a 2KΩ resistor.
| Pin   | Color   | Connection (Pi) |
|-------|---------|-----------------|
| VCC   | Red     | 5V              |
| GND   | Blue    | GND             |
| TRIQ  | Green   | GPIO20          |
| ECHO  | Black   | GPIO21          |



## Schematic
Devices are separately wired to the breadboard in the schematic for better overview.
<br>
Wiring for your load cell to the HX711 can be different from the schematic !

![IoT_groepsproject_bb_v1 3](https://github.com/r0901651/IoT-Groepsproject/assets/95848828/afbc68e9-d85f-46e8-b44f-228d583730e6)


