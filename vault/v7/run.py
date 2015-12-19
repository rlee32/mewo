#!/usr/bin/python

# We assume this is called from the case directory.

import os
from openfoam_python import force_read
from openfoam_python import boundary_conditions
from openfoam_python import controlDict
from openfoam_python import file_operations

# Parameters
MIN_SIM_TIME = 1.0 # The minimum simulation time before checking convergence. 
UPDATE_TIME = 0.1 # The period to check convergence.
MAX_SIM_TIME = 5.0
TRAIL_CHECK = 0.1 # The amount of time to average.
STOP_THRESHOLD_PERCENT = 1 # percent change below which simulation is stopped.

# Prepare the case.
print "Cleaning the case."
file_operations.clean_case()
os.system("mkdir logs")
print "Converting mesh."
os.system("mv ../bridge/main.msh main.msh")
os.system("gmshToFoam main.msh > logs/gmshToFoam")
print "Modifying BC."
boundary_file = "constant/polyMesh/boundary"
boundary_conditions.modify_empty_bc(boundary_file, "front_and_back", "empty")
boundary_conditions.modify_empty_bc(boundary_file, "wing", "wall")
controlDict.set_end_time(MIN_SIM_TIME)
controlDict.set_write_interval(MIN_SIM_TIME)
os.system("mv ../bridge/geometry.dat ./geometry.dat")

# Convergence loop
current_sim_time = MIN_SIM_TIME
current_lift_measurement = None;
while current_sim_time <= MAX_SIM_TIME:
  # Run simulation.
  print "Running OpenFOAM simulation to "+str(current_sim_time)
  os.system("pimpleFoam > logs/simulation")

  # Extract averaged performance figure.
  latest_force_time = force_read.get_latest_force_time("wing")
  forces_file = "postProcessing/wing/"+str(latest_force_time)+"/forces.dat"
  master_list = force_read.get_forces_dict(forces_file)
  time = master_list[0]
  drag = master_list[1]
  lift = master_list[2]
  moment = master_list[3]
  new_lift_measurement = force_read.trailing_average(time, lift, TRAIL_CHECK)

  # Check to stop
  if current_lift_measurement != None:
    diff = abs(new_lift_measurement-current_lift_measurement)
    ratio = diff / current_lift_measurement
    if ratio*100 < STOP_THRESHOLD_PERCENT:
      break
    else:
      current_lift_measurement = new_lift_measurement
  else:
    current_lift_measurement = new_lift_measurement

  # Prepare for next iteration.
  current_sim_time += UPDATE_TIME
  controlDict.set_end_time(current_sim_time)
  controlDict.set_write_interval(UPDATE_TIME)

# Post-processing
print "Obtaining performance figures."
L = force_read.trailing_average(time, lift, TRAIL_CHECK)
D = force_read.trailing_average(time, drag, TRAIL_CHECK)
M = force_read.trailing_average(time, moment, TRAIL_CHECK)
V = force_read.get_V()
q = 0.5*1.18*V*V
c = force_read.get_overall_chord()
A = c*force_read.get_cell_depth()
cl = L / A / q
cd = D / A / q
cm = M / A / q / c

# Store CFD solution
print "Storing CFD solution."
biggest_number = file_operations.get_highest_folder("../vault", "v")
new_vault_name = "v"+str(biggest_number+1)
new_vault_folder = "../vault/"+new_vault_name
os.system("mkdir "+new_vault_folder)
file_operations.leave_last_time()
os.system("cp -r ./* "+new_vault_folder+"/")

# Store performance result
print "Storing performance result."
new_vault_file = "../vault/"+new_vault_name+".dat"
os.system("mv ../bridge/physical_inputs.dat "+new_vault_file)
with open(new_vault_file, "a") as vf:
  vf.write("\n")
  vf.write(str(cl)+"\n")
  vf.write(str(cd)+"\n")
  vf.write(str(cm)+"\n")

# Clean up
print "Cleaning up case."
file_operations.clean_case()
print "Simulation finished!"
