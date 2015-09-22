import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image, ImageDraw

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
    data = pd.read_csv('../data/trainingData_Filtered.csv')
    data_filtered = data[['USERID', 'LONGITUDE', 'LATITUDE', 'FLOOR', 'BUILDINGID', 'TIMESTAMP']]

    im = loadImage()
    userIds = data_filtered['USERID'].unique()
    userIds.sort()
    for userId in userIds:
        user_data = data_filtered[data_filtered.USERID == userId]
        X = np.array(user_data['TIMESTAMP'])[:, None]
        
        #print(np.min(X))
        X -= np.min(X)
        Y = np.array(user_data[['LONGITUDE', 'LATITUDE']])
        t = np.transpose(X)[0]
        x = np.transpose(Y)[0]
        y = np.transpose(Y)[1]
        
        drawLines(t, x, y, im)
        
    im.save('output.png', 'PNG')
    os.startfile('output.png')



def plotGraph(t, x, y):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.plot(t, x, y)
    plt.show()



if __name__ == '__main__':
    main()