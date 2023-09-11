'''
Author: rocs
Date: 2023-02-08 15:33:10
LastEditors: rocs
LastEditTime: 2023-09-11 19:27:20
Description: get the targeted projects's data and analyse
'''
import sys
try:
  import requests
except ImportError:
  print('Please install the requests library')
  sys.exit(1)

#API Addr for TICS
# https://ticsdemo.tiobe.com/tiobeweb/DEMO/docs/index.html#doc=WebApiDocumentation.html%23measureapi

#All Metrics
locMetrics = ['language', 'loc', 'eloc', 'gloc', 'Log(loc,2)']
#cyclomatic complexity (average, max, total, nr of decision points)
cycloxMetrics = ['cycloxAverage', 'cycloxMax', 'cycloxTotal', 'nrOfDecisionPoints']
#fan out
fanoutMetrics = ['fanOut', 'nrOfFunctions']
#Dead Code (percentage)
deadCode = ['deadCode']
#Code Coverage (percentage)
coverageMetrics = ['avgCodeCoverage']
#Code Duplication (percentage)
dupCode = ['duplicatedCode']
#TQI Score and Sub Metrics
tqiMetrics = ['tqiVersion','tqi', 'tqiTestCoverage', 'tqiAbstrInt', 'tqiComplexity', 'tqiCompWarn', 'tqiCodingStd', 'tqiDupCode', 'tqiFanOut', 'tqiSecurity', 'tqiDeadCode']
#Lines Change
linesChange = ['linesAdded', 'linesDeleted', 'linesChanged'	, 'changerate']
#Violations
violations = ['Violations(CS)', 'Violations(CW)', 'Violations(AI)', 'Violations(SEC)']
#Violations Compliance
violationsCompliance = ['Compliance(CS)', 'Compliance(CW)', 'Compliance(AI)', 'Compliance(SEC)']

# only tqi version and loc
tvl = ['tqi','tqiVersion','loc']

#TQI Metrics
allMetrics = ['TestCoverage', 'AI', 'Complexity', 'CW', 'CS', 'DupCode', 'FanOut', 'SEC', 'DeadCode']

tqi3Metrics = ['TestCoverage', 'AI', 'Complexity', 'CW', 'CS', 'DupCode', 'FanOut', 'DeadCode']

tqi4Metrics = ['TestCoverage', 'AI', 'Complexity', 'CW', 'CS', 'DupCode', 'FanOut', 'SEC']

subjMetrics = ['AI', 'CS', 'SEC', 'CW']
objMetrics = ['TestCoverage', 'Complexity',  'DupCode', 'FanOut', 'DeadCode']


#pct metrics
pctMetrics = ['TQI', 'TQI Code Coverage', 'TQI Abstract Interpretation', 'TQI Cyclomatic Complexity', 'TQI Compiler Warnings', 'TQI Coding Standards', 'TQI Code Duplication', 'TQI Fan Out', 'TQI Security', 'TQI Dead Code', 
              'Metric Coverage for TQI Abstract Interpretation', 'Metric Coverage for TQI Compiler Warnings', 'Metric Coverage for TQI Coding Standards', 
              'Metric Coverage for TQI Security', 'Metric Coverage for TQI Code Duplication', 'Metric Coverage for TQI Fan Out',
               'Metric Coverage for TQI Dead Code', 'Metric Coverage for TQI Cyclomatic Complexity', 'Metric Coverage for TQI Code Coverage',
               'Abstract Interpretation Compliance', 'Compiler Warnings Compliance', 'Coding Standards Compliance', 'Security Compliance',
               'Dead Code (%)',  'Code Duplication (%)', 'Average Code Coverage']

floatMetrics = ['Average Cyclomatic Complexity', 
                'Average Fan Out:  External', 'Average Fan Out:  Internal' , 'Average Weighted Fan Out']
                
intMetrics = ['Decision Points (#)', 'Functions (#)', 'Lines of Code', 'Maximum Cyclomatic Complexity', 'Total Cyclomatic Complexity']

#the core metrics for TQI score calculation
coverageMetrics4 = [ 'Average Code Coverage' ,  'Code Duplication (%)', 'Average Cyclomatic Complexity', 'Average Weighted Fan Out', 'Compiler Warnings', 'Coding Standard Violations', 'Abstract Interpretation Violations', 'Security Violations']
coverageMetrics3 = [ 'Average Code Coverage' ,  'Code Duplication (%)', 'Average Cyclomatic Complexity', 'Average Weighted Fan Out', 'Compiler Warnings', 'Coding Standard Violations', 'Abstract Interpretation Violations', 'Dead Code (%)']

coverageMetrics3API = [ 'avgCodeCoverage' , 'duplicatedCode', 'deadCode', 'cycloxAverage', 'fanOut',  'Violations(CW)', 'Violations(CS)', 'Violations(AI)']
coverageMetrics4API = [ 'avgCodeCoverage' , 'duplicatedCode', 'cycloxAverage', 'fanOut',  'Violations(CW)', 'Violations(CS)', 'Violations(AI)', 'Violations(SEC)']

def getSubMetrics(metricTopic):
  selectedMetrics = ['loc','tqi','tqiVersion','ticsVersion']
  if (metricTopic == 'TestCoverage'):
     selectedMetrics += ['Coverage(tqiTestCoverage)','avgCodeCoverage', 'tqiTestCoverage']
  elif (metricTopic == 'Complexity'):
     selectedMetrics += ['Coverage(tqiComplexity)', 'cycloxAverage', 'cycloxMax', 'cycloxTotal', 'nrOfDecisionPoints', 'nrOfFunctions', 'tqiComplexity']
  elif (metricTopic == 'AI'):
     selectedMetrics += ['Coverage(tqiAbstrInt)', 'Violations(AI)', 'Compliance(AI)', 'tqiAbstrInt']
  elif (metricTopic == 'CW'):
     selectedMetrics += ['Coverage(tqiCompWarn)', 'Violations(CW)', 'Compliance(CW)', 'tqiCompWarn']
  elif (metricTopic == 'CS'):
     selectedMetrics += ['Coverage(tqiCodingStd)', 'Violations(CS)', 'Compliance(CS)', 'tqiCodingStd']
  elif (metricTopic == 'SEC'):
     selectedMetrics += ['Coverage(tqiSecurity)', 'Violations(SEC)', 'Compliance(SEC)', 'tqiSecurity']
  elif (metricTopic == 'DupCode'):
     selectedMetrics += ['Coverage(tqiDupCode)', 'duplicatedCode', 'DuplicatedCodeNum()','tqiDupCode']
  elif (metricTopic == 'FanOut'):
     selectedMetrics += ['Coverage(tqiFanOut)', 'fanOut','FanOutRatio(internal)', 'FanOutRatio(external)', 'nrOfFunctions', 'tqiFanOut']
  elif (metricTopic == 'DeadCode'):
     selectedMetrics += ['Coverage(tqiDeadCode)', 'deadCode', 'tqiDeadCode']
  else:
    print('Wrong metric topic!')
    sys.exit(1)
  
  return selectedMetrics
  
  
def isPctOrFloatMer(mer):
    if mer in pctMetrics:
        return 'pct'
    elif mer in floatMetrics:
        return 'float'
    else:
        return 'int'