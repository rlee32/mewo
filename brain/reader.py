#!/usr/bin/python

import os
import sys
import numpy

def read_feature_vector(path, n_features):
  """
  Reads a feature vector file with results. Assumes that there are n_features 
  first, then the rest of the file is results.
  '#' on lines denote comments.  
  """
  features = []
  results = []
  if os.path.isfile(path):
    with open(path, 'r') as f:
      feature = 0
      for line in f:
        if '#' not in line and line.strip() != '':
          if feature < n_features:
            features.append(float(line))
            feature += 1
          else:
            results.append(float(line))
  instance = (features, results)
  return instance

def get_all_dat_files(path):
  dat_files = [x for x in os.listdir(path) if '.dat' in x]
  return dat_files

def leave_one_out(my_list, index):
  return my_list[:index] + my_list[(index+1):]

def numpy_instance(instance):
  """
  Converts an instance defined with lists to an instance defined with 
  numpy.ndarray.
  """
  new_instance = (numpy.array(instance[0]), numpy.array(instance[1]))
  return new_instance

if __name__ == '__main__':
  lists = read_feature_vector('../vault/v87.dat', 25)
  nda = numpy_instance(lists)
  print nda

  dats = get_all_dat_files('../vault')
  print len(dats)

  dats2 = leave_one_out(dats,50)

  print len(dats)
  print len(dats2)

