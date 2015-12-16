#!/usr/bin/python

import os
from python_modules import force_read

TRAIL_CHECK = 0.1

forces_file = "postProcessing/wing/1.6/forces.dat"
master_list = force_read.get_forces_dict(forces_file)
time = master_list[0]
drag = master_list[1]
lift = master_list[2]
moment = master_list[3]
new_lift_measurement = force_read.trailing_average(time, lift, TRAIL_CHECK)


print new_lift_measurement