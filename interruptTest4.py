# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
#https://circuitpython.readthedocs.io/projects/mcp230xx/en/latest/api.html#mcp23017
# SPDX-License-Identifier: MIT

from time import sleep

import board
import busio
import smbus
import time
from digitalio import Direction, Pull
from RPi import GPIO
from adafruit_mcp230xx.mcp23017 import MCP23017
from datetime import datetime





# Initialize the I2C bus:
i2c = busio.I2C(board.SCL, board.SDA)
bus = smbus.SMBus(1)

# Initialize the MCP23017 chip on the bonnet
print("init mcp address")
mcp1 = MCP23017(i2c, address=0x20)
mcp2 = MCP23017(i2c, address=0x21)
mcp3 = MCP23017(i2c, address=0x22)

# address_map = {
#     0x00: 'IODIRA',   0x01: 'IODIRB',   0x02: 'IPOLA',   0x03: 'IPOLB',
#     0x04: 'GPINTENA', 0x05: 'GPINTENB', 0x06: 'DEFVALA', 0x07: 'DEVFALB',
#     0x08: 'INTCONA',  0x09: 'INTCONB',  0x0a: 'IOCON',   0x0b: 'IOCON',
#     0x0c: 'GPPUA',    0x0d: 'GPPUB',    0x0e: 'INTFA',   0x0f: 'INTFB',
#     0x10: 'INTCAPA',  0x11: 'INTCAPB',  0x12: 'GPIOA',   0x13: 'GPIOB',
#     0x14: 'OLATA',    0x15: 'OLATB'
# }
address_map = {
    0x0e: 'INTFA',   0x0f: 'INTFB', 0x10: 'INTCAPA',  0x11: 'INTCAPB',  0x12: 'GPIOA',   0x13: 'GPIOB'
}
register_map = {value: key for key, value in address_map.items()}
max_len = max(len(key) for key in register_map)

def print_values(bus):
    print ("-" * 20)
    for addr in address_map:
        value = bus.read_byte_data(0x21, addr)
        print ("%-*s = 0x%02X" % (max_len, address_map[addr], value))

# Optionally change the address of the device if you set any of the A0, A1, A2
# pins.  Specify the new address with a keyword parameter:
# mcp = MCP23017(i2c, address=0x21)  # MCP23017 w/ A0 set

# Make a list of all the pins (a.k.a 0-16)
pinsMcp1 = []
for pin in range(0, 16):
    pinsMcp1.append(mcp1.get_pin(pin))
    print("mcp1 Pin: {}".format(pin))
pinsMcp2 = []
for pin in range(0, 16):
    pinsMcp2.append(mcp2.get_pin(pin))
    print("mcp2 Pin: {}".format(pin))
pinsMcp3 = []
for pin in range(0, 16):
    pinsMcp3.append(mcp3.get_pin(pin))
    print("mcp3 Pin: {}".format(pin))

# Set all the pins to input
for pin in pinsMcp1:
    pin.direction = Direction.INPUT
    pin.pull = Pull.UP
    print("mcp1 Pin {} config: direction: {} Pull: {}".format(pin, pin.direction, pin.pull)) 
for pin in pinsMcp2:
    pin.direction = Direction.INPUT
    pin.pull = Pull.UP
    print("mcp1 Pin {} config: direction: {} Pull: {}".format(pin, pin.direction, pin.pull))
# Set all the pins to output
for pin in pinsMcp3:
    pin.direction = Direction.OUTPUT
    print("mcp1 Pin {} config: direction: {}".format(pin, pin.direction))
       
# Set up to check all the port B pins (pins 8-15) w/interrupts!
mcp1.interrupt_enable = 0xFFFF  # Enable Interrupts in all mcp1 pins
mcp2.interrupt_enable = 0xFFFF  # Enable Interrupts in all mcp2 pins 
# If intcon is set to 0's we will get interrupts on
# both button presses and button releases
mcp1.interrupt_configuration = 0x0000  # interrupt on any change
mcp2.interrupt_configuration = 0x0000  # interrupt on any change
mcp1.io_control = 0b01100000 #0x44  # Interrupt as open drain and mirrored
mcp2.io_control = 0b01100000 #0x44  # Interrupt as open drain and mirrored
mcp1.clear_ints()  # Interrupts need to be cleared initially
mcp2.clear_ints()  # Interrupts need to be cleared initially
# Or, we can ask to be notified CONTINUOUSLY if a pin goes LOW (button press)
# we won't get an IRQ pulse when the pin is HIGH!
# mcp.interrupt_configuration = 0xFFFF         # notify pin value
# mcp.default_value = 0xFFFF         # default value is 'high' so notify whenever 'low'


def print_interrupt(port):
#    GPIO.remove_event_detect(port)
    #"""Callback function to be called when an Interrupt occurs."""
  for pin_flag in mcp1.int_flag:
        #print("mcp1:")
        #print_values(bus)
        #mcp1.interrupt_enable = 0x0000  # Enable Interrupts in all mcp1 pins 
        #print("Interrupt on mcp1 disabled")
        #print("Interrupt connected to mcp1 Pin: {}".format(port))
      print("Pin number: {} changed to: {}".format(pin_flag, pinsMcp1[pin_flag].value))
      print_values(bus)
      now = datetime.now()
      current_time = now.strftime("%H:%M:%S")
      print("Current Time =", current_time)
        #mcp1.interrupt_enable = 0xFFFF  # Enable Interrupts in all mcp1 pins
        #print("Interrupt on mcp1 enabled")
        #mcp1.clear_ints()
        #print("Interrupt on mcp1 cleared")
        #print_values(bus)
  for pin_flag in mcp2.int_flag:
        #print("mcp2:")
        #print_values(bus)
        #mcp2.interrupt_enable = 0x0000  # Enable Interrupts in all mcp2 pins
        #print("Interrupt on mcp2 disabled")
        #print("Interrupt connected to mcp2 Pin: {}".format(port))
      print("Pin number: {} changed to: {}".format(pin_flag, pinsMcp2[pin_flag].value))
      print_values(bus)
      now = datetime.now()
      current_time = now.strftime("%H:%M:%S")
      print("Current Time =", current_time)
        #mcp2.interrupt_enable = 0xFFFF  # Enable Interrupts in all mcp2 pins 
        #print("Interrupt on mcp2 enabled")
        #for pinvalue in mcp2.int_capa:
        #    print("pinvalue = {}".format(pinvalue.value))
        #mcp2.clear_ints()
        #print("Interrupt on mcp2 cleared")
        #print_values(bus)


# connect either interrupt pin to the Raspberry pi's pin 18.
# They were previously configured as mirrored.
GPIO.setmode(GPIO.BCM)
interrupt = 18
GPIO.setup(interrupt, GPIO.IN, GPIO.PUD_UP)  # Set up Pi's pin as input, pull up
#GPIO.setup(17, GPIO.OUT)
# The add_event_detect fuction will call our print_interrupt callback function
# every time an interrupt gets triggered.
GPIO.add_event_detect(interrupt, GPIO.FALLING, bouncetime=500)
GPIO.add_event_callback(interrupt, print_interrupt)
# The following lines are so the program runs for at least 60 seconds,
# during that time it will detect any pin interrupt and print out the pin number
# that changed state and its current state.
# The program can be terminated using Ctrl+C. It doesn't matter how it
# terminates it will always run GPIO.cleanup().
try:
    print("When button is pressed you'll see a message")
    print_values(bus)
    while(True):
      #print("printing values before anything else")
      #print_values(bus)
      print("not frozen")
      pinsMcp3[7].value = True 
      print("pin7 true")
      sleep(10) 
      pinsMcp3[7].value = False
      print("pin7 false")
      sleep(10)
      #print("printing values")
      #print_values(bus)
      #sleep(2)
      #print("printing values again")
      #print_values(bus)
      #sleep(30)
finally:
    GPIO.cleanup()
