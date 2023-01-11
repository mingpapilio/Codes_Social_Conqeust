## File discription

There are four types of codes in this folder:

1. Codes for all biological processes (S1 and S2)
2. Codes for generating simple inputs for simulation codes (S3 and S4)
3. Codes for executing simulations (S5)
4. Codes for plotting (S6 and S7)

## File execusion

### Compiling
Both S1 and S2 file would only need to be compiled once, simulations are run by calling the compiled files and the input files. Compiled files are called __ca.out__ or __rd.out__, depends on the type of cooperation being modelled. 

In the case of GNU compiler, the commands are:

```{
_g++ -std=c++11 Code_S1_CollectiveActionSimulation.cpp -O2 -o ca.out_
_g++ -std=c++11 Code_S2_ResourceDefenseSimulation.cpp -O2 -o rd.out_
}```

### Generating inputs

### Execution

### Plotting
