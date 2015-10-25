from collections import deque
from scipy.spatial import KDTree

# Usage: Create a new Grid object grid = Grid(mazeName)
# Then run grid.query(x,y) to get the closest unblocked coordinate on the grid.
# The input x,y follows the grid coordinate system, but allows floating points.

path = 'pathfinding/maze/'

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
        self.initialise()
        
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
        
    def query(self,x,y):
        return self.unblockedPoints[self.tree.query((x,y))[1]]



if __name__ == '__main__':
    grid = Grid('floor18map')
    import random
    #for i in range(0,100000): # test speed
    for i in range(0,5): # test correctness
        x = float(random.randrange(0,1000))/10
        y = float(random.randrange(0,1000))/10
        print str((x,y)) + ' ' + str(grid.query(x,y)) # test correctness
        #grid.query(x,y) # test speed