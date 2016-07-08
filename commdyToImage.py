from sklearn.metrics.cluster import adjusted_rand_score
import os
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import pandas as pd
from PIL import Image
import random

def createImagesFromCommdyGroups(colorFile,mapFile):

    ############get the .color file
    with open(colorFile, 'r') as f:
        s = f.readline()
    lines = s.split('  ')
    groups = lines[0].split(' ')
    # totalNumberOfGroups = len(groups)
    colorsUsedForGroups = len(set(groups))
    print('There are '+str(colorsUsedForGroups)+' unique groups')
    nodes = lines[1:] #careful each node is a string right now not a list of colors as i'd like

    totalNumberOfNodes = len(nodes)
    print('There are '+str(totalNumberOfNodes)+' nodes')

    totalNumberOfTimestamps = len(nodes[0].split(' '))
    print('There are '+str(totalNumberOfTimestamps)+' number of timestamps')

    nodesPerRun = ([x.split(' ') for x in nodes])

    numberOfcolorsUsedForNodes =len(set([x for sublist in [x.split(' ') for x in nodes] for x in sublist]))
    colorsUsedForNodes =(set([x for sublist in [x.split(' ') for x in nodes] for x in sublist]))

    print(str(numberOfcolorsUsedForNodes)+' colors used for nodes')


    #########get the map file to map id back to pixel
    mapping = {}
    insieme = set()
    count = 0
    map = False
    with open(mapFile, 'r') as f:
        for line in f:

            if(map and len(line.strip().split(' '))>1):
                mapping[line.strip().split(' ')[0]] =line.split(' ')[1]
                insieme.add(line.strip().split(' ')[0])
                count +=1
            if(line.strip() == 'individual -> new id'):
                map = True

    print('there are '+ str(len(mapping))+' nodes')


    #######create the image

    row = 130
    col= 172

    colors = random.sample(range(0,16777216),numberOfcolorsUsedForNodes)

    mappingColors={}
    count=0
    ###assign a color to each group
    for c in colorsUsedForNodes:
        mappingColors[c]=str(colors[count])
        count+=1
    tot=0
    for timestamp in range(totalNumberOfTimestamps):
        image = np.zeros((row,col,3), 'uint8')
        for i in range(row):
            for j in range(col):
                pixelId = i*col+j
                pixelI = pixelId // col
                pixelJ = pixelId % col
                if insieme.__contains__(str(pixelId)): #if pixel is one of the one in the communities dynamic
                    group = nodesPerRun[int(mapping[str(pixelId)])-1][timestamp]
                    color = int(mappingColors[group])
                    R= color%256
                    G = color//256
                    B = color//(256**2)
                    tot +=1
                else:
                    R = 0
                    G = 0
                    B = 0
                image[pixelI,pixelJ,:]=[R,G,B]#[100,100,100]#colors[commId]
        img = Image.fromarray(image,'RGB')
        img.save('./imagesCommdy/image'+str(timestamp)+'.tif')


#calculateNullModel()
#calculateNullModelFromSameData()
mapFile = 'C:/Users/Umberto/Desktop/old/louvain.map'
colorFile = 'C:/Users/Umberto/Desktop/old/louvain_ipc-c111.color2'


