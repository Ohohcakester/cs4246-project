import os

targetDir = 'densityrenders/'

def makeDirs():
    try: os.mkdir(targetDir)
    except: pass

def generateTextFile(predictedDensityDist, scaleRatio, actualDensityDist):
    pass

def renderDensityFile(fileName):
    pass

def run(predictedDensityDist, scaleRatio, actualDensityDist):
    makeDirs()
    fileName = generateTextFile(predictedDensityDist, scaleRatio, actualDensityDist)
    renderDensityFile(fileName)
    



if __name__ == '__main__':
    # Generate test density dist
    import computedensities
