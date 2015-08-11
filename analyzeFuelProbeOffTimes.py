# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 11:21:41 2015

Just a program to mess around with to try new ideas.

@author: mriley
"""

import sys,os
import datetime
import time
import pandas as pd
import numpy as np

sys.path.append(r"C:\Users\mriley\Documents\GitHub\ATLASLink")

import ATLASlink

root = r"Z:\TrackData\2015"
#root = r"Z:\TrackData\2015\IC15_R11_FON"
#root = "C:\Users\mriley\Documents\GitHub\ATLASLink"

ATLAS = ATLAS_Session()

blankData = {'fileName': [],
             'lapName': [],
             'tConnect': [],
             'tDisconnect': []}

dfResults = pd.DataFrame(blankData)

tStart = datetime.datetime.now()
for path, subdirs, files in os.walk(root):
    for name in files:
        currPath = os.path.join(path, name)
        
        if currPath.endswith('.ssn'):
            
            sessionLoaded = ATLAS.loadSSNFile(currPath)
#            print currPath,sessionLoaded
            if sessionLoaded:
                
                if (ATLAS.lapCount > 68):
                    
                    for lap in range(ATLAS.lapCount):
                        ATLAS.setLapNum(lap)
                        
                        if ATLAS.lapTime < 360:
                            
                            carSpeed = ATLAS.getParamData("vCarmph")  
                            if carSpeed[carSpeed < 8].any():
                                
                                fuelProbe = ATLAS.getParamData("VFuelProbe")
                                
                                fuelProbe[fuelProbe>=2] = 4.8
                                fuelProbe[fuelProbe<2] = 0.5
                                
                                if fuelProbe[fuelProbe < 4.6].any():                
                                    
                                    print "The current file is ", name, ", the lap # is", lap
                                    
                                    fpDelta = pd.Series(fuelProbe.iloc[1:].values-fuelProbe.iloc[0:-1].values,index=fuelProbe.iloc[1:].index)
                                    fpPluggedIn = fpDelta[fpDelta < -3.5].copy()
                                    fpDisconnect = fpDelta[fpDelta > 3.5].copy()
                                    
                                    for i in range(fpPluggedIn.count()):
                                        if (i <= (fpPluggedIn.count()-1)) & (i <= (fpDisconnect.count()-1)):                           
                                            tConnect = fpDisconnect.index[i] - fpPluggedIn.index[i]
                                        tDisconnect = np.nan
                                        if not fpDisconnect.empty:
                                            if (i < (fpPluggedIn.count()-1)) & (i <= (fpDisconnect.count()-1)):
                                                tDisconnect = fpPluggedIn.index[i+1] - fpDisconnect.index[i]
                                        
                                        addData = {'fileName': [name],
                                                   'lapName': lap,
                                                   'tConnect': tConnect,
                                                   'tDisconnect': tDisconnect}
                                        
                                        addData = pd.DataFrame(addData)        
                                        
                                        dfResults = dfResults.append(addData,ignore_index=True)

tEnd = datetime.datetime.now()
print "Total time was",(tEnd-tStart),"seconds."

dfResults['tConnect'].plot()
print "-------------------------"
dfResults['tDisconnect'].plot()

                        



