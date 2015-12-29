# mewo
Multi-Element Wing Optimizer

Here I optimize a multi-element wing using CFD and machine learning.  

To obtain a single result using mesh refinement and in parallel:  

'source par_dyn_sched.sh'  

There will be various optimization scripts:  
1. optimize_feature.py: Optimizes a single feature. 
2. sweep_optimization.py: Optimizes for all features sequentially.
3. element_sweep.py: Optimizes for all features, but in a per-element ordering.

You must first make sure the gmsh path is correctly defined in 
'machine_shop/generate_mesh.sh'.

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
