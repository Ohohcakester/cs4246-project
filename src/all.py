#!/usr/bin/python

import pandas as pd
import numpy as np
import re

import generatetest
import bayes
import computedensities

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

	dfNew = dfNew.assign(SHORTEST_PATHS = map(lambda index: "" + str(df.iloc[index].d1) + ","
		+ str(df.iloc[index].d2) + "," + str(df.iloc[index].d3), range(0, len(df.index))))
	dfNew = dfNew.reset_index()

	return dfNew

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

	for user in uniqueUserID:
		userResult = bayes.predictGP(df[df['USER'] == user])
		result = pd.concat([result, userResult])

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
	return computedensities.compute(getMazeName(level), areas, df)

def calculateError(predictedDensityDist, actualDensityDist):
	"""
	Calculate Error from dataframe of densities
	---
	predictedDensityDist: dict {timestamp: densityDistribution}
				where densityDistribution defined in computedensities.py
	actualDensityDistribution: dict {timestamp: densityDistribution}
	---
	Returns: float error
	"""
	# Assuming now the timestamps are the same
	sum = 0.0
	count = 0.0

	zippedDensities = zip(predictedDensityDist.values(), actualDensityDist.values())

	for pair in zippedDensities:
		pairPredictedDensity = pair[0]
		pairActualDensity = pair[1]

		predictedDensityKeys = set(pairPredictedDensity.getPoints())
		actualDensityKeys = set(pairActualDensity.getPoints())

		# If keys in intersection, just compute difference
		for point in predictedDensityKeys.intersection(actualDensityKeys):
			sum += (predictedDensityDist.query(point) - actualDensityDist.query(point)) ** 2
			count += 1

		# For keys that are in actual but not in predicted, add error
		for point in (actualDensityKeys - predictedDensityKeys):
			sum += actualDensityDist ** 2
			count += 1

		# For keys in predicted not in actual, ignore

	return np.sqrt(sum/count)

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

	# Note: BayesResult returns some non-positive definite error
	densityDist = computeDensity(df, areas, level=1)

if __name__ == '__main__':
	focusPoints = readPointFile('focuspoints.csv')
	areas = readPointFile('areas.csv')

	tags = generatetest.listTags()[0:100]
	testTags, trainTags = generatetest.splitTags(tags, proportion=0.5)

	predictedDensityDist = computeAreaDensity(trainTags, focusPoints, areas)

	actualDensityDist = computeAreaDensity(testTags, focusPoints, areas)

	calculateError(predictedDensityDist, actualDensityDist)
