# IoT-Groepsproject

# Material Requirements
| item              | amount  |
|-------------------|---------|
| HX711             | 2       |
| 28BYJ             | 3       |
| 28BYJ Driver      | 3       |
| Raspberry pi 4B   | 1       |
| Rapsberry pi pico | 1       |
| BMP280            | 1       |
| Load cell         | 2       | 
| HC-SR04           | 1       |
| rfid rc522        | 1       |
| 1602 LCD Display  | 1       |
| lcm1602 iic       | 1       | 
| Resistor 220Ω     | 3       |
| Resistor 1KΩ      | 1       |
| Resistor 2KΩ      | 1       |
| Button            | 1       | 
<br>
Below you can find the stl files for the box used in the project.
<br>
[parts.zip](https://github.com/r0901651/IoT-Groepsproject/files/15448882/parts.zip)
<br>
Here is also an example of the setup used for the load cells.
![HX711_and_Combinator_board_hook_up_guide-02](https://github.com/r0901651/IoT-Groepsproject/assets/95848828/a591f61a-ee84-4797-bbca-6e24665b139d)
<br>

# Pinout Wiring
Below are the pinout wiring details for the RFID-RC522, HX711 1 and 2, the 28BYJ Driver for the main box, the box status LED's, the HC-SR04 for the box, the BMP-280, the LCM 1602 IIC LCD screen for the gate, the two 28BYJ Drivers for the gates and the raspberry pi pico.
<br>
Ensure that you connect each component to the correct GPIO pins of the Raspberry Pi 4 and pico as specified to avoid any issues.
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
> [!NOTE]
> LED's are wired with a 220Ω resistor.

| Pin    | Color  | Connection (Pi) |
|--------|--------|-----------------|
|   +    | Green  |     GPIO23      |
|   -    | Blue   |     GND         |

## Red LED (box)
> [!NOTE]
> LED's are wired with a 220Ω resistor.

| Pin    | Color  | Connection (Pi) |
|--------|--------|-----------------|
|   +    |  Red   |     GPIO24      |
|   -    | Blue   |     GND         |

## HC-SR04 (box)
> [!WARNING]
> The HC-SR04 needs a voltage divider between the Echo pin the GPIO input of your raspberry pi and the GND following one 1KΩ resistor > and a 2KΩ resistor. (see schematic for more details)

| Pin   | Color   | Connection (Pi) |
|-------|---------|-----------------|
| VCC   | Red     | 5V              |
| GND   | Blue    | GND             |
| TRIQ  | Green   | GPIO20          |
| ECHO  | Black   | GPIO21          |

## BMP-280

| Pin   | Color   | Connection (Pi) |
|-------|---------|-----------------|
| VCC   | Red     | 5V              |
| GND   | Blue    | GND             |
| SDI   | Yellow  | GPIO02          |
| SCK   | Green   | GPIO03          |

## LCM 1602 IIC
LCM 1602 IIC I2C backpack (LCD screen)
| Pin   | Color   | Connection (Pi) |
|-------|---------|-----------------|
| VCC   | Red     | 5V              |
| GND   | Blue    | GND             |
| SDA   | Yellow  | GPIO02          |
| SCL   | Green   | GPIO03          |

## Raspberry pi pico
> [!WARNING]
> Make sure the Pico and the main Pi have a common ground!

| Pin   | Color   | Connection (Pi) |
|-------|---------|-----------------|
| GND   | Blue    | GND             |
| GPIO16| White   | GPIO25          |

## 28BYJ Driver 1 (gate)

| Pin    | Color  | Connection (Pico) |
|--------|--------|-------------------|
| 5-12V+ | Red    |                   |
| 5-12V- | Blue   |                   |
| IN1    | Purple | GPIO2             |
| IN2    | Yellow | GPIO3             |
| IN3    | Green  | GPIO4             |
| IN4    | Orange | GPIO5             |

## 28BYJ Driver 2 (gate)

| Pin    | Color  | Connection (Pico) |
|--------|--------|-------------------|
| 5-12V+ | Red    |                   |
| 5-12V- | Blue   |                   |
| IN1    | Purple | GPIO6             |
| IN2    | Yellow | GPIO7             |
| IN3    | Green  | GPIO8             |
| IN4    | Orange | GPIO9             |


## Schematic
Devices are separately wired to the breadboard in the schematic for better overview.
<br>
Wiring for your load cell to the HX711 can be different from the schematic !


![IoT_groepsproject_bb_v1 3](https://github.com/r0901651/IoT-Groepsproject/assets/95848828/405d3f1e-a4b0-4aaa-96b9-c160b5dc527c)

