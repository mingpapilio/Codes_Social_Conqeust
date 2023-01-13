import pandas as pd
import matplotlib.pyplot as plt

def plot_properties1(fname1, fname2):
    df1 = pd.read_csv(fname1)
    df2 = pd.read_csv(fname2)
    
    plt.rcParams.update({'font.size': 16})

    plt.figure(figsize = (12, 10))
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    plt.subplot(221)
    plt.ylim(-0.1, 1.5)
    plt.errorbar(df2.resM, df2.cPropM, yerr=df2.cPropSD, fmt='o', elinewidth=2, capsize=4, label='Nonsocial population')
    plt.errorbar(df1.resM, df1.cPropM, yerr=df1.cPropSD, fmt='o', elinewidth=2, capsize=4, label='Social population')
    plt.xlabel("Resource availability")
    plt.ylabel("Proportion of cooperators")
    plt.legend(loc = 1, frameon = False)

    plt.subplot(222)
    plt.ylim(-0.1, 1.5)
    plt.errorbar(df2.resM, df2.cDegM, yerr=df2.cDegSD, fmt='o', elinewidth=2, capsize=4, label='Nonsocial population')
    plt.errorbar(df1.resM, df1.cDegM, yerr=df1.cDegSD, fmt='o', elinewidth=2, capsize=4, label='Social population')
    plt.xlabel("Resource availability")
    plt.ylabel("Average degree of cooperation")
    plt.legend(loc = 1, frameon = False)

    plt.subplot(223)
    plt.ylim(-333, 5000)
    plt.errorbar(df2.resM, df2.pSizeM, yerr=df2.pSizeSD, fmt='o', elinewidth=2, capsize=4, label='Nonsocial population')
    plt.errorbar(df1.resM, df1.pSizeM, yerr=df1.pSizeSD, fmt='o', elinewidth=2, capsize=4, label='Social population')
    plt.xlabel("Resource availability")
    plt.ylabel("Population size")
    plt.legend(loc = 1, frameon = False)

    plt.subplot(224)
    plt.ylim(-53, 810)
    plt.errorbar(df2.resM, df2.rSizeM, yerr=df2.rSizeSD, fmt='o', elinewidth=2, capsize=4, label='Nonsocial population')
    plt.errorbar(df1.resM, df1.rSizeM, yerr=df1.rSizeSD, fmt='o', elinewidth=2, capsize=4, label='Social population')
    plt.xlabel("Resource availability")
    plt.ylabel("Range size")
    plt.legend(loc = 1, frameon = False)

    plt.savefig("PFS_feat.pdf")


def plot_properties2(fname1, fname2, var_type):
    df1 = pd.read_csv(fname1)
    df2 = pd.read_csv(fname2)

    plt.rcParams.update({'font.size': 16})
    
    resM = df1.resM[0]
    suffix = ""
    if var_type == "Temporal":
        suffix = "hf"
    elif var_type == "Spatal":
        suffix = "hs"
    
    plt.figure(figsize = (5, 4))
    plt.ylim(-0.1, 1.5)
    plt.errorbar(df2.Range, df2.cPropM, yerr=df2.cPropSD, fmt='o', elinewidth=2, capsize=4, label='Nonsocial population')
    plt.errorbar(df1.Range, df1.cPropM, yerr=df1.cPropSD, fmt='o', elinewidth=2, capsize=4, label='Social population')
    plt.xlabel(var_type + " variability\n(Resource availability range)")
    plt.ylabel("Proportion of cooperators")
    plt.legend(loc = 1, frameon = False)
    plt.savefig("PFS"+str(resM)+suffix+"cp.pdf")

    plt.figure(figsize = (5, 4))
    plt.ylim(-0.1, 1.1)
    plt.errorbar(df2.Range, df2.cDegM, yerr=df2.cDegSD, fmt='o', elinewidth=2, capsize=4, label='Nonsocial population')
    plt.errorbar(df1.Range, df1.cDegM, yerr=df1.cDegSD, fmt='o', elinewidth=2, capsize=4, label='Social population')
    plt.xlabel(var_type + " variability\n(Resource availability range)")
    plt.ylabel("Average degree of cooperation")
    plt.legend(loc = 1, frameon = False)
    plt.savefig("PFS"+str(resM)+suffix+"cd.pdf")

    plt.figure(figsize = (5, 4))
    plt.ylim(-333, 5000)
    plt.errorbar(df2.Range, df2.pSizeM, yerr=df2.pSizeSD, fmt='o', elinewidth=2, capsize=4, label='Nonsocial population')
    plt.errorbar(df1.Range, df1.pSizeM, yerr=df1.pSizeSD, fmt='o', elinewidth=2, capsize=4, label='Social population')
    plt.xlabel(var_type + " variability\n(Resource availability range)")
    plt.ylabel("Population size")
    plt.legend(loc = 1, frameon = False)
    plt.savefig("PFS"+str(resM)+suffix+"ps.pdf")

    plt.figure(figsize = (5, 4))
    plt.ylim(-53, 810)
    plt.errorbar(df2.Range, df2.rSizeM, yerr=df2.rSizeSD, fmt='o', elinewidth=2, capsize=4, label='Nonsocial population')
    plt.errorbar(df1.Range, df1.rSizeM, yerr=df1.rSizeSD, fmt='o', elinewidth=2, capsize=4, label='Social population')
    plt.xlabel(var_type + " variability\n(Resource availability range)")
    plt.ylabel("Range size")
    plt.legend(loc = 1, frameon = False)
    plt.savefig("PFS"+str(resM)+suffix+"rs.pdf")


def plot_properties3(fname1, fname2, var_type):
    df1 = pd.read_csv(fname1)
    df2 = pd.read_csv(fname2)

    plt.rcParams.update({'font.size': 16})
    
    resM = df1.resM[0]
    suffix = ""
    if var_type == "Temporal":
        suffix = "hf"
    elif var_type == "Spatal":
        suffix = "hs"
    
    plt.figure(figsize = (12, 10))
    plt.subplots_adjust(hspace=0.4, wspace=0.4)
    plt.subplot(221)
    plt.ylim(-0.1, 1.5)
    plt.errorbar(df2.Range, df2.cPropM, yerr=df2.cPropSD, fmt='o', elinewidth=2, capsize=4, label='Nonsocial population')
    plt.errorbar(df1.Range, df1.cPropM, yerr=df1.cPropSD, fmt='o', elinewidth=2, capsize=4, label='Social population')
    plt.xlabel(var_type + " variability\n(Resource availability range)")
    plt.ylabel("Proportion of cooperators")
    plt.legend(loc = 1, frameon = False)

    plt.subplot(222)
    plt.ylim(-0.1, 1.1)
    plt.errorbar(df2.Range, df2.cDegM, yerr=df2.cDegSD, fmt='o', elinewidth=2, capsize=4, label='Nonsocial population')
    plt.errorbar(df1.Range, df1.cDegM, yerr=df1.cDegSD, fmt='o', elinewidth=2, capsize=4, label='Social population')
    plt.xlabel(var_type + " variability\n(Resource availability range)")
    plt.ylabel("Average degree of cooperation")
    plt.legend(loc = 1, frameon = False)

    plt.subplot(223)
    plt.ylim(-400, 6000)
    plt.errorbar(df2.Range, df2.pSizeM, yerr=df2.pSizeSD, fmt='o', elinewidth=2, capsize=4, label='Nonsocial population')
    plt.errorbar(df1.Range, df1.pSizeM, yerr=df1.pSizeSD, fmt='o', elinewidth=2, capsize=4, label='Social population')
    plt.xlabel(var_type + " variability\n(Resource availability range)")
    plt.ylabel("Population size")
    plt.legend(loc = 1, frameon = False)

    plt.subplot(224)
    plt.ylim(-53, 810)
    plt.errorbar(df2.Range, df2.rSizeM, yerr=df2.rSizeSD, fmt='o', elinewidth=2, capsize=4, label='Nonsocial population')
    plt.errorbar(df1.Range, df1.rSizeM, yerr=df1.rSizeSD, fmt='o', elinewidth=2, capsize=4, label='Social population')
    plt.xlabel(var_type + " variability\n(Resource availability range)")
    plt.ylabel("Range size")
    plt.legend(loc = 1, frameon = False)
    plt.savefig("PFS"+str(resM)+suffix+".png")
    
    
def plot_properties4(fname1, fname2, var_type, coop_type):
    df1 = pd.read_csv(fname1)
    df2 = pd.read_csv(fname2)

    plt.rcParams.update({'font.size': 16})
    
    resM = df1.resM[0]
    suffix = ""
    if var_type == "Temporal":
        suffix = "hf"
    elif var_type == "Spatal":
        suffix = "hs"
    
    if coop_type == "CA":
        col = "coral"
    elif coop_type == "RD":
        col = "steelblue"
    
    plt.figure(figsize = (5, 4))
    plt.ylim(-0.1, 1.5)
    plt.errorbar(df2.Range, df2.cPropM, yerr=df2.cPropSD, fmt='o', elinewidth=2, capsize=4, color="#AAAAAA", label='Nonsocial population')
    plt.errorbar(df1.Range, df1.cPropM, yerr=df1.cPropSD, fmt='o', elinewidth=2, capsize=4, color=col      , label='Social population')
    plt.xlabel(var_type + " variability\n(Resource availability range)")
    plt.ylabel("Proportion of cooperators")
    plt.legend(loc = 1, frameon = False)
    plt.savefig("PFS"+str(resM)+suffix+"cp.pdf")

    plt.figure(figsize = (5, 4))
    plt.ylim(-0.1, 1.1)
    plt.errorbar(df2.Range, df2.cDegM, yerr=df2.cDegSD, fmt='o', elinewidth=2, capsize=4, color="#AAAAAA", label='Nonsocial population')
    plt.errorbar(df1.Range, df1.cDegM, yerr=df1.cDegSD, fmt='o', elinewidth=2, capsize=4, color=col      , label='Social population')
    plt.xlabel(var_type + " variability\n(Resource availability range)")
    plt.ylabel("Average degree of cooperation")
    plt.legend(loc = 1, frameon = False)
    plt.savefig("PFS"+str(resM)+suffix+"cd.pdf")

    plt.figure(figsize = (5, 4))
    plt.ylim(-333, 5000)
    plt.errorbar(df2.Range, df2.pSizeM, yerr=df2.pSizeSD, fmt='o', elinewidth=2, capsize=4, color="#AAAAAA", label='Nonsocial population')
    plt.errorbar(df1.Range, df1.pSizeM, yerr=df1.pSizeSD, fmt='o', elinewidth=2, capsize=4, color=col      , label='Social population')
    plt.xlabel(var_type + " variability\n(Resource availability range)")
    plt.ylabel("Population size")
    plt.legend(loc = 1, frameon = False)
    plt.savefig("PFS"+str(resM)+suffix+"ps.pdf")

    plt.figure(figsize = (5, 4))
    plt.ylim(-53, 810)
    plt.errorbar(df2.Range, df2.rSizeM, yerr=df2.rSizeSD, fmt='o', elinewidth=2, capsize=4, color="#AAAAAA", label='Nonsocial population')
    plt.errorbar(df1.Range, df1.rSizeM, yerr=df1.rSizeSD, fmt='o', elinewidth=2, capsize=4, color=col      , label='Social population')
    plt.xlabel(var_type + " variability\n(Resource availability range)")
    plt.ylabel("Range size")
    plt.legend(loc = 1, frameon = False)
    plt.savefig("PFS"+str(resM)+suffix+"rs.pdf")
    
def plot_properties5(fname1, fname2, fname3, var_type):
    df1 = pd.read_csv(fname1)
    df2 = pd.read_csv(fname2)
    df3 = pd.read_csv(fname3)

    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams.update({'font.size': 8})
    
    resM = df1.resM[0]
    suffix = ""
    if var_type == "Temporal":
        suffix = "hf"
    elif var_type == "Spatal":
        suffix = "hs"
    
    plt.figure(figsize = (3.5, 3))
    plt.ylim(-0.113, 1.7)
    plt.errorbar(df3.Range, df3.cPropM, yerr=df3.cPropSD, fmt='o', elinewidth=2, capsize=4, color="#AAAAAA"  , label='Nonsocial population')
    plt.errorbar(df2.Range, df2.cPropM, yerr=df2.cPropSD, fmt='o', elinewidth=2, capsize=4, color="steelBlue", label='Social population (RD)')
    plt.errorbar(df1.Range, df1.cPropM, yerr=df1.cPropSD, fmt='o', elinewidth=2, capsize=4, color="coral"    , label='Social population (CA)')
    plt.xlabel(var_type + " variability\n(Resource availability range)")
    plt.ylabel("Proportion of cooperators")
    plt.legend(loc = 1, frameon = False)
    plt.savefig("PFS"+str(resM)+suffix+"cp.pdf", format="pdf")

    plt.figure(figsize = (3.5, 3))
    plt.ylim(-0.1, 1.1)
    plt.errorbar(df3.Range, df3.cDegM, yerr=df3.cDegSD, fmt='o', elinewidth=2, capsize=4, color="#AAAAAA"  , label='Nonsocial population')
    plt.errorbar(df2.Range, df2.cDegM, yerr=df2.cDegSD, fmt='o', elinewidth=2, capsize=4, color="steelBlue", label='Social population (RD)')
    plt.errorbar(df1.Range, df1.cDegM, yerr=df1.cDegSD, fmt='o', elinewidth=2, capsize=4, color="coral"    , label='Social population (CA)')
    plt.xlabel(var_type + " variability\n(Resource availability range)")
    plt.ylabel("Average degree of cooperation")
    plt.legend(loc = 1, frameon = False)
    plt.savefig("PFS"+str(resM)+suffix+"cd.pdf", format="pdf")

    plt.figure(figsize = (3.5, 3))
    plt.ylim(-200, 3000)
    plt.errorbar(df3.Range, df3.pSizeM, yerr=df3.pSizeSD, fmt='o', elinewidth=2, capsize=4, color="#AAAAAA"  , label='Nonsocial population')
    plt.errorbar(df2.Range, df2.pSizeM, yerr=df2.pSizeSD, fmt='o', elinewidth=2, capsize=4, color="steelBlue", label='Social population (RD)')
    plt.errorbar(df1.Range, df1.pSizeM, yerr=df1.pSizeSD, fmt='o', elinewidth=2, capsize=4, color="coral"    , label='Social population (CA)')
    plt.xlabel(var_type + " variability\n(Resource availability range)")
    plt.ylabel("Population size")
    plt.legend(loc = 1, frameon = False)
    plt.savefig("PFS"+str(resM)+suffix+"ps.pdf", format="pdf")

    plt.figure(figsize = (3.5, 3))
    plt.ylim(-60, 900)
    plt.errorbar(df3.Range, df3.rSizeM, yerr=df3.rSizeSD, fmt='o', elinewidth=2, capsize=4, color="#AAAAAA"  , label='Nonsocial population')
    plt.errorbar(df2.Range, df2.rSizeM, yerr=df2.rSizeSD, fmt='o', elinewidth=2, capsize=4, color="steelBlue", label='Social population (RD)')
    plt.errorbar(df1.Range, df1.rSizeM, yerr=df1.rSizeSD, fmt='o', elinewidth=2, capsize=4, color="coral"    , label='Social population (CA)')
    plt.xlabel(var_type + " variability\n(Resource availability range)")
    plt.ylabel("Range size")
    plt.legend(loc = 1, frameon = False)
    plt.savefig("PFS"+str(resM)+suffix+"rs.pdf", format="pdf")