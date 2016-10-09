#!usr/bin/python
# Filename:newRoc.py
# The intention is done by 4 spaces
# Written in Python2.7

__author__ = 'hyao'
import time
import sys
import os

plotFileDir = '../include/plot/'
fileName = 'testNewRoc'
fileStr = plotFileDir + fileName
outputStr = plotFileDir + fileName + '_out'

def join(obj, splitor = '\t'):
    jointStr = ''
    if isinstance(obj, list):
        jointStr = str(obj[0])
        for ele in obj[1:]:
            jointStr = jointStr + splitor + str(ele)
        jointStr = jointStr.strip(splitor)
    return jointStr

dataList = list()
with open(fileStr,'r')as fileInput:
    lines = fileInput.readlines()
    for line in lines:
        lineSet = line.strip('\r').strip('\n').split('\t')
        dataList.append(lineSet)

thresholdList = [i * 0.01 for i in range(101)]
statList = list()
for i in thresholdList:
    abovePosList = list()
    aboveNegList = list()
    belowPosList = list()
    belowNegList = list()
    for valueSet in dataList:
        if float(valueSet[0]) > i:
            abovePosList.append(int(valueSet[1]))
            aboveNegList.append(int(valueSet[2]))
        elif float(valueSet[0]) < i:
            belowPosList.append(int(valueSet[1]))
            belowNegList.append(int(valueSet[2]))
    sumAbovePosNum = sum(abovePosList)
    sumAboveNegNum = sum(aboveNegList)
    sumBelowPosNum = sum(belowPosList)
    sumBelowNegNum = sum(belowNegList)
    statList.append([sumAbovePosNum ,sumAboveNegNum ,sumBelowPosNum ,sumBelowNegNum])

with open(outputStr,'w') as fileOutput:
    for stat in statList:
        outStr = join(stat) + '\n'
        fileOutput.write(outStr)