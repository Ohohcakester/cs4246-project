#!/usr/bin/python

import pandas as pd
import numpy as np
import re
import GPyOpt

import generatetest
import bayes
import computedensities
import coordinateconverter

_coordGrids = {
    'floor2map' : coordinateconverter.Grid('floor2map'),
    'floor18map' : coordinateconverter.Grid('floor18map'),
}
_zToMazename = {
    0: 'floor2map',
    1: 'floor18map',
}

def getMazeName(z):
    """
    Reads in a z value and returns the maze name
    ---
    z: integer 0 or 1
    ---
    Returns: String of maze name
    """
    return _zToMazename[z]

def readPointFile(filename):
    """
    Reads in points from a file and returns the points as tuples in a list

    Can be changed such that each line is a set of focus points
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

def generateVisualisation(focusPoints, predictedDensityDist, scaleRatio, actualDensityDist):
    import visualisedensitymap
    fileName = visualisedensitymap.generateFileName(focusPoints)
    visualisedensitymap.run(fileName, predictedDensityDist, scaleRatio, actualDensityDist)

def runBayes(df, testTimes):
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

    print 'NOT BEING USED'; quit()
    df['SHORTEST_PATHS'] = df['SHORTEST_PATHS'].str.split(',')
    uniqueUserID = df['USER'].unique()

    result = pd.DataFrame()

    result = bayes.predictGP(df[df['USER'] == uniqueUserID[0]], testTimes)

    '''
    # Iterate through each user and regress then concat the output
    for user in uniqueUserID:
        userResult = bayes.predictGP(df[df['USER'] == user], testTimes)
        result = pd.concat([result, userResult])
    '''

    return result

def computeDensity(df, focusPoints, level=1):
    """
    Computes the predicted density for a list of focus points for a level
    ---
    df: Output dataframe from bayes step
        ['TIMESTAMP', 'Z', MU', 'VAR']
        where 'MU' and 'VAR' both contains series of 3-tuples
    focusPoints: list of focus points
        [(a, b), (c, d), (e, f)] where a through f are floats
    level: integer 0 or 1 representing floor2 or floor18
    ---
    Returns: dict {timestamp: densityDistribution}
    Note: to query, just densityDistribution.query(point)
    """
    print 'COMPUTING PREDICTED DENSITY'
    print 'Reference points = ' + str(focusPoints)
    print 'mazeName = ' + str(getMazeName(level))
    return computedensities.compute(getMazeName(level), focusPoints, df, quiet=True)


def computeAreaDensity(zCoord, tags, focusPoints, testTimes):
    """
    Takes in tags and compute densities for all the users
    for the focus points specified

    Note: This only needs to be run once per run, no need to do bayes opt
    so maybe we can preprocess and store in file?
    --
    tags: list of user tags
    focusPoints: list of focus points
    [(a, b), (c, d), (e, f)] where a through f are floats
    --
    Returns: dict {timestamp: densityDistribution}
    """

    dfFloor18 = generateTestCases(focusPoints, tags, level=zCoord)
    dfFormattedFloor18 = formatDf(dfFloor18)

    uniqueUserID = dfFormattedFloor18['USER'].unique()
    dfFormattedFloor18['SHORTEST_PATHS'] = dfFormattedFloor18['SHORTEST_PATHS'].str.split(',')

    result = pd.DataFrame()

    #result = bayes.predictGP(dfFormattedFloor18[dfFormattedFloor18['USER'] == uniqueUserID[0]], testTimes)

    densityDist = None
    numOfSkippedFile = 0

    # Iterate through each user
    for user in uniqueUserID:
        userResult = bayes.predictGP(
            dfFormattedFloor18[dfFormattedFloor18['USER'] == user],
            testTimes)

        userDensityDist = computeDensity(userResult, focusPoints, level=zCoord)

        if densityDist is None:
            densityDist = userDensityDist
        else:
            for timestamp in userDensityDist:
                # All timestamps the same
                # Add points
                userDensityDistTimestamp = userDensityDist[timestamp]
                densityDistTimestamp = densityDist[timestamp]
                userDensityDistTimestampPoints = userDensityDistTimestamp.getPoints()
                for point in userDensityDistTimestampPoints:
                    densityDistPoint = densityDistTimestamp.query(point)

                    if np.isnan(densityDistPoint):
                        densityDistPoint = 0

                    addedProb = densityDistTimestamp.query(point) + userDensityDistTimestamp.query(point)
                    densityDist[timestamp].setPoint(point, addedProb)

    return densityDist, numOfSkippedFile

def calculateError(predictedDensityDist, actualDensityDist, numOfSkippedFile=0):
    """
    Calculate Error from dataframe of densities
    ---
    predictedDensityDist: dict {timestamp: densityDistribution}
    where densityDistribution is a computedensities.DensityDistribution
    testTags: list of tags for test set
    ---
    Returns: float root mean square error
    """

    sum = 0.0
    count = 0.0

    minPredicted = 99999999
    maxPredicted = 0
    minActual = 99999999
    maxActual = 0

    scalebackRatio = 100 / (10 - numOfSkippedFile)

    # Verification code. Can comment out to run (not much) faster.
    #if set(predictedDensityDist.keys()) != set(actualDensityDist.keys()): print 'ERROR: TIMESTAMPS DO NOT MATCH'

    for timestamp in predictedDensityDist:
        predicted = predictedDensityDist[timestamp]
        actual = actualDensityDist[timestamp]

        # Verification code. Can comment out to run (not much) faster.
        #if set(predicted.getPoints()) != set(actual.getPoints()): print 'ERROR: POINTS DO NOT MATCH'

        for point in predicted.getPoints():
            predictedDensity = predicted.query(point)
            if np.isnan(predictedDensity):
                print 'NAN DETECTED', predictedDensity, point; quit()
                predictedDensity = 0.

            predictedValue = predictedDensity*scalebackRatio
            actualValue = actual.query(point)

            minActual = min(minActual, actualValue)
            maxActual = max(maxActual, actualValue)
            minPredicted = min(minPredicted, predictedValue)
            maxPredicted = max(maxPredicted, predictedValue)

            sum += (predictedDensity*scalebackRatio -
                    actual.query(point))**2
            count += 1

    print 'Actual Density Range: [', minActual,',',maxActual,'] | Predicted Density Range: [',minPredicted,',',maxPredicted,']'
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

def computeActualDensityDist(zCoord, predictedDensityDist, focusPoints, testTags):
    radius = 5.
    unitArea = np.pi * radius**2
    result = {}

    floor18grid = _coordGrids[getMazeName(zCoord)]
    def convertCoord(point):
        return floor18grid.convertToGridFloating(point[0], point[1])
    def withinRadius(point, radius):
        def fun(coord):
            dx = point[0]-coord[0]
            dy = point[1]-coord[1]
            return dx*dx+dy*dy <= radius*radius
        return fun

    dfFloor18 = map(generatetest.loadData, tags)
    dfFloor18 = pd.concat(dfFloor18)

    converted = dfFloor18[['X', 'Y']].apply(convertCoord, axis=1)
    dfFloor18['X'] = converted.apply(lambda p: p[0])
    dfFloor18['Y'] = converted.apply(lambda p: p[1])

    print 'COMPUTING ACTUAL DENSITY'
    print 'No. of Timestamps: ' + str(len(predictedDensityDist.keys()))
    for timestamp in predictedDensityDist:
        #print 'Computing actual density: ' + str(timestamp)
        df = dfFloor18[abs(dfFloor18['SNAPSHOT_TIMESTAMP'] - timestamp) <= 15]
        values = df[['X','Y']].values.tolist()
        actualDensityDist = ActualDensityDist()

        for point in predictedDensityDist[timestamp].getPoints():
            count = len(filter(withinRadius(point,radius), values))
            actualDensityDist.addPoint(point, count / unitArea)

        result[timestamp] = actualDensityDist

    return result

def makeOptFunc(testTimes, trainTags, testTags, visualise=False):
    zCoord = 1

    def optFunc(samples):
        #print samples
        rval = np.zeros((samples.shape[0], 1))

        for index, focusPoints in enumerate(samples):
            xCoords = filter(lambda x: x,
                             [p[1] if p[0] % 2 == 0 else None
                              for p in enumerate(focusPoints)])
            yCoords = filter(lambda x: x,
                             [p[1] if p[0] % 2 == 1 else None
                              for p in enumerate(focusPoints)])
            focusPoints = zip(xCoords, yCoords)
            print "Computing function value for:", focusPoints

            #Snap to nearest grid coordinate
            for i in range(0,len(focusPoints)):
                focusPoint = focusPoints[i]
                focusPoints[i] = _coordGrids[getMazeName(zCoord)].queryGrid(focusPoint[0], focusPoint[1])

            predictedDensityDist, numOfSkippedFile = computeAreaDensity(
                                                      zCoord,
                                                      trainTags,
                                                      focusPoints,
                                                      testTimes)

            actualDensityDist = computeActualDensityDist(zCoord,
                                                         predictedDensityDist,
                                                         focusPoints,
                                                         testTags)
            error = calculateError(predictedDensityDist, actualDensityDist,
                                   numOfSkippedFile)

            if visualise:
                generateVisualisation(focusPoints, predictedDensityDist, 10, actualDensityDist) 

            print 'Error: ', str(error)
            rval[index, 0] = error

        print "Batch result:", rval
        return rval

    return optFunc

if __name__ == '__main__':
    testTimes = pd.read_csv('test_times.csv')

    tags = generatetest.listTags()[0:100]
    trainTags, testTags = generatetest.splitTags(tags, proportion=0.1)
    print 'Training Tags: ', trainTags
    print 'Test Tags: ', tags

    acquisition_par = 0.01
    max_iter = 5
    bounds = [(0, 100)] * 6
    optFunc = makeOptFunc(testTimes, trainTags, tags, visualise=True)


    bOpt = GPyOpt.methods.BayesianOptimization(optFunc,
                                               bounds=bounds,
                                               acquisition='LCB',
                                               acquisition_par=acquisition_par)

    bOpt.run_optimization(max_iter,
                          acqu_optimize_method = 'fast_random',
                          acqu_optimize_restarts = 10,
                          eps=10e-6)
    print bOpt.x_opt
    print bOpt.fx_opt

