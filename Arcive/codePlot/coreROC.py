#!usr/bin/python
# Filename:coreROC.py
# The intention is done by 4 spaces
# Written in Python2.7


import time
import sys
import os

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

#private import
from lib.myUtility import *
from lib.netEvaHead import *
from lib.netEvaUtility import *

'''
PLOT DEF
'''
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
'''
PLOT DEF
'''

'''
DATA DEF
'''


'''
DATA DEF
'''























