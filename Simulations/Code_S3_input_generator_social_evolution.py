import os
import json
import time

def main():
    out_type = 1    # 1: population final state; 2: time series of population state
    res_mean = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]      # the mean of the environmental resource availability
    res_mean_offset = 0     # the change in the mean of the environmental resource availability (when environmental change happens)
    res_half_var_range_offset = 0   # the change in the half variation range of the environmental resource availability (when environmental change happens)
    init_coop_prop = 0.5    # the initial proportion of cooperators in the population
    env_change_time = 10000     # the time when the mean and the variation range of the environmental resource availability. if env_change_time == end_time, no change happens.
    end_time = 10000    # the end time of the simulation
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

    for s_type in sociality_type:
        if not os.path.isdir(f"data/social_evolution/{sociality_abbr[s_type]}"):
            os.makedirs(f"data/social_evolution/{sociality_abbr[s_type]}")

        input_list = []
        output_list = []

        for rm in res_mean:
            file_name_suffix = f"{out_type_abbr[out_type]}_{rm:02}xxm0p0"
            input_file_name = f"data/social_evolution/{sociality_abbr[s_type]}/{sociality_abbr[s_type]}i_{file_name_suffix}.txt"
            output_file_name = f"data/social_evolution/{sociality_abbr[s_type]}/{sociality_abbr[s_type]}o_{file_name_suffix}.csv"
            input_list.append(input_file_name)
            output_list.append(output_file_name)

            with open(input_file_name, "w") as f:
                f.write(f"{out_type}\n")

            for rhvr in range(rm+1):    # resource half variation range
                with open(input_file_name, "a") as f:
                    f.write(f"{rm}\t{rhvr}\t{res_mean_offset}\t{res_half_var_range_offset}\t{coop_efficiency[s_type]}\t{cost_rate[s_type]}\t{init_coop_prop}\t{env_change_time}\t{end_time}\t{init_replic}\t{replic_num}\t{span}\t{sociality[s_type]}\n")

        input_list_file_name = f"data/input_file_list_se_{out_type_abbr[out_type]}_{sociality_abbr[s_type]}.txt"
        output_list_file_name = f"data/output_file_list_se_{out_type_abbr[out_type]}_{sociality_abbr[s_type]}.txt"
        with open(input_list_file_name, "w") as fin:
            json.dump(input_list, fin)
        with open(output_list_file_name, "w") as fout:
            json.dump(output_list, fout)

        
if __name__ == "__main__":
    main()