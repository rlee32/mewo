#!/usr/bin/python

from openfoam_python import fvSchemes
from openfoam_python import controlDict

fvSchemes.first_order_spatial()
controlDict.set_courant_number("system/controlDict", 10)
controlDict.set_force_output_interval("system/controlDict", 5)
