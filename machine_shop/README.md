Meshes for OpenFOAM simulations are generated in this folder using Gmsh.  

Main usage:  

source generate_mesh.sh

Script explanations:  

1. integrate_inputs.py: Retrieves input specifications from the bridge and 
  codifies it as gmsh inputs.  
2. generate_mesh.sh: Be sure to use 'source generate_mesh.sh' to enable use of 
  aliases (on my system I have set 'gmsh' as an alias). Runs gmsh on your 
  geometry and outputs the mesh file to the bridge.  

Fixed parameters:  

1. 5 elements.  
2. Tube (leading edge) radius of 0.5 in.  
3. Joint distance factor of 4. This describes the length of the transition from 
  the round leading edge to the thin wing section.    

To view the geometry currently on file, use:  

gmsh main.geo  

