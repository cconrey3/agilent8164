import pyvisa
import sys

def laser_init():
    #view resources, find the GPIB
    rm = pyvisa.ResourceManager()
    rl = rm.list_resources()

    GPIB_list = [item for item in rl if item[0:4] == 'GPIB']
    if len(GPIB_list) == 0:
        sys.exit("No GPIB Instrument Found -- Chris Conrey.")
    else:
        my_GPIB = GPIB_list[0]
    #resource = rl[1] #grab name of GPIB source. This is hardcoded assuming which position the laser will hold.
    #construct a laser object with resource corresp. to laser's GPIB input
    inst = rm.open_resource(my_GPIB)

    my_laser = AL8164(inst)
    #my_laser = al8164.AL8164(inst)
    print("SUCCESSFUL CONSTRUCTION")
    print(my_laser.inst)

    my_laser.get_IDN()
    print("SUCCESSFUL QUERY")
    return my_laser

class AL8164:
    def __init__(self, inst):
        AL8164.inst = inst
        
    def get_IDN(self):
        ID = self.inst.query("*IDN?")
        print(ID)
        return ID

    def get_CW(self, source):
         lam = self.inst.query("sour{}:wav?".format(source))
         print("Wavelength of source {} is currently set to {} nm".format(source, lam))
         return lam

    def set_CW(self, source, wavelength):
         self.inst.query("sour{}:wav {}NM".format(source, wavelength))
         print("Wavelength of source {} has been set to {} nm".format(source, wavelength))


