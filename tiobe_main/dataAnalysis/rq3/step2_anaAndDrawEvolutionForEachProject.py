'''
Author: rocs
Date: 2023-08-30 21:21:46
LastEditors: rocs
LastEditTime: 2023-09-11 23:04:53
Description: draw the TQI evolution of each project
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
import monthlyInfoHelpers as mh

PREFIX = presetting.PREFIX
pl = pd.read_csv(PREFIX + '/docs/input/cleaned_projects_more_than_100_rows.txt', header=None)
projectList = pl[0].tolist()
#create a new dataframe to store the info of each project
df_projects = pd.DataFrame(columns=['Project Name', 'Site', 'Owner','hashedProjectName', 'hashedSite', 'hashedOwner', 'Programming language', 
                                    'Lines of Code(first)', 'Lines of Code(last)', 'Lines of Code(average)',
                                    'Average TQI Change(monthly)', 'Average TQI Change(monthly total)', 
                                    'Average TQI Change Rate(monthly)', 'Average TQI Change Rate(monthly total)', 'hasTQI3',
                                    'StartDate', 'LatestDate', 'Average TQI'])
#give the project name column the project list
df_projects['Project Name'] = projectList

#create a new dataframe 
    # use it to store three groups of  values for each project
    # 1. the pearson correlation coefficients between the TQI score and each metric
    # 3. the spearman correlation coefficients between the TQI score and each metric
    # 5. the slope of the linear regression between the TQI score and each metric
metricTopics = ['TestCoverage', 'DupCode', 'DeadCode', 'AI', 'SEC', 'FanOut', 'CS', 'CW', 'Complexity']
column_names = ['Project Name', 'Pearson Correlation Coefficient',  'Spearman Correlation Coefficient', 'Slope']
dataframes = {
    'SEC': pd.DataFrame(columns=column_names),
    'TestCoverage': pd.DataFrame(columns=column_names),
    'DupCode': pd.DataFrame(columns=column_names),
    'DeadCode': pd.DataFrame(columns=column_names),
    'AI': pd.DataFrame(columns=column_names),
    'FanOut': pd.DataFrame(columns=column_names),
    'CS': pd.DataFrame(columns=column_names),
    'CW': pd.DataFrame(columns=column_names),
    'Complexity': pd.DataFrame(columns=column_names)
}
for key in dataframes:
    dataframes[key]['Project Name'] = projectList


def anaAndDrawEvoPerProject(projectName):
    df = pd.read_csv(PREFIX + '/docs/output/rq3/cleaned/ClearTQI_' + projectName + '.csv', encoding='latin-1')
    print('Start drawing the evolution of ' + projectName + '.........................')

    #create a new dataframe to store the monthly info of each project
    df_projectMonthlyInfo = pd.DataFrame(columns=['yearMonth', 'monthlyCount', 'avgTQI', 'deltaTQI', 'avgTQIChangeRate', 'avgLines of Code', 'largestContributorMetric', 'largestContribution(%)',
                                            'avgTQI_TestCoverage', 'deltaTQI_TestCoverage', 'avgTQIChangeRate_TestCoverage', 'TestCoverage_Contribution(20%)',
                                            'avgTQI_DupCode', 'deltaTQI_DupCode', 'avgTQIChangeRate_DupCode', 'DupCode_Contribution(10%)',
                                            'avgTQI_DeadCode', 'deltaTQI_DeadCode', 'avgTQIChangeRate_DeadCode', 'DeadCode_Contribution(5%)',
                                            'avgTQI_AI', 'deltaTQI_AI', 'avgTQIChangeRate_AI', 'AI_Contribution(20%)',
                                            'avgTQI_SEC', 'deltaTQI_SEC','avgTQIChangeRate_SEC', 'SEC_Contribution(5%)',
                                            'avgTQI_FanOut', 'deltaTQI_FanOut', 'avgTQIChangeRate_FanOut', 'FanOut_Contribution(5%)',
                                            'avgTQI_CS', 'deltaTQI_CS', 'avgTQIChangeRate_CS', 'CS_Contribution(10%)',
                                            'avgTQI_CW', 'deltaTQI_CW', 'avgTQIChangeRate_CW', 'CW_Contribution(15%)',
                                            'avgTQI_Complexity', 'deltaTQI_Complexity', 'avgTQIChangeRate_Complexity', 'Complexity_Contribution(15%)',
                                            ])
    
    try:
        # #: Directly call the lineChanged metric in the API here
        ##: Supplement the cleaning of the newly added three columns: remove ', ', and convert to float
        df['Change Rate'] = df['Change Rate'].str.replace(',', '').astype(int)
        # df['Lines of Code: Added'] = df['Lines of Code: Added'].str.replace(',', '').astype(int)
        # df['Lines of Code: Deleted'] = df['Lines of Code: Deleted'].str.replace(',', '').astype(int)

        #create a new column called Change Rate("%") and calculate the change rate by dividing the current row's 'Change Rate' by the previous row's 'Lines of Code', for the  first row, divide the current row's 'Change Rate' by the first row's 'Lines of Code'
        df['Change Rate(%)'] = df['Change Rate'] / df['Lines of Code'].shift(1)
        # the first row's 'Change Rate' is NaN change it to 0cle
        df['Change Rate(%)'].iloc[0] = df['Change Rate'].iloc[0] / df['Lines of Code'].iloc[0]
        changeColor = '#bcebc5'

    #if exception occurs, then the df doesn't contain the 'Change Rate' column, so we need to calculate it
    except:
        #add a column called 'Lines Changed' to the df,after the column 'Lines of Code', and calculate the lines changed by the difference between the current and previous rows' 'Lines of Code'
        df.insert(df.columns.get_loc('Lines of Code') + 1, 'Lines Changed', df['Lines of Code'].diff())
        # the first row's 'Lines Changed' is NaN change it to 0
        df['Lines Changed'].iloc[0] = 0
        #add a column called 'Change Rate' to the df,after the column 'Lines Changed', and calculate the change rate by dividing the current row's 'Lines Changed' by the previous row's 'Lines of Code'
        df.insert(df.columns.get_loc('Lines Changed') + 1, 'Change Rate(%)', df['Lines Changed'] / df['Lines of Code'].shift(1))
        # the first row's 'Change Rate' is NaN change it to 0
        df['Change Rate(%)'].iloc[0] = 0
        changeColor = '#ccd0a4'

    #change the 'Change Rate' to percentage
    df['Change Rate(%)'] = df['Change Rate(%)'].apply(lambda x: format(x, '.3%'))
    #replace the "%" with '' in the 'Change Rate' column
    df['Change Rate(%)'] = df['Change Rate(%)'].str.replace('%', '').astype(float)

    

    #give the date column a datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    #get the change date array for tqi version
    changeDateArray = []
    lastTQIVer = df.loc[0, 'TQI Version']
    for index, row in df.iterrows():
        tqi_ver = row['TQI Version']
        if tqi_ver != lastTQIVer:
                changeDateArray.append([row['Date'], 'r', lastTQIVer, tqi_ver])
                lastTQIVer= tqi_ver

    #get the TQI change for each project
    df['TQI Change'] = df['TQI'].diff()
    df['TQI Change'].iloc[0] = 0


    #get the monthly average TQI score
    monthlyChangeRate = mh.getAvgMonthlyTQI('', df)
    
    #need a judgement to judge whether the project has 3.11 version
    monthlyChnageRate_TestCoverage = mh.getAvgMonthlyTQI('TestCoverage', df)
    monthlyChnageRate_DupCode = mh.getAvgMonthlyTQI('DupCode', df)
    monthlyChnageRate_DeadCode = mh.getAvgMonthlyTQI('DeadCode', df)
    monthlyChnageRate_AI = mh.getAvgMonthlyTQI('AI', df)
    monthlyChnageRate_SEC = mh.getAvgMonthlyTQI('SEC', df)
    monthlyChnageRate_FanOut = mh.getAvgMonthlyTQI('FanOut', df)
    monthlyChnageRate_CS = mh.getAvgMonthlyTQI('CS', df)
    monthlyChnageRate_CW = mh.getAvgMonthlyTQI('CW', df)
    monthlyChnageRate_Complexity = mh.getAvgMonthlyTQI('Complexity', df)

    #add the contents of the monthlyChangeRate to the df_projectMonthlyInfo, give the 'avgLines of Code' value according to the thisMonthLOC / monthlyCount
    for mo in monthlyChangeRate:
        df_projectMonthlyInfo = df_projectMonthlyInfo.append({'yearMonth': str(mo[0][0]) + '-' + str(mo[0][1]), 'monthlyCount': mo[0][2], 'avgTQI': mo[1], 'avgLines of Code': mo[0][3] / mo[0][2]}, ignore_index=True)

    # Define a list of tuples where each tuple contains the monthlyChangeRate and column name
    monthlyChangeRates = [
        (monthlyChnageRate_TestCoverage, 'avgTQI_TestCoverage'),
        (monthlyChnageRate_DupCode, 'avgTQI_DupCode'),
        (monthlyChnageRate_DeadCode, 'avgTQI_DeadCode'),
        (monthlyChnageRate_AI, 'avgTQI_AI'),
        (monthlyChnageRate_SEC, 'avgTQI_SEC'),
        (monthlyChnageRate_FanOut, 'avgTQI_FanOut'),
        (monthlyChnageRate_CS, 'avgTQI_CS'),
        (monthlyChnageRate_CW, 'avgTQI_CW'),
        (monthlyChnageRate_Complexity, 'avgTQI_Complexity')
    ]

    # Iterate over the monthly change rates and column names
    for monthlyChangeRate_mer, column_name in monthlyChangeRates:
        for mo in monthlyChangeRate_mer:
            year_month_str = f"{mo[0][0]}-{mo[0][1]}"
            df_projectMonthlyInfo.loc[df_projectMonthlyInfo['yearMonth'] == year_month_str, column_name] = mo[1]
            
    #traverse the df_projectMonthlyInfo to calculate the deltaTQI, avgTQIChange, deltaTQIChange, avgTQIChangeRate and other metrics' columns
    for index, row in df_projectMonthlyInfo.iterrows():
        #if the row is the first row,then set all deltavalue columns to 0
        if index == 0:
            # set all deltavalue columns to 0
            df_projectMonthlyInfo.loc[index, 'deltaTQI'] = 0
            df_projectMonthlyInfo.loc[index, 'avgTQIChangeRate'] = 0
            df_projectMonthlyInfo.loc[index, 'largestContributorMetric'] = ''
            df_projectMonthlyInfo.loc[index, 'largestContribution(%)'] = 0
            df_projectMonthlyInfo.loc[index, 'TestCoverage_Contribution(20%)'] = 0
            df_projectMonthlyInfo.loc[index, 'DupCode_Contribution(10%)'] = 0
            df_projectMonthlyInfo.loc[index, 'DeadCode_Contribution(5%)'] = 0
            df_projectMonthlyInfo.loc[index, 'AI_Contribution(20%)'] = 0
            df_projectMonthlyInfo.loc[index, 'SEC_Contribution(5%)'] = 0
            df_projectMonthlyInfo.loc[index, 'FanOut_Contribution(5%)'] = 0
            df_projectMonthlyInfo.loc[index, 'CS_Contribution(10%)'] = 0
            df_projectMonthlyInfo.loc[index, 'CW_Contribution(15%)'] = 0
            df_projectMonthlyInfo.loc[index, 'Complexity_Contribution(15%)'] = 0
            df_projectMonthlyInfo.loc[index, 'avgTQIChangeRate_TestCoverage'] = 0
            df_projectMonthlyInfo.loc[index, 'avgTQIChangeRate_DupCode'] = 0
            df_projectMonthlyInfo.loc[index, 'avgTQIChangeRate_DeadCode'] = 0
            df_projectMonthlyInfo.loc[index, 'avgTQIChangeRate_AI'] = 0
            df_projectMonthlyInfo.loc[index, 'avgTQIChangeRate_SEC'] = 0
            df_projectMonthlyInfo.loc[index, 'avgTQIChangeRate_FanOut'] = 0
            df_projectMonthlyInfo.loc[index, 'avgTQIChangeRate_CS'] = 0
            df_projectMonthlyInfo.loc[index, 'avgTQIChangeRate_CW'] = 0
            df_projectMonthlyInfo.loc[index, 'avgTQIChangeRate_Complexity'] = 0
            df_projectMonthlyInfo.loc[index, 'deltaTQI_TestCoverage'] = 0
            df_projectMonthlyInfo.loc[index, 'deltaTQI_DupCode'] = 0
            df_projectMonthlyInfo.loc[index, 'deltaTQI_DeadCode'] = 0
            df_projectMonthlyInfo.loc[index, 'deltaTQI_AI'] = 0
            df_projectMonthlyInfo.loc[index, 'deltaTQI_SEC'] = 0
            df_projectMonthlyInfo.loc[index, 'deltaTQI_FanOut'] = 0
            df_projectMonthlyInfo.loc[index, 'deltaTQI_CS'] = 0
            df_projectMonthlyInfo.loc[index, 'deltaTQI_CW'] = 0
            df_projectMonthlyInfo.loc[index, 'deltaTQI_Complexity'] = 0
        else:
            df_projectMonthlyInfo.loc[index, 'deltaTQI'] = row['avgTQI'] - df_projectMonthlyInfo.loc[index - 1, 'avgTQI']
            df_projectMonthlyInfo.loc[index, 'avgTQIChangeRate'] = (row['avgTQI'] - df_projectMonthlyInfo.loc[index - 1, 'avgTQI']) / df_projectMonthlyInfo.loc[index - 1, 'avgTQI']

            df_projectMonthlyInfo = mh.calculate_avgTQIChangeRate_Metric(index, row, df_projectMonthlyInfo, 'TestCoverage')
            df_projectMonthlyInfo = mh.calculate_avgTQIChangeRate_Metric(index, row, df_projectMonthlyInfo, 'DupCode')
            df_projectMonthlyInfo = mh.calculate_avgTQIChangeRate_Metric(index, row, df_projectMonthlyInfo, 'DeadCode')
            df_projectMonthlyInfo = mh.calculate_avgTQIChangeRate_Metric(index, row, df_projectMonthlyInfo, 'AI')
            df_projectMonthlyInfo = mh.calculate_avgTQIChangeRate_Metric(index, row, df_projectMonthlyInfo, 'SEC')
            df_projectMonthlyInfo = mh.calculate_avgTQIChangeRate_Metric(index, row, df_projectMonthlyInfo, 'FanOut')
            df_projectMonthlyInfo = mh.calculate_avgTQIChangeRate_Metric(index, row, df_projectMonthlyInfo, 'CS')
            df_projectMonthlyInfo = mh.calculate_avgTQIChangeRate_Metric(index, row, df_projectMonthlyInfo, 'CW')
            df_projectMonthlyInfo = mh.calculate_avgTQIChangeRate_Metric(index, row, df_projectMonthlyInfo, 'Complexity')
            
            #traverse the df_projectMonthlyInfo to calculate the largestContributorMetric and largestContribution(%)

            #get the largestContributorMetric and largestContribution(%)
            #the largest contributor metric is the metric with the largest deltaTQI * percentage
            #the percentage mapping is as follows:
            #TestCoverage: 20%
            #AI: 20%
            #CW: 15%
            #Complexity: 15%
            #DupCode: 10%
            #CS: 10%
            #DeadCode: 5%
            #SEC: 5%
            #FanOut: 5%
            #calcualte the Contribution(%) for each metric
            df_projectMonthlyInfo = mh.calculate_contributions(index, df_projectMonthlyInfo)
        
    df_projectMonthlyInfo.to_csv(PREFIX + "/docs/output/RQ3/monthInfo/ClearTQI_" + projectName + "_monthlyInfo.csv", index=False)
    #get the total number of months, average montly TQI growth for each project
    monthNum, monthNumGrowth, monthNumGrowthRate, monthNumDecline, monthNumDeclineRate = mh.getMonthlyChange(monthlyChangeRate)
    # get the average monthly TQI change rate for each project
    avgMonthlyTQIChange, avgMonthlyTQIChangeTotal, avgMonthlyTQIChangeRate, avgMonthlyTQIChangeRateTotal = mh.getAvgMonthlyTQIChangeRate(monthNum, monthNumGrowth, monthNumGrowthRate, monthNumDecline, monthNumDeclineRate)

    df_projects.loc[df_projects['Project Name'] == projectName, 'Average TQI Change(monthly)'] = avgMonthlyTQIChange
    df_projects.loc[df_projects['Project Name'] == projectName, 'Average TQI Change(monthly total)'] = avgMonthlyTQIChangeTotal
    df_projects.loc[df_projects['Project Name'] == projectName, 'Average TQI Change Rate(monthly)'] = avgMonthlyTQIChangeRate
    df_projects.loc[df_projects['Project Name'] == projectName, 'Average TQI Change Rate(monthly total)'] = avgMonthlyTQIChangeRateTotal

    #get the yearly average TQI score
    yearlyChangeRate = []
    yearlyCount = 0
    thisYearTQI = 0
    year = df['Date'].iloc[0].year

    #get the average TQI score for each year according to the 'Date' column
    for index, row in df.iterrows():
        #get the year of the current row
        cYear = row['Date'].year
        if year == cYear:
            yearlyCount += 1
            thisYearTQI += row['TQI']
            
        #if the year of the current row is different from the previous row, then calculate the average TQI score for the previous year
        else :
            #add the average TQI score to the list
            yearlyChangeRate.append([[year, yearlyCount], thisYearTQI / yearlyCount])
            #reset the yearlyCount and thisYearTQI
            yearlyCount = 1
            thisYearTQI = row['TQI']
            #update the year
            year = row['Date'].year
    
    # avgYearlyTQIChange = (yearlyChangeRate[-1][1] - yearlyChangeRate[0][1]) / (len(yearlyChangeRate) - 1)
    # avgYearlyTQIChangeTotal = (yearlyChangeRate[-1][1] + yearlyChangeRate[0][1]) / (len(yearlyChangeRate) - 1)
    # avgYearlyTQIChangeRate = (yearlyChangeRate[-1][1] - yearlyChangeRate[0][1]) / yearlyChangeRate[0][1]
    # avgYearlyTQIChangeRateTotal = (yearlyChangeRate[-1][1] + yearlyChangeRate[0][1]) / yearlyChangeRate[0][1]
    
    #add the last year's average TQI score to the list
    yearlyChangeRate.append([[year, yearlyCount], thisYearTQI / yearlyCount])
        
    df_projects.loc[df_projects['Project Name'] == projectName, '#Run'] = len(df)
    df_projects.loc[df_projects['Project Name'] == projectName, 'Site'] = df['Site'].iloc[-1]
    df_projects.loc[df_projects['Project Name'] == projectName, 'Owner'] = df['Owner'].iloc[-1]
    df_projects.loc[df_projects['Project Name'] == projectName, 'hashedProjectName'] = hf.hashName(projectName)
    df_projects.loc[df_projects['Project Name'] == projectName, 'hashedSite'] = hf.hashName(df['Site'].iloc[-1])
    df_projects.loc[df_projects['Project Name'] == projectName, 'hashedOwner'] = hf.hashName(df['Owner'].iloc[-1])
    df_projects.loc[df_projects['Project Name'] == projectName, 'Programming language'] = df['Programming language'].iloc[-1]
    df_projects.loc[df_projects['Project Name'] == projectName, 'Lines of Code(first)'] = df['Lines of Code'].iloc[0]
    df_projects.loc[df_projects['Project Name'] == projectName, 'Lines of Code(last)'] = df['Lines of Code'].iloc[-1]
    df_projects.loc[df_projects['Project Name'] == projectName, 'Lines of Code(change)'] = df['Lines of Code'].iloc[-1] - df['Lines of Code'].iloc[0]
    df_projects.loc[df_projects['Project Name'] == projectName, 'Lines of Code(average)'] = df['Lines of Code'].mean()
    df_projects.loc[df_projects['Project Name'] == projectName, 'Average TQI'] = df['TQI'].mean()
    df_projects.loc[df_projects['Project Name'] == projectName, 'Average TQI (first15))'] = df['TQI'].iloc[0:15].mean()
    df_projects.loc[df_projects['Project Name'] == projectName, 'Average TQI (last15))'] = df['TQI'].iloc[-15:].mean()
    df_projects.loc[df_projects['Project Name'] == projectName, 'StartDate'] = df['Date'].iloc[0]
    df_projects.loc[df_projects['Project Name'] == projectName, 'LatestDate'] = df['Date'].iloc[-1]
    df_projects.loc[df_projects['Project Name'] == projectName, 'Latest TQI Version'] = df['TQI Version'].iloc[-1]
    #use Lines of Code(last) column to calculate the latest code size 
    df_projects.loc[df_projects['Project Name'] == projectName, 'Latest Code Size'] = hf.returnCodeSize(df['Lines of Code'].iloc[-1])


    #if the df contians multiple TQI versions, then set the hasMultipleTQIVersions to True, or to False
    if len(df['TQI Version'].unique()) > 1:
        df_projects.loc[df_projects['Project Name'] == projectName, 'hasMultipleTQIVersions'] = True
        df_projects.loc[df_projects['Project Name'] == projectName, 'onlyTQIVersion'] = 0.0
    else:
        df_projects.loc[df_projects['Project Name'] == projectName, 'hasMultipleTQIVersions'] = False
        df_projects.loc[df_projects['Project Name'] == projectName, 'onlyTQIVersion'] = df['TQI Version'].iloc[0]
    
    #if the df contains 3.11 in TQI version, then set the hasTQI3 to True , or  to False
    if 3.11 in df['TQI Version'].values:
        df_projects.loc[df_projects['Project Name'] == projectName, 'hasTQI3'] = True
    else:
        df_projects.loc[df_projects['Project Name'] == projectName, 'hasTQI3'] = False

    # print(df_projects)
    
    #Count the avgTQI Score for the first week for each project
    startDate = df['Date'].iloc[0]
    endDate = startDate + datetime.timedelta(days=7)
    avgTQI = 0
    count = 0
    for index, row in df.iterrows():
        if row['Date'] >= startDate and row['Date'] <= endDate:
            avgTQI += row['TQI']
            count += 1
        else:
            break
    avgTQI = avgTQI / count
    df_projects.loc[df_projects['Project Name'] == projectName, 'Average TQI (first week)'] = avgTQI

    #Count the avgTQI Score for the first month for each project
    startDate = df['Date'].iloc[0]
    endDate = startDate + datetime.timedelta(days=30)
    avgTQI = 0
    count = 0
    for index, row in df.iterrows():
        if row['Date'] >= startDate and row['Date'] <= endDate:
            avgTQI += row['TQI']
            count += 1
        else:
            break
    avgTQI = avgTQI / count
    df_projects.loc[df_projects['Project Name'] == projectName, 'Average TQI (first month)'] = avgTQI


    ####################################################################################

    #get the three groups of values for each project for TestCoverage, DupCode, DeadCode, AI, SEC, FanOut, CS, CW, Complexity
    for key in dataframes:
        if key == 'SEC':
            #extract the rows from the df where the TQI version is not 3.11
            df_ver = df.loc[df['TQI Version'] != 3.11] 
            if len(df_ver) == 0:
                #give the nan to the three groups of values for each project
                dataframes[key].loc[dataframes[key]['Project Name'] == projectName, 'Pearson Correlation Coefficient'] = np.nan
                dataframes[key].loc[dataframes[key]['Project Name'] == projectName, 'Spearman Correlation Coefficient'] = np.nan
                dataframes[key].loc[dataframes[key]['Project Name'] == projectName, 'Slope'] = np.nan
            else:
                #change the 'SEC' column to float
                df_ver[hf.returnTQIMetricName(key)] = df_ver[hf.returnTQIMetricName(key)].astype(float)
                #give the pearson correlation coefficients between the TQI score and each metric
                dataframes[key].loc[dataframes[key]['Project Name'] == projectName, 'Pearson Correlation Coefficient'] = df_ver['TQI'].corr(df_ver[hf.returnTQIMetricName(key)], method='pearson')
                dataframes[key].loc[dataframes[key]['Project Name'] == projectName, 'Spearman Correlation Coefficient'] = df_ver['TQI'].corr(df_ver[hf.returnTQIMetricName(key)], method='spearman')
                dataframes[key].loc[dataframes[key]['Project Name'] == projectName, 'Slope'] = np.polyfit(df_ver['TQI'], df_ver[hf.returnTQIMetricName(key)], 1)[0]
        elif key == 'DeadCode':
            df_ver = df.loc[df['TQI Version'] == 3.11]
            if len(df_ver) == 0:
                #give the nan to the three groups of values for each project
                dataframes[key].loc[dataframes[key]['Project Name'] == projectName, 'Pearson Correlation Coefficient'] = np.nan
                dataframes[key].loc[dataframes[key]['Project Name'] == projectName, 'Spearman Correlation Coefficient'] = np.nan
                dataframes[key].loc[dataframes[key]['Project Name'] == projectName, 'Slope'] = np.nan
            else:
                #give the pearson correlation coefficients between the TQI score and each metric
                df_ver[hf.returnTQIMetricName(key)] = df_ver[hf.returnTQIMetricName(key)].astype(float)
                dataframes[key].loc[dataframes[key]['Project Name'] == projectName, 'Pearson Correlation Coefficient'] = df_ver['TQI'].corr(df_ver[hf.returnTQIMetricName(key)], method='pearson')
                dataframes[key].loc[dataframes[key]['Project Name'] == projectName, 'Spearman Correlation Coefficient'] = df_ver['TQI'].corr(df_ver[hf.returnTQIMetricName(key)], method='spearman')
                dataframes[key].loc[dataframes[key]['Project Name'] == projectName, 'Slope'] = np.polyfit(df_ver['TQI'], df_ver[hf.returnTQIMetricName(key)], 1)[0]
        else:
            df_ver[hf.returnTQIMetricName(key)] = df_ver[hf.returnTQIMetricName(key)].astype(float)
            #give the pearson correlation coefficients between the TQI score and each metric
            dataframes[key].loc[dataframes[key]['Project Name'] == projectName, 'Pearson Correlation Coefficient'] = df['TQI'].corr(df[hf.returnTQIMetricName(key)], method='pearson')
            dataframes[key].loc[dataframes[key]['Project Name'] == projectName, 'Spearman Correlation Coefficient'] = df['TQI'].corr(df[hf.returnTQIMetricName(key)], method='spearman')
            dataframes[key].loc[dataframes[key]['Project Name'] == projectName, 'Slope'] = np.polyfit(df['TQI'], df[hf.returnTQIMetricName(key)], 1)[0]

    ####################################################################################

    DRAW = True
    if DRAW == True:
        #draw the TQI evolution

        #set the figure size
        plt.figure(figsize=(10, 6))
        #set the title
        #Hash the projectName to a new readable name
        pName = 'Project-' + hf.hashName(projectName)+ '\'s'
        # plt.title(pName + ' TQI evolution')
        #set a subtitle below the title, sate the project's size, language, site and owner
        # plt.suptitle('Latest Info - Size: ' + str(df['Lines of Code'].iloc[-1]) + '('+ hf.returnCodeSize(df['Lines of Code'].iloc[-1])+ ')' + ', Language: [' + df['Programming language'].iloc[-1] + ']'+ ', Site: ' + hf.hashName(df['Site'].iloc[-1], 4) + ', Owner: ' + hf.hashName(df['Owner'].iloc[-1], 8), fontsize=9)
        

        #set the df['Date'] as the x axis
        #Display the label every year from the first date to the last date
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        plt.gca().xaxis.set_major_locator(mdates.YearLocator())
        #Display the dot every month from the first date without label
        plt.gca().xaxis.set_minor_locator(mdates.MonthLocator())
        #set the x axis range
        plt.xlim(df['Date'].iloc[0] - datetime.timedelta(days=60), df['Date'].iloc[-1] + datetime.timedelta(days= 60))


        #set the x axis label
        plt.xlabel('Date')
   
        #set 2 y axis 
        ax1 = plt.gca()
        ax2 = ax1.twinx()
        # Add vertical dashed lines for each date in changeDateArray, with different color
        for date in changeDateArray:
            ax1.axvline(x=date[0], color=date[1], linestyle='--', linewidth=1.3)

        #add mark for each vertical line
        for date in changeDateArray:
            text = str(date[2]) + ' to ' + str(date[3])
            ax1.text(date[0]+datetime.timedelta(days=10), 53, text, fontsize=8, color='black', rotation=0)

        #set the y axis range
        ax1.set_ylim(50, 100)
        ax2.set_ylim(-10, 10)
        #draw the TQI evolution
        ax1.plot(df['Date'], df['TQI'], color='blue', label='TQI')
        ax1.set_ylabel('TQI')
        #draw the lines changed evolution

        # ax2.plot(df['Date'], df['Change Rate(%)'], color= changeColor, label='LOC Change Rate')
        # ax2.plot(df['Date'], df['TQI Change'], color='pink', label='TQI Change')
        #ser the y axis label
        ax2.set_ylabel('Change Rate(%)')

        #draw the monthly average TQI scores' line on the ax1, the x value is the mid of each month, the y value is the average TQI score per month
        for monthly in monthlyChangeRate:
            #get the date of the mid of the month
            date = datetime.date(monthly[0][0], monthly[0][1], 15)
            #draw the line
            ax1.plot(date, monthly[1], color='green', marker='o', markersize=3)
        ax1.plot(0,0,label='Average Monthly TQI Score', color='green', marker='o', markersize=3)
        
        #draw the change rate of the average TQI score per month on the ax2, the first month's change rate is 0; 
        x_values = []
        y_values = []

        for monthly in monthlyChangeRate:
            # Get the date of the middle of the month
            date = datetime.date(monthly[0][0], monthly[0][1], 15)
            
            # Append the x and y values to the lists
            x_values.append(date)
            
            if monthlyChangeRate.index(monthly) == 0:
                y_values.append(0)
            else:
                y_values.append(monthly[1] - monthlyChangeRate[monthlyChangeRate.index(monthly) - 1][1])

        # Plot the line connecting the dots
        ax2.plot(x_values, y_values, color='#4c7cbd', marker='o', markersize=3, linestyle='-', linewidth=1, label='Monthly TQI Change Rate')

        #draw the yearly average TQI scores' line on the ax1, the x value is the mid of each year, the y value is the average TQI score per year
        for yearly in yearlyChangeRate:
            #get the date of the mid of the year
            date = datetime.date(yearly[0][0], 6, 15)
            #draw the line
            ax1.plot(date, yearly[1], color='red', marker='o', markersize=3)
            #add text to the line
            text = str(yearly[1])[0:4]
            ax1.text(date+datetime.timedelta(days=10), yearly[1], text, fontsize=8, color='black', rotation=0)

        #add a background color to the figure between the TQI Score 50 and 70
        ax1.axhspan(50, 70.1, facecolor='#ffeacf', alpha=0.5)
        ax1.axhspan(70.1, 80.1, facecolor='#ffffcc', alpha=0.5)
        ax1.axhspan(80.1, 90.1, facecolor='#e0efcc', alpha=0.5)
        ax1.axhspan(90.1, 100, facecolor='#cce0cc', alpha=0.5)
        #add a dashed line at the TQI Score 60
        ax1.axhline(y=50, color='#c6c4c2', linestyle='--', linewidth=1.1)
        ax1.axhline(y=60, color='#c6c4c2', linestyle='--', linewidth=1.1)
        ax1.axhline(y=70, color='#c6c4c2', linestyle='--', linewidth=1.1)
        ax1.axhline(y=80, color='#c6c4c2', linestyle='--', linewidth=1.1)
        ax1.axhline(y=90, color='#c6c4c2', linestyle='--', linewidth=1.1)
        ax1.axhline(y=100, color='#c6c4c2', linestyle='--', linewidth=1.1)
        #set the legend
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        #use ax3 o draw the Lines of Code evolution
        ax3 = ax1.twinx()
        #set the y axis range as the largest value of the 'Lines of Code' column * 1.1
        ax3.set_ylim(0, df['Lines of Code'].max() * 1.1)
        #draw the Lines of Code evolution
        ax3.plot(df['Date'], df['Lines of Code'], color='#e2beae', label='Lines of Code')
        #set the y axis label
        ax3.set_ylabel('Lines of Code')
        #set the legend
        ax3.legend(loc='lower left')
        #hide ax3
        ax3.get_yaxis().set_visible(False)
        

        #show the figure
        # plt.show()
        # sys.exit()
        plt.savefig(PREFIX + '/figs/RQ3/tqiEvo/RemoveLOC_TQI_evolution_' + hf.hashName(projectName) + '.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    print(projectName + ' TQI evolution figure saved')


#main
for projectName in projectList:
    anaAndDrawEvoPerProject(projectName)
        
df_projects.to_csv(PREFIX + '/docs/output/RQ3/projects_more_than_100_rows_info.csv', index=False)

#merge the dataframes in dataframes according to the 'Project Name' column
#then for every other cvolumn give a prefix  using the key of the dataframes
import pandas as pd

df_merged = dataframes['SEC'].rename(columns={
    'Pearson Correlation Coefficient': 'Pearson Correlation Coefficient_SEC',
    'Spearman Correlation Coefficient': 'Spearman Correlation Coefficient_SEC',
    'Slope': 'Slope_SEC'
})

for key in dataframes:
    if key == 'SEC':
        continue
    else:
        suffix = '_' + key
        df_to_merge = dataframes[key].add_suffix(suffix)
        df_to_merge.rename(columns={'Project Name'+suffix: 'Project Name'}, inplace=True)  # 将 'Project Name' 列名修改回原始名称
        df_merged = pd.merge(df_merged, df_to_merge, on='Project Name', how='left')


df_merged.to_csv(PREFIX + '/docs/output/RQ3/projects_more_than_100_rows_TQI_metrics_ver.csv', index=False)