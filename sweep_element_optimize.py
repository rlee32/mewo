#!/usr/bin/python

"""
This script performs a sequential one-by-one optimization of the feature 
vector, but the ordering is determined by grouping element-wise features. 
Obviously, it is a hill climbing approach.

We assume that optimal_vector.txt holds the feature vector to work on.
"""

import os
import sys
import element_optimize


if __name__ == '__main__':
  # if len(sys.argv) != 2:
  #   print "Please input correct arguments! Exiting."
  #   sys.exit()
  # vector = sys.argv[1]


  total_elements = 5
  for element_index in range(total_elements):
    print "++++++++++++++++++++++++++++++++++++++++"
    print "OPTIMIZING ELEMENT "+str(element_index)
    print "++++++++++++++++++++++++++++++++++++++++"
    vector = element_optimize.get_one_liner("optimal_vector.txt")
    if not os.path.isfile(vector):
      print "Feature vector file not found! Exiting."
      break
    os.system("./element_optimize.py "+str(vector)+" "
      +str(element_index))

  print "OPTIMIZATION FINISHED."