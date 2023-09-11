'''
Author: rocs
Date: 2023-07-11 19:20:47
LastEditors: rocs
LastEditTime: 2023-09-11 20:11:41
Description: this file is used to get the project list from projects.csv
'''

import pandas as pd
import sys
sys.path.append(sys.path[0][:-22])
#import presetting from same-level directory helper
from helper import presetting
PREFIX = presetting.PREFIX


#read csv projects.csv
df = pd.read_csv(PREFIX + '/docs/input/selectedProjectsForRq1and2.csv')
#get all project's name
projectList = df['ProjectName'].tolist()

def getProjectList():
    return projectList

def showProjectList():
    print(projectList)

def getProjectListSize():
    return len(projectList)

def getProjectInfo(projectName):
    #get the project's info from projects.csv
    projectInfo = df.loc[df['ProjectName'] == projectName]
    return projectInfo