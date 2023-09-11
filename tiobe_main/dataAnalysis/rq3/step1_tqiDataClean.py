'''
Author: rocs
Date: 2023-08-30 20:53:49
LastEditors: rocs
LastEditTime: 2023-09-11 22:05:05
Description: clean the pivoted files
'''
import numpy as np
import pandas as pd
import sys
sys.path.append(sys.path[0][:-17])

from helper import presetting
from helper import metricsPreset as mp
from helper import helperFuncs as hf
from dataAnalysis.rq3 import importStep1ProjectsList_rq3 as pl 

PREFIX = presetting.PREFIX

def tqiDataClean(projectName):
    metricTopics = ['DupCode', 'AI',  'FanOut', 'CS', 'CW', 'Complexity']

    df = pd.read_csv(PREFIX + '/docs/output/RQ3/uncleaned/' + projectName + '.csv')
    if df.empty:
        return
    
    # 1 remove all rows whose  column 'Lines of Code' contains 'All files are unbuildable', and replace the ',' in the value of 'Lines of Code' with '' and change it to an integer
    df = df[~df['Lines of Code'].str.contains('All files are unbuildable')]
    df = df[~df['Lines of Code'].str.contains('Item does not exist')]
    df = df[~df['Lines of Code'].str.contains('No data for this metric and selected filters')]
    df = df[~df['Lines of Code'].str.contains('ERROR')]
    df['Lines of Code'] = df['Lines of Code'].str.replace(',', '').astype(int)

    # 1.1 remove all rows whose column 'TQI' is not a percentage, and replace the '%' in the value of 'TQI' with '' and change it to a float
    df = df[df['TQI'].str.contains('%')]
    df['TQI'] = df['TQI'].str.replace('%', '').astype(float)

    # 2.1 remove all rows whose column 'MetricCoverage for {metricTopic}' is not a percentage, and replace the '%' in the value of 'MetricCoverage for {metricTopic}' with '' and change it to a float
    # 2.2 remove all rows whose column 'MetricCoverage for {metricTopic}' is less than 95
    for metricTopic in metricTopics:
        metricCol = 'Metric Coverage for ' + hf.returnTQIMetricName(metricTopic)
        df = df[df[metricCol].str.contains('%')]
        df[metricCol] = df[metricCol].str.replace('%', '').astype(float)
        df = df[df[metricCol] >= 95]
    
    
    # 3.1 remove all rows whose column '{metricTopic}' is not a percentage, and replace the '%' in the value of '{metricTopic}' with '' and change it to a float
    
    #change all 'TQI Code Coverage' column values which contain 'ERROR' to '0%'
    df.loc[df['TQI Code Coverage'].str.contains('ERROR'), 'TQI Code Coverage'] = '0%'
    #NOTE: this is not good since ERROR should be removed in the previous step
    
    #remove all rows whose column 'TQI Code Coverage' is 0%
    #df = df[df['TQI Code Coverage'] != '0%']
    metricTopics.append('TestCoverage')
    for metricTopic in metricTopics:
        metricCol = hf.returnTQIMetricName(metricTopic)
        df = df[df[metricCol].str.contains('%')]
        df[metricCol] = df[metricCol].str.replace('%', '').astype(float)


    # 4.1 for all rows whose column 'TQI Version' is '3.11', remove rows whose column 'MetricCoverage for TQI Dead Code' is not a percentage, and replace the '%' in the value of 'MetricCoverage for {metricTopic}' with '' and change it to a float
    df_3_11 = df[df['TQI Version'] == 3.11]
    df_3_11 = df_3_11[df_3_11['Metric Coverage for TQI Dead Code'].str.contains('%')]
    df_3_11 = df_3_11[df_3_11['TQI Dead Code'].str.contains('%')]
    df_3_11['Metric Coverage for TQI Dead Code'] = df_3_11['Metric Coverage for TQI Dead Code'].str.replace('%', '').astype(float)
    df_3_11['TQI Dead Code'] = df_3_11['TQI Dead Code'].str.replace('%', '').astype(float)

    # 4.2 for all rows whose column 'TQI Version' is not '3.11', remove rows whose column 'MetricCoverage for TQI Security' is not a percentage, and replace the '%' in the value of 'MetricCoverage for {metricTopic}' with '' and change it to a float
    df_4 = df[df['TQI Version'] != 3.11]
    df_4 = df_4[df_4['Metric Coverage for TQI Security'].str.contains('%')]
    df_4 = df_4[df_4['TQI Security'].str.contains('%')]
    df_4['Metric Coverage for TQI Security'] = df_4['Metric Coverage for TQI Security'].str.replace('%', '').astype(float)
    df_4['TQI Security'] = df_4['TQI Security'].str.replace('%', '').astype(float)

    
    #merge df_3_11 and df_4 and reset the index 
    df = pd.concat([df_3_11, df_4])
    df = df.reset_index(drop=True)

    #if the df's size is less than 100 then skip it
    if (df.shape[0] < 100):
        return
    else :
        #save the df to cleaned folder
        f.write(projectName + '\n')
        df.to_csv(PREFIX + "/docs/output/RQ3/cleaned/ClearTQI_" + projectName + ".csv", index=False)
    
    print(projectName + " is done")


f = open(PREFIX + "/docs/input/" + "cleaned_projects_more_than_100_rows.txt", "w")
projectList = pl.getProjectList()
for i in projectList:
    tqiDataClean(i)
f.close()