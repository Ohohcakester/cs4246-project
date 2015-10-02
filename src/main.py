import pandas as pd
import numpy as np
import GPy
from matplotlib import pyplot as plt
import climin
import os

def SVGP(X, Y):
    if Y.ndim != 2:
        Y = Y[:, None]

    Z = np.random.rand(20, 1)
    batchsize = 300
    m = GPy.core.SVGP(X, Y, Z,
                      GPy.kern.RBF(1) + GPy.kern.White(1),
                      GPy.likelihoods.Gaussian(), batchsize=batchsize)
    m.kern.white.variance = 1e-5
    m.kern.white.fix()

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

    kernel = GPy.kern.MLP(1) + GPy.kern.Bias(1)
    m = GPy.models.GPRegression(X, Y, kernel)
    m['.*Gaussian_noise'] = .05
    m['.*noise'].unconstrain()
    m['.*noise'].fix()
    m.optimize(messages=True, max_f_eval=1000)
    return m

def readData(filename):
    user = pd.read_csv(filename)

    X = np.array(user['SNAPSHOT_TIMESTAMP'])[:, None].astype(float)
    minTime = np.min(X)
    X -= minTime
    Y = np.array(user[['X', 'Y', 'Z']]).astype(float)

    return (X, Y, minTime)

def plot_graph(X, Y, m, dimension, targetFile):
    plt.figure()
    plt.plot(X, Y, 'bx', alpha=0.2)
    plt.xlabel('Time')
    plt.ylabel(dimension)
    plt.title(dimension + ' prediction with data')

    _ = m.plot(which_data_ycols=[0], plot_limits=(X.min(), X.max()))
    #plt.savefig('./fig/' + targetFile + '_' + dimension + '.png')
    plt.clf()
    #plt.show()

def run(X, Y, dimension, testTimes, targetFile):
    if (dimension == 'X'):
        col = 0
    elif (dimension == 'Y'):
        col = 1
    elif (dimension == 'Z'):
        col = 2

    m = GP(X, Y[:, col])
    #plot_graph(X, Y[:, col], m, dimension, targetFile)

    mu, var = m.predict(testTimes)

    return mu, var

def readTimes():
    times = pd.read_csv('test_times.csv')
    return np.array(times['TIME'])[:, None].astype(float)

times = readTimes()
files = os.listdir('data')
for targetFile in files[1:]:
    print targetFile
    X, Y, minTime = readData('data/' + targetFile)
    relativeTimes = times - minTime
    mu_X, var_X = run(X, Y, 'X', relativeTimes, targetFile)
    mu_Y, var_Y = run(X, Y, 'Y', relativeTimes, targetFile)
    mu_Z, var_Z = run(X, Y, 'Z', relativeTimes, targetFile)
    df = pd.DataFrame({'mu_X': mu_X.flatten(), 
                        'var_X': var_X.flatten(),
                        'mu_Y': mu_Y.flatten(),
                        'var_Y': var_Y.flatten(),
                        'mu_Z': mu_Z.flatten(),
                        'var_Z': var_Z.flatten()},
                        index = times.flatten().astype(int))
    df.to_csv('./stat/stat_' + targetFile)

