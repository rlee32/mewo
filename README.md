# mewo
Multi-Element Wing Optimizer

Here I use machine learning techniques to guide optimization of multi-element 
wing configurations using a CFD-based approach.

I plan to use neural networks to provide a nonlinear model of performance given 
a vector of features.

Since the overall CFD cost is anticipated to be much higher than the learning 
phase, we will use Python to implement the neural network, since it is easy to 
use I/O operations in. We will be storing CFD data points as files.

We fix some parameters:  

- 5 elements.  
- Tube (leading edge) radius of 0.5 in.  
- Joint distance factor of 4. This describes the length of the transition from 
  the round leading edge to the thin wing section.  

## Construction of the Neural Network

All features are combined in a one-layer neural network.

##Feature Vector File Format:  

<List of element chords (m)>  

<List of element angles of attack (deg)>  

<List of adjacent element gaps in x (m)>  

<List of adjacent element gaps in y (m)>  

<List of element inner span angles (affects camber) (deg)>  



To maintain usage of aliases, run shell scripts using 'source'!



Folder functions:  
- cfd: Holds the OpenFOAM case files. Simulation data is stored here.  
- bridge: This folder is the repository for all temporary files that need to be 
  communicated between other folders.  
- neural_network: holds the Python files that constitute the neural network.  
- mesh_factory: holds the Gmsh code to generate the CFD mesh.  
- data_points: This holds permanent 'data points' from CFD simulations.  



The code here was run successfully with:  
- Python 2.7.6  
- OpenFOAM 3.0.0  
- Gmsh 2.11  
