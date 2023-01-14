import pandas as pd

def concat_all_df(f_list, ffname):
    for i, v in enumerate(f_list):
        df = pd.read_csv(v)
        if i == 0:
            dfh = df
        else:
            dfh = pd.concat([dfh, df], axis = 0, ignore_index=True)

    dfh.to_csv(ffname, index=False)