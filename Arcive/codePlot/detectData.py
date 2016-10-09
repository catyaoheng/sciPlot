#!usr/bin/python
# Filename:detectData.py
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

distribute

def countPossitive    

#config
versionTime = time.asctime()
timeStamp = time.strftime('%Y%m%d%H%M%S',time.localtime())
featureNameList = ['domain_avg']
featureDict = {
    'domain_avg': [3, 17]
}
defaultNaMarker = 'n'
defaultDict = {
    20: 'infinity',
    29: '0.0',
    30: '-2.0',
    }
defaultList = list()
for i in defaultDict:
    if defaultDict[i].find(defaultNaMarker)!= -1:
        defaultList.append(i)
for i in defaultList:
    defaultDict.pop(i)
gsdIndexDir = '../include/gsd/'
observeFileDir = '../include/observe/'
sampleFileDir = '../include/sample/'
totalIndexName = 'possitive_rest83_100Negative'
foldNum = 5
logFileStr = sampleFileDir + 'makeSvmSample_' + totalIndexName + '_detect_log'
totalSampleFileStr = sampleFileDir + totalIndexName + '_totalSample'
'''test
#this dict should contain
defaultNaMarker = 'n'
defaultDict = {
    3: '0.0',
    5: '-2.0',
    7: 'infinity',
    8: 'infinity'
    }
defaultList = list()
for i in defaultDict:
    if defaultDict[i].find(defaultNaMarker)!= -1:
        defaultList.append(i)
for i in defaultList:
    defaultDict.pop(i)
sampleIndexDir = '../include/gsd/'
observeFileDir = '../include/observe/'
sampleFileDir = '../include/sample/'
totalIndexName = 'possitive_rest_test'
foldNum = 5
logFileStr = sampleFileDir + 'makeSvmSample_' + totalIndexName + '_detect_log'
totalSampleFileStr = sampleFileDir + totalIndexName + '_totalSample'
#'''
'''
work logic:
make the totalSample first
Then get data needed by the foldList
'''

# begin log
writeLog('=== ' + versionTime + ' ===\n')
# work flow
writeLog('>Detect data ...\n')
print('>Detect data ...')

totalSampleList = list()
with open(totalSampleFileStr, 'r') as fileTotalSample:
    writeLog('\t>preparing value ...\n')
    print('\t>preparing value ...')
    lines = fileTotalSample.readlines()
    for line in lines:
        lineSet = line.strip('\r').strip('\n').split('\t')
        vectorLength = len(lineSet)
        break
    writeLog('\t\t>vectorLength = ' + str(vectorLength) + ' ...\n')
    print('\t\t>vectorLength = ' + str(vectorLength) + ' ...')
    prepareInput(lines)
    for line in lines:
        process(True)
        lineSet = line.strip('\r').strip('\n').split('\t')
        totalSampleList.append(lineSet)
    
    valueDict = dict()
    for i in range(3,vectorLength):
        defaultList = ['n','NA']
        if i in defaultDict:
            defaultList.append(defaultDict[i])
        writeLog('\t\t>preparing vetctor[' + str(i) + '] defalutMarker is ' + str(defaultList) + '...\n')
        print('\t\t>preparing vetctor[' + str(i) + '] defalutMarker is ' + str(defaultList) + '...')
        valueMarkerPairList = list()
        prepareInput(totalSampleList)
        for lineSet in totalSampleList:
            process(True)
            currentMarker = lineSet[i]
            for defalutMarker in defaultList:
                #print(currentMarker + '\t' + defalutMarker + '\t' + str(currentMarker.find(defalutMarker)!=-1))
                if currentMarker.find(defalutMarker)!=-1:
                    valueMarkerPairList.append([int(lineSet[0]), 'n'])
                else:
                    valueMarkerPairList.append([int(lineSet[0]), float(currentMarker)])
        valueDict[i] = valueMarkerPairList
        
writeLog('\t>detect value ...' + '\n')
print('\t>detect velue ...')
distributionDict = dict()
for i in valueDict:
    writeLog('\t\t>detect value[' + str(i) + '] ...' + '\n')
    print('\t\t>detect velue[' + str(i) + '] ...')
    distribution = dict()
    valueMarkerPairList = valueDict[i]
    prepareInput(valueMarkerPairList)
    for valueMarkerPair in valueMarkerPairList:
        process()
        marker = valueMarkerPair[0]
        value = valueMarkerPair[1]
        if value in distribution:
            distribution[value].append(marker)
        else
            distributionList = list()
            distribution[value] = distributionList
            distribution[value].append(marker)
    distributionDict[i] = distribution


for featureName in featureNameList:
    writeLog('\t\t>detect value[' + featureName + '] ...' + '\n')
    print('\t\t>detect velue[' + featureName + '] ...')
    featureVectorInfo = featureDict[featureName]
    begin = featureVectorInfo[0]
    end = featureVectorInfo[1]
    featureValueMarkerPairList = list()
    beginValueMarkerPairList = valueDict[begin]
    for valueMarkerPair in beginValueMarkerPairList:
        featureValueMarkerPairList.append(valueMarkerPair)

    for i range(begin, end + 1):
        currentValueMarkerPairList = valueDict[i]
        for j in range(len(currentValueMarkerPairList)):
            currentValueMarkerPair = currentValueMarkerPairList[j]
            featureValueMarkerPairList[j].append(currentValueMarkerPair[1])



























