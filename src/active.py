import pandas as pd
import numpy as np
import GPy
import GPyOpt
from scipy.stats import norm
from matplotlib import pyplot as plt

#import signal

def myf(x, acquisition_par=0.01):
    fest = m.predict(x)
    acqu = norm.cdf((fest[0] - max(fest[0]) - acquisition_par) / fest[1])
    return acqu

user = pd.read_csv('data/3006.csv')
X = np.array(user['SNAPSHOT_TIMESTAMP'])[:, None].astype(int)
minTime = np.min(X)
X -= minTime
Y = np.array(user[['X', 'Y', 'Z']]).astype(int)
Y_xdim = Y[:, 0]

Y_xdim = Y_xdim[:, None]

bounds = [(X.min(), X.max())]
kernel = GPy.kern.MLP(1) + GPy.kern.Bias(1)
m = GPy.models.GPRegression(X, Y_xdim, kernel)
acquisition_par = 0.01
myBopt = GPyOpt.methods.BayesianOptimization(f=myf,
                                             bounds=bounds,
                                             acquisition='EI',
                                             acquisition_par=acquisition_par)

max_iter = 15
myBopt.run_optimization(max_iter,
                        acqu_optimize_method = 'fast_random',
                        acqu_optimize_restarts = 30,
                        eps=10e-6)
print myBopt.x_opt
print myBopt.fx_opt

figure = plt.figure()
sorted_x = np.sort(X, 0)
myfy = myf(sorted_x)

opt_x = np.max(myBopt.x_opt)
max_x = np.max(sorted_x)
min_myfy = np.min(myfy)
max_myfy = np.max(myfy)

plt.plot(sorted_x, myfy)
plt.axis([0, max_x, min_myfy, max_myfy])
plt.plot((opt_x, opt_x), (min_myfy, max_myfy), linewidth=2, color='red')

"""
class TimeoutError(Exception):
    pass

class timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message
    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)
    def __exit__(self, type, value, traceback):
        signal.alarm(0)

with timeout(seconds=10):
    myBopt.plot_acquisition()
"""
