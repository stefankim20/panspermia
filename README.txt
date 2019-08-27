This project attempts to model the influence panspermia has on life within a multi-planet system. Using this, we can determine cases unique to systems with panspermia, showing that system has been influenced by panspermia when detected. This project uses a Poisson distribution to simulate whether an abiogenesis, panspermia, extinction event has occurred. The likelihood of each event occurring can be modified by changing tau, the average time for an event to occur once. 

Although the programs can be run without any installations, using MPI (message passing interface) is recommended for efficiency.

The DistributionFunction contains the functions to model the system of planets. Using probability functions for abiogenesis, panspermia, and extinction, it counts the number of planets inhabited at the end of each time step over the duration of the trial, then repeats the trials the number of times requested. At the end of all trials, it returns a distribution of the number of planets inhabited at a given time. The required inputs are tau for each event, number of planets, number of trials, duration of each trial, and length of each timestep.

The DistributionSimulator, with or without MPI, is the code that uses the DistributionFunction and records the results converted into probabilities. It also generates a bar chart comparing the results with and without panspermia, the blue being the case with panspermia and red without.

The parameters for the simulation can be set at the top of the DistributionSimulator document, under "variables." The array "exp" contains the exponents of the tau of each event that will be simulated. "num" is the number of planets in the system, "trials" is the number of trials FOR EACH CORE, "years" is the length of the simulation and "t_step" is length of each time step, both in Gyr. "cores" is the number of cores that will run the program.
For example, with "exp" = [-1,0,1], "num" = 3, "trials" = 500, "years" = 5, "t_step" = 10**-3, "cores" = 2, the program will run each combination of tau = 0.5, 5, 50 Gyr for each of abiogenesis, panspermia, and extinction, leadingg to 9 separate cases. For each case, there will be three planets, modeled for 500 trials with 2 cores for a total of 1000 trials, each trial for 5 Gyr evaluated every 1 Myr.

After setting the "variables" the program can be run with MPI, "mpiexec -n N python DistributionSimulator.py," where N is the number put for "cores." It can also be run without MPI, in which case the program will be run on only one core and the NoMPI version should be used.

The LinearInterpolation program uses scipy.interpolate.LinearNDInterpolate to interpolate the results of the simulations from  DistributionSimulator. 
