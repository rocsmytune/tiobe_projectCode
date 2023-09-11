'''
Author: rocs
Date: 2023-03-15 11:12:31
LastEditors: rocs
LastEditTime: 2023-07-12 19:30:20
Description: 
'''


import requests
import sys, datetime
import pandas as pd
import socket
import importProjectsList as pl

sys.path.append(sys.path[0][:-22])
from helper import presetting
from helper import metricsPreset as mp
from helper import helperFuncs as hf

PREFIX = presetting.PREFIX
metricTopics = mp.allMetrics

def getMetricInfo(projectName, metricTopic):

    print("Getting the metric info of " + projectName + " for " + metricTopic + "......")
    selectedMetrics = mp.getSubMetrics(metricTopic)

    df = hf.collectMetricsValuesPerProject(projectName, selectedMetrics, True)
    df.to_csv(PREFIX + "/docs/output/RQ1/uncleaned/" + metricTopic + "/" + projectName +  ".csv")
    print("Metric info of " + projectName + " for " + metricTopic + " has been saved!\n")

def getSubjMetricInfoByLevel(projectName, metricTopic):
    if (metricTopic not in mp.subjMetrics):
        print("The metric topic is not in the subjMetrics list!")
        return
    
    selectedMetrics = ['Violations(' + metricTopic + ')']
    levelNum = hf.getLevelNum(metricTopic)

    dfs = []

    for i in range(1, levelNum+1):
        print("Getting the metric info  of " + projectName + " for " + metricTopic + " on level" + str(i) + "......")
        df = hf.collectMetricsLevelValuesPerProject(projectName, selectedMetrics,i)
        #store the df  into a list as df_i
        dfs.append(df)
    
    #if all dfs have the same size then merge the dfs  into one df accoring to the index, else print error
    if all(len(df) == len(dfs[0]) for df in dfs):
        #drop extra 'Date' column
        for i in range(1, levelNum):
            dfs[i] = dfs[i].drop(columns=['Date'])
        df = pd.concat(dfs, axis=1)
        df.to_csv(PREFIX + "/docs/output/RQ1/uncleaned/" + metricTopic + "/levels/" + projectName +  ".csv")
    print("Metric Levels info of " + projectName + " for " + metricTopic + " has been saved!\n")



projectList = pl.projectList
for i in projectList:
    for j in metricTopics:
        getMetricInfo(i, j)
        if (j in mp.subjMetrics):
            getSubjMetricInfoByLevel(i, j)

print("\n\n*****All Tasks Done*****")




