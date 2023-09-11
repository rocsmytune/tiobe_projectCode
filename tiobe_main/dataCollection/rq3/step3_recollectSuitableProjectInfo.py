'''
Author: rocs
Date: 2023-08-30 18:02:24
LastEditors: rocs
LastEditTime: 2023-08-30 23:43:18
Description:  recollect all suitable projects' info, including all tqi info
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

def getRQ3ProjectInfo(projectName):
    selectedMetrics = ['loc', 'linesAdded', 'linesDeleted','tqi','tqiVersion','ticsVersion', 'owner', 'site', 'language', 'changerate']                                                          
    #add metric coverage and tqi for every metric
    selectedMetrics += ['Coverage(tqiTestCoverage)', 'tqiTestCoverage']
    selectedMetrics += ['Coverage(tqiDupCode)', 'tqiDupCode']
    selectedMetrics += ['Coverage(tqiFanOut)',  'tqiFanOut']
    selectedMetrics += ['Coverage(tqiDeadCode)', 'tqiDeadCode']
    selectedMetrics += ['Coverage(tqiComplexity)','tqiComplexity']
    selectedMetrics += ['Coverage(tqiAbstrInt)', 'tqiAbstrInt']
    selectedMetrics += ['Coverage(tqiCompWarn)', 'tqiCompWarn']
    selectedMetrics += ['Coverage(tqiCodingStd)', 'tqiCodingStd']
    selectedMetrics += ['Coverage(tqiSecurity)', 'tqiSecurity']

    df = hf.collectMetricsValuesPerProject(projectName, selectedMetrics, True)
    df.to_csv(PREFIX + '/docs/output/RQ3/uncleaned/' + projectName + '.csv')

    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('projectName: ', projectName, ' finished')


pl = pd.read_csv(PREFIX + '/docs/input/projects_more_than_100_rows.txt', header=None)
projectList = pl[0].tolist()
for projectName in projectList:
    try:
        getRQ3ProjectInfo(projectName)
    except Exception as e:
        #save the error project name and metric name into a txt file
        with open(PREFIX + "/docs/output/error/rq3Collect_" + hf.getDatetime() + ".txt", "a") as f:
            f.write(str(e) + "\n" +"Error in " + projectName + "!" +  "\n\n")
        continue