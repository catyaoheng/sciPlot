#!usr/bin/python
# Filename:prepareRoc.py
# The intention is done by 4 spaces
# Written in Python2.7

import time
import os

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

def writeLog(logStr):
    with open(logFileStr,'a') as fileLog:
        fileLog.write(logStr)

# config
dataFileDir = '../include/plot/'
#dataFileDir = '../include/plot/old_profile/'
currentCor = 'poss'
#currentCor = 'nega'
dataNumList = [3]
#'''

def calculateRocMatrix(possitiveList, negativeList, correlationType):
    tpRatioList = []
    fpRatioList = []
    possitiveList = [0.0] + possitiveList + [0.0]
    negativeList = [0.0] + negativeList + [0.0]
    prepareInput(len(possitiveList))
    tp = 0
    fp = 0
    for i in range(len(possitiveList)):
        process(True)
        #cal tpRatio
        if correlationType == 'poss':
            tp = sum(possitiveList[i:])
            fp = sum(negativeList[i:])
        else:
            tp = sum(possitiveList[:i+1])
            fp = sum(negativeList[:i+1])
        #print(str(i) +'||'+ str(tp)+'||'+str(fp))           
        tpRatio = (tp*1.0) / sumPossitive
        fpRatio = (fp*1.0) / sumNegative
        tpRatioList.append(tpRatio)
        fpRatioList.append(fpRatio)
    return[tpRatioList, fpRatioList]


for i in range(len(dataNumList)):
    dataNum = dataNumList[i]
    dataFileName = 'possitive_rest83_100Negative_dataProfile_' + str(dataNum) + '_st_newCoex'
    dataFileOutName = 'Data_' + str(dataNum)
    dataFileStr = dataFileDir + dataFileName
    dataFileOutDir = dataFileDir + '/' +str(dataNum) + '/'
    if not os.path.exists(dataFileOutDir):
        os.makedirs(dataFileOutDir)
    dataFileOutStr = dataFileOutDir + dataFileOutName
    logFileStr = dataFileOutDir + 'prepareRoc_log'
    possitiveList = list()
    negativeList = list()
    print('prepareInput: vector[' + str(dataNum) + '] ...')
    writeLog('prepareInput: vector[' + str(dataNum) + '] ...' + '\n')
    with open(dataFileStr, 'r') as fileData:
        lines = fileData.readlines()
        firstLineSet = lines[0].strip('\r').strip('\n').split('\t')
        sumPossitive = float(firstLineSet[1])
        sumNegative = float(firstLineSet[2])
        prepareInput(lines)
        for j in range(2, len(lines)):
            process()
            lineSet = lines[j].strip('\r').strip('\n').split('\t')
            possitiveList.append(float(lineSet[1]))
            negativeList.append(float(lineSet[2]))
    #workFlow
    print('\tcalTprFpr ...')
    writeLog('\tcalTprFpr ...' + '\n')
    rocMatrix = calculateRocMatrix(possitiveList, negativeList, currentCor)
    tpRatioList = rocMatrix[0]
    fpRatioList = rocMatrix[1]
    print('\twrite ...')
    writeLog('\twrite ...' + '\n')
    with open(dataFileOutDir, 'w') as fileOutput:
        prepareInput(len(tpRatioList))
        for k in range(len(tpRatioList)):
            process()
            fileOutput.write(join([tpRatioList[k]+fpRatioList[k]]) + '\n')








