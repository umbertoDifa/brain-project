# brain-project
Dynamic Community Analysis from Brain Imaging Data

This software is provided 'as-is'.

This repo contains a collection of scripts to analyze brain imaging data, in particular for fluorescence data.
Keep in mind that not all the scripts are optimized and none is tested, but they all achived their purpose (untill now ;)) and most of them are commented , feel free to point out any bug and contribute.

-[Pipeline Manual](#pipeline-manual) 

-[Pipeline Auto](#pipeline-auto) 

-[Modular Scripts](#modular) 


# pipeline-manual

[pipeline-manual.txt](pipeline-manual.txt) 

This is not an executable, but it shows each of the command needed to execute the pipeline manually. It can be useful to check it out
to understand the general flow.


# pipeline-auto
[pipeline.sh](pipeline.sh)

*Usage:*``` /home/shared_brain/BrainCode/helpers/pachyPipelineAutomation/pipeline.sh # <pipeline starting point> <dataPath> <imagePath> <threshold> <window> <commdyCost>```
- dataPath : the folder with the input images
- imagePath : the path where to store the images of correlation
- correlation threshold : the correlation threshold
- correlation window : the window used to compute correlations
- commdyCosts : the costs used to run commdy

*Usage example:*``` /home/shared_brain/BrainCode/helpers/pachyPipelineAutomation/pipeline.sh corr /home/shared_brain/Data/RS_PCB_Oil/PCB196RS/PCB_196_RS_Activation_2/ /home/shared_brain/Output/Images/RS_PCB_Oil/PCB_196_RS/Activation2/w50_cor.70/```

The manual pipeline can be automated with the following script.
It is a script that combines the steps And can be started at any of the previous steps. Each of the above
steps is encapsulated into a single script [(modular)](#modular) and then those scripts are concatenated to execute the whole pipeline.
The pipeline can be started at any point and it keeps going till the end, so if it is started at Louvain 
than it also executes commdy and the statistics.

# modular
Keep in mind that in the folder BrainCode/helpers/pachyPipelineAutomation there is both the pipeline.sh
script and the modular script which are used by the pipeline but can also be used alone. Those script are very
easy to use and commented and can be used as subroutines for other scripts such as running commdy for several
costs parameters (by the way there is a script for that).

-[correlationScript](/pachyPipelineAutomation/correlationScript.sh) used to run the correlation algorithm.

-[louvainScript](/pachyPipelineAutomation/louvainScript.sh) used to run the correlation algorithm.

-[commdyScript](/pachyPipelineAutomation/commdyScript.sh) runs commdy.

-[statisticsScripts](/pachyPipelineAutomation/statisticsScript.sh) runs the statistics.

# multipleMakes
This script runs Louvain multiple times for the same pair files. It has been used to test the
robusteness of Louvain on multiple runs.

1. run make once
```
cp / home / shared_brain / BrainCode / Louvain / Makefile . 
make
```

2. run multiple times
```
cp / home / shared_brain / BrainCode / Louvain / multipleMakes .sh .
time source multipleMakes .sh
```

-Alternative : one liner
```
cp / home / shared_brain / BrainCode / Louvain / Makefile . && make && cp
/ home / shared_brain / BrainCode / Louvain / multipleMakes .sh . && time
source multipleMakes .sh
```
