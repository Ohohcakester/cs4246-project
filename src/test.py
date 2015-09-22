import pandas as pd
import numpy as np
import GPy
from matplotlib import pyplot as plt
import climin

def SVGP(X, Y):
    if Y.ndim != 2:
        Y = Y[:, None]
    Z = np.random.rand(20, 1)
    batchsize = 20
    m = GPy.core.SVGP(X, Y, Z,
            GPy.kern.Matern52(1),
            GPy.likelihoods.Gaussian(), batchsize=batchsize)
    #m.kern.white.variance = 1e-5
    #m.kern.white.fix()

    opt = climin.Adadelta(m.optimizer_array,
            m.stochastic_grad,
            step_rate=0.2, momentum=0.9)
    def callback(i):
        print m.log_likelihood(), "\r",
        if i['n_iter'] > 5000:
            return True
        return False

    info = opt.minimize_until(callback)
    print info

    return m

def GP(X, Y):
    if Y.ndim != 2:
        Y = Y[:, None]
    kernel = GPy.kern.RBF(1, 4, 0.2)
    m = GPy.models.GPRegression(X, Y, kernel)
    m.optimize(messages=True, max_f_eval=1000)
    return m

def splitData():
    data = pd.read_csv('../data/trainingData.csv')
    data_filtered = data[['USERID', 'LONGITUDE', 'LATITUDE', 'FLOOR', 'BUILDINGID', 'TIMESTAMP']]

    first_user = data_filtered[data_filtered.USERID == 2]
    #first_user = first_user[first_user.TIMESTAMP <= 1370900000]
    first_user.drop('USERID', axis=1)

    first_user.to_csv('second_user.csv', index=None)
    
def readData(filename):
    user = pd.read_csv(filename)

    X = np.array(user['TIMESTAMP'][:, None]).astype(float)
    X -= np.min(X)
    Y = np.array(user[['LONGITUDE', 'LATITUDE']])

    return (X, Y)


X, Y = readData('second_user.csv')

'''
N = len(X)
Y1 = np.sin(6*X) + 0.1*np.random.randn(N, 1)
Y2 = np.sin(3*X) + 0.1*np.random.randn(N, 1)
Y = np.hstack((Y1, Y2))
'''

fig1 = plt.figure(num=1)
plt.plot(X, Y[:, 1], 'bx', alpha=0.2)
plt.xlabel('Time')
plt.ylabel('LONGITUDE')
plt.title('SVI LONGITUDE prediction with data')

m = GP(X, Y[:, 1])
_ = m.plot(which_data_ycols=[0], plot_limits=(X.min(), X.max()), fignum=1)
