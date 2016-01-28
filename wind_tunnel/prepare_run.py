#!/usr/bin/python

# We assume this is called from the case directory.
# Call this before calling run.py.

import os
import sys
from openfoam_python import boundary_conditions
from openfoam_python import controlDict
from openfoam_python import file_operations

os.system("mkdir logs")

def transfer_and_convert_mesh():
  mesh_path = "../bridge/main.msh"
  if os.path.isfile(mesh_path):
    print "Converting mesh."
    os.system("mv "+mesh_path+" main.msh")
    os.system("gmshToFoam main.msh > logs/gmshToFoam")
  return
transfer_and_convert_mesh()

# def fix_boundary():
#   print "Fixing BC."
#   boundary_file = "constant/polyMesh/boundary"
#   boundary_conditions.modify_empty_bc(boundary_file, "front_and_back", \ 
#     "empty")
#   boundary_conditions.modify_empty_bc(boundary_file, "wing", "wall")
#   return
# fix_boundary()

os.system("changeDictionary > ../bridge/changeDictionaryLog.txt")

os.system("mv ../bridge/geometry.dat ./geometry.dat")