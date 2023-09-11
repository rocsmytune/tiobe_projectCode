'''
Author: rocs
Date: 2023-07-12 00:06:19
LastEditors: rocs
LastEditTime: 2023-09-11 20:42:00
Description: The helper functions for the whole project
'''
import datetime,requests
import sys
import pandas as pd

#The username and password, you can get it from TIOBE.
username = 'user'
password = 'pwd'
auth = requests.auth.HTTPBasicAuth(username, password)

# Specify where the TICS Viewer is located, you can get it from TIOBE.
base_url_parameters = dict(
  host='http://0.0.0.0',
  section='TED',
)
# print (base_url_parameters)
base_url = '{host}/tiobeweb/{section}/api/public/v1/'.format(**base_url_parameters)

def getBaseURL():
    return base_url

def getAuth():
    return auth


def hashName(name, _len=5):
    import hashlib
    #no matter what type the name is, convert it to string
    name = str(name)
    hashedName =  hashlib.md5(name.encode(encoding='UTF-8')).hexdigest()
    #here we use 5 for the length of the project name, 4 for the length of the site name, 6 for the length of the owner name
    return hashedName[0:_len]

def getDatetime():
    now = datetime.datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y-%m-%d-%H-%M")
    return str(dt_string)

#collect all projects' metrics result values
def collectMetricsValuesAllProjects(selectedMetrics):
    # Specify input parameters
    input_params = dict(
    metrics=','.join(selectedMetrics),
    # metrics='tqi,tqiVersion,loc',
    filters='Project()',
    # filters='ProjectGroup(OneCodeBase),Project(),Run()'
    )
    # Measure Query TICS API
    r = requests.get(base_url + 'Measure', auth = auth, params=input_params)
    # print(r)
    if not r.ok:
        print('An error occurred while querying the TICS API')
        print(r.text)
        sys.exit(1)

    df = pd.DataFrame(columns = ['MetricName', 'ProjectName', 'Date', 'Value'])

    # Use the response body
    response_body =  r.json()
    # print(response_body)
    idx = 0
    for metric in response_body['metrics']: #per metric
        for date in response_body['dates']: #per date
            for node in response_body['nodes']: #per node
                metric_value = response_body['data'][idx]
                df.loc[idx]=[metric['fullName'], node['fullPath'], date, metric_value['formattedValue']]
                #   print('Value for metric {metric}, node {node} at {date} is {formatted_value}'.format(metric=metric['fullName'], node=node['fullPath'], date=date, formatted_value=metric_value['formattedValue']))
                idx += 1

    return df

#collect onr project's metrics result values
def collectMetricsValuesPerProject(projectName, selectedMetrics, PIVOT = True):
    # Specify input parameters
    input_params = dict(
    metrics=','.join(selectedMetrics),
    # metrics='tqi,tqiVersion,loc',
    filters='Project({}),Run()'.format(projectName),
    # filters='ProjectGroup(OneCodeBase),Project(),Run()'
    )
    # Measure Query TICS API
    r = requests.get(base_url + 'Measure', auth = auth, params=input_params)
    # print(r)
    if not r.ok:
        print('An error occurred while querying the TICS API')
        print(r.text)
        sys.exit(1)

    df = pd.DataFrame(columns = ['MetricName', 'ProjectName', 'Date', 'Value'])

    # Use the response body
    response_body =  r.json()
    # print(response_body)
    idx = 0
    for metric in response_body['metrics']: #per metric
        for date in response_body['dates']: #per date
            for node in response_body['nodes']: #per node
                metric_value = response_body['data'][idx]
                df.loc[idx]=[metric['fullName'], node['fullPath'], date, metric_value['formattedValue']]
                #   print('Value for metric {metric}, node {node} at {date} is {formatted_value}'.format(metric=metric['fullName'], node=node['fullPath'], date=date, formatted_value=metric_value['formattedValue']))
                idx += 1

    if PIVOT == True:
        #pivot the df to have MetricName as columns
        df_pivoted = df.pivot(index='Date', columns='MetricName', values='Value').reset_index()
        # Rename the columns to include the metric names
        df_pivoted.columns.name = None
        df_pivoted.columns = ['Date'] + df_pivoted.columns[1:].tolist()
        df = df_pivoted
        
    return df

def collectMetricsLevelValuesPerProject(projectName, selectedMetrics,level):
    # Specify input parameters
    input_params = dict(
    metrics=','.join(selectedMetrics),
    # metrics='tqi,tqiVersion,loc',
    filters='Project({}),Run(),Level({})'.format(projectName, level),
    # filters='ProjectGroup(OneCodeBase),Project(),Run()'
    )
    # Measure Query TICS API
    r = requests.get(base_url + 'Measure', auth = auth, params=input_params)
    # print(r)
    if not r.ok:
        print('An error occurred while querying the TICS API')
        print(r.text)
        sys.exit(1)

    df = pd.DataFrame(columns = ['MetricName', 'ProjectName', 'Date', 'Value'])

    # Use the response body
    response_body =  r.json()
    # print(response_body)
    idx = 0
    for metric in response_body['metrics']: #per metric
        for date in response_body['dates']: #per date
            for node in response_body['nodes']: #per node
                metric_value = response_body['data'][idx]
                df.loc[idx]=[metric['fullName'], node['fullPath'], date, metric_value['formattedValue']]
                #   print('Value for metric {metric}, node {node} at {date} is {formatted_value}'.format(metric=metric['fullName'], node=node['fullPath'], date=date, formatted_value=metric_value['formattedValue']))
                idx += 1

    PIVOT = True
    if PIVOT == True:
        #pivot the df to have MetricName as columns
        df_pivoted = df.pivot(index='Date', columns='MetricName', values='Value').reset_index()
        # Rename the columns to include the metric names
        df_pivoted.columns.name = None
        df_pivoted.columns = ['Date'] + df_pivoted.columns[1:].tolist()
        df = df_pivoted
        
    return df

def getLevelNum(metricTopic):
    if (metricTopic == 'AI'):
        return 6
    elif (metricTopic == 'CS'):
        return 10
    elif (metricTopic == 'SEC' or metricTopic == 'CW'):
        return 3
    else:
        print("This metric topic is not in the subjMetrics list!")
        return 0
    
def returnTQIMetricName(metricTopic):
    pre = 'TQI '
    if (metricTopic == ''):
        return 'TQI'
    else:
        return pre + getMetricFullName(metricTopic)
    

def getTQILevel(tqi = 90.1):
    if (tqi >= 90):
        return 'A'
    elif (tqi >= 80):
        return 'B'
    elif (tqi >= 70):
        return 'C'
    elif (tqi >= 50):
        return 'D'
    elif (tqi >= 40):
        return 'E'
    else:
        return 'F'

def getMetricFullName(metricTopic):
    if (metricTopic == 'TestCoverage'):
        return 'Code Coverage'
    elif (metricTopic == 'Complexity'):
        return 'Cyclomatic Complexity'
    elif (metricTopic == 'AI'):
        return 'Abstract Interpretation'
    elif (metricTopic == 'CW'):
        return 'Compiler Warnings'
    elif (metricTopic == 'CS'):
        return 'Coding Standards'
    elif (metricTopic == 'SEC'):
        return 'Security'
    elif (metricTopic == 'DupCode'):
        return 'Code Duplication'
    elif (metricTopic == 'FanOut'):
        return 'Fan Out'
    elif (metricTopic == 'DeadCode'):
        return 'Dead Code'
    else:
        return 'Unknown Metric'
    
def returnCodeSize(loc = 1000000):
    if loc < 100000:
        return 'small'
    elif loc < 500000:
        return 'middle'
    else:
        return 'large'

def qkOut(df, PREFIX):
    df.to_csv(PREFIX + "/docs/output/tmp/" +"qkOut.csv")


y_pct = {'AI' : [10, 110], 'CS' : [10, 110], 'SEC' : [10, 110], 'CW' : [10, 110], 'TestCoverage' : [-0.5, 100.2], 'Complexity' : [10, 110], 'DupCode' : [10, 110], 'FanOut' : [10, 110], 'DeadCode' : [10, 110]}
y_tdd = { 'TestCoverage' : [-5, 105],  'DupCode' : [-5, 25], 'DeadCode' : [0, 40]}