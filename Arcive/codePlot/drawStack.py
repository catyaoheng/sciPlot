#!usr/bin/python
# Filename:drawStack.py
# The intention is done by 4 spaces
# Written in Python2.7

import numpy as np
import matplotlib.pyplot as plt

#DATA
possitiveNum   = [20, 35, 30, 35, 27, 10]
negativeNum = [25, 32, 34, 20, 25, 24]

#Yaxis
yScale = int((max(possitiveNum) + max(negativeNum))*1.2)
baseHight = int(max(negativeNum) * 1.2)
scale = 1
while max([max(possitiveNum), max(negativeNum)])/scale >1:
	scale = scale * 10

possitiveY = 0
while possitiveY < max(possitiveNum):
	possitiveY = possitiveY + scale
possitiveCoords = [i for i in range(scale, possitiveY)]

negativeY = 0
while negativeY < max(negativeNum):
	negativeY = negativeY + scale



ticks
ratioPoNe = [p/n for ]
ind = np.arange(N) + 10    # the x locations for the groups
ind = [2.5, 3.0, 5.0, 6.0, 6.5, 7.9]
#ind = range(6)
#ind = [1,2,3,4,5,6]
print(ind[1])
print(ind)
width = 0.35       # the width of the bars: can also be len(x) sequence

# matplotlib.pyplot.bar(left, height, width=0.8, bottom=None, hold=None, **kwargs)
p1 = plt.bar(ind, possitiveNum,   width, color='r', )
p2 = plt.bar(ind, negativeNum, width, color='y',
             bottom=possitiveNum)

plt.ylabel('Scores')
plt.title('Scores by group and gender')
xticksInd = [i+width/2 for i in ind]
#print xticksInd
#xticksInd = list()

plt.xticks(xticksInd, ('G1', 'G2', 'G3', 'G4', 'G5', 'G6') )
	#+width/2.)
#, ('G1', 'G2', 'G3', 'G4', 'G5') )
plt.yticks(np.arange(0,81,10))
plt.legend( (p1[0], p2[0]), ('Men', 'Women') )

plt.show()