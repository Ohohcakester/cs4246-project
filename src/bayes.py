import pandas as pd
import numpy as np

import GPy

import os

'''
Make the GP part take in a dataframe of [timestamp, user, shortest path] and return a dict of { timestamp: dataframe of [user, mean, var] }
'''

def GP(X, Y):
    if Y.ndim != 2:
        Y = Y[:, None]

    kernel = GPy.kern.MLP(1) + GPy.kern.Bias(1)
    m = GPy.models.GPRegression(X, Y, kernel)
    m['.*Gaussian_noise'] = 0.05
    m['.*noise'].unconstrain()
    m['.*noise'].fix()
    m.optimize(messages=True, max_f_eval=1000)
    return m

def run(df):
    m = GP(df['timestamp'], df['shortest_path'])
    mu, var = m.predict(df['timestamp'])

if __name__ == '__main__':
    # Currently assume data formatted already
    df = pd.read_csv('paths.csv')
    mu, var = run(df) 
    df_new = pd.DataFrame({'user': df['user'],
                            'mu': mu.flatten(),
                            'var': var.flatten()})
    userID = df['user'][0]
    newframe = {userID: df_new}
