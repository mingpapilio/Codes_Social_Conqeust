import math
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def OrgResM(fname):
    df = pd.read_table(fname, header=None, sep='\t').replace(-1, np.nan)
    table = np.zeros([30, 21])
    dfo   = pd.DataFrame(table, columns = ["bK", "CostRate", "Status", "pSizeM", "pSizeSD", "pSizeU", "pSizeL", 
                                           "cPropM", "cPropSD", "cPropU", "cPropL", "cDegM", "cDegSD", "cDegU", "cDegL", 
                                           "resM", "resSD","rSizeM", "rSizeSD", "rSizeU", "rSizeL"])
    rd = df.iloc[:,5].max()+1
    rmin = df.iloc[:,2].min()
    rmax = df.iloc[:,2].max()

    r = 0
    for i in range(rmax-rmin+1):
        dfo.loc[i, ["bK", "CostRate", "Status"]]     = list(df.iloc[0, [0,1,4]])
        dfo.loc[i, ["pSizeM", "cPropM", "cDegM"]]    = list(df.iloc[range(r, r+rd), [6,7,8]].mean())
        dfo.loc[i, ["pSizeSD", "cPropSD", "cDegSD"]] = list(df.iloc[range(r, r+rd), [6,7,8]].std())

        err1 = 1.959964*dfo.loc[i, ["pSizeSD", "cPropSD", "cDegSD"]]/math.sqrt(rd)
        dfo.loc[i, ["pSizeU", "cPropU", "cDegU"]] = list(list(dfo.loc[i, ["pSizeM", "cPropM", "cDegM"]]) + err1)
        dfo.loc[i, ["pSizeL", "cPropL", "cDegL"]] = list(list(dfo.loc[i, ["pSizeM", "cPropM", "cDegM"]]) - err1)

        dfo.loc[i,"resM"] = df.iloc[r,2]
        dfo.loc[i,"resSD"] = math.sqrt(((df.iloc[range(r, r+rd), range(1597, 2126)].std(axis=1))**2).mean())

        tmp = df.iloc[range(r, r+rd), range(10, 539)]
        rSize = []
        for j in range(tmp.shape[0]):
            rSize.append(len(tmp.iloc[j][tmp.iloc[j]>0]))
        rg = np.array(rSize)
        dfo.loc[i,"rSizeM"] = np.mean(rg)
        dfo.loc[i,"rSizeSD"] = np.std(rg)
        err2 = 1.959964*np.std(rg)/math.sqrt(rd)
        dfo.loc[i,"rSizeU"] = np.mean(rg) + err2
        dfo.loc[i,"rSizeL"] = np.mean(rg) - err2

        r = r + rd

    dfo.to_csv(fname[:-4]+".csv", index=False)


def OrgResVar(fname):
    df = pd.read_table(fname, header=None, sep='\t').replace(-1, np.nan)
    resM = df.iloc[0,2]
    table = np.zeros([resM+1, 22])
    dfo   = pd.DataFrame(table, columns = ["bK", "CostRate", "Status", "Range", "pSizeM", "pSizeSD", "pSizeU", "pSizeL", 
                                           "cPropM", "cPropSD", "cPropU", "cPropL", "cDegM", "cDegSD", "cDegU", "cDegL", 
                                           "resM", "resSD","rSizeM", "rSizeSD", "rSizeU", "rSizeL"])
    rd = df.iloc[:,5].max()+1
    
    r = 0
    for i in range(resM+1):
        dfo.loc[i, "Range"] = df.iloc[r,3]
        dfo.loc[i, ["bK", "CostRate", "Status"]]     = list(df.iloc[0, [0,1,4]])
        dfo.loc[i, ["pSizeM", "cPropM", "cDegM"]]    = list(df.iloc[range(r, r+rd), [6,7,8]].mean())
        dfo.loc[i, ["pSizeSD", "cPropSD", "cDegSD"]] = list(df.iloc[range(r, r+rd), [6,7,8]].std())
    
        err1 = 1.959964*dfo.loc[i, ["pSizeSD", "cPropSD", "cDegSD"]]/math.sqrt(rd)
        dfo.loc[i, ["pSizeU", "cPropU", "cDegU"]] = list(list(dfo.loc[i, ["pSizeM", "cPropM", "cDegM"]]) + err1)
        dfo.loc[i, ["pSizeL", "cPropL", "cDegL"]] = list(list(dfo.loc[i, ["pSizeM", "cPropM", "cDegM"]]) - err1)
    
        dfo.loc[i,"resM"] = resM
        dfo.loc[i,"resSD"] = math.sqrt(((df.iloc[range(r, r+rd), range(1597, 2126)].std(axis=1))**2).mean())
    
        tmp = df.iloc[range(r, r+rd), range(10, 539)]
        rSize = []
        for j in range(tmp.shape[0]):
            rSize.append(len(tmp.iloc[j][tmp.iloc[j]>0]))
        rg = np.array(rSize)
        dfo.loc[i,"rSizeM"] = np.mean(rg)
        dfo.loc[i,"rSizeSD"] = np.std(rg)
        err2 = 1.959964*np.std(rg)/math.sqrt(rd)
        dfo.loc[i,"rSizeU"] = np.mean(rg) + err2
        dfo.loc[i,"rSizeL"] = np.mean(rg) - err2
    
        r = r + rd

    dfo.to_csv(fname[:-4]+".csv", index=False)