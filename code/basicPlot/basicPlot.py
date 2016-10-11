#!usr/bin/python
# Filename:basicPlot.py
# The intention is done by 4 spaces
# Written in Python2.7

import time
import numpy as np
from numpy import array
from scipy.optimize import leastsq

from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.transforms import Bbox
from matplotlib.font_manager import FontProperties

'''
DATA
'''
#'''
#getdata from file
def prepareInput(inputObj):
    global currentLineNum
    global originalTermNumToken
    global originalTermNum
    currentLineNum = 0
    originalTermNumToken = 0
    originalTermNum = 0
    if isinstance(inputObj, str):
        with open(inputObj, 'r') as fileInput:
            originalTermNum = 0
            currentLine = fileInput.readline()
            while currentLine:
                originalTermNum = originalTermNum + 1
                currentLine = fileInput.readline()
            fileInput.seek(0)
    elif (isinstance(inputObj, list) or isinstance(inputObj, dict)):
        originalTermNum = len(inputObj)
    elif (isinstance(inputObj, int)):
        originalTermNum = inputObj

    if (originalTermNum < 10):
        originalTermNumToken = originalTermNum
    else:
        originalTermNumToken = int(originalTermNum / 10 * 10)
    return [originalTermNumToken, originalTermNum]

def process(isLog = True):
    global currentLineNum
    global originalTermNumToken
    currentLineNum = currentLineNum + 1

    progress = (10 * currentLineNum) % originalTermNumToken
    if originalTermNumToken < 10:
        if(isLog):
            writeLog("\t\t\t" + str(round((((1.0 * currentLineNum) / originalTermNumToken) * 100),1)) + "% " + time.asctime() + '\n')
        print("\t\t\t" + str(round((((1.0 * currentLineNum) / originalTermNumToken) * 100),1)) + "% " + time.asctime())
        return
    if (progress == 0):
        if(isLog):
            writeLog("\t\t\t" + str(round((((1.0 * currentLineNum) / originalTermNumToken) * 100),1)) + "% " + time.asctime() + '\n')
        print("\t\t\t" + str(round((((1.0 * currentLineNum) / originalTermNumToken) * 100),1)) + "% " + time.asctime())

def join(obj, splitor = '\t'):
    jointStr = ''
    if isinstance(obj, list):
        jointStr = str(obj[0])
        for ele in obj[1:]:
            jointStr = jointStr + splitor + str(ele)
        jointStr = jointStr.strip(splitor)
    return jointStr

def preparePlot():
    global matplotlib
    global fig
    global axes
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
    
    fig = plt.figure(figsize=(8, 6), dpi=100, facecolor="w")
    axes= plt.subplot(111, axisbelow=True)
    #fill
    #axes.fill_between(xPlotList, 0, yPlotList, color = '0.85', zorder=-1)
    #background color
    xFillList = []
    yFillList = []
    for i in range(1010):
        xFillList.append(i*1.0/1000)
        yFillList.append(i*1.0/1000)
    Xfill = array(xFillList)
    Yfill = array([i+1.01 for i in yFillList])
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

# config
#dataFileDir = '../include/plot/'
#dataFileDir = '../include/plot/beforeNewpsddata/'
#old_profile/'
dataFileDir = '../include/plot/'
currentCor = 'poss'
#currentCor = 'nega'
#dataNumList = [3,4,5,9,10,11,12,15]
#dataNumList = [19, 20, 21]
dataNumList = [6, 7]
#dataNumList = [3, 4, 5, 6, 7, 8, 9, 10]
#dataNumList = [8, 9, 10, 11, 12, 13, 14, 15]
#dataNumList = [16]
#dataNumList = [21]
#dataNumList = [21, 22, 23, 24, 25]
#dataNumList = [14, 15, 16, 17, 18]
#'''

def calculateRocMatrix(possitiveList, negativeList, correlationType):
    tpRatioList = []
    fpRatioList = []
    #possitiveList = [0.0] + possitiveList + [0.0]
    #negativeList = [0.0] + negativeList + [0.0]
    #print(possitiveList)
    #sumPossitive = sum(possitiveList)
    #print(negativeList)
    #sumNegative = sum(negativeList)
    prepareInput(len(possitiveList))
    if correlationType == 'poss':
        tp = sumPossitive
        fp = sumNegative
        for i in range(1, len(possitiveList)+1):
            process(False)
            #cal tpRatio
            tp = tp - possitiveList[i-1]
            #tp = sum(possitiveList[i:])
            fp = fp - negativeList[i-1]
            #fp = sum(negativeList[i:])
            #print(str(i) +'||'+ str(tp)+'||'+str(fp))           
            tpRatio = (tp*1.0) / sumPossitive
            fpRatio = (fp*1.0) / sumNegative
            tpRatioList.append(tpRatio)
            fpRatioList.append(fpRatio)
    else:
        tp = 0
        fp = 0
        for i in range(len(possitiveList)):
            process(False)
            #cal tpRatio
            tp = tp + possitiveList[i]
            #tp = sum(possitiveList[i:])
            fp = fp + negativeList[i]
            #fp = sum(negativeList[i:])
            #print(str(i) +'||'+ str(tp)+'||'+str(fp))           
            tpRatio = (tp*1.0) / sumPossitive
            fpRatio = (fp*1.0) / sumNegative
            tpRatioList.append(tpRatio)
            fpRatioList.append(fpRatio)
        #pass
        #            else:
        #        tp = sum(possitiveList[:i+1])
        #        fp = sum(negativeList[:i+1])
    return[tpRatioList, fpRatioList]

def fitLogisticCurve(x, y):
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

    '''
    #-------------------
    #Func & Fitter  
    #-------------------
    def exp(x, A, B, C, D):
        #4PL exp equation.
        return A * ((x - B)** C) + D
    
    def residuals(p, y, x):
        #Deviations of data from fitted curve
        A,B,C,D = p
        err = y - exp(x, A, B, C, D)
        return err
    
    def peval(x, p):
        #Evaluated value at x with current parameters.
        A,B,C,D = p
        return exp(x, A, B, C, D)
    
    # Initial guess for parameters
    p0 = [0, 0, 3, 0]
    # Fit equation using least squares optimization
    plsq = leastsq(residuals, p0, args=(y, x))
    #'''

    xPlotList = []
    for i in range(1010):
        xPlotList.append(i*1.0/1000)
    yPlotList = peval(array(xPlotList), plsq[0])
    return[xPlotList, yPlotList]

def plot(x, y, indexNum, dataNum):
    #calculate AUC
    auc = metrics.auc(x, y)
    #currentColor  = colorsDict[dataNum]
    #fit Curve
    plotMatix = fitLogisticCurve(x, y)
    xPlotList = plotMatix[0]
    yPlotList = plotMatix[1]
    
    color = colorsDict[indexNum]
    marker = markerDict[indexNum]

    #defalutColors = np.random.rand(len(dataNum))
    #axes.plot(xPlotList, yPlotList, color= color, linewidth= 1.5, linestyle= "-")
    axes.plot(x, y, color= color, linewidth= 1.5, linestyle= "-")
    plt.scatter(x, y, c= color, s= 20, linewidths= 0, alpha= 0.8, marker= marker)#, s=area, c=colors, alpha=0.5)
    legendList.append('vector[' + str(dataNum) + ']: AUC=' + str(round(auc, 3)))
    #'#005CAF'
    #plt.title('AUC =' + str(auc) + ', ValueNum = ' + str(dataNum))

#readData
dataDict = {}
colorsDict = {
    0: '#005CAF',
    1: '#D05A6E',
    2: '#BEC23F',
    3: '#FB966E',
    4: '#CA7A2C',
    5: '#6A4C9C',
    6: '#C1328E',
    7: '#5DAC81',
}
markerDict = {
    0: 'h',
    1: '^',
    2: 's',
    3: 'p', 
    4: '|',
    5: '_',
    6: 'D',
    7: '*',
}
legendList = []

#defalutColors = np.random.rand(len(dataNumList))
for i in range(len(dataNumList)):
    dataNum = dataNumList[i]
    #dataFileName = 'possitive_rest83_100Negative_dataProfile_' + str(dataNum) + '_st'
    #dataFileName = 'possitive_rest83_100Negative_dataProfile_' + str(dataNum) + '_st_newCoex'
    dataFileName = 'psdSummer_rest_100Negative_dataProfile_' + str(dataNum) + '_st_newCoex'
    #psdSummer_rest_100Negative_domain_dataProfile_3_st_newCoex
    #dataFileName = 'possitive_rest83_100Negative_dataProfile_domainFraction_' + str(dataNum) + '_st_newCoex'
    #possitive_rest83_100Negative_dataProfile_CoEx_feature_domain_avg_st_newCoex
    #possitive_rest83_100Negative_dataProfile_domainFraction_3_st_newCoex
    dataFileOutName = 'Data_' + str(dataNum)
    dataFileStr = dataFileDir + dataFileName
    dataFileOutStr = dataFileDir + dataFileOutName
    possitiveList = list()
    negativeList = list()
    with open(dataFileStr, 'r') as fileData:
        lines = fileData.readlines()
        firstLineSet = lines[0].strip('\r').strip('\n').split('\t')
        sumPossitive = float(firstLineSet[1])
        sumNegative = float(firstLineSet[2])
        for j in range(2, len(lines)):
            lineSet = lines[j].strip('\r').strip('\n').split('\t')
            possitiveList.append(float(lineSet[1]))
            negativeList.append(float(lineSet[2]))
    #workFlow
    rocMatrix = calculateRocMatrix(possitiveList, negativeList, currentCor)
    tpRatioList = rocMatrix[0]
    fpRatioList = rocMatrix[1]
    x = array(fpRatioList)
    y = array(tpRatioList)
    dataDict[dataNum] = [x, y, i]
    #colorsDict[dataNum] = defalutColors[i]
    #
'''
DATA END
'''
preparePlot()
for dataNum in dataDict:
    x = dataDict[dataNum][0]
    y = dataDict[dataNum][1]
    i = dataDict[dataNum][2]
    plot(x, y, i, dataNum)
#matplotlib.use('cairo')
#plotFonts = FontProperties(weight='normal', size='small')
#plt.title('Roc of The Feature of Phylogenetic(Tanimato)')
plt.legend(legendList, loc=(0.55, 0.05))
#plt.legend(legendList, loc=(0.5, 0.05), borderpad= 1.5, prop =plotFonts, handlelength=3, markerscale=10, handletextpad= 1)
#(0.55, 0.05)
plt.show()






