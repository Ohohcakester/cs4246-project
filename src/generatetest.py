from coordinateconverter import Grid 
from pathfind import runPathfinding
import pandas
import os
import math

zToMazename = {0: 'floor2map', 1: 'floor18map'}

def loadData(id):
    return pandas.read_csv('data/' + str(id) + '.csv')

def listTags():
    import random
    # The list of tags returned is deterministically shuffled. (Seeded)
    random.seed(4246)
    tags = map(int, map((lambda filename: filename[:-4]), os.listdir('data/')))
    random.shuffle(tags)
    return tags

def splitTags(tags, proportion):
    num = int(math.floor(proportion* len(tags)))
    return tags[:num], tags[num:]

def filterData(df, z):
    if z == 1:
        return df[df['Z'] > 0.6]
    else:
        return df[df['Z'] < 0.6]

def getFocusPoints():
    return [(0.0, 0.5), (0.2, 0.3), (0.5, 0.2)]

def convertData(df, focusPoints, level=1):
    print("TEST")
    mazeName = zToMazename[level]
    coordinates = df.loc[:, ['X', 'Y']].values.tolist()
    print("COORDINATE GENERATED")
    grid = Grid(mazeName)
    normalized = []
    for coordinate in coordinates:
        normalized.append(grid.queryActual(coordinate[0], coordinate[1]))
    print("COORDINATE Normalized")
    focus = map(lambda point: grid.queryGrid(point[0], point[1]), focusPoints)
    testcases = []
    for coordinate in normalized:
        testcases.append((coordinate[0], coordinate[1], focus[0][0], focus[0][1]))
        testcases.append((coordinate[0], coordinate[1], focus[1][0], focus[1][1]))
        testcases.append((coordinate[0], coordinate[1], focus[2][0], focus[2][1]))
    print("Test cases generated")
    print(len(testcases))
    result = runPathfinding(mazeName, testcases)
    return df.assign(d1 = map(lambda index: result[3*index  ], range(0, len(df.index))),
                    d2 = map(lambda index: result[3*index+1], range(0, len(df.index))),
                    d3 = map(lambda index: result[3*index+2], range(0, len(df.index))))

def run(data, focusPoints, level=1):
    df = convertData(filterData(data, 1), focusPoints, level=level)
    return df

if __name__ == '__main__':
    tags = listTags()[0:100]
    data = map(loadData, tags)
    concatenated = pandas.concat(data)
    
    #df = convertData(filterData(concatenated, 1), 1, getFocusPoints())
    df = run(concatenated, getFocusPoints())
