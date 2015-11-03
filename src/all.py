#!/usr/bin/python

import pandas as pd
import numpy as np

import generatetest

def calculateError():
	pass
	
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
	
def generateTestCases(focusPoints):
	"""
	Takes in the set of focus points read from file earlier and runs generatetest.py
	---
	focusPoints: list of focus points
				[(a, b), (c, d), (e, f)] where a through f are floats
	---
	Returns: dataframe with 3 additional columns of each row's shortest distance
			to the focus points in float
	"""
	tags = generatetest.listTags()[0:100]
	
	
if __name__ == '__main__':
	focusPoints = readFocusPoints('focuspoints.csv')
	df = generateTestCases(focusPoints)
	