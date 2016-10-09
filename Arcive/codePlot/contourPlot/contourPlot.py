import numpy as np
import sys
import getopt
import os
import matplotlib
import matplotlib.pyplot as plt


def cmpDot(x, y):
    if x[0] != y[0]:
        return cmp(x[0], y[0])
    else:
        return cmp(x[1], y[1])

contourStart = 0.00
contourEnd = 0.35
contourGap = 0.01
inputDir = ''
outputDir = ''
ifShow = False


opts, args = getopt.getopt(sys.argv[1:], "s:e:g:i:o:", ["show"])
for op, value in opts:
    if op == '-s':
        contourStart = float(value)
    elif op == '-e':
        contourEnd = float(value)
    elif op == '-g':
        contourGap = float(value)
    elif op == '-i':
        inputDir = value
    elif op == '-o':
        outputDir = value
    elif op == '--show':
        ifShow = True

'''
for root, dirNames, fileNames in os.walk(inputDir):
    inputPathOriginal = [os.path.join(root, fileName) for fileName in fileNames]
    inputPath = []
    for anyPath in inputPathOriginal:
        #print(anyPath)
        fileNameSet = anyPath.split('/')
        fileNameSetLen = len(fileNameSet)
        fileName = fileNameSet[fileNameSetLen-1]
        print(fileName)
        #print(fileName.find('.'))
        if fileName.find('.') == -1:
            inputPath.append(anyPath)
    print(inputPath)
    outputPath = [os.path.join(outputDir, fileName + '.png') for fileName in fileNames]
    print(outputPath)
#'''

fileNameListOriginal = os.listdir(inputDir)
inputPath = []
outputPath = []
for fileName in fileNameListOriginal:
    #print(fileName)
    #print(fileName.find('.'))
    if fileName.find('.') == -1:
        inputPath.append(inputDir + '/' + fileName)
        outputPath.append(inputDir + '/' + fileName + '.png')

for k in range(len(inputPath)):
    plt.figure()
    with open(inputPath[k], 'r') as inputFile:
        dotValue = []
        lines = inputFile.readlines()
        for line in lines:
            lineSet = line.strip('\n').strip('\r').split('\t')
            dotValue.append((float(lineSet[0]), float(lineSet[1]), float(lineSet[2])))
    dotValue.sort(lambda x, y: cmpDot(x, y))

    for i in range(len(dotValue)):
        if dotValue[i][0] != dotValue[0][0]:
            colNum = i
            break
    rowNum = len(dotValue) / colNum
    x = []
    y = []
    z = []
    for i in range(rowNum):
        tmpList = dotValue[i * colNum: (i + 1) * colNum]
        x.append([j[0] for j in tmpList])
        y.append([j[1] for j in tmpList])
        z.append([j[2] for j in tmpList])

    X = np.array(x)
    Y = np.array(y)
    Z = np.array(z)
    V = np.arange(contourStart, contourEnd, contourGap)

    CS = plt.contour(X, Y, Z, V)
    plt.clabel(CS, inline=1, fontsize=8)
    CB = plt.colorbar(CS, shrink=0.9, extend='both', orientation='horizontal')
    plt.title(inputPath[k][inputPath[k].rindex(os.sep) + 1:])

    plt.savefig(outputPath[k])
    if ifShow:
        plt.show()
