import pandas as pd

import GPy

def regressGP(df):
    """
    Regress a GP with data in df.
    ---
    df: a DataFrame of ['TIMESTAMP', 'SHORTEST_PATHS']. 'SHORTEST_PATH' should
        be a series of 3-tuples, each of which contain shortest distances to
        each of the 3 selected points.
    ---
    Return:
        A GPy model
    """

    y_cols = ['Y1', 'Y2', 'Y3']
    for n, col in enumerate(y_cols):
        df[col] = df['SHORTEST_PATHS'].apply(lambda paths: paths[n])
    df.drop('SHORTEST_PATHS', axis=1, inplace=True)

    X = df['TIMESTAMP'].values.reshape(-1, 1)
    Y = df[['Y1', 'Y2', 'Y3']].values.astype(float)

    kernel = GPy.kern.MLP(1) + GPy.kern.Bias(1)
    m = GPy.models.GPRegression(X, Y, kernel)
    m['.*Gaussian_noise'] = 0.05
    m['.*noise'].unconstrain()
    m['.*noise'].fix()
    m.optimize(messages=True, max_f_eval=1000)

    return m

def predictGP(df):
    """
    Predict the mean and variance for each timestamp in a DataFrame, assuming
    that all data in the DataFrame is regressed in the same series
    ---
    df: a DataFrame of ['TIMESTAMP', 'SHORTEST_PATHS']. 'SHORTEST_PATH' should
        be a series of 3-tuples, each of which contain shortest distances to
        each of the 3 selected points.
    ---
    Return:
        A DataFrame of ['TIMESTAMPE', 'MU', 'VAR']
        'MU' and 'VAR' both contains series of 3-tuples
    """
    m = regressGP(df)
    mu, var = m.predict(df['TIMESTAMP'].values.reshape(-1, 1))

    mu = map(tuple, mu)
    var = map(tuple, var)

    result_df = pd.DataFrame({'TIMESTAMP': df['TIMESTAMP'],
                              'MU': mu, 'VAR': var})
    return result_df

if __name__ == '__main__':
    df = pd.read_csv('testGP.csv')
    df['SHORTEST_PATHS'] = df['SHORTEST_PATHS'].str.split(',')

    userID = df['USER'][0]
    result = predictGP(df[df['USER'] == userID])

    print result
