import pyvisa
from al8164 import AL8164

#Instrument Initialization
rm = pyvisa.ResourceManager()
rl = rm.list_resources()
resource = rl[1]
inst = rm.open_resource(resource)
my_laser = AL8164(inst)
print("SUCCESSFUL CONSTRUCTION")
my_laser.get_IDN()
print("SUCCESSFUL QUERY")

#

