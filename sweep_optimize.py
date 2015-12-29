#!/usr/bin/python

"""
This script performs a sequential one-by-one optimization of the feature 
vector. Obviously, it is a hill climbing approach.
"""

import os
import sys

def get_one_liner(path):
  content = None
  if os.path.isfile(path):
    with open(path, 'r') as f:
      for line in f:
        content = line.strip()
        break
  return content

def determine_step(index):
  chord_step = 0.05
  alpha_step = 2.5
  xgap_step = 0.03
  ygap_step = 0.01
  span_step = 5
  if index in [10,15]:
    return None
  if index in range(5):
    return chord_step
  if index in range(5,10):
    return alpha_step
  if index in range(11,15):
    return xgap_step
  if index in range(16,20):
    return ygap_step
  if index in range(20,25):
    return span_step
  return None

def get_feature_description(index):
  if index in [10,15]:
    return "X- or Y- Gap, Element 0"
  if index in range(5):
    return "Chord, Element "+str(index)
  if index in range(5,10):
    return "Angle of Attack, Element "+str(index-5)
  if index in range(11,15):
    return "X-Gap, Element "+str(index-10)
  if index in range(16,20):
    return "Y-Gap, Element "+str(index-15)
  if index in range(20,25):
    return "Span Angle, Element "+str(index-20)
  return None

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print "Please input correct arguments! Exiting."
    sys.exit()
  vector = sys.argv[1]
  index =  int(sys.argv[2])
  if not os.path.isfile(vector):
    print "Feature vector file not found! Exiting."
    sys.exit()

  while index < 25:
    print "++++++++++++++++++++"
    print "OPTIMIZING FEATURE "+str(index)+" ("+\
      get_feature_description(index)+")"
    print "++++++++++++++++++++"
    step = determine_step(index)
    if step != None:
      os.system("./optimize_feature.py "+vector+" "+str(index)+" "+\
        str(step))
      new_vector = get_one_liner('optimal_vector.txt')
      if new_vector != None:
        vector = new_vector
    index += 1
