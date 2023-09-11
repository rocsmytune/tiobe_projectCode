'''
Author: rocs
Date: 2023-08-30 21:55:35
LastEditors: rocs
LastEditTime: 2023-09-06 05:50:23
Description: some helper functions for getting monthlyInfo
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

def getAvgMonthlyTQI(metric, df):
    if metric == 'SEC':
        #extract the rows from the df where the TQI version is not 3.11
        df = df.loc[df['TQI Version'] != 3.11]
        #reset the index of the df
        df = df.reset_index(drop=True)
        #set df['SEC'] to float
        df['TQI Security'] = df['TQI Security'].astype(float)

        if len(df) == 0:
            return []
    if metric == 'DeadCode':
        df = df.loc[df['TQI Version'] == 3.11]
        #reset the index of the df
        df = df.reset_index(drop=True)
        df['TQI Dead Code'] = df['TQI Dead Code'].astype(float)
        if len(df) == 0:
            return []

    #get the monthly average TQI score
    monthlyChangeRate = []
    monthlyCount = 0
    thisMonthTQI = 0
    thisMonthLOC = 0
    year = df['Date'].iloc[0].year
    month = df['Date'].iloc[0].month


    #get the average TQI score for each month according to the 'Date' column
    for index, row in df.iterrows():
        #get the year and month of the current row
        cYear = row['Date'].year
        cMonth = row['Date'].month
        if year == cYear and month == cMonth :
            monthlyCount += 1
            # print(row[returnTQIMetricName(metric)])
            thisMonthTQI += row[hf.returnTQIMetricName(metric)]
            thisMonthLOC += row['Lines of Code']
            
        #if the year or month of the current row is different from the previous row, then calculate the average TQI score for the previous month
        else :
            #add the average TQI score to the list
            monthlyChangeRate.append([[year,month, monthlyCount, thisMonthLOC], thisMonthTQI / monthlyCount])
            #reset the monthlyCount and thisMonthTQI
            monthlyCount = 1
            thisMonthLOC = row['Lines of Code']
            thisMonthTQI = row[hf.returnTQIMetricName(metric)]
            #update the year and month
            year = row['Date'].year
            month = row['Date'].month
    
    #add the last month's average TQI score to the list
    monthlyChangeRate.append([[year,month, monthlyCount, thisMonthLOC], thisMonthTQI / monthlyCount])
    # print(monthlyChangeRate)
    return monthlyChangeRate


def getMonthlyChange(monthlyChangeRate):
    #get the total number of months
    monthNum = len(monthlyChangeRate)
    #get the total number of months with TQI growth
    monthNumGrowth = 0.0
    monthNumGrowthRate = 0.0
    #get the total number of months with TQI decline
    monthNumDecline = 0.0
    monthNumDeclineRate = 0.0

    thisMonth = monthlyChangeRate[0][1]
    lastMonth = 0

    for mo in monthlyChangeRate:
        if monthlyChangeRate.index(mo) != 0:
            lastMonth = thisMonth
            thisMonth = mo[1]
            
            #calculate how many months between the two months according to the mo[0][0]: year and mo[0][1]: month
            distance = (mo[0][0] - monthlyChangeRate[monthlyChangeRate.index(mo) - 1][0][0]) * 12 + (mo[0][1] - monthlyChangeRate[monthlyChangeRate.index(mo) - 1][0][1])
            
            if thisMonth > lastMonth:
                monthNumGrowth += (thisMonth - lastMonth)  / distance
                monthNumGrowthRate += (thisMonth - lastMonth) / lastMonth
            elif thisMonth < lastMonth:
                monthNumDecline += (lastMonth - thisMonth) / distance
                monthNumDeclineRate += (lastMonth - thisMonth) / lastMonth
        else:
            continue
    return monthNum, monthNumGrowth, monthNumGrowthRate, monthNumDecline, monthNumDeclineRate


def getAvgMonthlyTQIChangeRate(monthNum, monthNumGrowth, monthNumGrowthRate, monthNumDecline, monthNumDeclineRate):
    
    avgMonthlyTQIChange = (monthNumGrowth - monthNumDecline) / (monthNum - 1)
    avgMonthlyTQIChangeTotal = (monthNumGrowth + monthNumDecline) / (monthNum - 1)
    avgMonthlyTQIChangeRate = (monthNumGrowthRate - monthNumDeclineRate) / (monthNum - 1)
    avgMonthlyTQIChangeRateTotal = (monthNumGrowthRate + monthNumDeclineRate) / (monthNum - 1)
    
    return avgMonthlyTQIChange, avgMonthlyTQIChangeTotal, avgMonthlyTQIChangeRate, avgMonthlyTQIChangeRateTotal

def calculate_avgTQIChangeRate_Metric(index, row, df_projectMonthlyInfo, metricTopic):
    if np.isnan(df_projectMonthlyInfo.loc[index - 1, 'avgTQI_' + metricTopic]) or df_projectMonthlyInfo.loc[index - 1, 'avgTQI_' + metricTopic] == 0 or np.isnan(row['avgTQI_' + metricTopic]) or row['avgTQI_' + metricTopic] == 0:
        df_projectMonthlyInfo.loc[index, 'avgTQIChangeRate_'+ metricTopic] = 0
        df_projectMonthlyInfo.loc[index, 'deltaTQI_'+ metricTopic] = 0
    else:
        df_projectMonthlyInfo.loc[index, 'avgTQIChangeRate_' + metricTopic] = (row['avgTQI_' + metricTopic] - df_projectMonthlyInfo.loc[index - 1, 'avgTQI_' + metricTopic]) / df_projectMonthlyInfo.loc[index - 1, 'avgTQI_' + metricTopic]
        df_projectMonthlyInfo.loc[index, 'deltaTQI_'+metricTopic] = row['avgTQI_' + metricTopic] - df_projectMonthlyInfo.loc[index - 1, 'avgTQI_' + metricTopic]
    
    return df_projectMonthlyInfo

def calculate_contributions(index, df_projectMonthlyInfo):
    df_projectMonthlyInfo.loc[index, 'TestCoverage_Contribution(20%)'] = df_projectMonthlyInfo.loc[index, 'deltaTQI_TestCoverage'] * 0.2
    df_projectMonthlyInfo.loc[index, 'DupCode_Contribution(10%)'] = df_projectMonthlyInfo.loc[index, 'deltaTQI_DupCode'] * 0.1
    df_projectMonthlyInfo.loc[index, 'DeadCode_Contribution(5%)'] = df_projectMonthlyInfo.loc[index, 'deltaTQI_DeadCode'] * 0.05
    df_projectMonthlyInfo.loc[index, 'AI_Contribution(20%)'] = df_projectMonthlyInfo.loc[index, 'deltaTQI_AI'] * 0.2
    df_projectMonthlyInfo.loc[index, 'SEC_Contribution(5%)'] = df_projectMonthlyInfo.loc[index, 'deltaTQI_SEC'] * 0.05
    df_projectMonthlyInfo.loc[index, 'FanOut_Contribution(5%)'] = df_projectMonthlyInfo.loc[index, 'deltaTQI_FanOut'] * 0.05
    df_projectMonthlyInfo.loc[index, 'CS_Contribution(10%)'] = df_projectMonthlyInfo.loc[index, 'deltaTQI_CS'] * 0.1
    df_projectMonthlyInfo.loc[index, 'CW_Contribution(15%)'] = df_projectMonthlyInfo.loc[index, 'deltaTQI_CW'] * 0.15
    df_projectMonthlyInfo.loc[index, 'Complexity_Contribution(15%)'] = df_projectMonthlyInfo.loc[index, 'deltaTQI_Complexity'] * 0.15


    #get the largestContributorMetric and largestContribution(%) from the above metrics, here first means the metric's name, second means the metric's contribution(%)
    # largestContributorMetric = max(df_projectMonthlyInfo.loc[index, 'TestCoverage_Contribution(20%)'], df_projectMonthlyInfo.loc[index, 'DupCode_Contribution(10%)'], df_projectMonthlyInfo.loc[index, 'DeadCode_Contribution(5%)'], df_projectMonthlyInfo.loc[index, 'AI_Contribution(20%)'], df_projectMonthlyInfo.loc[index, 'SEC_Contribution(5%)'], df_projectMonthlyInfo.loc[index, 'FanOut_Contribution(5%)'], df_projectMonthlyInfo.loc[index, 'CS_Contribution(10%)'], df_projectMonthlyInfo.loc[index, 'CW_Contribution(15%)'], df_projectMonthlyInfo.loc[index, 'Complexity_Contribution(15%)'])
    contribution_dict = {
        'TestCoverage': df_projectMonthlyInfo.loc[index, 'TestCoverage_Contribution(20%)'],
        'DupCode': df_projectMonthlyInfo.loc[index, 'DupCode_Contribution(10%)'],
        'DeadCode': df_projectMonthlyInfo.loc[index, 'DeadCode_Contribution(5%)'],
        'AI': df_projectMonthlyInfo.loc[index, 'AI_Contribution(20%)'],
        'SEC': df_projectMonthlyInfo.loc[index, 'SEC_Contribution(5%)'],
        'FanOut': df_projectMonthlyInfo.loc[index, 'FanOut_Contribution(5%)'],
        'CS': df_projectMonthlyInfo.loc[index, 'CS_Contribution(10%)'],
        'CW': df_projectMonthlyInfo.loc[index, 'CW_Contribution(15%)'],
        'Complexity': df_projectMonthlyInfo.loc[index, 'Complexity_Contribution(15%)']
    }
    
    maxContribution = float('-inf')

    for key, value in contribution_dict.items():
        if abs(value) > maxContribution:
            largestContributorMetric = key
            maxContribution = abs(value) 
    
    df_projectMonthlyInfo.loc[index, 'largestContributorMetric'] = largestContributorMetric
    df_projectMonthlyInfo.loc[index, 'largestContribution(%)'] = contribution_dict[largestContributorMetric]
    
    return df_projectMonthlyInfo