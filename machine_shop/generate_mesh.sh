#!/bin/bash

./integrate_inputs.py

gmsh main.geo -tol 1e-10 -3 -o ../bridge/main.msh

