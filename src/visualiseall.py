import pandas as pd
import numpy as np
import os
from PIL import Image, ImageDraw
import random
from math import floor, isnan

def readData(fileName):
    data = pd.read_csv(fileName)
    return data

def getMaxDensity(fileName):
    data = pd.read_csv(fileName)
    return data['density'].max()

def getSumAmount(data):
    return data['amount'].max()

class Drawer(object):
    def __init__(self):
        self.tile_size = 1
        resX = 4000 * self.tile_size
        resY = 3500 * self.tile_size

        self.im = Image.new('RGB', (resX, resY), (0,0,0))
        self.draw = ImageDraw.Draw(self.im)
        self.name = 'render_all'
    
    def drawSquare(self,x,y,colour):
        x1 = self.tile_size*x
        y1 = self.tile_size*y
        x2 = x1+self.tile_size - 1
        y2 = y1+self.tile_size - 1
        self.draw.rectangle((x1,y1,x2,y2),colour)
        
        
    def drawDensity(self,x,y,density, colour):
        self.drawSquare(x,y,colour)

    def render(self):
        try: os.mkdir('renders/')
        except: pass
        self.im.save('renders/'+self.name+'.png', 'PNG')
        
    def open(self):
        os.startfile('renders/'+self.name+'.png')

def render(data):
    draw = Drawer()
    for row in data.iterrows():
        if (row[1]['Z'] < 1 and not isnan(row[1]['X'] + 0.9)):
            x = int(floor((row[1]['X'] + 0.9) * 2500))
            y = int(floor((row[1]['Y'] + 0.7) * 2500))
            area = row[1]['AREA_ID']
            h = hash(area)
            rgb = (h % 128, ((h / 128) % 128), ((h / (128 * 128)) % 128))
            rgb = tuple([x+y for x,y in zip(rgb,(128,128,128))])
            draw.drawDensity(x, y, 1, rgb)
    draw.render()

data = readData('../4246Data/position_snapshot_1.csv')
render(data)
