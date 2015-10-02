import pandas as pd
import numpy as np
import os
import random


def readDataFrame(fileName):
    data = pd.read_csv('data/' + fileName)
    data['TAG'] = fileName[:-4]
    return data.drop(data.columns[[1,2]], 1)
    #data = pd.concat([data, data])
    #data = data.sort('SNAPSHOT_TIMESTAMP')

def withinTimeDistance(data, center, dist):
    s = center - dist
    t = center + dist
    return data[(data.SNAPSHOT_TIMESTAMP >= s) & (data.SNAPSHOT_TIMESTAMP < t)]

def countUniqueTags(data):
    return len(data['TAG'].unique())

def tagsWithinTimeDistance(*args):
    return withinTimeDistance(*args)['TAG'].unique()

def countWithinTimeDistance(*args):
    return len(tagsWithinTimeDistance(*args))

def filterWithinCircle(data, cx, cy, radius):
    return data[(data.X-cx)*(data.X-cx) + (data.Y-cy)*(data.Y-cy) < radius*radius]

def filterWithinBox(data, cx, cy, radius):
    return data[(abs(data.X-cx) < radius) & (abs(data.Y-cy) < radius)]

def filterZAxis(data, isLower):
    if isLower:
        return data[data.Z < 0.5]
    else:
        return data[data.Z >= 0.5]

def analyse(data, time, tolerance, cx, cy, radius, isLower):
    data = withinTimeDistance(data, time, tolerance)
    totalActiveTags = countUniqueTags(data)

    data = filterWithinBox(data, cx, cy, radius)
    data = filterZAxis(data, isLower)
    nearbyTags = countUniqueTags(data)

    return totalActiveTags, nearbyTags

def minDistance(a, S):
    if len(S) == 0: return 9999999999 #infinity
    return min(map(lambda s : abs(a-s), S))

def generateTestTimes(n):
    minTime = int(data['SNAPSHOT_TIMESTAMP'].min())
    maxTime = int(data['SNAPSHOT_TIMESTAMP'].max())
    timeList = []

    while len(timeList) < n:
        currTime = random.randrange(minTime,maxTime)
        total, nearby = analyse(data, currTime, 15, -0.5, -0.5, 0.1, False)
        if total > 300:
            if minDistance(currTime, timeList) > 200:
                timeList.append(currTime)
    return timeList

def getCrowdDensity(data, timestamp, x, y, z):
    cx = -0.8 + 0.2*x
    cy = -0.6 + 0.2*y
    isLower = (z == 0)
    total, nearby = analyse(data, timestamp, 15, cx, cy, 0.1, isLower)
    return {
        'timestamp': timestamp,
        'x_index': x,
        'y_index': y,
        'z_index': z,
        'amount': nearby,
        'density': nearby/float(total),
    }

def analyseCrowdDensities(data, timestamp, rows_list):
    for z in range(0,2):
        for y in range(0,7):
            for x in range(0,8):
                d = getCrowdDensity(data, timestamp, x, y, z)
                rows_list.append(d)


def loadData():
    files = os.listdir('data/')
    data = pd.concat(map(readDataFrame, files))
    data = data.sort('SNAPSHOT_TIMESTAMP')
    return data


data = loadData()
#total, nearby = analyse(data, 1216558690, 15, -0.5, -0.5, 0.1, False)
#print total, nearby
times = pd.read_csv('test_times.csv')
rows_list = []
for t in times['TIME']:
    print 'time: ' + str(t)
    analyseCrowdDensities(data, t, rows_list)

outputDf = pd.DataFrame(rows_list)
outputDf.to_csv('true_densities.csv')


"""
X bounds: [-0.84, 0.54] --> [-0.9,0.7] -> 8 points
Y bounds: [-0.62, 0.62] --> [-0.7,0.7] -> 7 points
Points: {0..7} x {0..6} x {0,1} => 50 points
Each point: -0.8+0.2*x + -0.6+0.2*y, r = 0.1
"""