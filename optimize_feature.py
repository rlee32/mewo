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
write_new_feature_vector(base_file, current_value+increment, feature_index)

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
results = get_results(base_file)
print "Starting objective values:"
print results