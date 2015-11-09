import pathfind
import integrate

nDivisions = 5 # all divisions are 5.

class DensityDistribution(object):
    def __init__(self, regions, densities):
        #regions: dict {point -> region index}
        #densities: dict {region index -> density}
        self.densities = {}
        for point in regions.keys():
            self.densities[point] = densities[regions[point]]

    def query(self, point):
        #Throws an error if the point does not exist in the density map.
        return self.densities[point]

    def getPoints(self):
        return self.densities.keys()
        
    def setPoint(self, point, value):
        # Sets a point 
        self.densities[point] = value
    

def drawRegions(regions):
    maxX = max(map(lambda t : t[0], regions.keys()))
    maxY = max(map(lambda t : t[1], regions.keys()))

    from PIL import Image, ImageDraw
    import os
    target_folder = 'test_display/'
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
            try: os.mkdir(target_folder)
            except: pass
            self.im.save(target_folder+self.name+'.png', 'PNG')

        def open(self):
            os.startfile(target_folder+self.name+'.png')

    draw = Drawer(5, 'labelledregions', maxX+5, maxY+5)
    for point in regions:
        region = regions[point]
        increment = 196/nDivisions
        if len(region) == 3:
            draw.drawSquare(point[0],point[1], (63 + increment*region[0],63 + increment*region[1], 63 + increment*region[2]))
        else:
            draw.drawSquare(point[0],point[1], (0,63 + increment*region[0],63 + increment*region[1]))

    draw.render()


class DistanceMap(object):

    #input is in tuples (x,y,distance)
    def __init__(self, output):
        self.points = dict(( (x[0],x[1]), x[2] ) for x in output)
        self.maxValue = max(self.points.values())
        self.minValue = min(self.points.values())
        self.division = (self.maxValue - self.minValue) / nDivisions

    def classify(self, point):
        a = int((self.points[point] - self.minValue)/self.division)
        if a < 0: return 0
        if a >= nDivisions: return nDivisions-1
        return a

    def clearPoints(self):
        self.points = None

    def getBounds(self, index):
        left = self.minValue + self.division*index
        return (left, left + self.division)

    def classifyValue(self, v):
        a = int((v - self.minValue)/self.division)
        if a < 0: return 0
        if a >= nDivisions: return nDivisions-1
        return a


def classifyAreas(mazeName, points):
    outputs = pathfind.runSingleSourceAllDestinations(mazeName, points)
    distanceMaps = list(map(lambda x: DistanceMap(x), outputs))

    points = distanceMaps[0].points.keys()
    # a point is a tuple (x,y). A region is a tuple of indexes 0 to nDivisions-1.
    regions = {} # Indicates the region for each point.
    regionCounts = {} # indicates the number of points in each region.
    for point in points:
        region = tuple(map(lambda dm : dm.classify(point), distanceMaps))
        regions[point] = region
        if region in regionCounts:
            regionCounts[region] += 1
        else:
            regionCounts[region] = 1

    for distanceMap in distanceMaps:
        distanceMap.clearPoints()

    return regions, regionCounts, distanceMaps

def classifyAndDrawAreas(mazeName, points):
    regions, regionCounts, distanceMaps = classifyAreas(mazeName, points)
    print "Number of Regions: ", len(regionCounts)
    drawRegions(regions)

# distributions is a list of probability density functions.
def getRegionDensities(regions, regionCounts, distanceMaps, muVar):
    densities = {}
    for region in regionCounts.keys():
        bounds = tuple([dm.getBounds(index) for index, dm in zip(region,distanceMaps)])
        density = sum(map(integGaussian(bounds), muVar)) / regionCounts[region] #regionCounts is the approximate area
        densities[region] = density
    return DensityDistribution(regions, densities)

def integ(bounds):
    def fun(distribution):
        res, err = integrate.tripleRectIntegrate(bounds, distribution)
        return res
    return fun

def integGaussian(bounds):
    def fun(muVar):
        res = integrate.tripleRectIntegrate2(bounds, muVar[0], muVar[1])
        return res
    return fun

"""
Input: Maze Name (string), tuple of reference points, dataframe['MU','TIMESTAMP','VAR']
Output: A dictionary {timestamp -> DensityDistribution}

A DensityDistribution object (defined above) allows you to query the density at any grid point on the map.
"""
def compute(mazeName, points, df, quiet=False):
    # build dictionary timestamp -> mu, var
    # one user, one entry
    muVars = {}
    keys = tuple(df)
    index_timestamp = keys.index('TIMESTAMP')
    index_mu = keys.index('MU')
    index_var = keys.index('VAR')
    for row in df.iterrows():
        mus = row[1][index_mu]
        vars = row[1][index_var]
        muVar = (mus, vars)
        #f = integrate.multivariateIndepGaussian(mus[0],mus[1],mus[2],vars[0],vars[1],vars[2])
        timestamp = row[1][index_timestamp]
        if timestamp in muVars:
            muVars[timestamp].append(muVar)
        else:
            muVars[timestamp] = [muVar]

    #confirm lengths are the same
    nUsers = None
    for key in muVars:
        length = len(muVars[key])
        if nUsers == None:
            nUsers = length
        elif nUsers != length:
            print "computedensities.py: ERROR: Number of users not consistent"

    if not quiet:
        print 'Classifying map into regions'

    # Classify areas into regions
    regions, regionCounts, distanceMaps = classifyAreas(mazeName, points)

    if not quiet:
        print 'Number of regions: ' + str(len(regionCounts))
        print 'Computing density: ' + str(nUsers) + ' users'

    # Compute density map for each timestamp
    densityDistributions = {}
    for timestamp in muVars:
        if not quiet:
            print 'Computing for timestamp: ' + str(timestamp)
        densityDistributions[timestamp] = getRegionDensities(regions, regionCounts, distanceMaps, muVars[timestamp])

    if not quiet:
        print 'Finished computing densities'

    # return dict {timestamp -> density map}
    return densityDistributions



if __name__ == '__main__':
    classifyAreas('floor18map', [(8,8), (89,60), (55,5)])

