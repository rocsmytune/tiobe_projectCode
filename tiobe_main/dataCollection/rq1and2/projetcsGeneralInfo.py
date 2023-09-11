'''
Author: rocs
Date: 2023-05-05 23:03:15
LastEditors: rocs
LastEditTime: 2023-09-11 20:08:56
Description:  first part iis used to draw the histogram and pie chart for all selected projects, second part is used to get and  out put the TQI related values for each project
'''

from matplotlib import pyplot as plt
import pandas as pd
import sys
import importProjectsList as pl
# print(sys.path[0][:-22])
sys.path.append(sys.path[0][:-22])
#import presetting from same-level directory helper
from helper import presetting
from helper import helperFuncs
from helper import metricsPreset as ma
PREFIX = presetting.PREFIX


df = pl.df
projectList = pl.getProjectList()
#generate 3 list for small, mid, large projects
projectList_small = []
projectList_mid = []
projectList_large = []

#e.g. all rows whose 'Size' is 'small' will be added into projectList_small
for i in range(len(projectList)):
    if df.loc[i, 'Size'] == 'small':
        projectList_small.append(projectList[i])
    elif df.loc[i, 'Size'] == 'mid':
        projectList_mid.append(projectList[i])
    elif df.loc[i, 'Size'] == 'large':
        projectList_large.append(projectList[i])

#get all project's language and store as String list
projectLanguageList = df['MainCodeType'].tolist()
# print(len(projectLanguageList))
#chaneg projectLanguageList's datatype to string 
projectLanguageList = [str(i) for i in projectLanguageList]

#trave the projetcLanguageList, split each item by '>' and store the first one into projectFirstLanguageList
# e.g. 'C++ > Python' will be stored as 'C++' 
projectFirstLanguageList = []
projectAllLanguageList = []
for i in range(len(projectLanguageList)):
    projectFirstLanguageList.append(projectLanguageList[i].split('>')[0])
    projectAllLanguageList.append(projectLanguageList[i].split('>'))

#count the number of each language
fLanguageCount = {}
languageCount = {}
for i in range(len(projectFirstLanguageList)):
    if projectFirstLanguageList[i] not in fLanguageCount:
        fLanguageCount[projectFirstLanguageList[i]] = 1
    else:
        fLanguageCount[projectFirstLanguageList[i]] += 1

for j in range(len(projectAllLanguageList)):
    for i in range(len(projectAllLanguageList[j])):
        if projectAllLanguageList[j][i] not in languageCount:
            languageCount[str(projectAllLanguageList[j][i])] = 1
        else:
            languageCount[str(projectAllLanguageList[j][i])] += 1

#sort the languageCount by value
fLanguageCount = sorted(fLanguageCount.items(), key=lambda x: x[1], reverse=True)
languageCount = sorted(languageCount.items(), key=lambda x: x[1], reverse=True)

#delete the , in the LOC column
df['LOC'] = df['LOC'].str.replace(',', '')
# change the column LOC to int
df['LOC'] = df['LOC'].astype(int)

#use a  map to store the project name and its LOC
projectListWithLOC = {}
for i in range(len(projectList)):
    projectListWithLOC[projectList[i]] = df.loc[i, 'LOC']
#sort the projectListWithLOC by value
projectListWithLOC = sorted(projectListWithLOC.items(), key=lambda x: x[1], reverse=True)

#count the number of each project's Site'
projectSiteCount = {}
for i in range(len(projectList)):
    if df.loc[i, 'CompanySite'] not in projectSiteCount:
        projectSiteCount[df.loc[i, 'CompanySite']] = 1
    else:
        projectSiteCount[df.loc[i, 'CompanySite']] += 1

#sort the projectSiteCount by value
projectSiteCount = sorted(projectSiteCount.items(), key=lambda x: x[1], reverse=True)

#write a function to draw histogram, x axis is the project name, y axis is the LOC
def drawHistogram(projectListWithLOC, title):
    plt.figure(figsize=(10, 4))
    #get the name of each project
    projectName = [helperFuncs.hashName(i[0],5) for i in projectListWithLOC]
    #get the LOC of each project
    projectLOC = [i[1] for i in projectListWithLOC]

    #draw histogram, use red color for LOC > 500000, use yellow color for 100000 < LOC < 500000, use blue color for LOC < 100000
    # Create a list to store bar colors based on conditions
    bar_colors = ['#EC6B56' if loc > 500000 else '#FFC154' if loc > 100000 else '#47B39C' for loc in projectLOC]
    plt.bar(projectName, projectLOC,  color=bar_colors)

    

    plt.xticks(rotation=90)
    # plt.title(title + ' LOC Distribution')
    plt.xlabel('Project Name', fontsize=13)
    plt.ylabel('Lines of Code', fontsize=13)
    plt.tight_layout()

    # #add horizontal dashed line to show LOC at 10000, 100000 and 500000
    # plt.axhline(y=100000, color='y', linestyle='--', label='100K', linewidth=0.85)
    # plt.axhline(y=500000, color='r', linestyle='--', label='500K', linewidth=0.85)

    #add legend, show the meaning of each color.
    plt.legend( handles = [plt.plot([], [], color='#47B39C', label='Small')[0], plt.plot([], [], color='#FFC154', label='Middle')[0], plt.plot([], [], color='#EC6B56', label='Large')[0]], loc='upper right', fontsize=10)


    # plt.show()
    plt.savefig(PREFIX + '/figs/RQ1AndRQ2/General/' + title + ' LOC Distribution.png', dpi=300, bbox_inches='tight')

#write a draw pie chart function for languageCount and fLanguageCount separately
def drawPieChartLang(languageCount, title):
    #use a subplot to draw pie chart and with the name of each language without the percentage, then use another subplot to draw bar chart to show the number of each language
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    #get the name of each language
    languageName = [i[0] for i in languageCount]
    #get the number of each language
    languageNum = [i[1] for i in languageCount]
    #draw pie chart
    plt.pie(languageNum, labels=languageName, autopct='%1.1f%%', pctdistance=0.8, colors=['#7bacd3', '#aec7e7', '#fc7f0f', '#fdbb79', '#2d9e2b',
                                                '#98df8a', '#d52924', '#fc9999', '#9266c1', '#c3afd5', '#89524b', '#cc9b93', '#e17dbf', '#f3b7d6', '#b9bd31'])
    # plt.title(title + ' Language Distribution')
    plt.subplot(1, 2, 2)
    #draw bar chart with the same color as pie chart
    plt.bar(languageName, languageNum, color=['#7bacd3', '#aec7e7', '#fc7f0f', '#fdbb79', '#2d9e2b',
                                                '#98df8a', '#d52924', '#fc9999', '#9266c1', '#c3afd5', '#89524b', '#cc9b93', '#e17dbf', '#f3b7d6', '#b9bd31'])
    
    # plt.title(title + ' Language Distribution')
    plt.xticks(rotation=90)
    plt.tight_layout()
    # plt.show()
    plt.savefig(PREFIX + '/figs/RQ1AndRQ2/General/' + title + ' Language Distribution.png', dpi=300, bbox_inches='tight')
#write a draw pie chart function for different size of project
def drawPieChartSize(projectList, title):
    #draw pie chart for different size of project
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    #get the name of each size
    sizeName = ['small', 'middle', 'large']
    #get the number of each size
    sizeNum = [len(projectList_small), len(projectList_mid), len(projectList_large)]
    #draw pie chart
    plt.pie(sizeNum, labels=sizeName, autopct='%1.1f%%',  explode=(0.02, 0.02, 0.02), colors=['#7bacd3', '#aec7e7', '#fc7f0f', '#fdbb79', '#2d9e2b',
                                                '#98df8a', '#d52924', '#fc9999', '#9266c1', '#c3afd5', '#89524b', '#cc9b93', '#e17dbf', '#f3b7d6', '#b9bd31'])
    # plt.title(title + ' Project Size Distribution')
    plt.subplot(1, 2, 2)
    #draw bar chart with the same color as pie chart
    #set yaxis to integer
    plt.yticks(range(0, 20))
    plt.bar(sizeName, sizeNum, color=['yellow', '#ff7f0e', 'red'])
    # plt.title(title + ' Project Size Distribution')
    plt.tight_layout()
    # plt.show()
    plt.savefig(PREFIX + '/figs/RQ1AndRQ2/General/' + title + ' Project Size Distribution.png', dpi=300, bbox_inches='tight')
#write a draw pie chart function for Site
def drawPieChartSite(projectSiteCount, title):
    #draw pie chart for different Site
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    #get the name of each Site
    siteName = [helperFuncs.hashName(i[0],4) for i in projectSiteCount]
    #get the number of each Site
    siteNum = [i[1] for i in projectSiteCount]
    #draw pie chart
    plt.pie(siteNum, labels=siteName, autopct='%1.1f%%', pctdistance=0.8, colors=['#7bacd3', '#aec7e7', '#fc7f0f', '#fdbb79', '#2d9e2b',
                                                '#98df8a', '#d52924', '#fc9999', '#9266c1', '#c3afd5', '#89524b', '#cc9b93', '#e17dbf', '#f3b7d6', '#b9bd31'])
    # plt.title(title + ' Site Distribution')
    plt.subplot(1, 2, 2)
    #draw bar chart with the same color as pie chart
    plt.bar(siteName, siteNum, color=['#7bacd3', '#aec7e7', '#fc7f0f', '#fdbb79', '#2d9e2b',
                                                '#98df8a', '#d52924', '#fc9999', '#9266c1', '#c3afd5', '#89524b', '#cc9b93', '#e17dbf', '#f3b7d6', '#b9bd31'])
    # plt.title(title + ' Site Distribution')
    plt.xticks(rotation=90)
    plt.tight_layout()
    # plt.show()
    plt.savefig(PREFIX + '/figs/RQ1AndRQ2/General/' + title + ' Site Distribution.png', dpi=300, bbox_inches='tight')


#use the function to draw pie chart for languageCount and fLanguageCount separately
drawPieChartLang(languageCount,  'All Selected Projects\'')
drawPieChartLang(fLanguageCount, 'All Selected Projects\' Primary')
#use the function to draw pie chart for different size of project
drawPieChartSize(projectList, 'All Selected Projects\'')
drawPieChartSite(projectSiteCount, 'All Selected Projects\'')
drawHistogram(projectListWithLOC, 'All Selected Projects\'')
