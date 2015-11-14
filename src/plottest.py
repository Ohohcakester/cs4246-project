import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image, ImageDraw
import random
import ast

top = 980
left = 145
scale = 3.43

def loadImage():
    im = Image.open('../img/locationmap.png')
    return im
    
def drawScaled(x1,y1,x2,y2,draw):
    x1 *= scale
    x2 *= scale
    y1 *= scale
    y2 *= scale
    x1 = left + x1
    x2 = left + x2
    y1 = top - y1
    y2 = top - y2
    #dx = x2-x1
    #dy = y2-y1
    draw.line((x1,y1,x2,y2),fill=128)
    
    
def drawLines(t, x, y, im):
    draw = ImageDraw.Draw(im)
    for i in range(1,len(t)):
        #print(','.join(map(str,[x[i-1],y[i-1],x[i],y[i]])))
        drawScaled(x[i-1],y[i-1],x[i],y[i], draw)
    
        
def main():
    #data = pd.read_csv('../data/trainingData_Filtered.csv')
    #data_filtered = data[['USERID', 'LONGITUDE', 'LATITUDE', 'FLOOR', 'BUILDINGID', 'TIMESTAMP']]

    #im = loadImage()
    #userIds = data_filtered['USERID'].unique()
    userIds = os.listdir('data')
    userIds.sort()
    #random.shuffle(userIds)
    for userId in userIds[2:3]:
        userId = '3252.csv'
        
        #user_data = data_filtered[data_filtered.USERID == userId]
        data = pd.read_csv('data/' + userId)
        data = data.sort('SNAPSHOT_TIMESTAMP')
        
        t = np.array(data['SNAPSHOT_TIMESTAMP'])[:, None]
        x = np.array(data['X'])[:, None]
        y = np.array(data['Y'])[:, None]
        t = np.transpose(t)[0]
        x = np.transpose(x)[0]
        y = np.transpose(y)[0]
        
        #print(np.min(X))
        #X -= np.min(X)
        #Y = np.array(data[['X', 'Y']])
        #t = np.transpose(X)[0]
        #x = np.transpose(Y)[0]
        #y = np.transpose(Y)[1]
     
        print 'Plotting: ' + userId
        plotGraph(t, x, y)
        #drawLines(t, x, y, im)
        
    #im.save('output.png', 'PNG')
    #os.startfile('output.png')


def plotShortestPaths():
    fileName = 'bayes_ext_temp_folder/1447379781035_A.csv'
    data = pd.read_csv(fileName)
    data = data.sort('TIMESTAMP')
    data['SHORTEST_PATHS'] = data['SHORTEST_PATHS'].apply(ast.literal_eval)
    
    t = np.array(data['TIMESTAMP'])[:, None]
    x = np.array(data['SHORTEST_PATHS'].apply(lambda paths: paths[0]))[:, None]
    y = np.array(data['SHORTEST_PATHS'].apply(lambda paths: paths[2]))[:, None]
    t = np.transpose(t)[0]
    x = np.transpose(x)[0]
    y = np.transpose(y)[0]

    x = map(float,x)
    y = map(float,y)
    
    #print(np.min(X))
    #X -= np.min(X)
    #Y = np.array(data[['X', 'Y']])
    #t = np.transpose(X)[0]
    #x = np.transpose(Y)[0]
    #y = np.transpose(Y)[1]
 
    print 'Plotting: ' + fileName
    plotGraph(t, x, y)


def plotGraph(t, x, y):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.plot(t, x, y)
    plt.show()



if __name__ == '__main__':
    #main()
    plotShortestPaths()