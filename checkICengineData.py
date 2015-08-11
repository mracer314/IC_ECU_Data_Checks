# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 17:45:26 2015

@author: mriley
"""


#paramList = {'aignitionAverage': ['End','OffThrottle','PerfDataSample'],
#             'AnEpProcessorTempm01_AnalogScaledResult': ['Max'],
#             'nEngSpeedInst': ['End']}

import pandas as pd

test = {'fileName': [],
        'lapName': [],
        'tConnect': [],
        'tDisconnect': []}

df = pd.DataFrame(test)

test2 = {'fileName': ['file1'],
        'lapName': 1,
        'tConnect': 0.5,
        'tDisconnect': 0.5}