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

    #construct a laser object with resource corresp. to laser's GPIB input
    inst = rm.open_resource(my_GPIB)
    my_laser = AL8164(inst)
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

    def sweep(self, start, stop, speed, trig_step):
        #run general setup
        self.inst.query("wav:swe:mode {}".format("CONT")) #right now hardcoded to continuous sweep
        self.inst.query("wav:swe:star {}nm".format(start))
        self.inst.query("wav:swe:stop {}nm".format(stop))
        self.inst.query("wav:swe:speed {}nm/s".format(speed))
        self.inst.query("wav:swe:step {}nm".format(trig_step))

        #Requisites for Lambda Logging
        #note that laser requires trig rate of less than 40 KHz, that is, speed/trig_step must be less than 40,000 steps/sec

        self.inst.query("trig1:outp STF") #set trigger to rising edge when each step finishes
        self.inst.query("wav:swe:cycl 1") #only sweep up and down once.
        self.inst.query("sour0:am:stat 0")#turn OFF AM capability
        self.inst.query("wav:swe:llog 1")

        self.inst.query("wav:swe STAR") #run the sweep

        #Now grab the lambda logging data
        lam_log = self.inst.query("sour0:read:data?")
        return lam_log
