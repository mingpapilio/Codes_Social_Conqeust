import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.core.pylabtools import figsize

def plot_heatmaps(fname):
    dfh = pd.read_csv(fname)

    figsize(16, 7)
    plt.rcParams.update({'font.size': 16})

    plt.figure(1)
    plt.subplot(121)
    plt.subplots_adjust(wspace=0.4)
    dfh1 = dfh.pivot("Range", "resM", "cPropM")
    ax1 = sns.heatmap(dfh1, square = True, cmap = "Wistia", cbar_kws={'label': 'Proportion of cooperators'})
    ax1.invert_yaxis()
    plt.xlabel("Mean resource availability")
    plt.ylabel("Resource availability range")
    #plt.savefig('cProp_resM_resRange.png')

    plt.subplot(122)
    dfh2 = dfh.pivot("Range", "resM", "cDegM")
    ax2 = sns.heatmap(dfh2, square = True, cmap = "Wistia", cbar_kws={'label': 'Average degree of cooperation'})
    ax2.invert_yaxis()
    plt.xlabel("Mean resource availability")
    plt.ylabel("Resource availability range")
    #plt.savefig('cDeg_resM_resRange.png')
    plt.savefig('coop_resM_resRange.png')

def plot_heatmaps2(fname, var_type):
    dfh = pd.read_csv(fname)

    figsize(8.5, 7)
    plt.rcParams.update({'font.size': 16})

    plt.figure(1)
    dfh1 = dfh.pivot("Range", "resM", "cPropM")
    ax1 = sns.heatmap(dfh1, square = True, cmap = "Wistia", cbar_kws={'label': 'Proportion of cooperators'})
    ax1.invert_yaxis()
    plt.xlabel("Mean resource availability")
    plt.ylabel(var_type + " variability\n(Resource availability range)")
    plt.savefig('cProp_resM_resRange.pdf')

    plt.figure(2)
    dfh2 = dfh.pivot("Range", "resM", "cDegM")
    ax2 = sns.heatmap(dfh2, square = True, cmap = "Wistia", cbar_kws={'label': 'Average degree of cooperation'})
    ax2.invert_yaxis()
    plt.xlabel("Mean resource availability")
    plt.ylabel(var_type + " variability\n(Resource availability range)")
    plt.savefig('cDeg_resM_resRange.pdf')
    #plt.savefig('coop_resM_resRange.png')
    
def plot_heatmaps3(fname, var_type, cmap):
    dfh = pd.read_csv(fname)

    figsize(4, 3)
    plt.rcParams.update({'font.size': 10})
    plt.rcParams['pdf.fonttype'] = 42

    plt.figure(1)
    dfh1 = dfh.pivot("Range", "resM", "cPropM")
    ax1 = sns.heatmap(dfh1, vmin = 0, vmax = 1, square = True, cmap = cmap, cbar_kws={'label': 'Proportion of cooperators'})
    ax1.invert_yaxis()
    plt.xlabel("Mean resource availability")
    plt.ylabel(var_type + " variability\n(Resource availability range)")
    plt.savefig('cProp_resM_resRange.pdf', format="pdf")

    plt.figure(2)
    dfh2 = dfh.pivot("Range", "resM", "cDegM")
    ax2 = sns.heatmap(dfh2, vmin = 0, vmax = 0.5, square = True, cmap = cmap, cbar_kws={'label': 'Average degree of cooperation'})
    ax2.invert_yaxis()
    plt.xlabel("Mean resource availability")
    plt.ylabel(var_type + " variability\n(Resource availability range)")
    plt.savefig('cDeg_resM_resRange.pdf', format="pdf")
    
    plt.figure(3)
    dfh2 = dfh.pivot("Range", "resM", "pSizeM")
    ax2 = sns.heatmap(dfh2, vmin = 0, square = True, cmap = cmap, cbar_kws={'label': 'Population size'})
    ax2.invert_yaxis()
    plt.xlabel("Mean resource availability")
    plt.ylabel(var_type + " variability\n(Resource availability range)")
    plt.savefig('pSize_resM_resRange.pdf', format="pdf")