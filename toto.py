#import quick2wire.i2c as i2c
#import mcp23017
import smbus
import time
 
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1
 
MCP01 = 0x20 # Device address (A0-A2)
MCP02 = 0x21 # Device address (A0-A2)
MCP03 = 0x22 # Device address (A0-A2)

GPIOAINPUT  = 0x12 # Register for input
GPIOBINPUT  = 0x13 # Register for input

IODIRA = 0x00; # IODIR register address controls the direction of the GPIO on the port expander
IODIRB = 0x01; # IODIR register address controls the direction of the GPIO on the port expander

IPOLA = 0x02; # Input Polarity Register
IPOLB = 0x03; # Input Polarity Register

GPINTA = 0x04; # Interrput on Change pin 
GPINTB = 0x05; # Interrput on Change pin 

DEFVALA = 0x06; # Default Compare Register for Interrupt-on-change
DEFVALB = 0x07; # Default Compare Register for Interrupt-on-change

INTCONA = 0x08; # IO Configuration: bank/mirror/seqop/disslw/haen/odr/intpol/notimp
INTCONB = 0x09; # IO Configuration: bank/mirror/seqop/disslw/haen/odr/intpol/notimp

IOCON = 0x0A;  # I/O Expander Configruation Register

GPPUA = 0x0C; # GPIO Pull-up resistor (0 = disabled, 1 = enabled)
GPPUB = 0x0D; # GPIO Pull-up resistor (0 = disabled, 1 = enabled)

INTFA = 0x0E; #Interrupt Flag Register
INTFB = 0x0F; #Interrupt Flag Register

INTCAPA = 0x10; #Interrupt Capture Register
INTCAPB = 0x11; #Interrupt Capture Register

GPIOA = 0x12; # GPIO register is used to read the pins input
GPIOB = 0x13; # GPIO register is used to read the pins input

OLATA = 0x14; # Output Latch register is used to set the pins output high/low
OLATB = 0x15; # Output Latch register is used to set the pins output high/low
 
# Set all GPA pins as input

bus.write_byte_data(MCP01,IODIRA,0x00)
bus.write_byte_data(MCP01,IODIRB,0x00)

# Set all GPA pins as pull-up

bus.write_byte_data(MCP01,GPPUA,0xFF)
bus.write_byte_data(MCP01,GPPUB,0xFF)


 
# Loop until user presses CTRL-C
while True:
 
  # Read state of GPIOA register
   MySwitch = bus.read_byte_data(MCP01,GPIOAINPUT)
   print (format(MySwitch, 'b'));
   time.sleep(1)
