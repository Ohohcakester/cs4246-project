import os
import random

def getUnanalysedFiles():
	statsFiles = os.listdir('stat/')
	dataFiles = set(os.listdir('data/'))

	trimHead = lambda s : s[s.find('_')+1:]
	statsFiles = set(map(trimHead,statsFiles))

	unanalysedFiles = list(dataFiles - statsFiles)
	random.shuffle(unanalysedFiles)

	return unanalysedFiles

if __name__ == '__main__':
	analysed = len(os.listdir('stat/'))
	unanalysed = len(getUnanalysedFiles())
	print 'analysed: ' + str(analysed)
	print 'unanalysed: ' + str(unanalysed)
	print 'percentage: ' + str(analysed/float(unanalysed))
