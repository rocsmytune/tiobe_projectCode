'''
Author: rocs
Date: 2023-08-18 17:51:14
LastEditors: rocs
LastEditTime: 2023-08-30 17:43:56
Description:  get core indicators for correlation analysis
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
metricTopics3 = mp.coverageMetrics3API
metricTopics4 = mp.coverageMetrics4API

def getIndicators(projectName, metricTopics, TQI3 = False):
    selectedMetrics = metricTopics + ['tqiVersion']
    df = hf.collectMetricsValuesPerProject(projectName, selectedMetrics, True)
    if TQI3:
        df.to_csv(PREFIX + "/docs/output/RQ2/uncleaned/" + projectName +  "_3.csv")
    else:
        df.to_csv(PREFIX + "/docs/output/RQ2/uncleaned/" + projectName +  "_4.csv")
    print("Core indicators info of " + projectName + " has been saved!\n")

projectList = pl.projectList
for i in projectList:
    getIndicators(i, metricTopics3, True)
    getIndicators(i, metricTopics4, False)