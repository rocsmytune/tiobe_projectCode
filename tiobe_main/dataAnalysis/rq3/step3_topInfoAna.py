'''
Author: rocs
Date: 2023-06-20 10:58:11
LastEditors: rocs
LastEditTime: 2023-09-11 20:44:36
Description: analyze the generated csv of 592 projects
'''
import datetime
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import warnings
warnings.filterwarnings('ignore')
import sys
sys.path.append(sys.path[0][:-17])
from matplotlib.ticker import MaxNLocator
from helper import presetting
from helper import metricsPreset as mp
from helper import helperFuncs as hf

PREFIX = presetting.PREFIX


# print(PREFIX)
df_projects = pd.read_csv(PREFIX + '/docs/output/RQ3/projects_more_than_100_rows_info.csv')
df_metrics = pd.read_csv(PREFIX + '/docs/output/RQ3/projects_more_than_100_rows_TQI_metrics_ver.csv')

# print(df_projects.columns)print(df_metrics.columns)

#count the average of 'Average TQI Change(monthly)' in df_projects
df_projects['Average TQI Change(monthly)'] = df_projects['Average TQI Change(monthly)'].astype(float)
#traverse the df_projects
# #sum up the 'Average TQI Change(monthly)' of each project
sum = 0
count = 0
for index, row in df_projects.iterrows():
    sum += row['Average TQI Change(monthly)']
    count += 1
#calculate the average
average = sum / count
print('average Average TQI Change(monthly): for', count, 'projects: ' , average)

#count the average of 'Average TQI Change Rate(monthly)' in df_projects
df_projects['Average TQI Change Rate(monthly)'] = df_projects['Average TQI Change Rate(monthly)'].astype(float)
#traverse the df_projects
# #sum up the 'Average TQI Change Rate(monthly)' of each project
sum = 0
count = 0
for index, row in df_projects.iterrows():
    sum += row['Average TQI Change Rate(monthly)']
    count += 1
#calculate the average
average = sum / count
#show the result using percentage
print('average Average TQI Change Rate(monthly): for', count, 'projects: ' , average * 100, '%')

print('---------------------------------------------')

#show the distribution of CodeSize in df_projects
# traverse the df_projects
# count the number of projects whose Latest Code Size is small, middle and large
# and show the percentage
count_small = 0
avgTQI_small = 0
avgTQIChange_small = 0
count_middle = 0
avgTQI_middle = 0
avgTQIChange_middle = 0
count_large = 0
avgTQI_large = 0
avgTQIChange_large = 0
for index, row in df_projects.iterrows():
    if row['Latest Code Size'] == 'small':
        count_small += 1
        avgTQI_small += row['Average TQI']
        avgTQIChange_small += row['Average TQI Change(monthly)']
    elif row['Latest Code Size'] == 'middle':
        count_middle += 1
        avgTQI_middle += row['Average TQI']
        avgTQIChange_middle += row['Average TQI Change(monthly)']
    else:
        count_large += 1
        avgTQI_large += row['Average TQI']
        avgTQIChange_large += row['Average TQI Change(monthly)']
print('number of projects with small CodeSize: ', count_small)
print('number of projects with middle CodeSize: ', count_middle)
print('number of projects with large CodeSize: ', count_large)
print('percentage of projects with small CodeSize: ', count_small / df_projects.shape[0] * 100, '%')
print('percentage of projects with middle CodeSize: ', count_middle / df_projects.shape[0] * 100, '%')
print('percentage of projects with large CodeSize: ', count_large / df_projects.shape[0] * 100, '%')
print('average TQI of projects with small CodeSize: ', avgTQI_small / count_small)
print('average TQI of projects with middle CodeSize: ', avgTQI_middle / count_middle)
print('average TQI of projects with large CodeSize: ', avgTQI_large / count_large)
print('average TQI Change(monthly) of projects with small CodeSize: ', avgTQIChange_small / count_small)
print('average TQI Change(monthly) of projects with middle CodeSize: ', avgTQIChange_middle / count_middle)
print('average TQI Change(monthly) of projects with large CodeSize: ', avgTQIChange_large / count_large)

print('---------------------------------------------')

#show the distribution of TQI Version in df_projects
# traverse the df_projects
disc_TQI = {}
# count the number of projects' Latest TQI Version 
# and show the percentage
for index, row in df_projects.iterrows():
    if row['Latest TQI Version'] not in disc_TQI:
        disc_TQI[row['Latest TQI Version']] = 1
    else:
        disc_TQI[row['Latest TQI Version']] += 1
#show the top 3 TQI Version and bottom 3 TQI Version
disc_TQI = sorted(disc_TQI.items(), key=lambda item:item[1], reverse=True)
print('top 3 TQI Version: ', disc_TQI[:3])
print('bottom 3 TQI Version: ', disc_TQI[-3:])

#show the distribution of  'hasMultipleTQIVersions' in df_projects
# traverse the df_projects
# count the number of projects' hasMultipleTQIVersions
# and show the percentage
count = 0
for index, row in df_projects.iterrows():
    if row['hasMultipleTQIVersions'] == True:
        count += 1
print('number of projects with multiple TQI Versions: ', count)
print('percentage of projects with multiple TQI Versions: ', count / df_projects.shape[0] * 100, '%')

print('---------------------------------------------')

#count the number of 'Average TQI Change(monthly)‘ larger than 0 in df_projects
#traverse the df_projects
# #count the number of 'Average TQI Change(monthly)‘ larger than 0
count = 0
for index, row in df_projects.iterrows():
    if row['Average TQI Change(monthly)'] > 0:
        count += 1
print('number of projects with Average TQI Change(monthly) larger than 0: ', count)
print('number of projects with Average TQI Change(monthly) less than 0: ', df_projects.shape[0] - count)


#count the number of 'hasTQI3' equals to True
count = 0
for index, row in df_projects.iterrows():
    if row['hasTQI3'] == True:
        count += 1
print('number of projects with TQI3: ', count)
#show the percentage
print('percentage of projects with TQI3: ', count / df_projects.shape[0] * 100, '%')
print('---------------------------------------------')

#count the distribution of 'Programming language' in df_projects
#traverse the df_projects
# for each row in df_projects['Programming language'], cut the String using ',' as delimiter
# and add the first element to a dict, count the number of each language
# and add all the elements including the first element to another dict, count the number of each language
dict_primary = {}
#use dict_primary_info to store the TQI info and Size info of each language
dict_primary_tqi = {}
dict_primary_small = {}
dict_primary_middle = {}
dict_primary_large = {}
dict_all = {}
one_language_cnt = 0
for index, row in df_projects.iterrows():
    # print(row['Programming language'])
    # print(type(row['Programming language']))
    if type(row['Programming language']) == str:
        #remove all the spaces in the string
        row['Programming language'] = row['Programming language'].replace(' ', '')
        # print('yes')
        languages = row['Programming language'].split(',')
        if len(languages) == 1:
            one_language_cnt += 1
        if languages[0] in dict_primary:
            dict_primary[languages[0]] += 1
        else:
            dict_primary[languages[0]] = 1
        
        if languages[0] in dict_primary_tqi:
            dict_primary_tqi[languages[0]] += row['Average TQI'] 
        else:
            dict_primary_tqi[languages[0]] = row['Average TQI']
        
        if languages[0] in dict_primary_small:
            if hf.returnCodeSize(row['Lines of Code(last)']) == 'small':
                dict_primary_small[languages[0]] += 1
        else:
            if hf.returnCodeSize(row['Lines of Code(last)']) == 'small':
                dict_primary_small[languages[0]] = 1

        if languages[0] in dict_primary_middle:
            if hf.returnCodeSize(row['Lines of Code(last)']) == 'middle':
                dict_primary_middle[languages[0]] += 1
        else:
            if hf.returnCodeSize(row['Lines of Code(last)']) == 'middle':
                dict_primary_middle[languages[0]] = 1

        if languages[0] in dict_primary_large:
            if hf.returnCodeSize(row['Lines of Code(last)']) == 'large':
                dict_primary_large[languages[0]] += 1
        else:
            if hf.returnCodeSize(row['Lines of Code(last)']) == 'large':
                dict_primary_large[languages[0]] = 1
        
        for language in languages:
            if language in dict_all:
                dict_all[language] += 1
            else:
                dict_all[language] = 1

#sort the two dicts with the value
dict_primary = sorted(dict_primary.items(), key=lambda x: x[1], reverse=True)
dict_all = sorted(dict_all.items(), key=lambda x: x[1], reverse=True)

#create a dict to store TQI,small,middle,large info of each language
dict_primary_info = {'Average TQI': {}, 'number':{}, 'small': {}, 'middle': {}, 'large': {}}

# count the percentage of each language in dict_primary and show the result
#show the number of languages in dict_primary
print('number of languages in dict_primary: ', len(dict_primary))
for key, value in dict_primary:
    #print(key, value, value / len(df_projects), '%') keep 3 decimal places in the percentage
    if key not in dict_primary_tqi:
        dict_primary_tqi[key] = 0
    if key not in dict_primary_small:
        dict_primary_small[key] = 0
    if key not in dict_primary_middle:
        dict_primary_middle[key] = 0
    if key not in dict_primary_large:
        dict_primary_large[key] = 0
    print(key, value, '%.3f' % (value / len(df_projects) * 100), '%', '  TQI', dict_primary_tqi[key] / (value ), '  small', dict_primary_small[key] , '  middle', dict_primary_middle[key], '  large', dict_primary_large[key])
    dict_primary_info['Average TQI'][key] = dict_primary_tqi[key] / value
    dict_primary_info['number'][key] = value
    dict_primary_info['small'][key] = dict_primary_small[key]
    dict_primary_info['middle'][key] = dict_primary_middle[key]
    dict_primary_info['large'][key] = dict_primary_large[key]
    
print('---------------------------------------------')

#draw a stacked bar chart of the number of each language in dict_primary_info
#set the size of the figure
plt.figure(figsize=(5, 8))
#set the title of the figure
# plt.title('number of each language in dict_primary', fontsize=20)
#set the x-axis label of the second subplot
plt.xlabel('Primary programming language')
#set the y-axis label of the second subplot
plt.ylabel('Number')
#set y-axis range
plt.ylim(0, 220)
#set the x-axis label of the second subplot
plt.xticks(rotation=34)
#the x labels are the keys in dict_primary_info
x = list(dict_primary_info['number'].keys())
#the first bar is the number of each language in dict_primary_small
y1 = list(dict_primary_info['small'].values())
#the second bar is the number of each language in dict_primary_middle
y2 = list(dict_primary_info['middle'].values())
#the third bar is the number of each language in dict_primary_large
y3 = list(dict_primary_info['large'].values())

#add line for 0, 25, 50, 75, 100, 125, 150, 175, 200, their layer should be below the bars
for i in range(0, 201, 25):
    plt.axhline(i, color='grey', linewidth=0.5)

#add a line chart of the TQI of each language in dict_primary_info
p1 = plt.plot(x, list(dict_primary_info['Average TQI'].values()) , color='#8eaabf', marker='o', linestyle='-', linewidth=2, markersize=3, zorder = 3, label='TQI')

#add the values of the TQI of each language in dict_primary_info on top of the line chart
# for a, b in zip(x, list(dict_primary_info['Average TQI'].values())):
#     plt.text(a, b + 1, '%.2f' % b, ha='center', va='bottom', fontsize=10)

#add the first bar
b1 = plt.bar(x, y1, label='small', color='#486ab3', zorder = 2)
#add the second bar
b2 = plt.bar(x, y2, bottom=y1, label='middle', color='#db6a32', zorder = 2)
#add the third bar
b3 = plt.bar(x, y3, bottom=np.array(y1) + np.array(y2), label='large', color='#f1b91f', zorder = 2)
#add the text of the dict_primary_info['number'] of each language in dict_primary_info on top of bar
for a, b in zip(x, list(dict_primary_info['number'].values())):
    plt.text(a, b + 1, '%.0f' % b, ha='center', va='bottom', fontsize=10, zorder = 2)



#show the legend  in the plot
plt.legend(bbox_to_anchor=(0.71, 0.98), loc='upper left', borderaxespad=0.)
#show the figure
plt.savefig(PREFIX + '/figs/RQ3/topAna/tqiinfo of each primary language.png', bbox_inches='tight')
plt.close()

print(one_language_cnt , ' projects have only one language')

print('---------------------------------------------')

#show the number of languages in dict_all
print('number of languages in dict_all: ', len(dict_all))
count = 0
for key, value in dict_all:
    #print(key, value, value / #elements in dict_all, '%') keep 3 decimal places in the percentage
    count += value
for key, value in dict_all:
    #print(key, value, value / #elements in dict_all, '%') keep 3 decimal places in the percentage
    print(key,':', value,'-', '%.3f' % (value / count * 100), '%')

print('---------------------------------------------')

#show the 'Average TQI Change(monthly)' of projects with different 'Programming language'
#traverse the df_projects

print('---------------------------------------------')

#merge the 'Owner' and 'Site' columns in df_projects
df_projects['Owner'] = df_projects['Owner'].astype(str)
df_projects['Site'] = df_projects['Site'].astype(str)
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
for key, value in dict_ownerSite[:15]:
    print(key, value)

print('---------------------------------------------')

def show_TQI_scatter_plot_and_lineChart(df_projects):
    #show the scatter plot and lineChartof 'Date' and 'Average TQI (first month)' in two subplots
    #set the size of the figure
    plt.figure(figsize=(20, 10))
    #set the title of the figure
    # plt.title('TQI of ' + hf.hashName(df_projects.iloc[0]['OwnerSite'], 9), fontsize=20)
    #set the x-axis label of the second subplot
    plt.xlabel('Start Date', fontsize=16)
    #set the y-axis label of the second subplot
    plt.ylabel('Average TQI (first first 30days)', fontsize=16)
    #set y-axis range
    plt.ylim(50, 100)
    #set the axis font size
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    #show the scatter plot of 'Date' and 'Average TQI (first month)' in the first subplot
    plt.scatter(df_projects['StartDate'], df_projects['Average TQI (first month)'], color = '#06a8ff')
    #show the lineChart of 'Date' and 'Average TQI (first month)' in the second subplot
    plt.plot(df_projects['StartDate'], df_projects['Average TQI (first month)'])
    #show the figure
    # plt.show()
    plt.savefig(PREFIX + '/figs/RQ3/topAna/TQI of ' + hf.hashName(df_projects.iloc[0]['Owner'], 6) + '-' + hf.hashName(df_projects.iloc[0]['Site'], 4) + '.png', bbox_inches='tight')
    plt.close()

#change the first week to the first 15 days
def show_TQI_scatter_plot_and_lineChart_o(df_projects):
    #show the scatter plot and lineChartof 'Date' and 'Average TQI (first week)' in two subplots
    #set the size of the figure
    plt.figure(figsize=(20, 10))
    #set the title of the figure
    plt.title('TQI of ' + hf.hashName(df_projects.iloc[0]['OwnerSite'], 9), fontsize=20)
    #set the x-axis label of the second subplot
    plt.xlabel('StartDate')
    #set the y-axis label of the second subplot
    plt.ylabel('Average TQI (first15))')
    #set y-axis range
    plt.ylim(50, 100)
    #show the scatter plot of 'Date' and 'Average TQI (first week)' in the first subplot
    plt.scatter(df_projects['StartDate'], df_projects['Average TQI (first15))'])
    #show the lineChart of 'Date' and 'Average TQI (first week)' in the second subplot
    plt.plot(df_projects['StartDate'], df_projects['Average TQI (first15))'])
    #show the figure
    # plt.show()
    plt.savefig(PREFIX + '/figs/RQ3/topAna/TQI of ' + hf.hashName(df_projects.iloc[0]['Owner'], 6) + '-' + hf.hashName(df_projects.iloc[0]['Site'], 4) + '_o.png', bbox_inches='tight')
    plt.close()
    

for key, value in dict_ownerSite[:7]:
    df_projects_temp = df_projects[df_projects['OwnerSite'] == key]
    #change the type of 'StartDate' to datetime
    df_projects_temp['StartDate'] = pd.to_datetime(df_projects_temp['StartDate'])
    #sort the df_projects_temp by 'StartDate'
    df_projects_temp = df_projects_temp.sort_values(by='StartDate')
    show_TQI_scatter_plot_and_lineChart(df_projects_temp)
    # show_TQI_scatter_plot_and_lineChart_o(df_projects_temp)

print('---------------------------------------------')

#create a dict for all unique 'Programming language' in df_projects
dict_language = {}
for index, row in df_projects.iterrows():
    if row['Programming language'] in dict_language:
        dict_language[row['Programming language']] += 1
    else:
        dict_language[row['Programming language']] = 1
#sort the dict_language by value
dict_language = sorted(dict_language.items(), key=lambda x: x[1], reverse=True)

#for each 'Programming language' in dict_language, calculate the avg 'Average TQI Change(monthly)' of projects with the 'Programming language'
#and show the result
languageSet_avgTQIChange = {}
for key, value in dict_language:
    df_projects_temp = df_projects[df_projects['Programming language'] == key]
    #calculate the avg 'Average TQI Change(monthly)' of projects with the 'Programming language'
    avg = df_projects_temp['Average TQI Change(monthly)'].mean()
    #store the avg in languageSet_avgTQIChange
    languageSet_avgTQIChange[key] = [value, avg]
#sort the languageSet_avgTQIChange by value[1]
languageSet_avgTQIChange = sorted(languageSet_avgTQIChange.items(), key=lambda x: x[1][1], reverse=True)


languageSetTQI = [[],  []]

# print the key and #value in languageSet_avgTQIChange and in dict_language
for key, value in languageSet_avgTQIChange:
    languages = key.split()
    if len(languages) == 1 and value[0] > 10:
        print(key, value[0], value[1])
        languageSetTQI[0].append(key)
        languageSetTQI[1].append(value[1])
print('---------------------------------------------')
# print the key and #value in languageSet_avgTQIChange and in dict_language
for key, value in languageSet_avgTQIChange:
    languages = key.split()
    if len(languages) == 2 and value[0] > 10:
        print(key, value[0], value[1])
        languageSetTQI[0].append(key)
        languageSetTQI[1].append(value[1])
print('---------------------------------------------')
# print the key and #value in languageSet_avgTQIChange and in dict_language
for key, value in languageSet_avgTQIChange:
    languages = key.split()
    if len(languages) == 3 and value[0] > 10:
        print(key, value[0], value[1])
        languageSetTQI[0].append(key)
        languageSetTQI[1].append(value[1])
print('---------------------------------------------')

#draw a line chart for languageSetTQI
#set the size of the figure
plt.figure(figsize=(8, 5))
#set the title of the figure
# plt.title('Average TQI Change(monthly) of languageSet', fontsize=20)
#set the x-axis label 
plt.xlabel('Language Set Index')
#set the y-axis label 
plt.ylabel('TQI Monthly Average Change')
#set y-axis range
plt.ylim(-0.1, 0.6)
#let the x-axis show every tick
xx = np.arange(1, 12, 1)
plt.xticks(xx)
#the x labels are the keys in languageSetTQI
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
#the y labels are the values in languageSetTQI
y = languageSetTQI[1]
#show the lineChart, show every x label
plt.plot(x, y, marker='o', linestyle='-', linewidth=2, markersize=3, zorder = 3, label='TQI MAC', color='#5ba585')
#add text on top of each dot
for a, b in zip(x, y):
    plt.text(a, b + 0.02, '%.3f' % b, ha='center', va='bottom', fontsize=10)
#show the figure
plt.legend(loc = 'upper right')
# plt.show()
plt.savefig(PREFIX + '/figs/RQ3/topAna/TQI MAC of languageSet.png', bbox_inches='tight')
plt.close()

#sort the df_projects by '#Runs' and draw the lineChart of '#Runs' and 'Average TQI Change(monthly)'
df_projects = df_projects.sort_values(by='#Run')
#set the size of the figure
plt.figure(figsize=(20, 10))
#set the title of the figure
plt.title('#Run and Average TQI Change(monthly)', fontsize=20)
#set the axis font size
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
#set the x-axis label of the second subplot
plt.xlabel('#Run')
#set the y-axis label of the second subplot
plt.ylabel('Average TQI Change(monthly)')
#show the lineChart of '#Runs' and 'Average TQI Change(monthly)'
plt.plot(df_projects['#Run'], df_projects['Average TQI Change(monthly)'])
#show the figure
# plt.show()
plt.savefig(PREFIX + '/figs/RQ3/topAna/#Run and Average TQI Change(monthly).png', bbox_inches='tight')
plt.close()

print('---------------------------------------------')

timeTQI = [[], [],  [], [], [], []]

for index, row in df_projects.iterrows():
    #calculate the days using the 'StartDate' and 'EndDate', date format like 2022-02-21 17:32:58+01:00
    days = datetime.datetime.strptime(row['LatestDate'], '%Y-%m-%d %H:%M:%S%z') - datetime.datetime.strptime(row['StartDate'], '%Y-%m-%d %H:%M:%S%z')
    #change the days to int
    days = days.days
    timeTQI[0].append(row['hashedProjectName'])
    timeTQI[1].append(days)
    timeTQI[2].append(row['Average TQI'])
    timeTQI[3].append(row['Average TQI Change(monthly)'])
    timeTQI[4].append(row['#Run'])
    timeTQI[5].append(row['StartDate'])

#set the size of the figure
plt.figure(figsize=(6, 5))
#set the title of the figure
# plt.title('Average TQI Change(monthly) of languageSet', fontsize=20)
#set the x-axis label
plt.xlabel('#Days')
#set the y-axis label
plt.ylabel('TQI Monthly Average Change')
#set y-axis range
plt.ylim(-1, 1)
# plt.ylim(50, 100)
#draw scatter plot of 'Days' and 'Average TQI Change(monthly)'
s1 = plt.scatter(timeTQI[1], timeTQI[3], marker='o', s=15, edgecolors='#483777', zorder = 3, label='TQI MAC', color='#866bcc')
#show the figure
# plt.show()
plt.savefig(PREFIX + '/figs/RQ3/topAna/TQI MAC of days.png', bbox_inches='tight')
# plt.clf()
#draw scatter plot of 'runs' and 'Average TQI Change(monthly)'
#remove the s1 from the figure
s1.remove()
plt.xlabel('#Runs')
s2 = plt.scatter(timeTQI[4], timeTQI[3], marker='o', s=15, edgecolors='#a77385', zorder = 3, label='TQI MAC', color='#efa4be')
# plt.scatter(timeTQI[1], timeTQI[3], marker='o', s=15, edgecolors='#a77385', zorder = 3, label='TQI MAC', color='#efa4be')
plt.savefig(PREFIX + '/figs/RQ3/topAna/TQI MAC of runs.png', bbox_inches='tight')
plt.close()

plt.figure(figsize=(8, 6.5))
plt.xlabel('#Days')
plt.ylabel('#Runs')
plt.ylim(0, 3600)
plt.xlim(0, 3600)
#set different colors for different dots

# s3 = plt.scatter(timeTQI[1], timeTQI[4], c = timeTQI[3],marker='o', s=15, edgecolors='#6c6460', zorder = 3, label='TQI MAC', color='#6c6460')
s3 = plt.scatter(timeTQI[1], timeTQI[4], c = timeTQI[3],marker='o', s=15,cmap='jet')
#set colorbar range
plt.clim(-0.4, 0.4)
plt.colorbar(s3)
# plt.show()
plt.savefig(PREFIX + '/figs/RQ3/topAna/TQI MAC of days and runs.png', bbox_inches='tight')
plt.close()

print('---------------------------------------------')

#draw the scatter plot of 'Average TQI Change(monthly)', postive 'Average TQI Change(monthly)' would be green and above the x-axis, negative 'Average TQI Change(monthly)' would be red and below the x-axis
#the dot is hollowimport matplotlib.pyplot as plt

plt.figure(figsize=(20, 10))
# plt.title('Average TQI Change(monthly)', fontsize=20)
plt.xlabel('Index', fontsize=16)
plt.ylabel('Average TQI Change(monthly)', fontsize=16)

#set the axis font size
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

# create a list of booleans
positive_condition = df_projects['Average TQI Change(monthly)'] > 0

# plot the positive and negative points separately
plt.scatter(
    df_projects.index, 
    df_projects['Average TQI Change(monthly)'],
    c=['green' if condition else 'red' for condition in positive_condition],
    marker='o',
    s=50,
    edgecolors='black'
)

plt.savefig(PREFIX + '/figs/RQ3/topAna/Average TQI Change(monthly).png', bbox_inches='tight')
plt.close()
# plt.show()
