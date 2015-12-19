#!/usr/bin/python

import os
import sys
import math
from openfoam_python import force_read

forces_path = "postProcessing/wing/0"
forces_file = forces_path+"/forces.dat"

if not os.path.isfile(forces_file):
  print "Forces file not found at "+forces_file
  print "Be sure that the case has been run and you have the right directory!"
  print "Exiting."
  sys.exit()

master_list = force_read.get_forces_dict(forces_file)
time = master_list[0]
drag = master_list[1]
lift = master_list[2]
moment = master_list[3]

# Scale the forces.
chord = force_read.get_overall_chord()
print "Chord: "+str(chord)
# We assume cell_depth is hard-coded elsewhere.
cell_depth = 0.1
# cell_depth = get_cell_depth()
# print "Cell Depth: "+str(cell_depth)
A = cell_depth*chord
rho = 1.18 # Assuming it is hard-coded elsewhere.
V = force_read.get_V()
print "Velocity: "+str(V)
q = 0.5*rho*V*V
denom = q*A
lift = [x / denom for x in lift]
drag = [x / denom for x in drag]
moment = [x / denom / chord for x in moment]

outputfile = open(forces_path+'/forces.txt','w')
for i in range(0,len(time)):
  outputfile.write(str(time[i])+' '+str(lift[i])+' '\
    +str(drag[i])+' '+str(moment[i])+'\n')
outputfile.close()

os.system("./gnuplot_script.sh")


