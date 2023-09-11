'''
Author: rocs
Date: 2023-07-12 01:23:58
LastEditors: rocs
LastEditTime: 2023-08-24 11:12:15
Description:  helperTest.py
'''

import sys
sys.path.append(sys.path[0][:-5])

from helper import helperFuncs
from helper import presetting
from helper import metricsPreset as ma

PREFIX = presetting.PREFIX
addr = PREFIX + '/docs/output/tmp/'


projectName = input("input:")
print(helperFuncs.hashName(projectName))
