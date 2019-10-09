import pyvisa
from al8164 import AL8164 #With this you can just call AL8164(inst)
from al8164 import laser_init
#from al8164 import*
#import al8164 #Here you'll ned to make a laser by al8164.AL8164(inst)

#call setup function to initialize laser
laser = laser_init()

#Now ensure laser object works
ID = laser.get_IDN()

#Make sure we can set the laser current wavelength
laser.set_CW(0, 1543) #set laser source 0 to 1543 nanometers

#Make sure we can get the laser current wavelength once set
lam = laser.get_CW(0) #get the current wavelenth set to source 0

#test sweep param setting. note, need speed/step < 40,000 step/sec
lam_log = laser.sweep(1500, 1600, 100, 5)