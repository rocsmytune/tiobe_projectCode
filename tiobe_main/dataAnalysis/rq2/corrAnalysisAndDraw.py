'''
Author: rocs
Date: 2023-08-18 19:51:56
LastEditors: rocs
LastEditTime: 2023-09-11 20:24:32
Description:  analysis the correlation between metrics' indicators
'''
import datetime
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import warnings
warnings.filterwarnings('ignore')
import sys
sys.path.append(sys.path[0][:-17])
from matplotlib.ticker import MaxNLocator
from helper import presetting
from helper import metricsPreset as mp
from helper import helperFuncs as hf
from dataCollection.rq1and2 import importProjectsList as pl 

PREFIX = presetting.PREFIX


def corrAnalysis(projectName, TQI3 = False, ifKeepDate = False):
    
    size = pl.getProjectInfo(projectName)['Size'].tolist()[0]
    fLang = pl.getProjectInfo(projectName)['FirstLang'].tolist()[0]

    if (TQI3 == False):
        corrMetrics = mp.coverageMetrics4
        if (ifKeepDate == True):
            df = pd.read_csv(PREFIX + "/docs/output/RQ2/cleaned/" + projectName + "_4.csv")
            suffix = '4'
        else:
            df = pd.read_csv(PREFIX + "/docs/output/RQ2/cleaned/" + projectName + "_dropSameValues_4.csv")
            suffix = '4_dropSameValues'
    else:
        corrMetrics = mp.coverageMetrics3
        if (ifKeepDate == True):
            df = pd.read_csv(PREFIX + "/docs/output/RQ2/cleaned/" + projectName + "_3.csv")
            suffix = '3'
        else:
            df = pd.read_csv(PREFIX + "/docs/output/RQ2/cleaned/" + projectName + "_dropSameValues_3.csv")
            suffix = '3_dropSameValues'

    # verify the correlation between 'Average Cyclomatic Complexity' and 'Coding Standard Violations' 
    df_corr = df[corrMetrics]
    corr = df_corr.corr(method='pearson')
    #save the .2f version of corr 
    corr_2f = corr.round(2)
    # print(corr)
    # plot the heatmap of correlation with short labels
    # plt.figure(figsize=(10, 10))
    sns.heatmap( corr_2f, annot=True, cmap='RdBu_r', vmax=1, vmin=-1)
    plt.xticks(rotation=90, fontsize=11)
    plt.yticks(rotation=0, fontsize=11)
    plt.tight_layout()


    # plt.title(hf.hashName(projectName) + ':' + 'Correlation Analysis')
    #projectName = hf.hashName(projectName)
    plt.savefig(PREFIX + '/figs/RQ1AndRQ2/RQ2/normal/' + hf.hashName(projectName) +'_' + suffix +'.png', bbox_inches='tight')
    plt.savefig(PREFIX + '/figs/RQ1AndRQ2/RQ2/' +  size + '/' + hf.hashName(projectName) +'_' + suffix +'.png', bbox_inches='tight')
    
    if (fLang in ['Java', 'C#', 'C++', 'C', 'Python']):
        plt.savefig(PREFIX + '/figs/RQ1AndRQ2/RQ2/lang/' +  fLang + '/' + hf.hashName(projectName) +'_' + suffix +'.png', bbox_inches='tight')
    else:
        plt.savefig(PREFIX + '/figs/RQ1AndRQ2/RQ2/lang/Other/' + hf.hashName(projectName) +'_' + suffix +'.png', bbox_inches='tight')


    #generate another heatmap without labels and colorbar 
    #remove the x and y labels
    plt.clf()
    sns.heatmap( corr_2f, annot=True, cmap='RdBu_r', vmax=1, vmin=-1, cbar=False, xticklabels=False, yticklabels=False)
    #cut the blank space
    plt.tight_layout()
    #make the heatmap 
    # plt.show()
    # sys.exit()
    plt.savefig(PREFIX + '/figs/RQ1AndRQ2/RQ2/nolabels/' + hf.hashName(projectName) +'_' + suffix +'.png', bbox_inches='tight')
   


    
    # plt.show()
    plt.clf()
    plt.close()

    print(projectName + ' correlation analysis finished!')
    



projectList = pl.getProjectList()

for projectName in projectList:
    try : 
        corrAnalysis(projectName, False, True)
        corrAnalysis(projectName, True, True)
    except Exception as e:
        #save the error project name and metric name into a txt file
        with open(PREFIX + "/docs/output/error/indiDataAna_" + hf.getDatetime() + ".txt", "a") as f:
            f.write(str(e) + "\n" +"Error in " + projectName + "!" +  "\n\n")
        continue