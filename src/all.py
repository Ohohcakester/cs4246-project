#!/usr/bin/python

import pandas as pd
import numpy as np
import re

import generatetest
import bayes
import computedensities
import coordinateconverter

def getMazeName(z):
    """
    Reads in a z value and returns the maze name
    ---
    z: integer 0 or 1
    ---
    Returns: String of maze name
    """
    zToMazename = {0: 'floor2map', 1: 'floor18map'}
    return zToMazename[z]

def readPointFile(filename):
    """
    Reads in points from a file and returns the points as tuples in a list

    Can be changed such that each line is a set of areas
    ---
    filename: string
    points formatted as (a, b), (c, d), (e, f)
    ---
    Returns: list of point tuples
    [(a, b), (c, d), (e, f)] where a through f are floats
    """
    file = open(filename, 'r')
    fileContents = file.read()

    listPoints = []
    m = re.findall('\(.*?\)', fileContents)

    for group in m:
        group = group.replace('(', '')
        group = group.replace(')', '')
        groupArr = [float(x) for x in group.split(',')]
        listPoints.append((groupArr[0], groupArr[1]))

    return listPoints

def generateTestCases(focusPoints, trainTags, level=1):
    """
    Takes in the set of focus points read from file earlier and runs shortest
    paths as per generatetest.py
    ---
    focusPoints: list of focus points
    [(a, b), (c, d), (e, f)] where a through f are floats
    trainTags: list of tags to generate test cases to
    ---
    Returns: dataframe with 3 additional columns of each row's shortest distance
    to the focus points in float
    """

    data = map(generatetest.loadData, trainTags)
    concatenated = pd.concat(data)

    return generatetest.run(concatenated, focusPoints, level=level)

def formatDf(df):
    """
    Takes in dataframe generated from generatetest.py and
    format it to be suitable for input for bayes.py
    ---
    df: dataframe output of generateTestCases method
    ['SNAPSHOT_TIMESTAMP', 'TAG_ID', 'AREA_ID', 'X', 'Y', 'Z',
    'd1', 'd2', 'd3']
    ---
    Returns: dataframe for bayes method
    ['TIMESTAMP', 'USER', 'SHORTEST_PATHS', 'Z']
    """

    dfNew = df[['SNAPSHOT_TIMESTAMP', 'TAG_ID', 'Z']]
    dfNew.columns = ['TIMESTAMP', 'USER', 'Z']

    dfNew = dfNew.assign(SHORTEST_PATHS =
                         map(lambda index: "" + str(df.iloc[index].d1) + ","
                             + str(df.iloc[index].d2) + ","
                             + str(df.iloc[index].d3),
                         range(0, len(df.index))))
    dfNew = dfNew.reset_index()

    return dfNew.drop(['index'], axis=1)

def runBayes(df):
    """
    Takes in a dataframe of ['TIMESTAMP', 'USER', 'Z', SHORTEST_PATHS'] and
    performs a GP regression and a GP prediction
    ---
    df: dataframe output from formatDf method
    ['TIMESTAMP', 'USER', 'Z', SHORTEST_PATHS'] where
    'SHORTEST_PATHS' is a series of 3-tuples, each of which contain shortest
    distances of each of the 3 selected points
    ---
    Returns:
    A DataFrame of ['TIMESTAMP', 'MU', 'VAR'] for all users concatenated
    'MU' and 'VAR' both contains series of 3-tuples
    """
    df['SHORTEST_PATHS'] = df['SHORTEST_PATHS'].str.split(',')
    uniqueUserID = df['USER'].unique()

    result = pd.DataFrame()

    # Iterate through each user and regress then concat the output
    result = bayes.predictGP(df[df['USER'] == uniqueUserID[0]])

    '''
    for user in uniqueUserID:
        userResult = bayes.predictGP(df[df['USER'] == user])
        result = pd.concat([result, userResult])
    '''
    return result

def computeDensity(df, areas, level=1):
    """
    Computes the predicted density for a list of areas for a level
    ---
    df: Output dataframe from bayes step
    ['TIMESTAMP', 'Z', MU', 'VAR']
    where 'MU' and 'VAR' both contains series of 3-tuples
    areas: list of areas
    [(a, b), (c, d), (e, f)] where a through f are floats
    level: integer 0 or 1 representing floor2 or floor18
    ---
    Returns: dict {timestamp: densityDistribution}
    Note: to query, just densityDistribution.query(point)
    """
    return computedensities.compute(getMazeName(level), areas, df, quiet=True)

def bayesOpt():
    """
    Supposed to do some bayesian optimisation here
    """
    pass

def computeAreaDensity(tags, focusPoints, areas):
    """
    Takes in tags and compute densities for all the users
    for the areas specified

    Note: This only needs to be run once per run, no need to do bayes opt
    so maybe we can preprocess and store in file?
    --
    tags: list of user tags
    focusPoints: list of focus points
    [(a, b), (c, d), (e, f)] where a through f are floats
    areas: list of areas
    [(a, b), (c, d), (e, f)] where a through f are floats
    --
    Returns: dict {timestamp: densityDistribution}
    """

    dfFloor18 = generateTestCases(focusPoints, tags, level=1)
    dfFormattedFloor18 = formatDf(dfFloor18)

    bayesResult = runBayes(dfFormattedFloor18)

    densityDist = computeDensity(bayesResult, areas, level=1)

    return densityDist

def calculateError(predictedDensityDist, actualDensityDist):
    """
    Calculate Error from dataframe of densities
    ---
    predictedDensityDist: dict {timestamp: densityDistribution}
    where densityDistribution is a computedensities.DensityDistribution
    testTags: list of tags for test set
    ---
    Returns: float error
    """

    sum = 0.0
    count = 0.0

    for timestamp in predictedDensityDist:
        predicted = predictedDensityDist[timestamp]
        actual = actualDensityDist[timestamp]

        for point in predicted:
            sum += (predicted.query(point)*10 - actual.query(point))**2
            count += 1

    return np.sqrt(sum / count)

class ActualDensityDist:
    def __init__(self):
        self.points = {}

    def addPoint(self, point, density):
        self.points[point] = density

    def getPoints(self):
        return self.points

    def query(self, point):
        return self.points[point]

def computeActualDensityDist(predictedDensityDist, focusPoints, testTags):
    radius = 5.
    unitArea = np.pi * radius**2
    result = {}

    floor18grid = coordinateconverter.Grid(getMazeName(1))
    def convertCoord(point):
        return floor18grid.convertToGridFloating(point[0], point[1])

    dfFloor18 = generateTestCases(focusPoints, tags, level=1)
    converted = dfFloor18[['X', 'Y']].apply(convertCoord, axis=1)
    dfFloor18['X'] = converted.apply(lambda p: p[0])
    dfFloor18['Y'] = converted.apply(lambda p: p[1])

    for timestamp in predictedDensityDist:
        df = dfFloor18[dfFloor18['SNAPSHOT_TIMESTAMP'] == timestamp]
        actualDensityDist = ActualDensityDist()

        for point in predictedDensityDist[timestamp].getPoints():
            distsToPoint = ((df['X'] - point[0])**2 +
                            (df['Y'] - point[1])**2).apply(np.sqrt)
            count = distsToPoint[distsToPoint <= radius].shape[0]
            actualDensityDist.addPoint(point, count / unitArea)

        result[timestamp] = actualDensityDist

    return result

if __name__ == '__main__':
    focusPoints = readPointFile('focuspoints.csv')
    areas = readPointFile('areas.csv')

    tags = generatetest.listTags()[0:100]
    testTags, trainTags = generatetest.splitTags(tags, proportion=0.5)

    predictedDensityDist = computeAreaDensity(trainTags, focusPoints, areas)
    actualDensityDist = computeActualDensityDist(predictedDensityDist,
                                                 focusPoints,
                                                 testTags)
    error = calculateError(predictedDensityDist, actualDensityDist)
