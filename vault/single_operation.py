#!/usr/bin/python

# Assuming zip file

import os
import sys

zipfile = sys.argv[1]+".zip"
os.system("unzip "+zipfile)
folder = zipfile.split('.')[0]

os.chdir(folder)
os.system('cp -r ../../wind_tunnel/0 ./')
os.chdir('../')

os.system('zip -r '+folder+" "+folder)
os.system('rm -r '+folder)