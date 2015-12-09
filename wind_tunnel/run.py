#!/usr/bin/python

import os
from python_modules import force_read
from python_modules import settings_change
from python_modules import file_operations

# Parameters
MIN_SIM_TIME = 1 # The minimum simulation time before checking convergence. 
UPDATE_TIME = 0.25 # The period to check convergence.
MAX_SIM_TIME = 5
TRAIL_CHECK = 0.1 # The amount of time to average.
STOP_THRESHOLD = 0.01 # Ratio of change, below which simulation is stopped.

# Preprocessing
os.system("./convert_mesh.sh")
os.system("./modify_boundary.py")

# Convergence loop
current_sim_time = MIN_SIM_TIME
current_lift_measurement = None;
os.system("echo \"Starting a new OpenFOAM simulation:\n\" > log")
while current_sim_time <= MAX_SIM_TIME:
  # Run simulation.
  os.system("pimpleFoam >> log")

  # Extract averaged performance figure.
  master_list = force_read.get_forces_dict(forces_file)
  time = master_list[0]
  drag = master_list[1]
  lift = master_list[2]
  moment = master_list[3]
  new_lift_measurement = trailing_average(time, lift, TRAIL_CHECK)

  # Check to stop
  if current_lift_measurement != None:
    diff = abs(new_lift_measurement-current_lift_measurement)
    ratio = diff / current_lift_measurement
    if ratio < STOP_THRESHOLD:
      break
    else:
      current_lift_measurement = new_lift_measurement

  # Prepare for next iteration.
  file_operations.change_file_name("postProcessing/wing/0/forces.dat", \
    "_"+str(current_sim_time)+".dat")
  current_sim_time += UPDATE_TIME
  settings_change.set_end_time(current_sim_time, "system/controlDict", \
    "system/controlDict_new")
  os.system("mv system/controlDict_new system/controlDict")

# Post-processing
biggest_number = file_operations.get_highest_folder("../vault", "v")
new_vault_name = "v"+str(biggest_number+1)
lift_measurement = trailing_average(time, lift, TRAIL_CHECK)
drag_measurement = trailing_average(time, drag, TRAIL_CHECK)
moment_measurement = trailing_average(time, moment, TRAIL_CHECK)

# Store CFD solution
new_vault_folder = "../vault/"+new_vault_name
os.system("mkdir "+new_vault_folder)
os.system("cp -r ./* "+new_vault_folder+"/")

# Store performance result
new_vault_file = "../vault/"+new_vault_name+".dat"
os.system("cp ../bridge/physical_inputs.dat "+new_vault_file)
with open(new_vault_file, "a") as vf:
  vf.write("\n")
  vf.write(str(lift_measurement)+"\n")
  vf.write(str(drag_measurement)+"\n")
  vf.write(str(moment_measurement)+"\n")

# Clean up
os.system("rm -r postProcessing")


