import json
import board
import busio
import smbus
from digitalio import Direction, Pull
from RPi import GPIO
from adafruit_mcp230xx.mcp23017 import MCP23017

# Initialisation du bus I2C:
i2c = busio.I2C(board.SCL, board.SDA)
bus = smbus.SMBus(1)
keys = ["l", "ob", "g", "y2", "y1", "w3", "w2", "w1", "l", "ob", "g", "y2", "y1", "w3", "w2", "w1"]
def read_mcp_input(mcp_address):

# Pour initialiser les chip mcp2317
    mcp = MCP23017(i2c, address=mcp_address)
# Créer la liste de tout les pins (0-16) incluant clé
    pinsMcp = []
    pinsMcp_string_array = []
    for pin in range(0, 16):
        pinsMcp.append(mcp.get_pin(pin))
#setup des pin en input avec pull up
    for i, (pin) in enumerate(pinsMcp):
        pin.direction = Direction.INPUT
        pin.pull = Pull.UP
# combine les valeurs des input avec les clé json et leur valeur (true ou false)
        if pin.value:
            pinsMcp_string_array.append({keys[i]: "false"})
        else:
            pinsMcp_string_array.append({keys[i]: "true"})
    return pinsMcp_string_array

pinsMcp1 = read_mcp_input(0x20)
pinsMcp2 = read_mcp_input(0x21)
pinsMcp3 = read_mcp_input(0x22)
pinsMcp4 = read_mcp_input(0x23)
#split les input de mcpx (16 in) en thermostat (8in)
zones = {"th1": pinsMcp1[:8]} , {"th2": pinsMcp1[8:]} , {"th3": pinsMcp2[:8]} , {"th4": pinsMcp2[8:]}, {"th5": pinsMcp3[:8]} , {"th6": pinsMcp3[8:]}, {"th7": pinsMcp4[:8]} , {"th8": pinsMcp4[8:]}

# Convertis le JSON original en Python dictionary
original_dict = json.loads(json.dumps(zones))

# Création d'un dictionary vide pour stocker le JSON formaté
formatted_dict = {"zones": {}}

# Loop dans le dictionnaire original et format le JSON
for item in original_dict:
    for key, value in item.items():
        zones = {}
        for val in value:
            for k, v in val.items():
                zones[k] = v
        formatted_dict["zones"][key] = zones

# Converti le dictionary formaté en string JSON
formatted_json = json.dumps(formatted_dict)

#output (payload)
print(formatted_json)


