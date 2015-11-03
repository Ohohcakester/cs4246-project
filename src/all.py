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

def readFocusPoints(filename):
	"""
	Reads in focus points from a file and returns the points as tuples in a list
	
	Can be changed such that each line is a set of focus points
	---
	filename: string
			focus points formatted as (a, b), (c, d), (e, f)
	---
	Returns: list of focus points
			[(a, b), (c, d), (e, f)] where a through f are floats
	"""
	file = open(filename, 'r')
	fileContents = file.read()
	m = re.findall('\(.*?\)', fileContents)
	
	focusPointsList = []
	
	for group in m:
		group = group.replace('(', '')
		group = group.replace(')', '')
		groupArr = [float(x) for x in group.split(',')]
		focusPointsList.append((groupArr[0], groupArr[1]))
	
	return focusPointsList
	
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
        A DataFrame of ['TIMESTAMPE', 'MU', 'VAR']
        'MU' and 'VAR' both contains series of 3-tuples
	"""
	df['SHORTEST_PATHS'] = df['SHORTEST_PATHS'].str.split(',')
	uniqueUserID = df['USER'].unique()
	# TODO: Iterate through the list and predict 
	
	userID = df['USER'][1]
	df[df['USER']==userID].to_csv('testuser.csv', index=None)

	result = bayes.predictGP(df[df['USER'] == userID])
	return result
	
def computeDensity(df, level=1, areas):
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
	Returns: Not sure yet
	"""
	computedensities.compute(getMazeName(level), areas, df)
	
def calculateError():
	"""
	Calculate Error from dataframe of densities
	---
	---
	Returns: float error
	"""
	pass	
	
if __name__ == '__main__':
	focusPoints = readFocusPoints('focuspoints.csv')
	tags = generatetest.listTags()
	testTags, trainTags = generatetest.splitTags(tags, proportion=0.5)
	
	dfFloor18 = generateTestCases(focusPoints, trainTags, level=1)
	
	dfFormattedFloor18 = formatDf(dfFloor18)
	bayesResult = runBayes(dfFormattedFloor18)
	
	# Can also let areas be read in from file
	#computeDensity(df, level=1, areas)