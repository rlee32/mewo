#!/usr/bin/python

from openfoam_python import fvSchemes
from openfoam_python import controlDict
from openfoam_python import fvSolution

fvSchemes.second_order_spatial()
controlDict.set_courant_number("system/controlDict", 1)
controlDict.set_force_output_interval("system/controlDict", 50)
fvSolution.set_piso_correctors(5)
