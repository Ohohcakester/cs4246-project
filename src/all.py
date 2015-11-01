#!/usr/bin/python

'''
To run all other files
'''

import pandas as pd
import numpy as np

import os

import pathfind
import coordinateconverter

floor2map = 'floor2map'
floor2grid = coordinateconverter.Grid(floor2map)

floor18map = 'floor18map'
floor18grid = coordinateconverter.Grid(floor18map)

directory = '../data/'
f = os.listdir(directory)[0] # Testing with one file first
df = pd.read_csv(directory + f)
user = int(f[:4])   # Get the first four numbers as userID
df_pairs_floor2 = pd.DataFrame(columns=['timestamp', 'user', 'pair', 'Z'])
df_pairs_floor18 = pd.DataFrame(columns=['timestamp', 'user', 'pair', 'Z'])

# If z = 0: use floor2, else use floor18
# Assume no shortest path between floor2 and floor18 first
for index, row in df.iterrows():
    if index != 0 and row.Z == df.iloc[index-1].Z:
        if row.Z == 0:        
            current_coordinate = floor2grid.queryActual(row.X, row.Y)
            prev_coordinate = floor2grid.queryActual(df.iloc[index-1].X, df.iloc[index-1].Y)
            df_pairs_floor2 = df_pairs_floor2.append({'timestamp': row.SNAPSHOT_TIMESTAMP, 'Z': row.Z, 'user': user, 'pair': (prev_coordinate + current_coordinate)}, ignore_index=True)
        else:
            current_coordinate = floor18grid.queryActual(row.X, row.Y)
            prev_coordinate = floor18grid.queryActual(df.iloc[index-1].X, df.iloc[index-1].Y)
            df_pairs_floor18 = df_pairs_floor18.append({'timestamp': row.SNAPSHOT_TIMESTAMP, 'Z': row.Z, 'user': user, 'pair': (prev_coordinate + current_coordinate)}, ignore_index=True)

list_pairs_floor2 = list(df_pairs_floor2.pair)
list_pairs_floor18 = list(df_pairs_floor18.pair)
df_pairs_floor2['shortestpaths'] = pathfind.runPathfinding(floor2map, list_pairs_floor2)
df_pairs_floor18['shortestpaths'] = pathfind.runPathfinding(floor18map, list_pairs_floor18)
df_new = pd.concat([df_pairs_floor2, df_pairs_floor18])
df_new = df_new.sort('timestamp')



