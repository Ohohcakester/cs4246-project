import pandas as pd
import numpy as np
import os
from PIL import Image, ImageDraw
import random

#DEFAULT SETTINGS - DO NOT TOUCH
y_tiles = 7
x_tiles = 8
tile_size = 40
target_folder = 'renders/'
#DEFAULT SETTINGS - END

#ALTERNATE SETTINGS - START
y_tiles = 35
x_tiles = 40
tile_size = 10
target_folder = 'test_renders/'
#DEFAULT SETTINGS - END

def readData(fileName):
    data = pd.read_csv(fileName)
    #create unique list of names
    uniqueTimestamps = data.timestamp.unique()

    #create a data frame dictionary to store your data frames
    d = {t : pd.DataFrame for t in uniqueTimestamps}

    for key in d.keys():
        d[key] = data[:][data.timestamp == key]
    return d

def getMaxDensity(fileName):
    data = pd.read_csv(fileName)
    return data['density'].max()

class Drawer(object):
    def __init__(self, timestamp, z):
        self.tile_size = tile_size
        resX = x_tiles * self.tile_size
        resY = y_tiles * self.tile_size

        self.im = Image.new('RGB', (resX, resY), (0,0,0))
        self.draw = ImageDraw.Draw(self.im)
        self.name = '_'.join(map(str,[z,timestamp]))
    
    def drawSquare(self,x,y,colour):
        x1 = self.tile_size*x
        y1 = self.tile_size*y
        x2 = x1+self.tile_size
        y2 = y1+self.tile_size
        self.draw.rectangle((x1,y1,x2,y2),colour)
        
        
    def drawDensity(self,x,y,density):
        c = int((density**0.2)*255*2)
        colour = (c, 255-c, 0)
        self.drawSquare(x,y,colour)

    def render(self):
        try: os.mkdir(target_folder)
        except: pass
        self.im.save(target_folder+self.name+'.png', 'PNG')
        
    def open(self):
        os.startfile(target_folder+self.name+'.png')

def render(data, key, z):
    data = data[data.z_index == z]
    print 'rendering ' + str(key) + ', z = ' + str(z)
    draw = Drawer(key, z)
    for row in data[['density','x_index','y_index']].itertuples():
        draw.drawDensity(row[2],row[3],row[1])
    draw.render()


dataDict = readData('test_densities.csv')
for key in dataDict.keys():
    render(dataDict[key], key, 0)
    render(dataDict[key], key, 1)