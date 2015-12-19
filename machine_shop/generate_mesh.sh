#!/bin/bash

./integrate_inputs.py

echo "Running Gmsh."
gmsh main.geo -tol 1e-10 -3 -o main.msh > mesh_log

mv geometry.dat ../bridge/
mv main.msh ../bridge/
mv mesh_log ../bridge/
