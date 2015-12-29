#!/usr/bin/python

"""
This script finds a local optimum of one element of the feature vector by 
hill climbing the (1D) single-feature space (other features held 
constant).

Usage: optimize_feature.py <1> <2> <3>
1: base feature vector file
2: index of feature to optimize (start at zero)
3: feature value iteration increment (sign denotes initial search direction)

We assume this is called form the main directory, and only one simulation is 
being worked on at a time.
"""

import os
import sys

# Hard-coded parameters for the current application.
MAX_FEATURES = 25

if len(sys.argv) != 4:
  print "Please enter the correct amount of arguments (see script header)."
  sys.exit()

base_file = sys.argv[1]
feature_index = int(sys.argv[2])
increment = float(sys.argv[3])
print "Feature index to optimize: "+str(feature_index)
print "Increment value: "+str(increment)

# Preliminary checks.
if not os.path.isfile(base_file):
  print base_file+" not found! Exiting."
  sys.exit()

def get_current_feature_value(path, index):
  current_value = None
  index_ = 0
  with open(path,'r') as f:
    for line in f:
      if '#' not in line and line.strip() != '':
        if index_ == index:
          current_value = float(line)
          break
        index_ += 1
  return current_value
current_value = get_current_feature_value(base_file, feature_index)
if current_value == None:
  print "For some reason, the current feature value could not be found. \
    Exiting."
  sys.exit()
print "Current feature value: "+str(current_value)

def write_new_feature_vector(base_path, value, index, \
  new_path="schedule/new.dat"):
  new_vector = open(new_path, 'w')
  index_ = 0
  with open(base_path,'r') as f:
    for line in f:
      if '#' not in line and line.strip() != '':
        if index_ == index:
          # print "New value: "+str(value)
          new_vector.write(str(value)+"\n")
        else:
          new_vector.write(line)
        index_ += 1
      else:
        new_vector.write(line)
      if index_ >= MAX_FEATURES:
        break
  new_vector.close()
  return

def get_results(path):
  results = []
  index_ = 0
  with open(path, 'r') as f:
    for line in f:
      if '#' not in line and line.strip() != '':
        if index_ >= MAX_FEATURES:
          results.append(float(line))
        index_ += 1
  return results
current_optimization = get_results(base_file)
print "Starting objective values:"
print current_optimization

# Begin optimization procedure.
increasing = False
reverse = False
optimal_data_file = base_file
print "Starting with feature "+str(feature_index)+" at "+str(current_value)
while True:
  new_feature_value = current_value+increment
  write_new_feature_vector(base_file, new_feature_value, feature_index)
  print "===================="
  print "Running "+str(new_feature_value)
  print "===================="
  os.system('./par_dyn_sched.sh')
  # Get file for new data point
  newest_data_file = None
  with open("bridge/newest_data_file.txt",'r') as f:
    for line in f:
      newest_data_file = line.strip()
      break
  # Assume bad results when no data file
  if newest_data_file == None or newest_data_file == '':
    if reverse or increasing:
      break
    else:
      increment = -increment
      reverse = True
  else:
    new_results = get_results(newest_data_file)
    dL = new_results[0] - current_optimization[0]
    dD = new_results[1] - current_optimization[1]
    objective = dL - dD
    if objective >= 0:
      optimal_data_file = newest_data_file
      current_optimization = new_results
      current_value = new_feature_value
      increasing = True
    else:
      if increasing or reverse:
        break
      else:
        increment = -increment
        reverse = True

print "===================="
print "Optimization complete. Optimal feature set: "+optimal_data_file
print "===================="
with open('optimal_vector.txt', 'w') as f:
  f.write(optimal_data_file)