#!/usr/bin/python

import os
import sys
import numpy
import random

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

def leave_k_out(my_list, start_index, k):
  train_set = my_list[:start_index] + my_list[(start_index+k):]
  test_set = my_list[start_index:(start_index+k)]
  return (train_set, test_set)

def split_data(data_original, training_fraction, test_fraction):
  """
  Splits data into a training, validation, and test sets.
  """
  validation_fraction = 1-training_fraction-test_fraction
  if validation_fraction < 0:
    total = training_fraction + test_fraction
    training_fraction /= total
    validation_fraction = 0
    test_fraction /= total

  # Deep copy
  data = data_original[:]
  random.shuffle(data)
  
  n_data = len(data)
  n_training = int(training_fraction*n_data)
  n_validation = int(validation_fraction*n_data)
  n_test = int(test_fraction*n_data)
  new_total = n_training + n_validation + n_test
  diff = n_data - new_total
  n_training += diff

  training_data = data[:n_training]
  validation_data = data[n_training:-n_test]
  test_data = data[-n_test:]

  return (training_data, validation_data, test_data)

def get_neural_network_data(vault_path):
  dat_files = get_all_dat_files(vault_path)
  all_instances = [ read_feature_vector(vault_path+"/"+x, 25) \
    for x in dat_files ]
  (training_data, validation_data, test_data) = \
    split_data(all_instances, 0.6, 0.2)
  return (training_data, validation_data, test_data)

def common_elements(list1, list2):
  return [element for element in list1 if element in list2]

def shuf(data):
  b = data[:]
  random.shuffle(b)
  return b

def numpy_instance(instance):
  """
  Converts an instance defined with lists to an instance defined with 
  numpy.ndarray.
  """
  new_instance = (numpy.array(instance[0]), numpy.array(instance[1]))
  return new_instance

if __name__ == '__main__':
  """
  Testing grounds.
  """
  lists = read_feature_vector('../vault/v87.dat', 25)
  nda = numpy_instance(lists)
  print nda

  dats = get_all_dat_files('../vault')
  print len(dats)

  (dats2, dats3) = leave_k_out(dats,50,10)

  print len(dats)
  print len(dats2)
  print len(dats3)

  orig = dats2
  dats2 = shuf(dats2)
  print  orig == dats2
  print orig[0]
  print dats2[0]

  (tr, v, te) = split_data(dats,0.6,0.2)
  print tr
  print v
  print te
  print len(tr)
  print len(v)
  print len(te)

  print common_elements(tr,v)
  print common_elements(te,v)
  print common_elements(tr,te)

  tr,v,te = get_neural_network_data("../vault")
  print tr
  print v
  print te
  print len(tr)
  print len(v)
  print len(te)