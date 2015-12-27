#!/usr/bin/python

from openfoam_python import fvSchemes
from openfoam_python import controlDict
from openfoam_python import fvSolution

fvSchemes.first_order_spatial()
controlDict.set_courant_number("system/controlDict", 5)
controlDict.set_force_output_interval("system/controlDict", 5)
fvSolution.set_piso_correctors(8)
