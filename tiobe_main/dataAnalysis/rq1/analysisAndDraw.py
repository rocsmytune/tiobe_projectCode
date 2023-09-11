'''
Author: rocs
Date: 2023-07-13 01:16:08
LastEditors: rocs
LastEditTime: 2023-09-11 22:21:18
Description: analysis and draw the result of rq1
'''

import datetime
import pandas as pd
import numpy as np
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
from dataCollection.rq1and2 import importProjectsList as pl 

PREFIX = presetting.PREFIX

def ana_draw(projectName, metricTopic, ifKeepDate = True):
    
    size = pl.getProjectInfo(projectName)['Size'].tolist()[0]
    fLang = pl.getProjectInfo(projectName)['FirstLang'].tolist()[0]

    #1. Get the targeted project's data
    suffix = ''
    if (ifKeepDate == True):
        XAXIS = 'Date'
    else:
        XAXIS = 'Index'
        suffix = '_dropSameValues'
    
    #2. Fet the project's info from pl
    df_projectInfo = pl.getProjectInfo(projectName)

    df = pd.read_csv(PREFIX + '/docs/output/RQ1/cleaned/' + metricTopic + '/' + projectName + suffix +'.csv')

    if (df.empty):
        print('Empty df for ' + projectName + ' ' + metricTopic +'\n')
        return
    
    #add a column 'Index' to df's first column
    df.insert(0, 'Index', range(0, len(df)))
    df['Index'] = np.arange(1, len(df) + 1)

    metricTQI = hf.returnTQIMetricName(metricTopic)
    #Loop over each row in the DataFrame and update the 'TQI Level' column
    for index, row in df.iterrows():
        metric_tqi = row[metricTQI]
        tqi_level = hf.getTQILevel(metric_tqi)
        df.loc[index, 'TQI Level'] = tqi_level

    
    df['Date'] = pd.to_datetime(df['Date'])
    # Loop over each row in the DataFrame and find each row whose 'TQI Level' is different from last row, record the 'Date' values into a list
    levelChangeArray = []
    lastTQILevel = df.loc[0, 'TQI Level']
    for index, row in df.iterrows():
        tqi_level = row['TQI Level']
        if tqi_level != lastTQILevel:
                if tqi_level < lastTQILevel: 
                    #current metric's tqi_level is better than lastTQILevel, 'A' < 'B' < 'C' < 'D'
                    levelChangeArray.append([row[XAXIS], 'g'])
                else:
                    levelChangeArray.append([row[XAXIS], 'r'])
                lastTQILevel = tqi_level

    #get the change date array for tqi version
    tqiVerChangeArray = []
    lastTQIVer = df.loc[0, 'TQI Version']
    for index, row in df.iterrows():
        tqi_ver = row['TQI Version']
        if tqi_ver != lastTQIVer:
                tqiVerChangeArray.append([row[XAXIS], 'm', lastTQIVer, tqi_ver])
                lastTQIVer= tqi_ver
    ##########################################################
    
    #DRAWING
    #1. Set rhe y-axis labels

    y_main1 = ''
    y_main2 = ''
    y_main3 = ''
    main1_color = 'red'
    main2_color = 'teal'
    main3_color = 'cadetblue'
    y_extra = ''

    y_pct_lim = hf.y_pct[metricTopic]

    #Lines of Code label
    y_loc = 'Lines of Code'
    loc_color = 'darkorange'
    #TQI Level label
    y_tqi = hf.returnTQIMetricName(metricTopic)
    tqi_color = 'blue'
    #Metric Coverage label
    y_mc = 'Metric Coverage for ' + hf.returnTQIMetricName(metricTopic)
    mc_color = 'darkturquoise' 
    #Compliance label for AI, CS, SEC, CW
    if (metricTopic == 'AI' or metricTopic == 'CS' or metricTopic == 'SEC' or metricTopic == 'CW'):
        y_main1 = hf.getMetricFullName(metricTopic) + ' Compliance'
        if metricTopic == 'CW':
            y_main2 = hf.getMetricFullName(metricTopic)
        elif metricTopic == 'CS':
            y_main2 = 'Coding Standard Violations'
        else:
            y_main2 = hf.getMetricFullName(metricTopic) + ' Violations'
        levelsNum = hf.getLevelNum(metricTopic)
        #add y-axis labels for each level
        y_levels = []
        levelsColor = ['black', 'maroon', 'orangered', 'coral', 'gold', 'yellow', 'olive', 'yellowgreen', '#c0e1bd', 'lightskyblue']
        for i in range(levelsNum):
            if metricTopic == 'CW':
                y_levels.append(hf.getMetricFullName(metricTopic) + ' for level ' + str(i+1))
            elif metricTopic == 'CS':
                y_levels.append('Coding Standard Violations for level ' + str(i+1))
            else:
                y_levels.append(hf.getMetricFullName(metricTopic) + ' Violations for level ' + str(i+1))
    elif (metricTopic == 'TestCoverage'):
        y_main1 = 'Average Code Coverage'
    elif (metricTopic == 'Complexity'):
        y_main1 = 'Average Cyclomatic Complexity'
    elif (metricTopic == 'DupCode'):
        y_main1 = 'Code Duplication (%)'
    elif (metricTopic == 'FanOut'):
        y_main1 = 'Average Weighted Fan Out'
        y_main2 = 'Average Fan Out:  External'
        y_main3 = 'Average Fan Out:  Internal'
    elif (metricTopic == 'DeadCode'):
        y_main1 = 'Dead Code (%)'
    else:
        print('Unknown metricTopic: ' + metricTopic + '\n')
        return
    
    #2. Set the x-axis labels
    if XAXIS == 'Date':
        x_label = 'Date'
    elif XAXIS == 'Index':
        x_label = 'Index'
    else:
        print('Unknown XAXIS: ' + XAXIS + '\n')
        return

    #3. Set the figure size, and draw the figure
    fig, ax1 = plt.subplots(figsize=(18, 9))
    ax2 = ax1.twinx()

    #set the title and suptitle
    # plt.suptitle('Latest Project Info - Size: ' + str(df_projectInfo['LOC'].iloc[-1]) + '('+ df_projectInfo['Size'].iloc[-1]+ ')' + ', Language: [' + df_projectInfo['MainCodeType'].iloc[-1] + ']'+ ', Owne-Site: ' + hf.hashName(df_projectInfo['CompanySite'].iloc[-1], 7), fontsize=18, y=0.95)

    #add a dashed line at the TQI Score 60
    for i in range(1, 11):
        ax2.axhline(y=i * 10, color='#c6c4c2', linestyle='--', linewidth=1.1)
    
    #add a background color to the figure between the TQI Score
    ax2.axhspan(-0.5, 40.1, facecolor='#ffcccc', alpha=0.5)
    ax2.axhspan(40.1, 50.1, facecolor='#ffd9cc', alpha=0.5)
    ax2.axhspan(50.1, 70.1, facecolor='#ffeacf', alpha=0.5)
    ax2.axhspan(70.1, 80.1, facecolor='#ffffcc', alpha=0.5)
    ax2.axhspan(80.1, 90.1, facecolor='#e0efcc', alpha=0.5)
    ax2.axhspan(90.1, 110.1, facecolor='#cce0cc', alpha=0.5)
    
    if x_label == 'Date':
        #Display the label every year from the first date to the last date
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        ax1.xaxis.set_major_locator(mdates.YearLocator())
        #Display the dot every month from the first date without label
        ax1.xaxis.set_minor_locator(mdates.MonthLocator())
        #set the x axis range
        ax1.set_xlim(df['Date'].iloc[0] - datetime.timedelta(days=60), df['Date'].iloc[-1] + datetime.timedelta(days= 60))

    else:
        #Display the dot every 30 dots from the first date without label
        ax1.xaxis.set_major_locator(MaxNLocator(30))
        #set the x axis range
        ax1.set_xlim(-5, len(df) + 5)

    # Add vertical dashed lines for each date in changeDateArray, with different color
    for date in levelChangeArray:
        ax1.axvline(x=date[0], color=date[1], linestyle='--', linewidth=0.85)
    # Add vertical dashed lines for each date in tqiVerChangeArray, with different color
    for date in tqiVerChangeArray:
        ax1.axvline(x=date[0], color=date[1], linestyle='--', linewidth=1.2)
    #add mark for each vertical line
    for date in tqiVerChangeArray:
        text = str(date[2]) + ' to ' + str(date[3])
        if x_label == 'Date':
            #text (x coordinate: Add 10 days here to generate offset, y coordinate, text content, font size, color, rotation angle )
            ax2.text(date[0] - datetime.timedelta(days=100), 24, text, fontsize=12, color='black', rotation=0)
        else:
            ax2.text(date[0]-20, 24, text, fontsize=12, color='black', rotation=0)
       
    #3.1 draw the three lines: LOC and TQI Level and Metric Coverage
    # plt.title( metricTopic + '-' +  hf.hashName(projectName, 5) +  ' Evolution Graph', fontsize=11)
    ax1.plot(df[x_label], df[y_loc], color=loc_color, label=y_loc, linewidth= 1.2)
    ax2.plot(df[x_label], df[y_mc], color=mc_color, label=y_mc)
    ax2.plot(df[x_label], df[y_tqi], color=tqi_color, label=y_tqi, linewidth=1.5)
    ax2.plot(0, 0, color=loc_color, label=y_loc, linewidth=1.5)

    #set the y-axis range and legend
    ax1.set_xlabel(x_label, fontsize=16)
    ax1.set_ylabel(y_loc, fontsize=16)
    ax1.set_ylim([0, df[y_loc].max() * 1.1])
    # ax2.set_ylabel(y_tqi)
    ax2.set_ylabel('TQI Socre and ' + y_mc, fontsize=16)
    ax2.set_ylim(y_pct_lim)
    ax2.legend(loc='lower right')
    
    plt.savefig(PREFIX + '/figs/RQ1AndRQ2/RQ1/' + metricTopic + '/normal/' + hf.hashName(projectName, 5)  + suffix + '.png', dpi=300, bbox_inches='tight')
    plt.savefig(PREFIX + '/figs/RQ1AndRQ2/RQ1/' + metricTopic + '/size/' + size + '/' +hf.hashName(projectName, 5)  + suffix + '.png', dpi=300, bbox_inches='tight')
    if fLang in ['Java', 'C#', 'C++', 'C', 'Python']:
        plt.savefig(PREFIX + '/figs/RQ1AndRQ2/RQ1/' + metricTopic + '/lang/' + fLang + '/' +hf.hashName(projectName, 5)  + suffix + '.png', dpi=300, bbox_inches='tight')
    else:
        plt.savefig(PREFIX + '/figs/RQ1AndRQ2/RQ1/' + metricTopic + '/lang/Other/' +hf.hashName(projectName, 5)  + suffix + '.png', dpi=300, bbox_inches='tight')
    
    # plt.savefig(PREFIX + '/figs/Share/RQ1/' + metricTopic + '/normal/' + hf.hashName(projectName, 5) + suffix + '.png', dpi=300, bbox_inches='tight')
    # plt.savefig(PREFIX + '/figs/Share/RQ1/' + metricTopic + '/size/' + size + '/' +hf.hashName(projectName, 5) + suffix + '.png', dpi=300, bbox_inches='tight')
    # if fLang in ['Java', 'C#', 'C++', 'C', 'Python']:
    #     plt.savefig(PREFIX + '/figs/Share/RQ1/' + metricTopic + '/lang/' + fLang + '/' +hf.hashName(projectName, 5) + suffix + '.png', dpi=300, bbox_inches='tight')
    # else:
    #     plt.savefig(PREFIX + '/figs/Share/RQ1/' + metricTopic + '/lang/Other/' +hf.hashName(projectName, 5) + suffix + '.png', dpi=300, bbox_inches='tight')
    
    # plt.clf()
    # plt.show()
    # sys.exit(0)
    ax2.cla()


    #3.2 draw the main lines: y_main1 and y_main2 and y_main3 and y_loc
    #ax1 for loc ax2 for pct and ax3 for others
    ax3 = ax1.twinx()

    if metricTopic in ['TestCoverage',  'DupCode', 'DeadCode']:
        #for these metrics, only one main line, left: loc, right: compliance
        ax2.set_yticks([], size=16)
        
        if metricTopic == 'DupCode' or metricTopic == 'DeadCode':
            ax3.set_ylabel(y_main1, fontsize=16)
        else:
            ax3.set_ylabel(y_main1+'(%)', fontsize=16)

        ax3.set_ylim(hf.y_tdd.get(metricTopic))
        ax3.plot(df[x_label], df[y_main1], color=main1_color, label=y_main1, linewidth=1.5)
        ax3.plot(0,0, color=loc_color, label=y_loc, linewidth=1.5)
        ax3.legend(loc='lower right')
        # plt.title(metricTopic + ':' + y_main1 + '-' +  hf.hashName(projectName, 5) +  ' Evolution Graph', fontsize=11)
    elif metricTopic in ['Complexity', 'FanOut']:
        ax2.set_yticks([], size=16)
        #for these metrics, no pct line, left: loc, right: related values
        ax3.plot(df[x_label], df[y_main1], color=main1_color, label=y_main1, linewidth=1.5)
        ax3.set_ylim([0, df[y_main1].max() * 1.1])
        if metricTopic == 'FanOut':
            ax3.plot(df[x_label], df[y_main2], color=main2_color, label=y_main2, linewidth=1.5)
            ax3.plot(df[x_label], df[y_main3], color=main3_color, label=y_main3, linewidth=1.5)
            ax3.set_ylabel('Average Fan Out', fontsize=16)
        else:
            ax3.set_ylabel(y_main1, fontsize=16)
        ax3.plot(0,0, color=loc_color, label=y_loc, linewidth=1.5)
        ax3.legend(loc='lower right')
        # plt.title(metricTopic + ':' + 'Related Values' + '-' +  hf.hashName(projectName, 5) +  ' Evolution Graph', fontsize=11)
    elif metricTopic in ['AI', 'CS', 'SEC', 'CW']:
        #for these metrics, multiple main lines
        #the original ax1 is used to draw violations
        ax1.set_ylabel('Violations', fontsize=16)
        ax1.set_ylim([-2, df[y_main2].max() * 1.1])
        ax1.plot(df[x_label], df[y_main2], color=main2_color, label=y_main2, linewidth=1.5)
        #add y-axis labels for each level
        for i in y_levels:
            ax1.plot(df[x_label], df[i], color=levelsColor.pop(), label=i, linewidth=1.2)
        ax1.plot(0, 0, color=main1_color, label=y_main1, linewidth=1.5)
        ax1.legend(loc='center left')

        # use ax2 to store the original loc line
        ax2.plot(df[x_label], df[y_loc], color=loc_color, label=y_loc, linewidth= 1.0)
        ax2.set_ylim([0, df[y_loc].max() * 1.1])
        ax2.set_yticks([], size=16)
        #use ax3 to store the compliance line
        ax3.plot(df[x_label], df[y_main1], color=main1_color, label=y_main1, linewidth=1.5)
        ax3.set_ylabel('Compliance(%)', fontsize=16)
        ax3.set_ylim(60, 110)

        # plt.title(metricTopic + ':' + 'Violations Distribution' + '-' +  hf.hashName(projectName, 5) +  ' Evolution Graph', fontsize=11)
       

    # plt.show()
    plt.savefig(PREFIX + '/figs/RQ1AndRQ2/RQ1/' + metricTopic + '/normal/' + hf.hashName(projectName, 5)  + suffix + '_main.png', dpi=300, bbox_inches='tight')
    plt.savefig(PREFIX + '/figs/RQ1AndRQ2/RQ1/' + metricTopic + '/size/' + size + '/' +hf.hashName(projectName, 5)  + suffix + '_main.png', dpi=300, bbox_inches='tight')
    if fLang in ['Java', 'C#', 'C++', 'C', 'Python']:
        plt.savefig(PREFIX + '/figs/RQ1AndRQ2/RQ1/' + metricTopic + '/lang/' + fLang + '/' +hf.hashName(projectName, 5)  + suffix + '_main.png', dpi=300, bbox_inches='tight')
    else:
        plt.savefig(PREFIX + '/figs/RQ1AndRQ2/RQ1/' + metricTopic + '/lang/Other/' +hf.hashName(projectName, 5)  + suffix + '_main.png', dpi=300, bbox_inches='tight')
    
    # plt.savefig(PREFIX + '/figs/Share/RQ1/' + metricTopic + '/normal/' + hf.hashName(projectName, 5) + suffix + '_main.png', dpi=300, bbox_inches='tight')
    # plt.savefig(PREFIX + '/figs/Share/RQ1/' + metricTopic + '/size/' + size + '/' +hf.hashName(projectName, 5) + suffix + '_main.png', dpi=300, bbox_inches='tight')
    # if fLang in ['Java', 'C#', 'C++', 'C', 'Python']:
    #     plt.savefig(PREFIX + '/figs/Share/RQ1/' + metricTopic + '/lang/' + fLang + '/' +hf.hashName(projectName, 5) + suffix + '_main.png', dpi=300, bbox_inches='tight')
    # else:
    #     plt.savefig(PREFIX + '/figs/Share/RQ1/' + metricTopic + '/lang/Other/' +hf.hashName(projectName, 5) + suffix + '_main.png', dpi=300, bbox_inches='tight')
    
    plt.clf()
    print('RQ1: ' + projectName + ' ' + metricTopic + ' done')




projectList = pl.getProjectList()
metricTopics = mp.allMetrics
# projectList = ['DDBC120_DALI_V4']
# metricTopics =[ 'TestCoverage']
# metricTopics = ['DupCode', 'DeadCode']
for metricTopic in metricTopics:
    for projectName in projectList:
        ifKeepDate = False
        #if there is exception, then save the exception and continue
        try:
            ana_draw(projectName, metricTopic, ifKeepDate)
        except Exception as e:
            #save the error project name and metric name into a txt file
            with open(PREFIX + "/docs/output/error/anaAndDraw_" + hf.getDatetime() + ".txt", "a") as f:
                f.write(str(e) + "\n" +"Error in " + metricTopic + " for " + projectName + "!" +  "\n\n")
            continue

        
