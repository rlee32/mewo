# mewo
Multi-Element Wing Optimizer

Here I optimize a multi-element wing using a CFD and machine learning.  

The modules are divided into their own folders:  
1. wind_tunnel: OpenFOAM CFD simulation  
2. machine_shop: Gmsh meshing  
3. brain: Python neural network  
4. vault: CFD results  
5. bridge: temporary file storage for interaction between modules / folders.
6. schedule: contains the to-do simulations as feature vectors.

The CFD solver parameters and general meshing characteristics are fixed for 
each optimization study. See the modules for details.

The code here was run successfully with:  
- Python 2.7.6  
- OpenFOAM 3.0.0  
- Gmsh 2.11  
