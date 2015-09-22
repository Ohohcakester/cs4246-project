import pandas as pd 
import numpy as np
import GPy
from matplotlib import pyplot as plt
import climin

data = pd.read_csv('../data/trainingData.csv')
data_filtered = data[['USERID', 'LONGITUDE', 'LATITUDE', 'FLOOR', 'BUILDINGID', 'TIMESTAMP']]

first_user = data_filtered[data_filtered.USERID == 1]
first_user.drop('USERID', axis=1)

X = np.array(first_user['TIMESTAMP'][:, None]).astype(float)
Y = np.array(first_user[['LONGITUDE', 'LATITUDE', 'FLOOR']])

Z = np.random.rand(20, 1)
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

fig1 = plt.figure(num=1)
plt.plot(X, Y[:, 0], 'bx', alpha=0.2)
plt.xlabel('Time')
plt.ylabel('LONGITUDE')
plt.title('SVI LONGITUDE prediction with data')
_ = m.plot(which_data_ycols=[0], plot_limits=(X.min(), X.max()), fignum=1)
