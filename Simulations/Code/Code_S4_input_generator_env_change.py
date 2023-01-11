import os
import json
import time

def main():
    out_type = 1    # 1: population final state; 2: time series of population state
    res_mean = [7, 13]      # the mean of the environmental resource availability
    res_half_var_range = [[1, 4], [1, 7]]  # the half variation range of the environmental resource availability [[the half ranges used for simulations as res_mean == res_mean[0]], [the half ranges used for simulations as res_mean == res_mean[1]], ...]
    res_mean_offset = [-1, -2, -3]    # the change in the mean of the environmental resource availability (when environmental change happens)
    res_half_var_range_offset = [1, 2, 3]   # the change in the half variation range of the environmental resource availability (when environmental change happens)
    init_coop_prop = 0.5    # the initial proportion of cooperators in the population
    env_change_time = 10000     # the time when the mean and the variation range of the environmental resource availability. if env_change_time == end_time, no change happens.
    end_time = 10100    # the end time of the simulation
    init_replic = 0     # the initial serial number of the simulation replication. Useful on restarts.
    replic_num = 100    # total number of replications
    span = 1    # the time interval which determines the frequency of the time series output

    sociality_type = [1, 2, 3]  # 1: non-social, 2: collective action, 3: resource defense

    # parameters related to sociality type
    sociality_abbr = {1: "ns", 2: "ca", 3: "rd"}
    sociality = {1: 0, 2: 1, 3: 1}   # the sociality of the whole population: [non-social, collective action, resource defense]
    coop_efficiency = {1: 0, 2: 2.5, 3: 10}  # the efficiency of transfering cooperation efforts to cooperation benefits
    cost_rate = {1: 0, 2: 0.7, 3: 0.16}  # the percentage decrease in the reproduction rate caused by per unit cooperation degree

    out_type_abbr = {1: "pfs", 2: "ts"}

    data_path = f"data/env_change/raw"
    if not os.path.isdir(data_path):
        os.makedirs(data_path)

    for s_type in sociality_type:

        input_list = []
        output_list = []

        for i, rm in enumerate(res_mean):
            for rhvr in res_half_var_range[i]:
                file_name_suffix = f"{out_type_abbr[out_type]}_{rm:02}{rhvr:02}m0p0"
                input_file_name = f"{data_path}/{sociality_abbr[s_type]}i_{file_name_suffix}.txt"
                output_file_name = f"{data_path}/{sociality_abbr[s_type]}o_{file_name_suffix}.csv"
                input_list.append(input_file_name)
                output_list.append(output_file_name)
                with open(input_file_name, "w") as f:
                    f.write(f"{out_type}\n{rm}\t{rhvr}\t{0}\t{0}\t{coop_efficiency[s_type]}\t{cost_rate[s_type]}\t{init_coop_prop}\t{env_change_time}\t{env_change_time}\t{init_replic}\t{replic_num}\t{span}\t{sociality[s_type]}\n")

                for rmo in res_mean_offset:
                    file_name_suffix = f"{out_type_abbr[out_type]}_{rm:02}{rhvr:02}m{abs(rmo)}p0"
                    input_file_name = f"{data_path}/{sociality_abbr[s_type]}i_{file_name_suffix}.txt"
                    output_file_name = f"{data_path}/{sociality_abbr[s_type]}o_{file_name_suffix}.csv"
                    input_list.append(input_file_name)
                    output_list.append(output_file_name)
                    with open(input_file_name, "w") as f:
                        f.write(f"{out_type}\n{rm}\t{rhvr}\t{rmo}\t{0}\t{coop_efficiency[s_type]}\t{cost_rate[s_type]}\t{init_coop_prop}\t{env_change_time}\t{end_time}\t{init_replic}\t{replic_num}\t{span}\t{sociality[s_type]}\n")

                for rhvro in res_half_var_range_offset:
                    file_name_suffix = f"{out_type_abbr[out_type]}_{rm:02}{rhvr:02}m0p{rhvro}"
                    input_file_name = f"{data_path}/{sociality_abbr[s_type]}i_{file_name_suffix}.txt"
                    output_file_name = f"{data_path}/{sociality_abbr[s_type]}o_{file_name_suffix}.csv"
                    input_list.append(input_file_name)
                    output_list.append(output_file_name)
                    with open(input_file_name, "w") as f:
                        f.write(f"{out_type}\n{rm}\t{rhvr}\t{0}\t{rhvro}\t{coop_efficiency[s_type]}\t{cost_rate[s_type]}\t{init_coop_prop}\t{env_change_time}\t{end_time}\t{init_replic}\t{replic_num}\t{span}\t{sociality[s_type]}\n")

        input_list_file_name = f"data/input_file_list_ec_{out_type_abbr[out_type]}_{sociality_abbr[s_type]}.txt"
        output_list_file_name = f"data/output_file_list_ec_{out_type_abbr[out_type]}_{sociality_abbr[s_type]}.txt"
        with open(input_list_file_name, "w") as fin:
            json.dump(input_list, fin)
        with open(output_list_file_name, "w") as fout:
            json.dump(output_list, fout)


        
if __name__ == "__main__":
    main()