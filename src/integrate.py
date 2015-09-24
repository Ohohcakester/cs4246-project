from scipy import integrate
import numpy as np

# f is a function (probability distribution) of x, y.
# Finds area under a circle at (cx,cy), radius r.
def circleIntegrate(cx, cy, r, f):
    yTop = lambda x : cy + (r*r - (x - cx)*(x - cx))**0.5
    yBot = lambda x : cy - (r*r - (x - cx)*(x - cx))**0.5

    res, err = integrate.dblquad(f, cx - r, cy + r, yBot, yTop)
    print 'Result: ' + str(res)
    print 'Error: ' + str(err)

# f is a function (probability distribution) of x, y, z.
# Integrates over a cylinder at (cx,cy), radius r, from z = zMin to z = zMax
def cylinderIntegrate(cx, cy, r, zMin, zMax, f):
    yTop = lambda x : cy + (r*r - (x - cx)*(x - cx))**0.5
    yBot = lambda x : cy - (r*r - (x - cx)*(x - cx))**0.5
    zTop = lambda x, y : zMax
    zBot = lambda x, y : zMin
    
    res, err = integrate.tplquad(f, cx - r, cy + r, yBot, yTop, zBot, zTop)
    print 'Result: ' + str(res)
    print 'Error: ' + str(err)


def multivariateGaussian(mean_x, mean_y, mean_z, cov_matrix):
    inv_matrix = np.linalg.inv(cov_matrix)
    det = np.linalg.det(cov_matrix)
    const = 1 / (((2*np.pi)**3 * det)**0.5)
    def f(x,y,z):
        v = np.array([[x-mean_x],[y-mean_y],[z-mean_z]])
        return const*np.exp(-0.5*np.dot(np.transpose(v),np.dot(inv_matrix,v)))
    return f
    
# Testing code
if __name__ == '__main__':
    f = multivariateGaussian(0,0,0,np.array([[1,0,0],[0,1,0],[0,0,0.001]]))
    cylinderIntegrate(0,0,10,-1,1,f)