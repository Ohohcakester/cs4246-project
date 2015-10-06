import pandas
import integrate
import os

def loadDensities():
    return pandas.read_csv('true_densities.csv')

def loadDistributions():
    files = os.listdir('stat/')
    distributions = {}
    for fileName in files:
        data = pandas.read_csv('stat/' + fileName, index_col=0)
        data['tag']  = fileName[:-4]
        data.index = data.index.set_names('timestamp', level=None)
        distributions[fileName[5:-4]] = data
    return distributions

def getExpectedOne(meanX, meanY, meanZ, varX, varY, varZ, x, y, z):
    radius =0.1
    distribution = integrate.multivariateIndepGaussian(meanX, meanY, meanZ, varX, varY, varZ)
    cx = -0.8 + 0.2 * x
    cy = -0.6 + 0.2 * y
    
    if z == 0:
        zMin = -0.6
        zMax = 0.6
    else:
        zMin = 0.6
        zMax = 1.8
    

    (result, error) = integrate.boxIntegrate(cx, cy, radius, zMin, zMax, distribution)
    return result

def getExpectedAll(distributions, timestamp, x, y, z):
    def integrateOne(dataRow):
        return getExpectedOne(dataRow['mu_X'], dataRow['mu_Y'], dataRow['mu_Z'],
                dataRow['var_X'], dataRow['var_Y'], dataRow['var_Z'],
                x, y, z)
    result = 0
    for key in distributions:
        distribution = distributions[key]
        filteredDistribution = distribution[distribution.index == timestamp]
        result += filteredDistribution.apply(integrateOne, axis=1).sum()
    return result

def difference(amount1, amount2):
    pass

def evaluate():
    densities = loadDensities()
    distributions = loadDistributions()
    densities.sort(columns=['timestamp'], inplace=True)

    densities.set_index(keys=['timestamp'], drop=False, inplace=True)

    timestamps = densities['timestamp'].unique().tolist()

    def evaluateOne(densityRow):
        predicted = 0
        if (True):
            filename = 'predicted/' + str(densityRow['timestamp']) + ' ' + str(densityRow['x_index']) + ' ' + str(densityRow['y_index']) + ' ' + str(densityRow['z_index'])+ '.csv'
            if (os.path.exists(filename)):
                result = pandas.read_csv(filename).transpose()
                return pandas.Series({'timestamp': result[1][1],
                        'x_index': result[2][1],
                        'y_index': result[3][1],
                        'z_index': result[4][1],
                        'predicted': result.index[1],
                        'real': result[0][1]})
            else:

                predicted = getExpectedAll(distributions,
                        densityRow['timestamp'],
                        densityRow['x_index'],
                        densityRow['y_index'],
                        densityRow['z_index'])
                


                result =  pandas.Series({'timestamp': densityRow['timestamp'],
                    'x_index': densityRow['x_index'],
                    'y_index': densityRow['y_index'],
                    'z_index': densityRow['z_index'],
                    'predicted': predicted,
                    'real': densityRow['amount']})

                result.to_csv('predicted/' + str(densityRow['timestamp']) + ' ' + str(densityRow['x_index']) + ' ' + str(densityRow['y_index']) + ' ' + str(densityRow['z_index'])+ '.csv')
                return result
        else:
            return 0


    result = densities.apply(evaluateOne, axis=1);
    return result


output = evaluate()
output.to_csv('predicted_densities.csv')
