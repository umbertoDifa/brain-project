import sys
import numpy as np
import os
import pandas as pd
import random
from PIL import Image

def generate_picture(infomapDir):
    row = 130
    col= 172

    files = [f for f in os.listdir(os.path.join(infomapDir)) if os.path.isfile(os.path.join(infomapDir, f))]
    if not os.path.exists(os.path.join(infomapDir, 'img')):
        print('Creating folder ' + os.path.join(infomapDir, 'img'))
        os.mkdir(os.path.join(infomapDir, 'img'))
    for f in files:
        # if community file and that timestamp
            if f.endswith(".clu"):
                #create matrix
                image = np.zeros((row,col,3), 'uint8')
                df = pd.read_csv(os.path.join(infomapDir, f), sep=' ', header=None, skiprows = 2)
                df.sort_values(by=1,inplace=True) #order by community

                #randomly choose colors for first cluster
                colorR = random.sample(range(0,256),1)[0]
                colorG = random.sample(range(0,256),1)[0]
                colorB = random.sample(range(0,256),1)[0]
                oldCommId = 1 #first comm always one

                for riga in df.iterrows():
                    pixelId = int(riga[1][0])
                    commId = int(riga[1][1])
                    if commId != oldCommId: #select new colors for the new community
                        colorR = random.sample(range(0,256),1)[0]
                        colorG = random.sample(range(0,256),1)[0]
                        colorB = random.sample(range(0,256),1)[0]
                    pixelI = pixelId // col
                    pixelJ = pixelId % col
                    image[pixelI,pixelJ,:]=[colorR,colorG,colorB]
                img = Image.fromarray(image,'RGB')
                timestamp = int(f.split('-t')[1].split('.clu')[0])
                img.save(os.path.join(infomapDir, 'img', str(timestamp)) + '.tif')


##################################################
def startme():
    #folder = 'C:/Users/Umberto/Desktop'
    folder = sys.argv[1]
    print('Looking for resultInfomap in '+folder)
    for dir in os.listdir(folder):
        if dir == 'resultInfomap':
            print(dir)
            generate_picture(os.path.join(folder,dir))

###################################

