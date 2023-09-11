'''
Author: rocs
Date: 2023-08-30 17:35:21
LastEditors: rocs
LastEditTime: 2023-09-11 19:29:33
Description: get all projects' info, only tqi
'''

import requests
import sys, datetime
import pandas as pd
import socket
import numpy as np

sys.path.append(sys.path[0][:-19])
from helper import presetting
from helper import metricsPreset as mp
from helper import helperFuncs as hf

PREFIX = presetting.PREFIX

def getAllProjectRunsInfo(projectName, fList):

    selectedMetrics = ['tqi']
    df = hf.collectMetricsValuesPerProject(projectName, selectedMetrics, False)

    if len(df) > 100:
        print(projectName + ' has ' + str(len(df)) + ' points')
        #add the value to df according to the projectName
        df.loc[df['ProjectName'] == projectName, 'OriginalPoints'] = len(df)
        #add the projectName and its points to the new file
        f.write(projectName + ',' + str(len(df)) + '\n')
        fList.append(projectName)




df = pd.read_csv(PREFIX + '/docs/input/allProjectsRecent.csv')
#add a blank column 'OriginalPoints' to df, which means the rows of the project before the project is filtered
df['OriginalPoints'] = np.nan
projectList = df['ProjectName'].tolist()
finalList = []
#create a txt file to store the projects have large than 100 points
f = open(PREFIX + '/docs/input/allProjectsRecent_oriPointsCnt.txt', 'w')

for projectName in projectList:
    getAllProjectRunsInfo(projectName, finalList)
f.close()

df.to_csv(PREFIX + '/docs/input/allProjectsRecent_withOriPoints.csv', index=False)
#save the finalList to a txt file
ff = open(PREFIX + '/docs/input/projects_more_than_100_rows.txt', 'w')
for item in finalList:
    ff.write(item + '\n')
ff.close()
