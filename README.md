# brain-project
Dynamic Community Analysis from Brain Imaging Data

This software is provided 'as-is'.

This repo contains a collection of scripts to analyze brain imaging data, in particular for fluorescence data.
Keep in mind that not all the scripts are optimized and none is tested, but they all achived their purpose (untill now ;)) and most of them are commented , feel free to point out any bug and contribute.

-[Pipeline Manual](#pipeline-manual) 

-[Pipeline Auto](#pipeline-auto) 

-[Modular Scripts](#modular)

-[Multiple Louvain](#multiple-louvain) 

-[Multiple Commdy for Louvain](#multiple-commdy-for-louvain) 

 -[Generate Louvain Images](#louvain-images) 

 -[Generate Commdy Images](#commdy-images) 
 
 -[Run Infomap](#infomap)
 
 -[Generate Infomap images](#infomap-image)

-[Multiple commdy costs](#multiple-commdy-costs)


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

# multiple-louvain
This script runs Louvain multiple times for the same pair files. It has been used to test the
robusteness of Louvain on multiple runs.

1- run make once
```
cp /home/shared_brain/BrainCode/Louvain/Makefile . 
make
```
2- run multiple times
```
cp /home/shared_brain/BrainCode/Louvain/multipleMakes.sh .
time source multipleMakes .sh
```

-Alternative : one liner
```
cp /home/shared_brain/BrainCode/Louvain/Makefile . && make && cp
/home/shared_brain/BrainCode/Louvain/multipleMakes.sh . && time
source multipleMakes .sh
```

# multiple-commdy-for-louvain

Usually after multiple Louvain are run then also multiple commdy are run, a commdy for each run to test
the robusteness of commdy on louvain runs.
```
source
/home/shared_brain/BrainCode/helpers/pachyPipelineAutomation/multipleCommdy.sh
```

#louvain-images
[louvainClustersImages.py](louvainClustersImages.py)

The input is the folder with the louvain_comm files
```
python /home/shared_brain/BrainCode/Louvain/louvainClustersImages.py
/home/shared_brain/Output/Young_vs_Old/Young_11-15-13_brain_33/Activation1
```

#commdy-images
[louvainClustersImages.py](commdyToImage.py)

#infomap
-Single , just run on a single file
```
/home/shared_brain/BrainCode/infoMap/Infomap/Infomap --tree --map --clu
--input-format link-list <fileName > < outputFolderThatMustExists >
```

-Multiple , run for each pair file in the folder
```
mkdir resultInfomap
for i in *. pair ; do
/home/shared_brain/BrainCode/infoMap/Infomap/Infomap --tree --map
--clu --input-format link-list $i resultInfomap ; done
```

#infomap-image
[infomapAndImagePipe.py](Infomap/infomapAndImagePipe.py)

[infomapClustersImages.py](Infomap/infomapClustersImages.py)

#multiple-commdy-costs
[multipleCostsCommdy.py](multipleCostsCommdy.py)

Run commdy for several costs on the pair files.
Notice in the multipleCostCommdy.py you can decide which costs to use.
Also notice how this scripts uses the pipeline.sh script as subroutine.

Go in the folder with the pair files , usually the core folder
```
cd /home/shared_brain/Output/Young_vs_Old/Young_11-09-13_brain_39/Activation3/w50_cor.70/core
time python /home/shared_brain/BrainCode/helpers/multipleCostsCommdy.py
```