import pandas as pd
import numpy as np
import os
import random

#DEFAULT SETTINGS - DO NOT TOUCH
tolerance = 15
z_floors = 2
y_tiles = 7
x_tiles = 8
xy_radius = 0.1
x_centerfun = lambda x : -0.8 + 0.2*x
y_centerfun = lambda y : -0.6 + 0.2*y
#DEFAULT SETTINGS - END

#ALTERNATE SETTINGS - START
"""
tolerance = 15
z_floors = 2
y_tiles = 35
x_tiles = 40
xy_radius = 0.02
x_centerfun = lambda x : -0.8 + 0.04*x
y_centerfun = lambda y : -0.6 + 0.04*y
"""
#DEFAULT SETTINGS - END


def readDataFrame(fileName):
    data = pd.read_csv('data/' + fileName)
    data['TAG'] = fileName[:-4]
    return data.drop(data.columns[[1,2]], 1)
    #data = pd.concat([data, data])
    #data = data.sort('SNAPSHOT_TIMESTAMP')

def withinTimeDistance(data, center, dist):
    s = center - dist
    t = center + dist
    #return data[data.SNAPSHOT_TIMESTAMP >= s]
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
    
def filterXInterval(data, cx, radius):
    return data[abs(data.X-cx) < radius]
    
def filterYInterval(data, cy, radius):
    return data[abs(data.Y-cy) < radius]

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
    
def analyseAll(data, cx, cy, radius, isLower):
    totalActiveTags = countUniqueTags(data)
    
    data = filterWithinBox(data, cx, cy, radius)
    data = filterZAxis(data, isLower)
    nearbyTags = countUniqueTags(data)
    
    return totalActiveTags, nearbyTags
    
    
def getCrowdDensity(data_filtered, total, timestamp, x, y, z):
    #cx = x_centerfun(x)
    #cy = y_centerfun(y)
    #data_filtered = filterWithinBox(data_filterZ, cx, cy, xy_radius)
    nearbyTags = countUniqueTags(data_filtered)
    #total, nearby = analyseAll(dataFiltered, cx, cy, xy_radius, isLower)
    if total == 0: total = 1
    return {
        'timestamp': timestamp,
        'x_index': x,
        'y_index': y,
        'z_index': z,
        'amount': nearbyTags,
        'density': nearbyTags/float(total),
    }

def analyseCrowdDensities(data, timestamp, rows_list):
    dataFiltered = withinTimeDistance(data, timestamp, tolerance)
    totalActiveTags = countUniqueTags(dataFiltered)
    
    for z in range(0,z_floors):
        isLower = (z == 0)
        data_filterZ = filterZAxis(dataFiltered, isLower)
        for y in range(0,y_tiles):
            cy = y_centerfun(y)
            data_filterYZ = filterYInterval(data_filterZ, cy, xy_radius)
            for x in range(0,x_tiles):
                cx = x_centerfun(x)
                data_filterXYZ = filterXInterval(data_filterYZ, cx, xy_radius)
                d = getCrowdDensity(data_filterXYZ, totalActiveTags, timestamp, x, y, z)
                rows_list.append(d)


def loadData():
    files = os.listdir('data/')
    data = pd.concat(map(readDataFrame, files))
    data = data.set_index('SNAPSHOT_TIMESTAMP', drop=False)
    data = data.sort_index()
    #data = data.sort('SNAPSHOT_TIMESTAMP')
    return data


def main():
    data = loadData()
    print 'Data loaded'
    #total, nearby = analyse(data, 1216558690, 15, -0.5, -0.5, 0.1, False)
    #print total, nearby
    times = pd.read_csv('test_times.csv')
    rows_list = []
    for t in times['TIME']:
        print 'time: ' + str(t)
        analyseCrowdDensities(data, t, rows_list)

    outputDf = pd.DataFrame(rows_list)
    outputDf.to_csv('test_densities.csv')

main()
"""
X bounds: [-0.84, 0.54] --> [-0.9,0.7] -> 8 points
Y bounds: [-0.62, 0.62] --> [-0.7,0.7] -> 7 points
Points: {0..7} x {0..6} x {0,1} => 112 points
Each point: -0.8+0.2*x + -0.6+0.2*y, r = 0.1
"""