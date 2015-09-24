from scipy import integrate
import numpy as np

def circleIntegrate(cx, cy, r, f):
    yTop = lambda x : cy + (r*r - (x - cx)*(x - cx))**0.5
    yBot = lambda x : cy - (r*r - (x - cx)*(x - cx))**0.5

    res, err = integrate.dblquad(f, cx - r, cy + r, yBot, yTop)
    print 'Result: ' + str(res)
    print 'Error: ' + str(err)
    
def cylinderIntegrate(cx, cy, r, zMin, zMax, f):
    yTop = lambda x : cy + (r*r - (x - cx)*(x - cx))**0.5
    yBot = lambda x : cy - (r*r - (x - cx)*(x - cx))**0.5
    zTop = lambda x, y : zMax
    zBot = lambda x, y : zMin
    
    res, err = integrate.tplquad(f, cx - r, cy + r, yBot, yTop, zBot, zTop)
    print 'Result: ' + str(res)
    print 'Error: ' + str(err)


def f(x,y,z):
    return 1
cylinderIntegrate(0,0,1,-1,1,f)