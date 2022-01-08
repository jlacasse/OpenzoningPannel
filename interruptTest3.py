# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
#
# SPDX-License-Identifier: MIT

from time import sleep

import board
import busio
from digitalio import Direction, Pull
from RPi import GPIO
from adafruit_mcp230xx.mcp23017 import MCP23017

# Initialize the I2C bus:
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize the MCP23017 chip on the bonnet
mcp1 = MCP23017(i2c, address=0x20)
mcp2 = MCP23017(i2c, address=0x21)
mcp3 = MCP23017(i2c, address=0x22)

# Optionally change the address of the device if you set any of the A0, A1, A2
# pins.  Specify the new address with a keyword parameter:
# mcp = MCP23017(i2c, address=0x21)  # MCP23017 w/ A0 set

# Make a list of all the pins (a.k.a 0-16)
pinsMcp1 = []
for pin in range(0, 16):
    pinsMcp1.append(mcp1.get_pin(pin))
pinsMcp2 = []
for pin in range(0, 16):
    pinsMcp2.append(mcp1.get_pin(pin))

# Set all the pins to input
for pin in pinsMcp1:
    pin.direction = Direction.INPUT
    pin.pull = Pull.UP
for pin in pinsMcp2:
    pin.direction = Direction.INPUT
    pin.pull = Pull.UP

# Set up to check all the port B pins (pins 8-15) w/interrupts!
mcp1.interrupt_enable = 0xFFFF  # Enable Interrupts in all mcp1 pins
mcp2.interrupt_enable = 0xFFFF  # Enable Interrupts in all mcp2 pins 
# If intcon is set to 0's we will get interrupts on
# both button presses and button releases
mcp1.interrupt_configuration = 0x0000  # interrupt on any change
mcp2.interrupt_configuration = 0x0000  # interrupt on any change
mcp1.io_control = 0x44  # Interrupt as open drain and mirrored
mcp2.io_control = 0x44  # Interrupt as open drain and mirrored
mcp1.clear_ints()  # Interrupts need to be cleared initially
mcp2.clear_ints()  # Interrupts need to be cleared initially
# Or, we can ask to be notified CONTINUOUSLY if a pin goes LOW (button press)
# we won't get an IRQ pulse when the pin is HIGH!
# mcp.interrupt_configuration = 0xFFFF         # notify pin value
# mcp.default_value = 0xFFFF         # default value is 'high' so notify whenever 'low'


def print_interruptMcp1(port):
    """Callback function to be called when an Interrupt occurs."""
    for pin_flag in mcp1.int_flag:
        print("Interrupt connected to mcp1 Pin: {}".format(port))
        print("Pin number: {} changed to: {}".format(pin_flag, pinsMcp1[pin_flag].value))
    mcp1.clear_ints()

def print_interruptMcp2(port):
    """Callback function to be called when an Interrupt occurs."""
    for pin_flag in mcp2.int_flag:
        print("Interrupt connected to mcp2 Pin: {}".format(port))
        print("Pin number: {} changed to: {}".format(pin_flag, pinsMcp2[pin_flag].value))
    mcp2.clear_ints()


# connect either interrupt pin to the Raspberry pi's pin 17.
# They were previously configured as mirrored.
GPIO.setmode(GPIO.BCM)
interruptMcp1 = 18
GPIO.setup(interruptMcp1, GPIO.IN, GPIO.PUD_UP)  # Set up Pi's pin as input, pull up
interruptMcp2 = 17
GPIO.setup(interruptMcp2, GPIO.IN, GPIO.PUD_UP)  # Set up Pi's pin as input, pull up

# The add_event_detect fuction will call our print_interrupt callback function
# every time an interrupt gets triggered.
GPIO.add_event_detect(interruptMcp1, GPIO.FALLING, callback=print_interruptMcp1, bouncetime=20)
GPIO.add_event_detect(interruptMcp2, GPIO.FALLING, callback=print_interruptMcp2, bouncetime=20)
# The following lines are so the program runs for at least 60 seconds,
# during that time it will detect any pin interrupt and print out the pin number
# that changed state and its current state.
# The program can be terminated using Ctrl+C. It doesn't matter how it
# terminates it will always run GPIO.cleanup().
try:
    print("When button is pressed you'll see a message")
    while(True):
      sleep(5)
      mcp1.clear_ints()  # Interrupts need to be cleared initially
      mcp2.clear_ints()  # Interrupts need to be cleared initially
finally:
    GPIO.cleanup()
