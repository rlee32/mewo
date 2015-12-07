Meshes for OpenFOAM simulations are generated in this folder using Gmsh.

The python and bash scripts provide an interface:   

1. integrate_inputs.py: Retrieves 'physical_inputs.dat' from '../bridge' and 
  codifies it as gmsh inputs.  
2. generate_mesh.sh: Be sure to use 'source generate_mesh.sh' to enable use of 
  aliases (on my system I have set 'gmsh' as an alias). Runs gmsh on your 
  geometry and outputs the mesh file to '../bridge'.  