#!/usr/bin/python

import os
import sys

def read_file(file_name):
  with open(file_name) as f:
    content = f.readlines()
  f.close()
  return content

def modify_empty_bc(file_path, patch_name, new_bc):
  file_contents = read_file(file_path)
  section_flag = False
  with open(file_path, 'w') as f:
    for line in file_contents:
      if patch_name in line:
        section_flag = True
      if section_flag and "type" in line:
        line = line.replace("patch", new_bc)
      if section_flag and "physicalType" in line:
        line = line.replace("patch", new_bc)
      if "}" in line and section_flag == True:
        section_flag = False
      f.write(line)
  f.close()
  return

boundary_file = "constant/polyMesh/boundary"

modify_empty_bc(boundary_file, "front_and_back", "empty")
modify_empty_bc(boundary_file, "wing", "wall")