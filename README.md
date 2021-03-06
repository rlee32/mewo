# mewo: Multi-Element Wing Optimizer

Here I optimize a multi-element wing using CFD and machine learning techniques.  
A neural network model is in the works, but currently a simple hill-climbing 
optimization procedure is employed.  

The modules are divided into their own folders:  
1. wind_tunnel: OpenFOAM CFD simulation  
2. machine_shop: Gmsh meshing  
3. brain: Python neural network  
4. vault: CFD results  
5. bridge: temporary file storage for interaction between modules / folders.  
6. schedule: contains the to-do simulations as feature vectors.   

## Main Usage

To improve all features, grouped by element:  

sweep_element_optimization.py <start_features.txt>  

## Details

You must first make sure the gmsh path is correctly defined in 
'machine_shop/generate_mesh.sh'.  

To obtain a single result using mesh refinement and in parallel:  

'source par_dyn_sched.sh'  

Other optimization scripts:  
1. optimize_feature.py: Optimizes a single feature.  
2. sweep_optimization.py: Optimizes for all features sequentially 
  (feature vector order).  
3. element_optimization.py: Optimizes for all features squentially for a 
  single element.  

The CFD solver parameters and general meshing characteristics are fixed for 
each optimization study. See the individual module readmes for details.  

## Neural Network Performance

At the time of writing this section, I tried there were only 88 total 
instances to train, validate, and test on. 
The results are a bit inconclusive.
After playing with the parameters a little bit, it seems that 
currently the parameters do not affect the results that much, and that may be 
due to too little data. 
The training and test errors are usually off on the order of a few percent, 
but occasionally you get errors on the order of 10%. 
With more training data, I think the results will be more consistent. 
Using more hidden layers did not produce a noticeable trend in results. 
Much of the training data are 'near' each other in the feature set; much of the 
data were produced by changing a single feature by a step change.  

Ultimately, the utility of the neural network is to reduce the number of 
expensive simulations (or physical iterations) required to improve designs.
I intend to use the neural network to seek out better solutions 'near' current 
solutions.
Then, a simulation on this prediction will be performed. These steps 
are repeated until some optimality condition is met. 
In the process, the neural network is improved by the inclusion of more data.
This method is hopefully faster and more effective than basic iterative 
optimization methods that involve many simulations, each of which are 
expensive.  

One thing to try is to omit outlier data or 'far away' data, since we are 
only interested in the behavior nearby the current operating point.  

## Software
The code here was run successfully with:   
- Python 2.7.6  
- OpenFOAM 3.0.0  
- Gmsh 2.11  
