## Introduction

This is a modified version of code that can be found on:  
https://github.com/mnielsen/neural-networks-and-deep-learning/blob/master/src  

The feature vectors are obtained from the .dat files in the vault, where each 
.dat file represents a single instance.

## Performance

At the time of writing this section, there were only 88 total instances to 
train, validate, and test on. Still, the performance was promising. After 
playing with the parameters a little bit, it seems that currently the 
parameters do not affect the results that much. The training and test error are 
usually off by a few percent or less, but occasionally you get errors on the 
order of 10%. With more instances, I think the results will be more reliable. 
However, much of the training data are 'near' each other in the feature set, 
and this fact may artificially inflate the accuracies.

## Scaling

The feature data must be scaled first to [0,1]. The results must also be scaled 
to [0,1]. This is handled in the feature_scaling.dat and result_scaling.dat 
files. They both are specified as follows:

<start_index>, <end_index>. <start_value>, <end_value>

So the following specification:  

0, 4, -1, 1  
5, 10, -2, 5  

means starting from index 0 and ending at index 4, we expect values to be 
between -1 and 1. 
The program will scale appropriately so that [-1,1] becomes [0,1]. 
Then starting from index 5, we scale so that [-2, 5] becomes [0,1]. 
Hopefully this is clear. 
