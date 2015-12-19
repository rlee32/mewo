#!/usr/bin/python

import os
import sys



def change_line(file_path, included_strings, excluded_strings, replacement):
  """
  Goes through file_path line-by-line and if all of included_strings are in 
  the line and all of excluded_strings are not in the line, then the whole line 
  is replaced by replacement.
  Assumes file_path+'_temp' is not already a file.
  """
  if not os.path.isfile(file_path):
    print file_path+" file not found!"
    return
  temp_path = file_path+"_temp"
  temp_file = open(temp_path, 'w')
  with open(file_path, 'r') as f:
    for line in f:
      if all([x in line for x in included_strings]) and \
        all([x not in line for x in excluded_strings]):
        temp_file.write(replacement)
      else:
        temp_file.write(line)
  temp_file.close()
  os.system("mv "+temp_path+" "+file_path)
  return



def set_grid_spacings(fine, coarse):
  """
  We assume the inputs file is in the same directory.
  """
  change_line("numerical_inputs.geo", ["wing_grid"], ["inner"], \
    "wing_grid = "+str(fine)+";\n")
  change_line("numerical_inputs.geo", ["inner_wing_grid"], [], \
    "inner_wing_grid = "+str(coarse)+";\n")
  return



if len(sys.argv) != 3:
  print "Please input 2 arguments; the fine and coarse grid size."
  sys.exit()
set_grid_spacings(sys.argv[1],sys.argv[2])