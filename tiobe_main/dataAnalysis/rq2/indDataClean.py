'''
Author: rocs
Date: 2023-08-18 18:21:42
LastEditors: rocs
LastEditTime: 2023-08-18 19:49:47
Description:  clean the data of core indicators
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



def dataClean(projectName, TQI3 = False):
    #read csv, if the metricTopic is in the subjMetrics list, then read the csv in the levels folder
    if (TQI3 == True):
        df = pd.read_csv(PREFIX + "/docs/output/RQ2/uncleaned/" + projectName +  "_3.csv")
    else:
        df = pd.read_csv(PREFIX + "/docs/output/RQ2/uncleaned/" + projectName +  "_4.csv")    

    #change the 'Date' type from string to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    #remove unnamed column
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    subMetricList = df.columns.tolist()
    subMetricList.pop(0)
    #change all other columns' type to string
    for m in subMetricList:
        df[m] = df[m].astype(str)
    
    #For these two metrics, we only need the values in right TQI Version
    if (TQI3 == False):
        #drop rows whose 'TQI Version' are 3.11
        df = df.drop(df[df['TQI Version'] == '3.11'].index)
        suffix = '4'
    else:
        #drop rows whose 'TQI Version' are 3.11
        df = df.drop(df[df['TQI Version'] != '3.11'].index)
        suffix = '3'
    

    #reset the index
    df_clear = df.reset_index(drop=True)


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
    subMetricList.remove('TQI Version')
    #remove all rows whose column values are string '0'
    df_clear = df_clear.drop(df_clear[(df_clear[subMetricList] == 0).all(axis=1)].index)


    #remove all rows which are completely same as its last row, keep the first one
    df_clear_dropSameValues = df_clear.drop_duplicates(subset=subMetricList, keep='first')
    df_clear_dropSameValues = df_clear_dropSameValues.reset_index(drop=True)

    #output the cleaned csv
    #if row number is less than 2, then we do not output the csv
    df_clear.to_csv(PREFIX + "/docs/output/RQ2/cleaned/"  + projectName + '_' + suffix + ".csv")
    df_clear_dropSameValues.to_csv(PREFIX + "/docs/output/RQ2/cleaned/" + projectName + "_dropSameValues"+ '_' + suffix +  ".csv")

    

# projectList = ['ZigBee-Platform-EFR32-MG13']
# metricTopics = ['AI']

for i in projectList:
    #if there is exception, then save the exception and continue
    # dataClean(i, TQI3 = False)
    try:
        dataClean(i, TQI3 = False)
        dataClean(i, TQI3 = True)
    except Exception as e:
        #save the error project name and metric name into a txt file
        with open(PREFIX + "/docs/output/error/indiDataClean_" + hf.getDatetime() + ".txt", "a") as f:
            f.write(str(e) + "\n" +"Error in " + i + "!" +  "\n\n")
        continue

print("Data Clean Done!")