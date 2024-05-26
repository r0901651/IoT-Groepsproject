# IoT-Groepsproject

# Pinout Wiring
Below are the pinout wiring details for the RFID-RC522, HX711, and 28BYJ Driver. Ensure that you connect each component to the correct GPIO pins of the Raspberry Pi 4 as specified to avoid any issues.
## RFID-RC522

| Pin   | Color   | Connection (Pi) |
|-------|---------|-----------------|
| VCC   | Red     | 3.3V            |
| GND   | Blue    | GND             |
| MISO  | Black   | GPIO9           |
| MOSI  | White   | GPIO10          |
| SCK   | Yellow  | GPIO11          |
| SDA   | Green   | GPIO8           |

## HX711

| Pin   | Color   | Connection (Pi) |
|-------|---------|-----------------|
| VCC   | Red     | 3.3V            |
| GND   | Blue    | GND             |
| DT    | Black   | GPIO5           |
| SCK   | White   | GPIO6           |

## 28BYJ Driver

| Pin    | Color  | Connection (Pi) |
|--------|--------|-----------------|
| 5-12V+ | Red    | 5V              |
| 5-12V- | Blue   | GND             |
| IN1    | Yellow | GPIO17          |
| IN2    | Green  | GPIO27          |
| IN3    | Purple | GPIO22          |
| IN4    | Black  | GPIO26          |

## Schematic
Devices are separately wired to the breadboard in the schematic for better overview.
<br>
Wiring for your load cell to the HX711 can be different from the schematic !

![IoT_groepsproject_bb_v1 3](https://github.com/r0901651/IoT-Groepsproject/assets/95848828/afbc68e9-d85f-46e8-b44f-228d583730e6)


