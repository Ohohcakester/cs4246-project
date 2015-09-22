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
    kernel = GPy.kern.RBF(1, 4, 0.2)
    m = GPy.models.GPRegression(X, Y, kernel)
    m.optimize(messages=True, max_f_eval=1000)
    return m

def splitData():
    data = pd.read_csv('../data/position_snapshot.csv')
    data = data.dropna()

    first_user = data[data.TAG_ID == 3994]
    first_user.to_csv('first_user.csv', index=None)

def timestampToMs(timestamp):
    return int(pd.to_datetime(timestamp).strftime("%s")) * 1000

def readData(filename):
    user = pd.read_csv(filename)

    converted = user['SNAPSHOT_TIMESTAMP'].apply(timestampToMs)
    X = np.array(converted)[:, None].astype(float)
    X -= np.min(X)
    Y = np.array(user[['X', 'Y', 'Z']]).astype(float)

    return (X, Y)


X, Y = readData('first_user.csv')

fig1 = plt.figure(num=1)
plt.plot(X, Y[:, 0], 'bx', alpha=0.2)
plt.xlabel('Time')
plt.ylabel('X')
plt.title('X prediction with data')

#m = GP(X, Y[:, 1])
#_ = m.plot(which_data_ycols=[0], plot_limits=(X.min(), X.max()), fignum=1)
