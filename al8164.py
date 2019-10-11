import pyvisa
import sys
from time import sleep

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
    inst = rm.open_resource(my_GPIB, values_format = 3)
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
         self.inst.write("sour{}:wav {}NM".format(source, wavelength))
         print("Wavelength of source {} has been set to {} nm".format(source, wavelength))

    def enable(self):
        self.inst.write("sour0:pow:stat 1")

    def disable(self):
        self.inst.write("sour0:pow:stat 0")

    def get_llog(self):
        self.inst.query("sour0:read:data? llog")    

    def sweep(self, start, stop, speed, trig_step):
        #run general setup
        self.inst.write("wav:swe:mode {}".format("CONT")) #right now hardcoded to continuous sweep
        self.inst.write("wav:swe:star {}nm".format(start))
        self.inst.write("wav:swe:stop {}nm".format(stop))
        self.inst.write("wav:swe:speed {}nm/s".format(speed))
        self.inst.write("wav:swe:step {}nm".format(trig_step))

        #Requisites for Lambda Logging
        #note that laser requires trig rate of less than 40 KHz, that is, speed/trig_step must be less than 40,000 steps/sec

        self.inst.write("trig1:outp STF") #set trigger to rising edge when each step finishes
        self.inst.write("wav:swe:cycl 1") #only sweep up and down once.
        self.inst.write("sour0:am:stat 0") #turn OFF AM capability
        self.inst.write("wav:swe:llog 1") #turn on lambda logging
        print("CONFIRMING LLOG IS ON")
        print(self.inst.write("wav:swe:llog?"))
        print("CONFIRMING SWEEP PARAMTERS")
        ok_msg = self.inst.query("sour0:wav:swe:chec?")
        print(ok_msg)
        self.inst.write("wav:swe STAR") #run the sweep
        print("SWEEP RUNNING")
        sleep((stop - start)/speed + 5)
        #sleep(10)
        print("SWEEP COMPLETE")
        #Now grab the lambda logging data
        print("CHECK IF LLOG STILL ON")
        print(self.inst.query("wav:swe:llog?"))
        print("RETRIEVING LAMBDA LOG")
        #lam_log = self.inst.query("sour0:chan1:read:data?")
        #return lam_log
