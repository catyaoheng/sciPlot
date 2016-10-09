#!usr/bin/python
# Filename:drawRoc.py
# The intention is done by 4 spaces
# Written in Python2.7

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from numpy import array
from scipy.optimize import leastsq
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import pandas as pd

'''
DATA
'''
#'''
#getdata from file
def join(obj, splitor = '\t'):
    jointStr = ''
    if isinstance(obj, list):
        jointStr = str(obj[0])
        for ele in obj[1:]:
            jointStr = jointStr + splitor + str(ele)
        jointStr = jointStr.strip(splitor)
    return jointStr

dataFileDir = '../include/plot/'
possR = [3,6]
negaR = [5,4]
dataNum = 20
isCutDefault = 0
isCutTail = 0
isFixNegativeCorr = 0
isFixNegativeNum = 1
isFixPosstiveNum = 0

#currentR = negaR
currentR = possR
dataFileName = 'possitive_rest83_100Negative_dataProfile_' + str(dataNum) + '_st'
#possitive_rest83_100Negative_dataProfile_CoEx_feature_domain_avg_st_newCoex
#possitive_rest83_100Negative_dataProfile_domainFraction_3_st_newCoex
dataFileOutName = 'Data_' + str(dataNum)
dataFileStr = dataFileDir + dataFileName
dataFileOutStr = dataFileDir + dataFileOutName
#'''
#'''
abovePossitiveList = list()
belowNegativeList = list()
outList = list()
with open(dataFileStr, 'r') as fileData:
    lines = fileData.readlines()
    firstLineSet = lines[0].strip('\r').strip('\n').split('\t')
    sumPossitive = float(firstLineSet[1])
    sumNegative = float(firstLineSet[2])
    outList.append([sumPossitive, sumNegative])
    for i in range(2, len(lines)):
        lineSet = lines[i].strip('\r').strip('\n').split('\t')
        abovePossitiveList.append(lineSet[currentR[0]])
        belowNegativeList.append(lineSet[currentR[1]])
        outList.append([lineSet[currentR[0]], lineSet[currentR[1]], lineSet[7]])

with open(dataFileOutStr, 'w') as fileDataOut:
    for outSet in outList:
        outStr = join(outSet) + '\n'
        fileDataOut.write(outStr)

if isCutDefault:
    abovePossitiveList.pop(0)
    belowNegativeList.pop(0)

if isCutTail:
    abovePossitiveList.pop(len(abovePossitiveList) - 1)
    belowNegativeList.pop(len(belowNegativeList) - 1)    

if isFixNegativeNum:
    belowNegativeList = [float(belowNegativeList[i]) - float(belowNegativeList[0]) for i in range(len(belowNegativeList))]

if isFixNegativeCorr:
    abovePossitiveList = [float(abovePossitiveList[i]) - float(abovePossitiveList[len(abovePossitiveList)-1]) for i in range(len(abovePossitiveList))]

if isFixPosstiveNum:
    abovePossitiveList = [float(abovePossitiveList[i]) - float(abovePossitiveList[len(abovePossitiveList)-1]) for i in range(len(abovePossitiveList))]

sumPossitive = float(abovePossitiveList[0])
sumNegative = float(belowNegativeList[len(belowNegativeList)-1])

tpRatio = [float(i)/sumPossitive for i in abovePossitiveList]
fpRatio = [1 - (float(j))/sumNegative for j in belowNegativeList]
#'''

'''had making data
abovePossitiveList = [2210, 2209, 2209, 2209, 2209, 2208, 2208, 2200, 2200, 2195, 2194, 2194, 2192, 2118, 2118, 2118, 2118, 2057, 2057, 2056, 2048, 2048, 2048, 2045, 2045, 1545, 1545, 1545, 1545, 1544, 1544, 1544, 1544, 1544, 1479, 1479, 1479, 1479, 1479, 1478, 1478, 1478, 1478, 1478, 1478, 1468, 1468, 1468, 1468, 1468, 998, 998, 998, 998, 998, 998, 997, 997, 997, 997, 997, 997, 997, 997, 997, 997, 997, 989, 989, 989, 989, 989, 989, 989, 989, 988, 988, 988, 987, 987, 987, 987, 987, 987, 987, 987, 987, 987, 987, 986, 986, 986, 986, 986, 986, 986, 986, 986, 986, 986, 0]
belowNegativeList = [0, 30, 38, 40, 45, 45, 46, 48, 48, 54, 54, 63, 87, 124, 124, 124, 124, 407, 407, 410, 410, 433, 433, 445, 445, 445, 908, 908, 908, 908, 908, 909, 909, 909, 1352, 1352, 1352, 1352, 1355, 1355, 1355, 1356, 1356, 1356, 1356, 1370, 1370, 1370, 1370, 1370, 1370, 2430, 2430, 2430, 2430, 2430, 2431, 2431, 2431, 2431, 2431, 2433, 2433, 2433, 2433, 2433, 2433, 2477, 2477, 2477, 2477, 2477, 2477, 2477, 2477, 2477, 2506, 2506, 2507, 2507, 2507, 2507, 2507, 2507, 2507, 2507, 2507, 2507, 2507, 2507, 2507, 2507, 2507, 2507, 2507, 2507, 2507, 2507, 2507, 2507, 2507]
sumPossitive = 2210
sumNegative = 2507

tpRatio = [float(i)/sumPossitive for i in abovePossitiveList]
fpRatio = [1 - (float(j))/sumNegative for j in belowNegativeList]

#'''
x = array(fpRatio)
y = array(tpRatio)
auc = metrics.auc(x,y)
#'''
#-------------------
#Func & Fitter  #2
#-------------------
def logistic4(x, A, B, C, D):
    """4PL lgoistic equation."""
    return ((A-D)/(1.0+((x/C)**B))) + D

def residuals(p, y, x):
    """Deviations of data from fitted 4PL curve"""
    A,B,C,D = p
    err = y-logistic4(x, A, B, C, D)
    return err

def peval(x, p):
    """Evaluated value at x with current parameters."""
    A,B,C,D = p
    return logistic4(x, A, B, C, D)

# Initial guess for parameters
p0 = [0, 1, 1, 1]

# Fit equation using least squares optimization
plsq = leastsq(residuals, p0, args=(y, x))
#'''

#'''
#for i in range(10000):
X = x
tprtemp = peval(x,plsq[0])
tprList = list()
for i in tprtemp:
    if i<0:
        tprList.append(0.0)
    else:
        tprList.append(i)
Y = array(tprList)

'''
DATA
'''


matplotlib.rc('font', family = 'sans')
matplotlib.rc('font', size = '10')
matplotlib.rc('axes', facecolor = 'white')
matplotlib.rc('lines', markeredgewidth = 1.0)
matplotlib.rc('grid', color='white')
matplotlib.rc('grid', linewidth=1)
matplotlib.rc('grid', linestyle='-')
#matplotlib.rc('xtick.major', size = 0.0)
#matplotlib.rc('xtick.minor', size = 0.0)
matplotlib.rc('xtick', color='w')
matplotlib.rc('ytick', direction = 'out')
#matplotlib.rc('ytick.major', size = 0.0)
#matplotlib.rc('ytick.minor', size = 0.0)

fig = plt.figure(figsize=(8, 6), dpi=100,facecolor="w")
axes= plt.subplot(111, axisbelow=True)
axes.plot(X, Y, color = '0.4', linewidth=1.5, linestyle="-")

#fill
axes.fill_between(X, 0, Y, color = '0.85', zorder=-1)
#background color
Xfill = array([1.01] + fpRatio)
Yfill = array([1.01] + [i+1.01 for i in tprList])
axes.fill_between(Xfill, 0, Yfill, color = '0.92', zorder=-2)

axes.set_xlim(0, 1.01)
axes.set_ylim(0, 1.01)

axes.set_yticks([0,1])

axes.spines['left'].set_color('none')
axes.spines['right'].set_color('none')
axes.spines['top'].set_color('none')
axes.spines['bottom'].set_color('none')

axes.xaxis.set_ticks_position('bottom')
axes.yaxis.set_ticks_position('left')

#grid
axes.xaxis.set_major_locator(MultipleLocator(0.25))
axes.xaxis.set_minor_locator(MultipleLocator(0.125))
axes.grid(which='major', axis='x', linewidth=1.5)
axes.grid(which='minor', axis='x', linewidth=0.5)
axes.yaxis.set_major_locator(MultipleLocator(0.25))
axes.yaxis.set_minor_locator(MultipleLocator(0.125))
axes.grid(which='major', axis='y', linewidth=1.5)
axes.grid(which='minor', axis='y', linewidth=0.5)
for label in axes.get_xticklabels():
    label.set_color('0.5')
for label in axes.get_yticklabels():
    label.set_color('0.5')
#scatter
#plt.Circle(x, y, radius=0.3, color='#005CAF')
plt.title('AUC =' + str(auc) + ', ValueNum = ' + str(dataNum))
plt.scatter(x, y, c='#005CAF', s=50, linewidths=0, alpha=0.75)#, s=area, c=colors, alpha=0.5)
plt.show()






