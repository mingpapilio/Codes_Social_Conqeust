## File discription

There are four types of codes in this folder:

1. The biological processes (S1 and S2)
2. Generating inputs for simulation codes (S3 and S4)
3. Executing simulations (S5)
4. Plotting (S6 and S7)

## File execusion

### Part 1: compiling
Both S1 and S2 file would only need to be compiled once, simulations are done by calling the compiled files and the input files. Therefore, compiled files should be named as __ca.out__ and __rd.out__, standing for collective action and resource defense (i.e., the two types of cooperation in the paper). 

In the case of GNU compiler, the commands are:

```
g++ -std=c++11 Code_S1_CollectiveActionSimulation.cpp -O2 -o ca.out
g++ -std=c++11 Code_S2_ResourceDefenseSimulation.cpp -O2 -o rd.out
```

### Part 2.1: generating inputs
Run the command below to produce the input files and folders:
```
python3 Code_S3_input_generator_social_evolution.py
python3 Code_S4_input_generator_env_change.py
```

### Part 2.2: file structure and naming rules
The output of these python codes are structured as:
```
├── Data
│   ├── input_file_list_{scenario}_{out_type}_{sociality_type}.txt
│   ├── output_file_list_{scenario}_{out_type}_{sociality_type}.txt
│   ├── social_evolution
│   │   ├── ca
│   │   ├── rd
│   │   ├── ns
│   ├── env_change
│   │   ├── ca
│   │   ├── rd
│   │   ├── ns
```
where the two text files are lists of input and output filenames. The subfolders contain inputs files for different types of simulation: __social_evolution__ is used for modelling various resource availability and variability; __env_change__ is used for modelling the cases of climate change. Within each subfolder, there are three sub-subfolders: ca, rd, and ns. They stand for collective action, resource defense, and non-social, respectively. The simulation inputs and outputs are located in these folders (at this step you would only have the input files because simulations haven't been executed). 

Regarding the brackets in the input/output_file_list, __scenario__ specifies the type of simulation: __ec__ for env_change, __se__ for social evolution. __out_type__ specifies the type of output: __pfs__ for population final state (i.e., the last time step), __ts__ for the full time series. __sociality_type__ specifies the type of sociality: __ca__ for collective action, __rd__ for resource defense, and __ns__ for non-social.

Lastly, the naming rules of input/output files are as following:
```
{sociality_type}{file_type}_{out_type}_{res_mean}{res_half_var_range}{res_mean_offset}{res_half_var_range_offset}.txt
```
where __sociality_type__ and __out_type__ are identical to the description in input/output file list. __file_type__ specifies whether the file is an input or output in a single letter: __i__ or __o__. Next, __res_mean__ specifies the average available resource and __res_half_var_range__ specifies the resource variability, both are in the form of two-digit numbers. The final bit of the file name, __res_mean_offset__ and __res_half_var_range_offset__, specifies the degree of climate change and are only used for __env_change__ simulations. If any of them are __xx__, it means unspecified, which is usually the case when it is a variable in the simulations. In an example file name, __cai_pfs_0701m0p1.txt__, the name would mean the file is an input file for collective action simulation with climate change; with average resouece of 7, half range of resource variability (uniform distribution) of 1, average offset (degree of deviation, or amount of decrease in mean) of 0, and variability offset (degree of deviation, or amount of increase in var) of 1.

### Part 3: executing simulations
Run the command below to start all simulations:
```
python3 Code_S5_subprocess_social_conquest.py
```
Option of simulation types and sociality types can be modified in the code file. Note that the __out_type__ between Code_S5 and Code_S3/Code_S4 need to be identical otherwise there will be no matching input file for executing simulations.

### Part 4: plotting
There are two plotting codes, one for social evolution simulations, __S6__, and the other for climate change simulations, __S7__. Each jupyter notebook contains code for concatenating results files and making figures. 
