#!/usr/bin/python

import os

def get_some_file():
  files = [ x for x in os.listdir('./') if '.dat' in x ]
  return files[0]

file_to_transfer = get_some_file()
print "Transferring: "+file_to_transfer
os.system('mv '+file_to_transfer+' ../bridge/physical_inputs.dat')
