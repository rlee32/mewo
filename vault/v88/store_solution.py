#!/usr/bin/python

# We assume this is called from the case directory.
# This stores whatever is currently in the wind_tunnel.

# These parameters are 
TRAIL_CHECK = 0.1 # The amount of time to average; also defined in run.py.

import os
from openfoam_python import force_read
from openfoam_python import file_operations

# Extract averaged performance figure.
latest_force_time = force_read.get_latest_force_time("wing")
forces_file = "postProcessing/wing/"+str(latest_force_time)+"/forces.dat"
master_list = force_read.get_forces_dict(forces_file)
time = master_list[0]
drag = master_list[1]
lift = master_list[2]
moment = master_list[3]

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
new_vault_folder = "../vault/"+new_vault_name.strip()
os.system("mkdir "+new_vault_folder)
file_operations.leave_last_time()
os.system("cp -r ./* "+new_vault_folder+"/")
if os.path.isdir("./"+new_vault_folder+"/openfoam_python/.git") or \
  os.path.isfile("./"+new_vault_folder+"/openfoam_python/.git"):
  # print "Removing .git"
  os.system("rm -r ./"+new_vault_folder+"/openfoam_python/.git")
if os.path.isfile("./"+new_vault_folder+"/main.msh"):
  os.system("rm ./"+new_vault_folder+"/main.msh")
if os.path.isdir("./"+new_vault_folder+"/logs"):
  os.system("rm -r ./"+new_vault_folder+"/logs")
if os.path.isdir("./"+new_vault_folder+"/processor0"):
  os.system("rm -r ./"+new_vault_folder+"/processor*")

# Store performance result
print "Storing performance result."
new_vault_file = "../vault/"+new_vault_name+".dat"
os.system("mv ../bridge/physical_inputs.dat "+new_vault_file)
with open(new_vault_file, "a") as vf:
  vf.write("\n")
  vf.write(str(cl)+"\n")
  vf.write(str(cd)+"\n")
  vf.write(str(cm)+"\n")
with open("../bridge/newest_data_file.txt",'w') as f:
  f.write("vault/"+new_vault_name+".dat")
