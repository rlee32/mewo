#!/bin/bash

./integrate_inputs.py

echo "Running Gmsh."
gmsh main.geo -tol 1e-10 -3 -o ../bridge/main.msh > ../bridge/mesh_log

mv geometry.dat ../bridge/
