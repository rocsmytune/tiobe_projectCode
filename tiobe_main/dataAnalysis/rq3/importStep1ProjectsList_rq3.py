'''
Author: rocs
Date: 2023-08-30 21:09:12
LastEditors: rocs
LastEditTime: 2023-08-30 21:12:41
Description:  get all projects' name in projects_more_than_100_rows.txt
'''

import pandas as pd
import sys
sys.path.append(sys.path[0][:-19])
from helper import presetting
PREFIX = presetting.PREFIX


#read csv projects.csv
df = pd.read_csv(PREFIX + '/docs/input/projects_more_than_100_rows.txt', header=None)
#get all project's name
projectList = df[0].tolist()

def getProjectList():
    return projectList

def showProjectList():
    print(projectList)

def getProjectListSize():
    return len(projectList)
