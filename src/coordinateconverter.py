from collections import deque
from scipy.spatial import KDTree

# Usage: Create a new Grid object grid = Grid(mazeName)
#
# Then run grid.queryActual(rx,ry) to get the closest unblocked coordinate on the grid.
# The input rx,ry follows the dataset's coordinate system, within [-0.9,0.7]x[-0.7x0.7]
#
# Alternatively run grid.queryGrid(x,y) to get the closest unblocked coordinate on the grid.
# The input x,y follows the grid coordinate system, but allows floating points.

path = 'pathfinding/maze/'

baseCoordinates = {
'floor2map': (8,3),
'floor18map': (3,2),
}

def readRow(rowstr):
    row = map(int, rowstr.split())
    return list(map(lambda v : v != 0, row))

def readMaze(mazeName):
    f = open(path + mazeName + '.txt')
    s = f.read().split('\n')
    f.close()
    w,h = tuple(map(int,s[0].split(' ')))
    rows = list(map(readRow, s[1:]))
    return w,h,rows

class Grid(object):

    def __init__(self, mazeName):
        self.mazeName = mazeName
        self.w,self.h,self.blocked = readMaze(mazeName)
        self.baseX, self.baseY = self.getBasePosition(mazeName)
        self.initialise()

    def getBasePosition(self, mazeName):
        return baseCoordinates[mazeName]

    def outOfBounds(self,x,y):
        return x < 0 or y < 0 or x >= self.w or y >= self.h

    def onBorder(self,(x,y)):
        hasUnblocked = False
        hasBlocked = False
        for j in range(y-1,y+1):
            for i in range(x-1,x+1):
                if self.outOfBounds(i,j): continue
                if self.blocked[j][i]: hasBlocked = True
                else: hasUnblocked = True
        return hasUnblocked and hasBlocked

    def unblocked(self,(x,y)):
        for j in range(y-1,y+1):
            for i in range(x-1,x+1):
                if self.outOfBounds(i,j): continue
                if self.blocked[j][i]: continue
                return True
        return False

    def initialise(self):
        coords = [(x,y) for y in range(0,self.w+1) for x in range(0,self.h+1)]
        self.unblockedPoints = list(filter(self.unblocked, coords))
        #self.borderpoints = list(filter(self.onBorder, coords))
        self.tree = KDTree(self.unblockedPoints)

    def queryGrid(self,x,y):
        return self.unblockedPoints[self.tree.query((x,y))[1]]

    def queryActual(self,rx,ry):
        gx = (rx+0.9)*111/1.6 - self.baseX
        gy = (rx+0.7)*97/1.4 - self.baseY
        return self.queryGrid(gx,gy)



if __name__ == '__main__':
    grid = Grid('floor2map')
    import random
    #for i in range(0,100000): # test speed
    for i in range(0,5): # test correctness
        #x = float(random.randrange(0,1000))/10
        #y = float(random.randrange(0,1000))/10
        #print str((x,y)) + ' ' + str(grid.queryGrid(x,y)) # test correctness

        x = float(random.randrange(0,1600))/1000 - 0.9
        y = float(random.randrange(0,1400))/1000 - 0.7
        print str((x,y)) + ' ' + str(grid.queryActual(x,y)) # test correctness
        #grid.queryActual(x,y) # test speed
