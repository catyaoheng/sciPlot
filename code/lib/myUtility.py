#!usr/bin/python
# Filename:#!usr/bin/python
# Filename:myUtility.py
# The intention is done by 4 spaces
# Written in Python2.7

__author__ = 'hyao'
import time
import sys
import os

#general function
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

def process(isLog):
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

def initiaFileNameList(folderDir_or_nameList):
    fileNameList = []
    if isinstance(folderDir_or_nameList, str):
        originalFileNameList = os.listdir(folderDir_or_nameList)
        for fileName in originalFileNameList:
            if fileName.find('.') == -1:
                fileNameList.append(fileName)
    else:
        fileNameList = folderDir_or_nameList
    return fileNameList

#Read File
def readFile(filePath, printInfo = False):
    if printInfo:
        print("reading file: " + filePath)
    gene2TermDict = {}
    with open(filePath, 'r') as currentFile:
        lines = currentFile.readlines() 
    return lines

def prepareXmlLikeFile(lines, header = '#'):
    '''
    DATA STR : Key(Str):Value(List)
    '''
    xmlLikeDict = {}
    currentKey = ''
    for line in lines:
        lineSet = line.strip('\n').strip('\r').split('\t')
        lineMark = lineSet[0]
        if lineMark == header:
            currentKey = lineMark
        else:
            if currentKey in xmlLikeDict:
                xmlLikeDict[currentKey] = xmlLikeDict[currentKey] + lineSet
            else:
                xmlLikeDict[currentKey] = lineSet
    return xmlLikeDict
#Write File

#KEY, V1, V2, V3
#write: KEY\tV1splitorV2splitorV3\n
def writeFlatDict(dcitNeed2WriteFlat, filePath, splitor):
    print("writing flatDict: " + filePath)
    with open(filePath, 'w') as flatDictFile:
        prepareInput(dcitNeed2WriteFlat)
        for key in dcitNeed2WriteFlat:
            process(False)
            values = dcitNeed2WriteFlat[key]
            flatDictFile.write(join([key, join(values, splitor)]) + '\n')