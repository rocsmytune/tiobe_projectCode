'''
Author: rocs
Date: 2023-08-30 17:04:11
LastEditors: rocs
LastEditTime: 2023-08-30 17:40:08
Description:  show all projects' recent info, including: LOC, TQI, Site, Language, Owner
'''

import requests
import sys, datetime
import pandas as pd
import socket
import numpy as np

sys.path.append(sys.path[0][:-19])
from helper import presetting
from helper import helperFuncs as hf
PREFIX = presetting.PREFIX

def showAllProjectRecentInfo():

    selectedMetrics = ['owner', 'loc', 'site', 'language', 'tqi']
    df = hf.collectMetricsValuesAllProjects(selectedMetrics)

    # remove 'HIE://' in projectName
    df['ProjectName'] = df['ProjectName'].str.replace('HIE://', '')

    df_site = df[df['MetricName'] == 'Site']
    df_pl = df[df['MetricName'] == 'Programming language']
    df_loc = df[df['MetricName'] == 'Lines of Code']
    df_ow = df[df['MetricName'] == 'Owner']
    df_tqi = df[df['MetricName'] == 'TQI']

    #then merge these info into one dataframe
    #remove column 'MetricName'
    df_loc = df_loc.drop(['MetricName'], axis=1)
    #Rename column 'Value' to 'LOC'
    df_loc = df_loc.rename(columns={'Value': 'LOC'})

    #add a blank column 'TQI', 'Site', 'Language', 'Owner' to df_loc
    df_loc['TQI'] = np.nan
    df_loc['Site'] = np.nan
    df_loc['Language'] = np.nan
    df_loc['Owner'] = np.nan

    #traverse all projects in df_tqi, df_ow, df_site, df_pl
    for index, row in df_tqi.iterrows():
        df_loc.loc[df_loc['ProjectName'] == row['ProjectName'], 'TQI'] = row['Value']
    for index, row in df_ow.iterrows():
        df_loc.loc[df_loc['ProjectName'] == row['ProjectName'], 'Owner'] = row['Value']
    for index, row in df_site.iterrows():
        df_loc.loc[df_loc['ProjectName'] == row['ProjectName'], 'Site'] = row['Value']
    for index, row in df_pl.iterrows():
        df_loc.loc[df_loc['ProjectName'] == row['ProjectName'], 'Language'] = row['Value']
    
    #remove ',' in column 'LOC'
    df_loc['LOC'] = df_loc['LOC'].str.replace(',', '')
    #remove rows have 'LOC' is not number
    df_loc = df_loc[df_loc['LOC'].str.isdigit()]
    #remove rows have 'LOC' less than 7000
    df_loc = df_loc[df_loc['LOC'].astype(int) > 7000]

    df_loc.to_csv (PREFIX + '/docs/input/allProjectsRecent.csv', index = False, header=True)


showAllProjectRecentInfo()