#!/usr/bin/python

# We assume this is called from the case directory.

from openfoam_python import file_operations

print "Cleaning the case."
file_operations.clean_case()
