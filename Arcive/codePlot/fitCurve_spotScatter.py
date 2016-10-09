#!/usr/bin/python
# Filename : fitCurve_spotScatter.py
# The intention is done by 4 spaces.

from numpy import array
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq

#-------------------
#Data   
#-------------------
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
possR = [0,7]
dataNum = 17

#currentR = negaR
currentR = possR
dataFileName = 'possitive_rest83_100Negative_dataProfile_' + str(dataNum) + '_st'
dataFileOutName = 'Data_' + str(dataNum)
dataFileStr = dataFileDir + dataFileName
dataFileOutStr = dataFileDir + dataFileOutName

valueList = list()
llList = list()
outList = list()
with open(dataFileStr, 'r') as fileData:
    lines = fileData.readlines()
    for i in range(3, len(lines)):
        lineSet = lines[i].strip('\r').strip('\n').split('\t')
        abPoNumR = float(lineSet[3])/(13330-5704)
        blNeNumR = (float(lineSet[6]) - 293002)/(688970-293002)
        valueList.append(float(lineSet[currentR[0]]))
        llList.append(abPoNumR/blNeNumR)


#Date
#AllInt & AllPro
value = array(valueList)
ll = array(llList)
x = value
y = ll
#ArthInt & ArthPro
#interaction1 = array([0,0,360,1109,3207,4998,12940,14036,17668,17645]);
#protein1 = array([0,0,295,892,1720,2582,5708,6049,7200,7187])

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
#-------------------
#Calculation & fit  
#-------------------




#-------------------
#Plot  
#-------------------
# Plot title
#plt.title('The Explosion of Protein-Protein Interaction Data in Past 10 Years')
# Plot curve
#plt.plot(x,peval(x,plsq[0]),x,y_meas,'o',x,y_true)
plt.plot(x,peval(x,plsq[0]),x,y,"o")
#plt.legend(['Fit Explosion Curve','Number of available proteins'], loc='upper left')
# Plot scatter
#plt.scatter(x, y)#, s=area, c=colors, alpha=0.5)
'''
plt.title('Least-squares 4PL fit to noisy data')
plt.legend(['Fit', 'Noisy', 'True'], loc='upper left')
for i, (param, actual, est) in enumerate(zip('ABCD', [A,B,C,D], plsq[0])):
    plt.text(10, 3-i*0.5, '%s = %.2f, est(%s) = %.2f' % (param, actual, param, est))
plt.show()
'''

plt.show()