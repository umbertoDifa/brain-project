# Purpose : run commdy with multiple costs
import os
import re
import sys
#fol = 'C:/Users/Umberto/Desktop/tmp'

bashCommand = '/home/shared_brain/BrainCode/helpers/pachyPipelineAutomation/pipeline.sh louvain junk junk junk junk {cost}'
costs = ['311','113','131','111','331','133','313','511','151','115']

# brain = sys.argv[1]
# # print('in '+brain)
# for activation in [x for x in os.listdir(os.path.join(brain)) if os.path.isdir(os.path.join(brain,x))]:
#     m = re.search('Activation[0-9]{1}$', activation)  #search the frame number at the end
#     if m != None: #activation exists in that format name
#         print('Doing activation '+activation)
#         interestFolder = os.path.join(brain,activation,'w50_cor.70') #enter in this folder

        #run multiple costs in that activation
        #moiving
for c in costs:
    print('executing commdy  wiht cost '+c)
    os.system(bashCommand.format(cost =c))  #execute commdy
