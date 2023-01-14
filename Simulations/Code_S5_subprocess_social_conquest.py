import time
import json
import subprocess

def main():
    scenario = 1    # 1: social evlution; 2: environmental change
    out_type = 1    # 1: population final state; 2: time series
    sociality_type = 1  # 1: non-social; 2: social (collective action); 3: social (resource defense)
    
    scenario_abbr = {1: "se", 2: "ec"}  # 1: social evlution; 2: environmental change
    out_type_abbr = {1: "pfs", 2: "ts"} # 1: population final state; 2: time series
    sociality_abbr = {1: "ns", 2: "ca", 3: "rd"}    # 1: non-social; 2: social (collective action); 3: social (resource defense)
    
    s_time = time.time()

    input_list_file_name = f"data/input_file_list_{scenario_abbr[scenario]}_{out_type_abbr[out_type]}_{sociality_abbr[sociality_type]}.txt"
    output_list_file_name = f"data/output_file_list_{scenario_abbr[scenario]}_{out_type_abbr[out_type]}_{sociality_abbr[sociality_type]}.txt"

    # determine the compiled program to use
    if sociality_abbr[sociality_type] == "ns":
        exe_filename = "ca.out"
    else:
        exe_filename = f"{sociality_abbr[sociality_type]}.out"

    with open(input_list_file_name, "r") as fin:
        input_list = json.load(fin)

    with open(output_list_file_name, "r") as fout:
        output_list = json.load(fout)

    assert len(input_list) == len(output_list)

    for i in range(len(input_list)):
        ref_time = time.time()
        fi = open(input_list[i],  "r")
        fo = open(output_list[i], "w")
        subprocess.run([f"./{exe_filename}"], stdin=fi, stdout=fo)
        fi.close()
        fo.close()
        print(f"[{i+1}/{len(input_list)}] time: {time.strftime('%Mm%Ss', time.gmtime(time.time()-ref_time))}")

    e_time = time.time()
    print(f"Total consumed time: {time.strftime('%Hh%Mm%Ss', time.gmtime(e_time-s_time))}")

if __name__ == "__main__":
    main()