'''
Author: rocs
Date: 2023-07-11 19:21:13
LastEditors: rocs
LastEditTime: 2023-09-11 19:26:00
Description:  This file is used to preset some parameters for the whole project, you need to customize it according to your own environment
'''

import socket
import re
import warnings
warnings.filterwarnings('ignore')
import sys
#save part of current file path, end at 'tiobe_main/'
hostname=socket.gethostname()
ipAddr = socket.gethostbyname(hostname)

if re.match(r'10.10.10.*', ipAddr, re.I) == None and (hostname == 'Rocss-MacBook-Pro.local' or hostname == 'Rocss-MBP'):
    PREFIX = '/Users/rocs/Desktop/Master study/Graduation Project/graduation part2/code'
elif re.match(r'10.10.10.*', ipAddr, re.I) != None or hostname == 'Mingzhe-Desktop':
    PREFIX = 'D:/tiobe_project/TIOBE_DataAnalysis'
else:
    PREFIX = 'C:/Users/rocs/Desktop/code'

def getIpAddr():
    return ipAddr
def getHostname():
    return hostname

