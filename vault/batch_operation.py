#!/usr/bin/python

"""
Executes single_operation.sh on all of the input arguments, passing each input 
argument as the input argument of single_operation.sh.
"""

import os
import sys

if len(sys.argv) < 2:
  print "No arguments!"
  sys.exit()

for item in sys.argv[1:]:
  os.system("./single_operation.py "+item)