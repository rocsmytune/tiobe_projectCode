'''
Author: rocs
Date: 2023-07-12 20:19:38
LastEditors: rocs
LastEditTime: 2023-09-11 22:03:37
Description:  dat clean file for RQ1
'''

import numpy as np
import pandas as pd
import sys
sys.path.append(sys.path[0][:-17])

from helper import presetting
from helper import metricsPreset as mp
from helper import helperFuncs as hf
from dataCollection.rq1and2 import importProjectsList as pl 

PREFIX = presetting.PREFIX

#read csv projects.csv
df_pl = pl.df
projectList = df_pl['ProjectName'].tolist()
metricTopics = mp.allMetrics

#generate 3 list for small, mid, large projects
projectList_small = []
projectList_mid = []
projectList_large = []

#e.g. all rows whose 'Size' is 'small' will be added into projectList_small
for i in range(len(projectList)):
    if df_pl.loc[i, 'Size'] == 'small':
        projectList_small.append(projectList[i])
    elif df_pl.loc[i, 'Size'] == 'mid':
        projectList_mid.append(projectList[i])
    elif df_pl.loc[i, 'Size'] == 'large':
        projectList_large.append(projectList[i])


def dataClean(projectName, metricTopic):
    #read csv, if the metricTopic is in the subjMetrics list, then read the csv in the levels folder
    df = pd.read_csv(PREFIX + "/docs/output/RQ1/uncleaned/" + metricTopic + "/" + projectName +  ".csv")
    if (metricTopic in mp.subjMetrics):
        df_extra = pd.read_csv(PREFIX + "/docs/output/RQ1/uncleaned/" + metricTopic + "/levels/" + projectName +  ".csv")
        df_extra = df_extra.drop(columns=['Date'])
        #merge the two dfs accoring to the index
        df = pd.concat([df, df_extra], axis=1)

    #change the 'Date' type from string to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    #remove unnamed column
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    subMetricList = df.columns.tolist()
    #drop the first column 'Date'
    subMetricList.pop(0)
    #change all other columns' type to string
    for m in subMetricList:
        df[m] = df[m].astype(str)
    
    #For these two metrics, we only need the values in right TQI Version
    if (metricTopic == 'SEC'):
        #drop rows whose 'TQI Version' are 3.11
        df = df.drop(df[df['TQI Version'] == '3.11'].index)
    if (metricTopic == 'Dead Code'):
        #drop rows whose 'TQI Version' are 3.11
        df = df.drop(df[df['TQI Version'] != '3.11'].index)
    
    #Since this part is for Metric Analysis, if MC for TQI Metric  is 0, then it is meaningless, so we drop these rows
    #drop rows whose 'Metric Coverage' are 0 Metric Coverage for TQI Abstract Interpretation
    mcForMer = 'Metric Coverage for ' + hf.returnTQIMetricName(metricTopic)
    df_clear = df.drop(df[df[mcForMer] == '0.00%'].index)
    #reset the index
    df_clear = df_clear.reset_index(drop=True)


    #change all rows whose 'Value' contains 'ERROR' or '<>' to NaN
    for m in subMetricList:
        df_clear.loc[df_clear[m].str.contains('ERROR') == True, m] = '0'
        df_clear.loc[df_clear[m].str.contains('</') == True, m] = '0'
        df_clear.loc[df_clear[m] == '-'] = '0'

        #change all column values contains ',' or '%' to float type
        df_clear[m] = df_clear[m].str.replace(',', '')
    

    #now remove all unnecessary rows, back to float type
    for i in subMetricList:
        #these three columns are not necessary for type conversion
        if  i == 'TQI Version' or i == 'TICS Version':
            continue
        else: 
            if (mp.isPctOrFloatMer(i) == 'pct'):
               df_clear[i] = df_clear[i].str.replace('%', '').astype(float)

               #NOTE: here I comment this line, because I want to keep the original value
                #divide all values by 100
                # df_clear[i] = df_clear[i] / 100.0
            elif (mp.isPctOrFloatMer(i) == 'float'): 
                #change all column values to int type
                df_clear[i] = df_clear[i].astype(float)
            else:
                df_clear[i] = df_clear[i].astype(int)


    #NOTE: I want to keep mopre values for metric analysis
    #remove all rows whose 'MetricCoverage for {}' is less than 95
    # df_clear = df_clear[df_clear[mcForMer] >= 95]

    #some column values are '0', so we drop these rows,we use subMetricList to remove
    #remove 'TICS Version', 'TQI Version'  from subMetricList
    subMetricList.remove('TICS Version')
    subMetricList.remove('TQI Version')
    #remove all rows whose column values are string '0'
    df_clear = df_clear.drop(df_clear[(df_clear[subMetricList] == 0).all(axis=1)].index)

    #remove all rows which are completely same as its last row, keep the first one
    df_clear_dropSameValues = df_clear.drop_duplicates(subset=subMetricList, keep='first')
    df_clear_dropSameValues = df_clear_dropSameValues.reset_index(drop=True)

    #output the cleaned csv
    df_clear.to_csv(PREFIX + "/docs/output/RQ1/cleaned/" + metricTopic + "/" + projectName +  ".csv")
    df_clear_dropSameValues.to_csv(PREFIX + "/docs/output/RQ1/cleaned/" + metricTopic  + "/"+ projectName + "_dropSameValues" +  ".csv")

for i in projectList:
    for j in metricTopics:
        #if there is exception, then save the exception and continue
        try:
            dataClean(i, j)
        except Exception as e:
            #save the error project name and metric name into a txt file
            with open(PREFIX + "/docs/output/error/dataClean_" + hf.getDatetime() + ".txt", "a") as f:
                f.write(str(e) + "\n" +"Error in " + i + " for " + j + "!" +  "\n\n")
            continue

print("Data Clean Done!")