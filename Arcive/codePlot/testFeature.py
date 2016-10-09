#!usr/bin/python
# Filename:testFeature.py
# The intention is done by 4 spaces
# Written in Python2.7

__author__ = 'hyao'
import time
import sys
import os

#function
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

def writeLog(logStr):
    with open(logFileStr,'a') as fileLog:
        fileLog.write(logStr)

def join(obj, splitor = '\t'):
    jointStr = ''
    if isinstance(obj, list):
        jointStr = str(obj[0])
        for ele in obj[1:]:
            jointStr = jointStr + splitor + str(ele)
        jointStr = jointStr.strip(splitor)
    return jointStr

#config
versionTime = time.asctime()
timeStamp = time.strftime('%Y%m%d%H%M%S',time.localtime())
plotFileDir = '../include/plot/'
totalIndexName = 'possitive_rest83_100Negative'
logFileStr = plotFileDir + 'detectSvmSample_' + totalIndexName + '_log'
plotFileStr = plotFileDir + totalIndexName + '_dataProfile_CoEx'
#ncFeatureList = []#ncFeature = negativeCorrelationFeature

with open(plotFileStr, 'r') as filePlot:
    lines = filePlot.readlines()
    for line in lines:
        lineSet = line.strip('\r').strip('\n').split('\t')
        valueNum = lineSet[0]
        if (valueNum == '21'):
            print(valueNum)
            possitiveDict = dict()
            negativeDict = dict()
            valueNameList = list()
            print('\tprepare value')
            for i in range(1, len(lineSet)):
                valueName = lineSet[i].split(': ')[0]
                if valueName.find('n') == -1:
                    valueProfile = lineSet[i].split(': ')[1]
                    profileSet = valueProfile.split('|')
                    possitiveDict[float(valueName)] = float(profileSet[0])
                    negativeDict[float(valueName)] = float(profileSet[1])
                    valueNameList.append(float(valueName))
            #the value is sorted
            valueNameList.sort()
            valuePossitiveSortedList = list()
            valueNegativeSortedList = list()
            print('\tprepare poss/nega')
            for valueName in valueNameList:
                valuePossitiveSortedList.append(possitiveDict[valueName])
                valueNegativeSortedList.append(negativeDict[valueName])
    
            valueProfileList = list()
            sumPosstiveNum = sum(valuePossitiveSortedList)
            sumNegativeNum = sum(valueNegativeSortedList)
            valueProfileList.append(['sum', sumPosstiveNum, sumNegativeNum])
            valueProfileList.append(['valueName', 'posNum', 'negNum', 'abPosNum', 'bePosNum', 'abNegNum', 'beNegNum', 'llRatio'])
    
            print('\tcal likelihood')
            
            prepareInput(valueNameList)
            for i in range(len(valueNameList)):
                process()
                possitiveNum = valuePossitiveSortedList[i]
                negativeNum = valueNegativeSortedList[i]
                aboveValuePossitiveNum = sum(valuePossitiveSortedList[i:])
                belowValuePossitiveNum = sum(valuePossitiveSortedList[:i+1])
                aboveValueNegativeNum = sum(valueNegativeSortedList[i:])
                belowValueNegativeNum = sum(valueNegativeSortedList[:i+1])
                if (aboveValueNegativeNum/sumNegativeNum) == 0:
                    currentLikelihoodRatio = 'infinity'
                else:
                    currentLikelihoodRatio = (aboveValuePossitiveNum/sumPosstiveNum)/(aboveValueNegativeNum/sumNegativeNum)
                valueProfileList.append([
                    valueNameList[i], #0A
                    possitiveNum, #1B
                    negativeNum, #2C
                    aboveValuePossitiveNum, #3D
                    belowValuePossitiveNum, #4E
                    aboveValueNegativeNum, #5F
                    belowValueNegativeNum, #6G
                    currentLikelihoodRatio #7H
                    ])
            print('\twrite file')
            with open(plotFileStr + '_' + valueNum +'_st_newCoex','w') as fileLikelihood:
                for profile in valueProfileList:
                    outStr = join(profile) + '\n'
                    fileLikelihood.write(outStr)












