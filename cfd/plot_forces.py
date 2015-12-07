#!/usr/bin/python

import os
import sys
import math

forces_path = "postProcessing/wing/0"
forces_file = forces_path+"/forces.dat"

if not os.path.isfile(forces_file):
  print "Forces file not found at "+forces_file
  print "Be sure that the case has been run and you have the right directory!"
  print "Exiting."
  sys.exit()

def line2dict(line):
  tokens_unprocessed = line.split()
  tokens = [x.replace(")","").replace("(","") \
    for x in tokens_unprocessed]
  floats = [float(x) for x in tokens]
  data_dict = {}
  data_dict['time'] = floats[0]
  force_dict = {}
  force_dict['pressure'] = floats[1:4]
  force_dict['viscous'] = floats[4:7]
  force_dict['porous'] = floats[7:10]
  moment_dict = {}
  moment_dict['pressure'] = floats[10:13]
  moment_dict['viscous'] = floats[13:16]
  moment_dict['porous'] = floats[16:19]
  data_dict['force'] = force_dict
  data_dict['moment'] = moment_dict
  return data_dict

def get_overall_chord():
  # Searches file for the chord.
  chord = 0
  with open("../mesh_factory/shapes/global_wing_chord.dat","r") as cfile:
    for line in cfile:
      # Assume first line is the chord.
      chord = float(line)
  cfile.close()
  return chord

def get_cell_depth():
  # Searches file for the cell_depth.
  cell_depth = 0
  with open("../mesh_factory/numerical_inputs.geo","r") as cfile:
    for line in cfile:
      if "cell_depth" in line:
        cell_depth = float( (line.split("=")[1]).strip().replace(';','') )
  cfile.close()
  return cell_depth
  return

def get_V():
  # Searches file for the velocity.
  velocity = 0
  with open("0/include/initialConditions","r") as ufile:
    for line in ufile:
      if "flowVelocity" in line:
        vector = line[line.find("(")+1:line.find(")")]
        velocity = float(vector.split()[0])
  ufile.close()
  return velocity

time = []
drag = []
lift = []
moment = []
with open(forces_file,"r") as datafile:
  for line in datafile:
    if line[0] == "#":
      continue
    data_dict = line2dict(line)
    time += [data_dict['time']]
    drag += [data_dict['force']['pressure'][0] + \
      data_dict['force']['viscous'][0]]
    lift += [data_dict['force']['pressure'][1] + \
      data_dict['force']['viscous'][1]]
    moment += [data_dict['moment']['pressure'][2] + \
      data_dict['moment']['viscous'][2]]
datafile.close()

# Scale the forces.
chord = get_overall_chord()
print "Chord: "+str(chord)
cell_depth = get_cell_depth()
print "Cell Depth: "+str(cell_depth)
A = cell_depth*chord
rho = 1.18 # Assuming it is hard-coded elsewhere.
V = get_V()
print "Velocity: "+str(V)
q = 0.5*rho*V*V
denom = q*A
lift = [x / denom for x in lift]
drag = [x / denom for x in drag]
moment = [x / denom for x in moment]

outputfile = open('forces.txt','w')
for i in range(0,len(time)):
  outputfile.write(str(time[i])+' '+str(lift[i])+' '\
    +str(drag[i])+' '+str(moment[i])+'\n')
outputfile.close()

os.system("./gnuplot_script.sh")


