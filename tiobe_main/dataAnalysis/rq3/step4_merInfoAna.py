'''
Author: rocs
Date: 2023-06-21 16:58:41
LastEditors: rocs
LastEditTime: 2023-09-11 20:56:18
Description: 
'''
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import warnings
warnings.filterwarnings('ignore')
import sys
sys.path.append(sys.path[0][:-17])
from helper import presetting
from helper import helperFuncs as hf

PREFIX = presetting.PREFIX

def getColor(metric):
    if metric == 'TestCoverage':
        return 'blue'
    elif metric == 'DupCode':
        return 'yellow'
    elif metric == 'DeadCode':
        return 'red'
    elif metric == 'AI':
        return 'green'
    elif metric == 'SEC':
        return 'black'
    elif metric == 'FanOut':
        return 'purple'
    elif metric == 'CS':
        return 'orange'
    elif metric == 'CW':
        return 'brown'
    elif metric == 'Complexity':
        return 'pink'
    else:
        print('Error: metric name is not correct!')
        sys.exit()
metricTopics = ['TestCoverage', 'DupCode', 'DeadCode', 'AI', 'SEC', 'FanOut', 'CS', 'CW', 'Complexity']
# metricTopics = ['DupCode', 'DeadCode', 'AI', 'SEC', 'FanOut', 'CS', 'CW', 'Complexity']
def returnLargest(df):
    largestPearson = 0
    largestPearsonMetric = ''
    largestSpearman = 0
    largestSpearmanMetric = ''
    largestSlope = 0
    largestSlopeMetric = ''
    
    for metric in metricTopics:
        pearson = df['Pearson Correlation Coefficient_' + metric]
        spearman = df['Spearman Correlation Coefficient_' + metric]
        slope = df['Slope_' + metric]
        
        if pearson > largestPearson:
            largestPearson = pearson
            largestPearsonMetric = metric
        
        if spearman > largestSpearman:
            largestSpearman = spearman
            largestSpearmanMetric = metric
        
        if slope > largestSlope:
            largestSlope = slope
            largestSlopeMetric = metric
    
    return largestPearson, largestPearsonMetric, largestSpearman, largestSpearmanMetric, largestSlope, largestSlopeMetric



df_projects = pd.read_csv(PREFIX + '/docs/output/RQ3/projects_more_than_100_rows_info.csv')
df_metrics = pd.read_csv(PREFIX + '/docs/output/RQ3/projects_more_than_100_rows_TQI_metrics_ver.csv')
#change all blank/nan values in df_merge to  0
df_metrics = df_metrics.fillna(0)
# print(df_projects.columns)print(df_metrics.columns)

#merge two dataframes according to project name
df_merge = pd.merge(df_projects, df_metrics, on='Project Name', how='inner')


#add new columns: largest Pearson value and its corresponding metric, and the largest Spearman value and its corresponding metric, and the largest Kendall value and its corresponding metric
df_merge['Largest Pearson'] = 0
df_merge['Largest Pearson Metric'] = ''
df_merge['Largest Spearman'] = 0
df_merge['Largest Spearman Metric'] = ''
df_merge['Largest Slope'] = 0
df_merge['Largest Slope Metric'] = ''
df_merge['Largest Metric'] = ''

threeSame = 0
peaSlopeSame = 0
threeDiff  = 0
projectNum = df_merge.shape[0]

#for every project, record the largest Pearson value and its corresponding metric, and the largest Spearman value and its corresponding metric, and the largest Kendall value and its corresponding metric
for index, row in df_merge.iterrows():
    row['Largest Pearson'] , row['Largest Pearson Metric'], row['Largest Spearman'], row['Largest Spearman Metric'], row['Largest Slope'], row['Largest Slope Metric'] = returnLargest(row)
    # print(row['Largest Pearson Metric'], row['Largest Spearman Metric'], row['Largest Slope Metric'])
    df_merge.loc[index, 'Largest Pearson'] = row['Largest Pearson']
    df_merge.loc[index, 'Largest Pearson Metric'] = row['Largest Pearson Metric']
    df_merge.loc[index, 'Largest Spearman'] = row['Largest Spearman']
    df_merge.loc[index, 'Largest Spearman Metric'] = row['Largest Spearman Metric']
    df_merge.loc[index, 'Largest Slope'] = row['Largest Slope']
    df_merge.loc[index, 'Largest Slope Metric'] = row['Largest Slope Metric']

    if row['Largest Pearson Metric'] == row['Largest Spearman Metric'] and row['Largest Spearman Metric'] == row['Largest Slope Metric']:
        df_merge.loc[index, 'Largest Metric'] = row['Largest Pearson Metric']
        threeSame += 1
    elif row['Largest Pearson Metric'] != row['Largest Spearman Metric']:
        if row['Largest Pearson Metric']  == row['Largest Slope Metric']:
            df_merge.loc[index, 'Largest Metric'] = row['Largest Pearson Metric']
            peaSlopeSame += 1
        else:
            df_merge.loc[index, 'Largest Metric'] = ''
            df_merge.loc[index, 'Largest Metric'] = row['Largest Slope Metric']
            threeDiff += 1
    else:
        df_merge.loc[index, 'Largest Metric'] = ''
        df_merge.loc[index, 'Largest Metric'] = row['Largest Slope Metric']
        threeDiff += 1

#print threeSame, peaSlopeSame, threeDiff in percentage(compare to projectNum) keepin 2 decimal places
threeSame = round(threeSame/projectNum, 4)
peaSlopeSame = round(peaSlopeSame/projectNum, 4)
threeDiff = round(threeDiff/projectNum, 4)
print('threeResultsSame: ', '%.2f' % (threeSame * 100),'%', ' pearsonSlopeSame: ', '%.2f' % (peaSlopeSame * 100),'%', ' Other: ', '%.2f' % (threeDiff * 100),'%')

dict_metricCnt = {}
for metric in metricTopics:
    dict_metricCnt[metric] = 0

for index, row in df_merge.iterrows():
    if row['Largest Metric'] != '':
        dict_metricCnt[row['Largest Metric']] += 1

#sort dict_metricCnt by value
dict_metricCnt = dict(sorted(dict_metricCnt.items(), key=lambda item: item[1], reverse=True))
dict_metricCntPer = dict_metricCnt.copy()
#print dict_metricCnt in percentage(compare to projectNum) keepin 2 decimal places
for metric in metricTopics:
    dict_metricCntPer[metric] = round(dict_metricCntPer[metric]/projectNum, 4)
print(dict_metricCntPer)

#draw the pie chart and bar chart of dict_metricCnt in one figure
plt.figure(figsize=(13, 8))
plt.subplot(1, 2, 1)
#draw pie chart, the percentages are dict_metricCnt.values()
plt.pie(dict_metricCnt.values(), colors=[getColor(metric) for metric in dict_metricCnt.keys()], labels=dict_metricCnt.keys(), shadow=False, startangle=90, pctdistance=0.9, explode=(0,0,0,0,0,0,0,0.1,0.15))
# plt.title('The Most TQI Score-Related Metric Distribution', y=-0.1, fontsize=10, fontweight='bold', color='black')
plt.subplot(1, 2, 2)
#draw bar with the same color as pie chart
plt.bar(dict_metricCnt.keys(), dict_metricCnt.values(), color=[getColor(metric) for metric in dict_metricCnt.keys()])
for x, y in zip(dict_metricCnt.keys(), dict_metricCnt.values()):
            # plt.text(x, y + 0.05, '%d' % y, ha='center', va='bottom')
            #show the percentage of the largest metric
            plt.text(x, y + 0.05, '%.2f%%' % (y/sum(dict_metricCnt.values())*100), ha='center', va='bottom')
plt.xticks(rotation=45)
# plt.show()
plt.savefig(PREFIX + '/figs/RQ3/general/mostTQIScoreRelatedMetric.png', dpi=300, bbox_inches='tight')  
plt.close()

df_merge.to_csv(PREFIX + '/docs/output/RQ3/projects_more_than_100_rows_TQI_metrics_ver_largest.csv', index=False)

projectList = df_merge['Project Name'].tolist()
DRAW = True
if DRAW == True:

    #draw the line chart of every project showing the TQI score and the largest metric'ssocre according to df
    for project in projectList:
        df_project = pd.read_csv(PREFIX + '/docs/output/RQ3/cleaned/ClearTQI_' + project + '.csv', encoding='latin-1')
        df_project['Date'] = pd.to_datetime(df_project['Date'])
        #draw lines of TQI and the largest metric
        plt.figure(figsize=(10, 6))    
        
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        plt.gca().xaxis.set_major_locator(mdates.YearLocator())
        #Display the dot every month from the first date without label
        plt.gca().xaxis.set_minor_locator(mdates.MonthLocator())
        #set the x axis range
        plt.xlim(df_project['Date'].iloc[0] - datetime.timedelta(days=60), df_project['Date'].iloc[-1] + datetime.timedelta(days= 60))
        plt.ylim(0, 110)
        #set the x axis label
        plt.xlabel('Date')
        plt.ylabel('TQI Score')
        ax1 = plt.gca()
        ax1.plot(df_project['Date'], df_project['TQI'], label='TQI', color='blue', linewidth=1.0, linestyle='--')
        ax1.plot(df_project['Date'], df_project[hf.returnTQIMetricName(df_merge[df_merge['Project Name'] == project]['Largest Metric'].values[0])], label=df_merge[df_merge['Project Name'] == project]['Largest Metric'].values[0], color='red', linewidth=1.0, linestyle='--')
        ax1.legend(loc='upper left')

        #add a new axis on the right side for Lines of Code
        ax2 = plt.gca().twinx()
        ax2.plot(df_project['Date'], df_project['Lines of Code'], label='Lines of Code', color='green', linewidth=1.0, linestyle='-')
        ax2.legend(loc='upper right')
        ax2.set_ylabel('Lines of Code')
        #set the y axis range
        ax2.set_ylim(0, df_project['Lines of Code'].max()*1.4)

        pName = 'Project-' + hf.hashName(project)+ '\'s'
        # plt.title(pName + ' TQI Score and Most Significant Metric TQI Score')
        #set a subtitle below the title, sate the project's size, language, site and owner
        # plt.suptitle('Latest Info - Size: ' + str(df_project['Lines of Code'].iloc[-1]) + '('+ hf.returnCodeSize(df_project['Lines of Code'].iloc[-1])+ ')' + ', Language: [' + df_project['Programming language'].iloc[-1] + ']'+ ', Site: ' +  hf.hashName(df_project['Site'].iloc[-1], 4) + ', Owner: ' +  hf.hashName(df_project['Owner'].iloc[-1], 8), fontsize=9)
        
        plt.savefig(PREFIX + '/figs/RQ3/linesTQI/ana_' + hf.hashName(project) + '.png', dpi=300, bbox_inches='tight')
        # plt.show()
        plt.close()
