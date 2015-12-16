#!/usr/bin/python
import os
import copy
def make_iterated_name(base, full):
  # takes name such as 'v<id>.dat' and outputs 'v<id+1>.dat'. If no number, 
  # then 'v.dat' becomes 'v0.dat'.
  name = full.split('.')[0]
  extension = full.split('.')[1]
  id_str = name.replace(base,'')
  id_next = 0
  if id_str != '':
    id_next = int(id_str)+1
  return base+str(id_next)+"."+extension
def write_feature_vector(vec, path):
  if os.path.isfile(path):
    print "Cannot write feature vector! File already exists!"
  else:
    with open(path, 'w') as f:
      f.write("# The ordering of the variables is hard-coded.\n")
      f.write("# Chords (m) (multiple values)\n")
      f.write("# AOAs (deg) (multiple values)\n")
      f.write("# x gaps (m) (multiple values)\n")
      f.write("# y gaps (m) (multiple values)\n")
      f.write("# Cloth span angles (for camber) (deg) (multiple values)\n")
      for v in vec:
        f.write(str(v)+"\n")
  return
def read_feature_vector(path):
  vector = []
  with open(path,'r') as f:
    for line in f:
      if '#' in line:
        continue
      else:
        vector.append(float(line))
  return vector
def perturb_element(vec, index, dd):
  vec[index] += dd
  return vec 
def perturb_each(v0, perturb):
  vectors = []
  for k in range(0,5):
    vectors.append(perturb_element(copy.deepcopy(v0), k, perturb['chord']))
  for k in range(5,10):
    vectors.append(perturb_element(copy.deepcopy(v0), k, perturb['angle']))
  for k in range(11,15):
    vectors.append(perturb_element(copy.deepcopy(v0), k, perturb['xgap']))
  for k in range(16,20):
    vectors.append(perturb_element(copy.deepcopy(v0), k, perturb['ygap']))
  for k in range(20,25):
    vectors.append(perturb_element(copy.deepcopy(v0), k, perturb['span']))
  return vectors

# Perturbation settings.
perturb = {}
perturb['chord'] = 0.05
perturb['angle'] = 2
perturb['xgap'] = 0.01
perturb['ygap'] = 0.03
perturb['span'] = 5

current_name = 'v0.dat'
vector = read_feature_vector(current_name)
perturbed = perturb_each(vector, perturb)
for v in perturbed:
  new_name = make_iterated_name('v', current_name)
  write_feature_vector(v, new_name)
  current_name = new_name