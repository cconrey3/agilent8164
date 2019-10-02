import pyvisa

class AL8164:
    def __init__(self, inst):
        AL8164.inst = inst
        
    def get_IDN(self):
        print(self.inst.query("*IDN?"))


#view resources, find the GPIB
rm = pyvisa.ResourceManager()
rl = rm.list_resources()
resource = rl[1] #grab name of GPIB source. This is hardcoded assuming which position the laser will hold.
#construct a laser object with resource corresp. to laser's GPIB input
inst = rm.open_resource(resource)

my_laser = AL8164(inst)
print("SUCCESSFUL CONSTRUCTION")
print(my_laser.inst)

my_laser.get_IDN()
print("SUCCESSFUL QUERY")


