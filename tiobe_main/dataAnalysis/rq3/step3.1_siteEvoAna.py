'''
Author: rocs
Date: 2023-08-31 01:10:23
LastEditors: rocs
LastEditTime: 2023-09-11 20:50:58
Description: show the evo line of the  projects in one site
'''
import datetime
import matplotlib.pyplot as plt
import pandas as pd

import sys
sys.path.append(sys.path[0][:-17])
from helper import helperFuncs as hf
from helper import presetting

PREFIX = presetting.PREFIX

def showEvoLineForAllProjInOneSite(ownerSite, df_projects):
    #show the evolution of TQI of all projects in one site
    #set the size of the figure
    plt.figure(figsize=(18, 6))
    #set the title of the figure
    # plt.title('TQI Evolution of OwnerSite:' + hf.hashName(ownerSite, 7), fontsize=20)
    owner = ownerSite.split('-')[0]
    site = ownerSite.split('-')[1]
    df_ownerSite = df_projects[df_projects['OwnerSite'] == ownerSite]
    projectList = df_ownerSite['Project Name'].tolist()

    #traverse the df_ownerSite, find the latest 'StartDate' and the earliest 'StartDate'
    latest = df_ownerSite.iloc[0]['StartDate']
    earliest = df_ownerSite.iloc[0]['StartDate']
    # print(len(df_ownerSite))
    for index, row in df_ownerSite.iterrows():
        if row['StartDate'] > latest:
            latest = row['StartDate']
        if row['StartDate'] < earliest:
            earliest = row['StartDate']

    #change latest and earliest to datetime.date type, like 2017-09-19 11:43:23+02:00
    latest = datetime.datetime.strptime(latest, '%Y-%m-%d %H:%M:%S%z').date()
    earliest = datetime.datetime.strptime(earliest, '%Y-%m-%d %H:%M:%S%z').date()
    #set the x-axis range to the latest 'StartDate' minus 3 days and the earliest 'StartDate' plus 17 days
    plt.xlim(earliest - datetime.timedelta(days=3), latest + datetime.timedelta(days=33))
    #set the x-axis label of the second subplot
    plt.xlabel('Date')

    #set the y-axis label of the second subplot
    plt.ylabel('TQI')
    #set y-axis range
    plt.ylim(50, 100)

    for projectName in projectList:
        #get the details of the project
        df_project = pd.read_csv(PREFIX + '/docs/output/RQ3/cleaned/ClearTQI_' + projectName + '.csv')
        #change the type of 'Date' to datetime.date
        df_project['Date'] = pd.to_datetime(df_project['Date'])
        #keep the first two weeks' data
        # tmpDate = df_project.iloc[0]['Date']
        # tmpDate = datetime.datetime.strptime(tmpDate, '%Y-%m-%d %H:%M:%S%z').date()
        # limitDate = tmpDate + datetime.timedelta(days=14)
        df_project = df_project[df_project['Date'] <= df_project.iloc[0]['Date'] + datetime.timedelta(days=30)]
        #plot the lineChart of 'Date' and 'TQI' in the second subplot
        plt.plot(df_project['Date'], df_project['TQI'], label=hf.hashName(projectName, 5))
    #show the legend outside the figure
    # plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)
    #show the figure
    # plt.show()
    plt.savefig(PREFIX + '/figs/RQ3/topAna/TQI evolution of ' + hf.hashName(owner, 6) + '-' + hf.hashName(site, 4) + '.png', dpi=300, bbox_inches='tight')
    plt.close()


df_projects = pd.read_csv(PREFIX + '/docs/output/RQ3/projects_more_than_100_rows_info.csv')
df_projects['OwnerSite'] = df_projects['Owner'].str.cat(df_projects['Site'], sep='-')
#count the number of each 'OwnerSite' in df_projects and sort the result and show the top 15 results 
df_projects['OwnerSite'] = df_projects['OwnerSite'].astype(str)
dict_ownerSite = {}
for index, row in df_projects.iterrows():
    if row['OwnerSite'] in dict_ownerSite:
        dict_ownerSite[row['OwnerSite']] += 1
    else:
        dict_ownerSite[row['OwnerSite']] = 1
dict_ownerSite = sorted(dict_ownerSite.items(), key=lambda x: x[1], reverse=True)
print('number of OwnerSite in df_projects: ', len(dict_ownerSite))
for key, value in dict_ownerSite[:8]:
    print(key, value)

print('---------------------------------------------')

#stroring the top 8 'OwnerSite''s projectNames into 8 lists
list_ownerSite = []
for key, value in dict_ownerSite[:8]:
    list_ownerSite.append(key)
list_projects = []

id = 1
for ownerSite in list_ownerSite:
    id += 1
    if id > 8:
        break
    # if id == 3:
    showEvoLineForAllProjInOneSite(ownerSite, df_projects)