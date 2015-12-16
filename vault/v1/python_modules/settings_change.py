#!/usr/bin/python

import os
import sys

def set_end_time(new_end_time, case_path="./"):
  controlDict_path = case_path+"/system/controlDict"
  output_file = open(controlDict_path+"_temp", 'w')
  with open(controlDict_path, 'r') as input_file:
    for line in input_file:
      if ("endTime" in line) and ("stopAt" not in line):
        time_value = line.split()[1]
        new_line = line.replace(time_value, str(new_end_time)+";")
        output_file.write(new_line)
      else:
        output_file.write(line)
  output_file.close()
  os.system("mv "+controlDict_path+"_temp "+controlDict_path)
  return

def set_write_interval(new_write_interval, case_path="./"):
  controlDict_path = case_path+"/system/controlDict"
  output_file = open(controlDict_path+"_temp", 'w')
  with open(controlDict_path, 'r') as input_file:
    for line in input_file:
      if ("writeInterval" in line):
        time_value = line.split()[1]
        new_line = line.replace(time_value, str(new_write_interval)+";")
        output_file.write(new_line)
      else:
        output_file.write(line)
  output_file.close()
  os.system("mv "+controlDict_path+"_temp "+controlDict_path)
  return


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
