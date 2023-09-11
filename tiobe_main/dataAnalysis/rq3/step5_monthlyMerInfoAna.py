'''
Author: rocs
Date: 2023-07-04 17:07:06
LastEditors: rocs
LastEditTime: 2023-09-11 21:02:58
Description: draw the monthly largest metric line chart
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
import monthlyInfoHelpers as mh

PREFIX = presetting.PREFIX

metricTopics = ['TestCoverage', 'DupCode', 'DeadCode', 'AI', 'SEC', 'FanOut', 'CS', 'CW', 'Complexity']
# metricTopics = ['DupCode', 'DeadCode', 'AI', 'SEC', 'FanOut', 'CS', 'CW', 'Complexity']


df_merver = pd.read_csv(PREFIX + '/docs/output/RQ3/projects_more_than_100_rows_TQI_metrics_ver.csv')
def returnMetricContrib(metric):
    if metric == 'TestCoverage':
        return 'TestCoverage_Contribution(20%)'
    elif metric == 'DupCode':
        return 'DupCode_Contribution(10%)'
    elif metric == 'DeadCode':
        return 'DeadCode_Contribution(5%)'
    elif metric == 'AI':
        return 'AI_Contribution(20%)'
    elif metric == 'SEC':
        return 'SEC_Contribution(5%)'
    elif metric == 'FanOut':
        return 'FanOut_Contribution(5%)'
    elif metric == 'CS':
        return 'CS_Contribution(10%)'
    elif metric == 'CW':
        return 'CW_Contribution(15%)'
    elif metric == 'Complexity':
        return 'Complexity_Contribution(15%)'
    else:
        print('Error: metric name is not correct!')
        sys.exit()

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

def ana_metric_per_project_per_month(projectName, df_project):
    df_mon = pd.read_csv(PREFIX + '/docs/output/RQ3/monthInfo/ClearTQI_' + projectName + '_monthlyInfo.csv')

    #create a dict to store the every metrics' contribution to TQI in total and their appearance times
    metricInfo = {}
    for metric in metricTopics:
        #[total contribution, largest times]
        metricInfo[metric] = [0, 0]

    #traverse every row in the dataframe
    for index, row in df_mon.iterrows():
        #if this is the first row, then skip it
        if index == 0:
            continue
        #traverse every metric in the row
        for metric in metricTopics:
            #add the contribution to the total contribution
                metricInfo[metric][0] += row[returnMetricContrib(metric)]
        #if the largestContributorMetric is not empty, then add 1 to the largest times
        if len(row['largestContributorMetric']) > 0:
            metricInfo[row['largestContributorMetric']][1] += 1
        
    mostFreqMetric = ''
    mostContriMetric = ''

    #find the most frequent metric  according to the appearance times(metricInfo[metric][1])
    largestTimes = 0
    for metric in metricTopics:
        if metricInfo[metric][1] > largestTimes:
            largestTimes = metricInfo[metric][1]
            mostFreqMetric = metric
    #find the most contribution metric  according to the contribution(metricInfo[metric][0])
    largestContribution = 0
    for metric in metricTopics:
        if metricInfo[metric][0] > largestContribution:
            largestContribution = metricInfo[metric][0]
            mostContriMetric = metric

    # print('projectName: ', projectName, 'mostFreqMetric: ', mostFreqMetric, 'mostContriMetric: ', mostContriMetric)
    # sys.exit()
    #add the [total contribution, largest times] to the dataframe according to the projectName
    df_project.loc[df_project['Project Name'] == projectName, 'mostFreqMetric'] = mostFreqMetric
    df_project.loc[df_project['Project Name'] == projectName, 'mostContriMetric'] = mostContriMetric

    print('#############################################')
    DRAW = True
    if DRAW == True:
        #draw the monthly largest metric line chart
        df = pd.read_csv(PREFIX + '/docs/output/RQ3/cleaned/ClearTQI_' + projectName + '.csv')#give the date column a datetime format
        df['Date'] = pd.to_datetime(df['Date'])
        monthlyChangeRate = mh.getAvgMonthlyTQI('', df)
        #create a plot
        #set the figure size
        plt.figure(figsize=(10, 6))
        #set the title
        # plt.title(hf.hashName(projectName) + ' monthly largest metric line chart')
        # plt.suptitle('Latest Info - Size: ' + str(df['Lines of Code'].iloc[-1]) + '('+ hf.returnCodeSize(df['Lines of Code'].iloc[-1])+ ')' + ', Language: [' + df['Programming language'].iloc[-1] + ']'+ ', Site: ' + hf.hashName(df['Site'].iloc[-1], 4) + ', Owner: ' +  hf.hashName(df['Owner'].iloc[-1], 8), fontsize=9)
            
        #set the df['Date'] as the x axis
        #Display the label every month from the first date to the last date
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        plt.gca().xaxis.set_major_locator(mdates.YearLocator())
        #Display the dot every month from the first date without label
        plt.gca().xaxis.set_minor_locator(mdates.MonthLocator())
        #set the x axis range
        plt.xlim(df['Date'].iloc[0] - datetime.timedelta(days=60), df['Date'].iloc[-1] + datetime.timedelta(days= 60))

        x_label = []
        y_label = []
        m_label = ['']

        #the x axis is the date, the y axis is the avgTQI
        #draw the monthly average TQI scores' line on the ax1, the x value is the mid of each month, the y value is the average TQI score per month
        for monthly in monthlyChangeRate:
            #get the date of the mid of the month
            date = datetime.date(monthly[0][0], monthly[0][1], 15)
            x_label.append(date)
            y_label.append(monthly[1])
        
        #travese df_mon to get the largest metric
        for index, row in df_mon.iterrows():
            #if this is the first row, then skip it
            if index == 0:
                continue
            #add it to the m_label
            m_label.append(row['largestContributorMetric'])
        # print(m_label)
        x_draw_label = []
        y_draw_label = []

        #traverse the m_label 
        for i in range(len(m_label)):
            #if index is 0, then skip it
            if i == 0:
                #add the first x_label and y_label to the x_draw_label and y_draw_label
                x_draw_label.append(x_label[i])
                y_draw_label.append(y_label[i])
            else:
                #if the m_label[i] is not equal to the m_label[i-1], then add the x_label and y_label to the x_draw_label and y_draw_label
                if m_label[i] == m_label[i-1]:
                    x_draw_label.append(x_label[i])
                    y_draw_label.append(y_label[i])
                else:
                    x_draw_label.append(x_label[i])
                    y_draw_label.append(y_label[i])
                    # plt.plot(x_draw_label, y_draw_label, color=getColor(m_label[i]), marker='.', markersize=3)
                    plt.plot(x_draw_label, y_draw_label, color=getColor(m_label[i]), linewidth=1.5, linestyle='-')
                    #keep the last x_label and y_label in the x_draw_label and y_draw_label 
                    x_draw_label = [x_label[i]]
                    y_draw_label = [y_label[i]]
        # plt.plot(x_draw_label, y_draw_label, color=getColor(m_label[-1]), marker='.', markersize=3)
        plt.plot(x_draw_label, y_draw_label, color=getColor(m_label[i]), linewidth=1.5, linestyle='-')

        #draw the monthly average TQI scores' line on the ax1, the x value is the mid of each month, the y value is the average TQI score per month
        i = 0
        for monthly in monthlyChangeRate:
            #get the date of the mid of the month
            date = datetime.date(monthly[0][0], monthly[0][1], 15)
            x_label.append(date)
            y_label.append(monthly[1])
            #draw the line
            plt.plot(date, monthly[1], color='black', marker='o', markersize=4, markerfacecolor='white')
            #set the label 
            if (i  + 6) % 6 == 0:
                # plt.text(date, monthly[1], str(round(monthly[1], 2)), ha='center', va='bottom', fontsize=7)
                #change the above text to a little higher
                plt.text(date, monthly[1] + 0.4, str(round(monthly[1], 2)), ha='center', va='bottom', fontsize=7)
            i+=1

        #show the mappping between the color and the metric in function getColor() with legend in the figure
        plt.plot(0,0,label='TestCoverage', color='blue', linewidth=1.5, linestyle='-')
        plt.plot(0,0,label='DupCode', color='yellow', linewidth=1.5, linestyle='-')
        plt.plot(0,0,label='DeadCode', color='red', linewidth=1.5, linestyle='-')
        plt.plot(0,0,label='AI', color='green', linewidth=1.5, linestyle='-')
        plt.plot(0,0,label='SEC', color='black', linewidth=1.5, linestyle='-')
        plt.plot(0,0,label='FanOut', color='purple', linewidth=1.5, linestyle='-')
        plt.plot(0,0,label='CS', color='orange', linewidth=1.5, linestyle='-')
        plt.plot(0,0,label='CW', color='brown', linewidth=1.5, linestyle='-')
        plt.plot(0,0,label='Complexity', color='pink', linewidth=1.5, linestyle='-')
        plt.plot(0,0,label='Average Monthly TQI Score', color='black', marker='o', markersize=2.5, markerfacecolor='white')
        plt.legend(loc='lower left')

        #set the y axis label
        plt.ylabel('Average Monthly TQI Score')
        #set the y axis range
        plt.ylim(0, 100)
        #set the x axis label
        plt.xlabel('Date')
        #set the legend
        # plt.show()
        # sys.exit(0)
        plt.savefig(PREFIX + '/figs/RQ3/MetricsTQI/' + hf.hashName(proj) + '_TQI.png', dpi=300, bbox_inches='tight')
        plt.close()

    return df_project

#main
if __name__ == '__main__':
    DRAW = True
    df_project = pd.read_csv(PREFIX + '/docs/output/RQ3/projects_more_than_100_rows_info.csv')
    projLis = pd.read_csv(PREFIX + '/docs/output/RQ3/projects_more_than_100_rows_info.csv')
    projList = projLis['Project Name'].tolist()
    # projList = ['ACP Routing Tool']
    for proj in projList:
        df_project = ana_metric_per_project_per_month(proj, df_project)

    
    df_project.to_csv(PREFIX + '/docs/output/RQ3/projects_more_than_100_rows_info_withLargestMetrics.csv', index=False)

    if DRAW == True:
        #use a dict to store the number of the largest metric in the df_project
        metricFreqNum = {}
        metricContriNum = {}
        for metric in metricTopics:
            metricFreqNum[metric] = 0
            metricContriNum[metric] = 0
        
        #traverse the df_project to get the number of the largest metric
        for index, row in df_project.iterrows():
            if row['mostFreqMetric'] != '':
                metricFreqNum[row['mostFreqMetric']] += 1
            if row['mostContriMetric'] != '':
                metricContriNum[row['mostContriMetric']] += 1

        #sort the metricFreqNum and metricContriNum from the largest to the smallest
        metricFreqNum = dict(sorted(metricFreqNum.items(), key=lambda item:item[1], reverse=True))
        metricContriNum = dict(sorted(metricContriNum.items(), key=lambda item:item[1], reverse=True))
        
        #draw the pie chart and histogram in one figure
        #the pie chart only shows the metrics' name and the histogram shows the percentage of the largest metric
        #the color follows the function getColor()

        plt.figure(figsize=(13, 8))
        plt.subplot(1, 2, 1)
        plt.pie(metricFreqNum.values(), labels=metricFreqNum.keys(), shadow=False, startangle=90, colors=[getColor(metric) for metric in metricFreqNum.keys()], pctdistance=0.9, explode=(0,0,0,0,0,0.2,0.4,0.6,0.8))
        #add a title on the bottom of the pie chart
        # plt.title('The Number of the Most Frequent Metric', y=-0.1, fontsize=10, fontweight='bold', color='black')
        plt.subplot(1, 2, 2)
        #draw the histogram, rotate the x axis label 45 degree, show the value on the top of the bar
        plt.bar(metricFreqNum.keys(), metricFreqNum.values(), color=[getColor(metric) for metric in metricFreqNum.keys()])
        for x, y in zip(metricFreqNum.keys(), metricFreqNum.values()):
            # plt.text(x, y + 0.05, '%d' % y, ha='center', va='bottom')
            #show the percentage of the largest metric
            plt.text(x, y + 0.05, '%.2f%%' % (y/sum(metricFreqNum.values())*100), ha='center', va='bottom')

        plt.xticks(rotation=45)
        # plt.show()
        plt.savefig(PREFIX + '/figs/RQ3/general/mostFreqMetric.png', dpi=300, bbox_inches='tight')
        # sys.exit(0)
        plt.close()

        plt.figure(figsize=(13, 8))
        plt.subplot(1, 2, 1)
        plt.pie(metricContriNum.values(), labels=metricContriNum.keys(), shadow=False, startangle=90, colors=[getColor(metric) for metric in metricContriNum.keys()], pctdistance=0.9, explode=(0,0,0,0,0,0,0,0.1,0.2))
        #add a title on the bottom of the pie chart
        # plt.title('The Number of the Most Contribution Metric', y=-0.1, fontsize=10, fontweight='bold', color='black')
        plt.subplot(1, 2, 2)
        #draw the histogram, rotate the x axis label 45 degree, show the value on the top of the bar
        plt.bar(metricContriNum.keys(), metricContriNum.values(), color=[getColor(metric) for metric in metricContriNum.keys()])
        for x, y in zip(metricContriNum.keys(), metricContriNum.values()):
            # plt.text(x, y + 0.05, '%d' % y, ha='center', va='bottom')
            #show the percentage of the largest metric
            plt.text(x, y + 0.05, '%.2f%%' % (y/sum(metricContriNum.values())*100), ha='center', va='bottom')
        
        plt.xticks(rotation=45)
        # plt.show()
        plt.savefig(PREFIX + '/figs/RQ3/general/mostContriMetric.png', dpi=300, bbox_inches='tight')
        # sys.exit(0)
        plt.close()


    print('Done!')