import os
import sys

def plotDistributionOfCommSize(activation,run,timestamp):
    import os
    import pandas as pd
    from collections import Counter
    from matplotlib import pyplot as plt
    import matplotlib

    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 35}

    matplotlib.rc('font', **font)
    plt.rcParams['figure.figsize'] = 170, 170

    files = [f for f in os.listdir(os.path.join(activation, run)) if os.path.isfile(os.path.join(activation,run, f))]


    for f in files:
        # if community file and that timestamp
        if f.endswith(".louvain_comm") and int(f.split('-t')[1].split('.louvain_comm')[0])==timestamp:
            df = pd.read_csv(os.path.join(activation, run, f),sep='\t', header=None)
            counts = Counter(df[1])
            sizes = [x for x in counts.values()]
            plt.hist(sizes,color='green')
            plt.grid(True)
            plt.xlabel('Community Size')
            plt.ylabel('Counts')



def generate_picture(activation):
    import numpy as np
    import os
    import pandas as pd
    import random
    from PIL import Image

    row = 130
    col= 172


    files = [f for f in os.listdir(os.path.join(activation)) if os.path.isfile(os.path.join(activation,f))]
    if not os.path.exists(os.path.join(activation, 'img')):
        print('Creating folder '+os.path.join(activation,'img'))
        os.mkdir(os.path.join(activation, 'img'))
    for f in files:
        # if community file and that timestamp
            if f.endswith(".louvain_comm"):
                #create matrix
                image = np.zeros((row,col,3), 'uint8')
                df = pd.read_csv(os.path.join(activation, f),sep='\t', header=None)
                df.sort_values(by=1,inplace=True)
                colorsR = random.sample(range(0,256),max(df[1])+1)
                colorsG = random.sample(range(0,256),max(df[1])+1)
                colorsB = random.sample(range(0,256),max(df[1])+1)
                for riga in df.iterrows():
                    pixelId = riga[1][0]
                    commId = riga[1][1]
                    pixelI = pixelId // col
                    pixelJ = pixelId % col
                    image[pixelI,pixelJ,:]=[colorsR[commId],colorsG[commId],colorsB[commId]]#[100,100,100]#colors[commId]
                img = Image.fromarray(image,'RGB')
                timestamp = int(f.split('-t')[1].split('.louvain_comm')[0])
                img.save(os.path.join(activation,'img',str(timestamp))+'.tif')


###########################
# activation = 'C:/Users/Umberto/Desktop/louvainRobustness/louvainRuns_Old_11-10-13_Act6'
# run='run0'
# timestamp = 22000

##################################################
#folder = 'C:/Users/Umberto/Desktop/louvainRobustness/syntheticMesh/r100'
folder = sys.argv[1]
# print('Looking for louvainRuns in '+folder)
# for activation in os.listdir(folder):
#     if activation.startswith('louvainRuns'):
#         print(activation)
#         generate_picture(os.path.join(folder,activation))

###################################

print(folder)
generate_picture(os.path.join(folder))
