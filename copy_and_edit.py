#!/usr/bin/python

import os
import sys

if len(sys.argv) != 2:
  print "Please input a feature vector file already in the vault to copy."
  sys.exit()

feature = sys.argv[1]

os.system("cp vault/"+feature+" schedule/new.dat")

os.system("nano schedule/new.dat")
