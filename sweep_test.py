from al8164 import AL8164
from al8164 import laser_init

laser = laser_init()
laser.sweep(1500,1600,100,5)
lam = laser.get_llog()

print(lam)