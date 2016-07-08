# brain-project
Dynamic Community Analysis from Brain Imaging Data

This software is provided 'as-is'.

This repo contains a collection of scripts to analyze brain imaging data, in particular for fluorescence data.
Keep in mind that not all the scripts are optimized and none is tested, but they all achived their purpose (untill now ;)) and most of them are commented , feel free to point out any bug and contribute.

[Pipeline Manual](#pipeline-manual) 
[Pipeline Auto](#pipeline-auto) 

# pipeline-manual

**pipeline-manual.txt** This is not an executable, but it shows each of the command needed to execute the pipeline manually. It can be useful to check it out
to understand the general flow.

# pipeline-auto
**pipeline.sh**
*Usage: * /home/shared_brain/BrainCode/helpers/pachyPipelineAutomation/pipeline.sh # <pipeline starting point> <dataPath> <imagePath> <threshold> <window> <commdyCost>
*Usage example:* /home/shared_brain/BrainCode/helpers/pachyPipelineAutomation/pipeline.sh corr /home/shared_brain/Data/RS_PCB_Oil/PCB196RS/PCB_196_RS_Activation_2/ /home/shared_brain/Output/Images/RS_PCB_Oil/PCB_196_RS/Activation2/w50_cor.70/
The manual pipeline can be automated with the following script.
It is a script that combines the steps And can be started at any of the previous steps. Each of the above
steps is encapsulated into a single script and then those scripts are concatenated to execute the whole pipeline.
The pipeline can be started at any point and it keeps going till the end, so if it is started at Louvain 
than it also executes commdy and the statistics.
