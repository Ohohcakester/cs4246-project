import os

targetDir = 'densityrenders/'

def makeDirs():
    try: os.mkdir(targetDir)
    except: pass

def generateFileName(focusPoints):
    dashjoin = lambda l : '-'.join(map(str, l))
    return '_'.join(map(dashjoin,focusPoints))


def generateTextFile(fileName, predictedDensityDist, scaleRatio, actualDensityDist):
    sb = []
    sb.append('PREDICTED')
    if set(predictedDensityDist.keys()) != set(actualDensityDist.keys()):
        print 'ERROR: TIMESTAMPS DO NOT MATCH'

    for timestamp in predictedDensityDist.keys():
        predicted = predictedDensityDist[timestamp]
        actual = actualDensityDist[timestamp]

        if set(predicted.getPoints()) != set(actual.getPoints()):
            print 'ERROR: POINTS DO NOT MATCH'

        sb.append('>>> ' + str(timestamp))
        for point in predicted.getPoints():
            predictedDensity = predicted.query(point) * scaleRatio
            actualDensity = actual.query(point)
            sb.append(str(point) + ' : ' + str((predictedDensity, actualDensity)))

    f = open(targetDir + fileName + '.txt', 'w+')
    f.write('\n'.join(sb))
    f.close()


def renderDensityFile(fileName, predictedDensityDist, scaleRatio, actualDensityDist):
    from PIL import Image, ImageDraw
    import os
    class Drawer(object):
        def __init__(self, tile_size, name, x_tiles, y_tiles):
            self.tile_size = tile_size
            resX = x_tiles * self.tile_size
            resY = y_tiles * self.tile_size

            self.im = Image.new('RGB', (resX, resY), (0,0,0))
            self.draw = ImageDraw.Draw(self.im)
            self.name = name

        def drawSquare(self,x,y,colour):
            x1 = self.tile_size*x
            y1 = self.tile_size*y
            x2 = x1+self.tile_size
            y2 = y1+self.tile_size
            self.draw.rectangle((x1,y1,x2-1,y2-1),colour)

        def render(self):
            self.im.save(targetDir+self.name+'.png', 'PNG')

        def open(self):
            os.startfile(targetDir+self.name+'.png')

    def densityToColour(density):
        density *= 10
        return (min(int(density*255),255), min(int((1-density)*255),255), 0)

    if set(predictedDensityDist.keys()) != set(actualDensityDist.keys()):
        print 'ERROR: TIMESTAMPS DO NOT MATCH'

    for timestamp in predictedDensityDist.keys():
        predicted = predictedDensityDist[timestamp]
        actual = actualDensityDist[timestamp]

        if set(predicted.getPoints()) != set(actual.getPoints()):
            print 'ERROR: POINTS DO NOT MATCH'

        maxX = max(map(lambda t : t[0], predicted.getPoints()))
        maxY = max(map(lambda t : t[1], predicted.getPoints()))
        drawPredicted = Drawer(5, fileName +'_'+ str(timestamp) + '_predicted', maxX+5, maxY+5)
        drawActual = Drawer(5, fileName +'_'+ str(timestamp) + '_actual', maxX+5, maxY+5)

        for point in predicted.getPoints():
            #print point
            predictedDensity = predicted.query(point) * scaleRatio
            drawPredicted.drawSquare(point[0],point[1], densityToColour(predictedDensity))

            actualDensity = actual.query(point)
            drawActual.drawSquare(point[0],point[1], densityToColour(actualDensity))

        drawPredicted.render()
        drawActual.render()


def drawRegions(regions):
    maxX = max(map(lambda t : t[0], regions.keys()))
    maxY = max(map(lambda t : t[1], regions.keys()))

    from PIL import Image, ImageDraw
    import os
    class Drawer(object):
        def __init__(self, tile_size, name, x_tiles, y_tiles):
            self.tile_size = tile_size
            resX = x_tiles * self.tile_size
            resY = y_tiles * self.tile_size

            self.im = Image.new('RGB', (resX, resY), (0,0,0))
            self.draw = ImageDraw.Draw(self.im)
            self.name = name

        def drawSquare(self,x,y,colour):
            x1 = self.tile_size*x
            y1 = self.tile_size*y
            x2 = x1+self.tile_size
            y2 = y1+self.tile_size
            self.draw.rectangle((x1,y1,x2,y2),colour)

        def render(self):
            self.im.save(targetDir+self.name+'.png', 'PNG')

        def open(self):
            os.startfile(targetDir+self.name+'.png')

    draw = Drawer(5, 'labelledregions', maxX+5, maxY+5)
    for point in regions:
        region = regions[point]
        increment = 196/nDivisions
        if len(region) == 3:
            draw.drawSquare(point[0],point[1], (63 + increment*region[0],63 + increment*region[1], 63 + increment*region[2]))
        else:
            draw.drawSquare(point[0],point[1], (0,63 + increment*region[0],63 + increment*region[1]))

    draw.render()
    draw.open()


def run(fileName, predictedDensityDist, scaleRatio, actualDensityDist):
    makeDirs()
    generateTextFile(fileName, predictedDensityDist, scaleRatio, actualDensityDist)
    renderDensityFile(fileName, predictedDensityDist, scaleRatio, actualDensityDist)
    



if __name__ == '__main__':
    # Generate test density dist
    import computedensities
    #regions: dict {point -> region index}
    #densities: dict {region index -> density}
    regions = {(3,3): 0, (3,4): 1, (4,3): 1, (5,3): 1, (5,4): 2, (4,4): 2, (4,5): 3}
    
    densities = {0: 0.01, 1: 0.02, 2: 0.03, 3: 0.04}
    dtbn1a = computedensities.DensityDistribution(regions, densities)
    
    densities = {0: 0.04, 1: 0.03, 2: 0.02, 3: 0.08}
    dtbn1b = computedensities.DensityDistribution(regions, densities)

    predictedDensityDist = {1011: dtbn1a, 1035: dtbn1b}


    scaleRatio = 10


    densities = {0: 0.6, 1: 0.4, 2: 0.6, 3: 0.4}
    dtbn2a = computedensities.DensityDistribution(regions, densities)
    
    densities = {0: 0.7, 1: 0.4, 2: 0.2, 3: 0}
    dtbn2b = computedensities.DensityDistribution(regions, densities)

    actualDensityDist = {1011: dtbn2a, 1035: dtbn2b}

    focusPoints = [(0,0),(0,1000),(1000,0)]
    fileName = generateFileName(focusPoints)
    run(fileName, predictedDensityDist, scaleRatio, actualDensityDist)