#!/bin/bash
#
#Right now takes as argument the 
# <pipeline starting point> <dataPath> <imagePath> <threshold> <window> <commdyCost>
# the point where to start the pipeline "corr" | "louvain" | "commdy" | "stats"
# dataPath 
# the path where to store the images of correlation
# correlation threshold
# correlation window
# commdyCosts
#
# NB right now all arguments are positional, so although if I need commdy I don't need to provide the window length, right now the only way is to put junk parameters 
# example pipeline commdy junk junk junk junk 111
# TODO make the arguments positional
##

##check if the entry point is present
if [ $# -eq 0 ]
		then
			echo "Please supply more arguments:"
			echo "Entry point"
			exit 1
	fi

#####DEFAULT PARAMETERS####
defaultCorrelation=0.70
defaultWindow=50
defaultCommdyCost=111
##########################


######UNPACK ARGUMENTS
startPoint="$1"
dataPath="$2"
imagePath="$3"
correlation=${4:-$defaultCorrelation}
window=${5:-$defaultWindow}
commdyCost=${6:-$defaultCommdyCost}
#######################

MY_PATH="/home/shared_brain/BrainCode/helpers/pachyPipelineAutomation/"

#declare variable that signals when the pipeline is started so the condition
#about the entry point are no longer checked

isStarted=false


if [ "$startPoint" = "corr" ]; then 
	#check if there are enough arguments
	if [ $# -lt 3 ]  #threshold and window can miss
		then
			echo "Please supply more arguments:"
			echo "Entry point - dataPath - imagePath - [threshold] - [window] - [commdyCost]"
			exit 1
	fi
	#<dataPath> <imagePath> <correlation> <window>
	#echo 'runninc corr'$dataPath' image '$imagePath' corr'$correlation' window'$window
	source $MY_PATH'correlationScript.sh' $dataPath $imagePath $correlation $window
   echo 'Starting the split file with corr '$correlation
   #split the pair file (cor_weights_cor75 è il file da splittare)
   /home/shared_brain/BrainCode/Louvain/split_files.py cor_weights_cor$correlation.pair
    
	isStarted=true
fi

if [ "$startPoint" = "louvain" ] || [ "$isStarted" = true ]; then
	source $MY_PATH'louvainScript.sh' $correlation
	isStarted=true
fi

if [ "$startPoint" = "commdy" ] || [ "$isStarted" = true ]; then
	source $MY_PATH'commdyScript.sh' $commdyCost
	isStarted=true
fi

if [ "$startPoint" = "stats" ] || [ "$isStarted" = true ]; then
	source $MY_PATH'statisticsScript.sh' 'louvain_ipc-c'$commdyCost'.color2'
	isStarted=true
fi

if [ "$isStarted" = false ]; then
	echo "YOU INSERTED AN INVALID ENTRY POINT!"
fi
