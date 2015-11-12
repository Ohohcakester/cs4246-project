import pandas as pd

import ast
import GPy
import sys

BASE_TIME = 1216375000

def regressGP(df):
    """
    Regress a GP with data in df.
    ---
    df: a DataFrame of ['TIMESTAMP', 'Z', SHORTEST_PATHS'].
        'SHORTEST_PATHS' should be a series of 3-tuples, each of which contains
        shortest distances to each of the 3 selected points.
    ---
    Return:
        A GPy model
    """

    y_cols = ['Y1', 'Y2', 'Y3']
    for n, col in enumerate(y_cols):
        df[col] = df['SHORTEST_PATHS'].apply(lambda paths: paths[n])
    df.drop('SHORTEST_PATHS', axis=1, inplace=True)

    X = df['TIMESTAMP'].values.reshape(-1, 1) - BASE_TIME
    Y = df[['Y1', 'Y2', 'Y3']].values.astype(float)

    kernel = GPy.kern.Exponential(1)
    m = GPy.models.GPRegression(X, Y, kernel)
    m['.*Gaussian_noise'] = 0.05
    m['.*noise'].unconstrain()
    m['.*noise'].fix()
    m.optimize(messages=True, max_f_eval=1000)

    m.plot(which_data_ycols=[0], plot_limits=(X.min(), X.max()))

    return m

def predictGP(df, testTimes):
    """
    Predict the mean and variance for each timestamp in a DataFrame, assuming
    that all data in the DataFrame is regressed in the same series
    ---
    df: a DataFrame of ['TIMESTAMP', 'SHORTEST_PATHS']. 'SHORTEST_PATH' should
        be a series of 3-tuples, each of which contain shortest distances to
        each of the 3 selected points.
    ---
    Return:
        A DataFrame of ['TIMESTAMP', 'Z', 'MU', 'VAR']
        'MU' and 'VAR' both contains series of 3-tuples
    """

    m = regressGP(df)

    mu, var = m.predict((testTimes['TIME'] - BASE_TIME).values.reshape(-1, 1))

    mu = map(tuple, mu)

    varlist = var.flatten().tolist()
    var = map(tuple, [[x]*3 for x in varlist])

    result_df = pd.DataFrame({'TIMESTAMP': testTimes['TIME'],
                              'MU': mu, 'VAR': var})
    return result_df


def predictGPonFile(fileName):
    df = pd.read_csv(fileName+'_A.csv', converters={"SHORTEST_PATHS": ast.literal_eval})
    testTimes = pd.read_csv(fileName+'_B.csv')
    result_df = predictGP(df, testTimes)
    result_df.to_csv(fileName+'_OUT.csv')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        predictGPonFile(sys.argv[1])
        quit()

    df = pd.read_csv('testGP.csv')
    testTimes = pd.read_csv('test_times.csv')
    df['SHORTEST_PATHS'] = df['SHORTEST_PATHS'].str.split(',')

    result = predictGP(df, testTimes)
    import computedensities
    densityDistribution = computedensities.compute('floor18map',
                                                   [(8,8), (89,60), (55,5)],
                                                   result)
    print densityDistribution

    #userID = df['USER'][0]
    #result = predictGP(df[df['USER'] == userID])

    #print result
