#!/usr/bin/python

import os
import sys

def check_file(path):
  if not os.path.isfile(path):
    print "Could not find '"+path+"'! Exiting."
    sys.exit()
  return

def check_inputs(arguments):
  if len(arguments) < 2:
    print "Please input feature vector file!"
    sys.exit()
  if not os.path.isfile(arguments[1]):
    print "Could not find '"+arguments[1]+"'!"
    sys.exit()
  return

def read_feature_vector(file_name):
  with open(file_name) as f:
    content = f.readlines()
  f.close()
  content = [x.strip() for x in content if x[0] != "#"]
  return content

def write_gmsh_input(feature_vector, gmsh_input_file):
  chords = feature_vector[0:5]
  aoas = feature_vector[5:10]
  x_gaps = feature_vector[10:15]
  y_gaps = feature_vector[15:20]
  spans = feature_vector[20:25]
  with open(gmsh_input_file, 'w') as f:
    f.write("// Element-wise parameters.\n")
    f.write("element_chords[] = {"+', '.join(chords)+"};\n")
    f.write("element_aoas[] = {"+', '.join(aoas)+"};\n")
    f.write("gap_x[] = {"+', '.join(x_gaps)+"};\n")
    f.write("gap_y[] = {"+', '.join(y_gaps)+"};\n")
    f.write("cloth_span_angles[] = {"+', '.join(spans)+"};")
  f.close()
  return



# check_inputs(sys.argv)

# feature_vector = read_feature_vector(sys.argv[1])

check_file("../bridge/physical_inputs.dat")

feature_vector = read_feature_vector("../bridge/physical_inputs.dat")

write_gmsh_input(feature_vector, "physical_inputs.geo")
