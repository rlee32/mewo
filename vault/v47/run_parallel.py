#!/usr/bin/python

# We assume this is called from the case directory.
# Be sure to call prepare_run.py first.
# Input arguments are the extra time to run before checking and the maximum 
# extra time to run. 

# Hard-coded parameters.
UPDATE_TIME = 0.1 # The period to check convergence.
TRAIL_CHECK = 0.1 # The amount of time to average; also defined in 
  # store_solution.py.
STOP_THRESHOLD_PERCENT = 0.5 # percent change below which simulation is stopped.

import os
import sys
from openfoam_python import force_read
from openfoam_python import boundary_conditions
from openfoam_python import controlDict
from openfoam_python import fvSchemes
from openfoam_python import file_operations

if len(sys.argv) != 3:
  print "Please input the extra time before checking and max extra time!"
  sys.exit()

# Check for mesh.
if not os.path.isdir("constant/polyMesh"):
  print "Mesh not found! Exiting."
  sys.exit()

# Get latest time in case.
time_folders = [float(x) for x in file_operations.get_time_folders()]
time_folders.sort()
latest_time = 0 if len(time_folders) == 0 else time_folders[-1]

# Get command-line arguments.
min_extra_time = float(sys.argv[1])
max_extra_time = float(sys.argv[2])

# Parameters
MIN_SIM_TIME = latest_time + min_extra_time # The minimum simulation time 
  # before checking convergence. 
MAX_SIM_TIME = latest_time + max_extra_time

# Adjust controlDict
controlDict.set_end_time(MIN_SIM_TIME)
controlDict.set_write_interval(MIN_SIM_TIME)

print "Decomposing case for parallel run."
os.system("decomposePar > logs/par_log")

# Convergence loop
current_sim_time = MIN_SIM_TIME
current_lift_measurement = None;
while current_sim_time <= MAX_SIM_TIME:
  # Run simulation.
  print "Running OpenFOAM simulation to "+str(current_sim_time)
  os.system("mpirun -np 4 pimpleFoam -parallel > logs/simulation")

  # Extract averaged performance figure.
  latest_force_time = force_read.get_latest_force_time("wing")
  forces_file = "postProcessing/wing/"+str(latest_force_time)+"/forces.dat"
  master_list = force_read.get_forces_dict(forces_file)
  time = master_list[0]
  drag = master_list[1]
  lift = master_list[2]
  moment = master_list[3]
  new_lift_measurement = force_read.trailing_average(time, lift, TRAIL_CHECK)
  new_drag_measurement = force_read.trailing_average(time, drag, TRAIL_CHECK)
  new_moment_measurement = \
    force_read.trailing_average(time, moment, TRAIL_CHECK)

  # Check to stop
  if current_lift_measurement != None:
    diff_lift = abs(new_lift_measurement-current_lift_measurement)
    diff_drag = abs(new_drag_measurement-current_drag_measurement)
    diff_moment = abs(new_moment_measurement-current_moment_measurement)
    ratio_lift = diff_lift / current_lift_measurement
    ratio_drag = diff_drag / current_drag_measurement
    ratio_moment = diff_moment / current_moment_measurement
    ratio = max([ratio_lift, ratio_drag, ratio_moment])
    if ratio*100 < STOP_THRESHOLD_PERCENT:
      break
    else:
      current_lift_measurement = new_lift_measurement
      current_drag_measurement = new_drag_measurement
      current_moment_measurement = new_moment_measurement
  else:
    current_lift_measurement = new_lift_measurement
    current_drag_measurement = new_drag_measurement
    current_moment_measurement = new_moment_measurement

  # Prepare for next iteration.
  current_sim_time += UPDATE_TIME
  controlDict.set_end_time(current_sim_time)
  controlDict.set_write_interval(UPDATE_TIME)

print "Reconstructing case."
os.system("reconstructPar -latestTime >> logs/par_log")
