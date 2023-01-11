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

### Part 2: generating inputs
Run the command below to produce the input files:
```
python3 Code_S3_input_generator_social_evolution.py
python3 Code_S4_input_generator_env_change.py
```

#### File structure and naming
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

### Part 3: executing simulations
Run the command below to start all simulations:
```
python3 Code_S5_subprocess_social_conquest.py
```

### Part 4: plotting

