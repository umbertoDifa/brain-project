import os
import re
import sys
from infomapClustersImages import generate_picture
#fol = 'C:/Users/Umberto/Desktop/tmp'
bashCommand = 'for i in {interestFolder}/*-t*.pair; do /home/shared_brain/BrainCode/infoMap/Infomap/Infomap --tree --map --clu --input-format link-list $i {interestFolder}/resultInfomap; done'
infomapFolder = 'resultInfomap'
#brain ='.'
brain = sys.argv[1]
print('in '+brain)
for activation in [x for x in os.listdir(os.path.join(brain)) if os.path.isdir(os.path.join(brain,x))]:
    m = re.search('Activation[0-9]{1}$', activation)  #search the frame number at the end
    if m != None: #activation exists in that format name
        print('Doing activation '+activation)
        interestFolder = os.path.join(brain,activation,'w50_cor.70') #enter in this folder

        if not os.path.exists(os.path.join(interestFolder,infomapFolder)):
            print('making dir resultInfomap in '+interestFolder)
            os.mkdir(os.path.join(interestFolder,infomapFolder)) #create output folder for infomap

        print('executing infomap')
        os.system(bashCommand.format(interestFolder =interestFolder))  #execute infomap on each pair file

        #create images
        generate_picture(os.path.join(interestFolder,infomapFolder))