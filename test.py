import pyvisa
import AL8164_mod

#view resources, find the GPIB
rm = pyvisa.ResourceManager()
rl = rm.list_resources()
resource = rl[1] #grab name of GPIB source. This is hardcoded assuming which position the laser will hold.
#construct a laser object with resource corresp. to laser's GPIB input
inst = rm.open_resource(resource)


#inst = pyvisa.resources.gpib.GPIBInstrument()

my_laser = AL8164(inst)