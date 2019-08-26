This project attempts to model the influence panspermia has on life within a multi-planet system. Using this, we can determine cases unique to systems with panspermia, showing that system has been influenced by panspermia when detected. This project uses a Poisson distribution to simulate whether an abiogenesis, panspermia, extinction event has occurred. The likelihood of each event occurring can be modified by changing tau, the average time for an event to occur once. 

Although the programs can be run without any installations, using MPI (message passing interface) is recommended for efficiency.

The DistributionFunction contains the functions to model the system of planets. Using probability functions for abiogenesis, panspermia, and extinction, it counts the number of planets inhabited at the end of each time step over the duration of the trial, then repeats the trials the number of times requested. At the end of all trials, it returns a distribution of the number of planets inhabited at a given time. The required inputs are tau for each event, number of planets, number of trials, duration of each trial, and length of each timestep.

The DistributionSimulator, with or without MPI, is the code that uses the DistributionFunction to record the 
