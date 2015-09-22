#!/usr/bin/python

import pandas as pd 
import numpy as np
import GPy
from matplotlib import pyplot as plt
import climin

import sys

data = pd.read_csv('data/trainingData.csv')
data_filtered = data[['USERID', 'LONGTITUDE', 'LATITUDE', 'FLOOR', 'BUILDINGID', 'TIMESTAMP']]

first_user = data_filtered[data_filtered.USERID == 1]
first_user.drop('USERID', axis=1)

X = np.arrayfirst_user['TIMESTAMP'])[:, None]
Y = np.array(first_user[['LONGTITUDE', 'LATITUDE', 'FLOOR']])
Y_1d = np.transpose(Y[:0])

Z = np.random.rand(20,1)

batchsize = 10
m = GPy.core.SVGP(X, Y, Z, GPy.kern.RBF(1) + GPy.kern.White(1), GPy.likelihoods.Gaussian(), batchsize=batchsize)
m.kern.white.variance = 1e-5
m.kern.white.fix()


opt = climin.Adadelta(m.optimizer_array, m.stochastic_grad, step_rate=0.2, momentum=0.9)
def callback(i):
    print m.log_likelihood(), "\r",
    #Stop after 5000 iterations
    if i['n_iter'] > 5000:
        return True
    return False
info = opt.minimize_until(callback)

