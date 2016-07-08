#!/bin/bash
# This program runs the all pipeline for several values of the window
# <dataPath> <imagePath> <correlationThreshold> <startingWindow> <incrementWindow> <repretitions>
# dataPath : where are the input images
#imagePath: where are going to be the output images 
#correlationThreshold: the correlation threshold
# startingWindow = which size to start e.g. 50
# incrementWindow = how much to add each time e.g. 100
# repetitions= how many times to increment
##

dataPath="$1"
imagePath="$2"
threshold="$3"
startingWindow="$4"
incrementWindow="$5"
repetitions="$6"

echo 'Starting the multiple window pipeline'

COUNTER=0
currentWindow=$startingWindow
while [ $COUNTER -lt $repetitions ]; do
	echo 'Starting with window  = '$currentWindow
	
	# make dir to store pair file for this window
	newDir='./w'$currentWindow'_cor'$threshold
	mkdir $newDir
	
	#make dir for images	
	newImageDir=$imagePath'/w'$currentWindow'_cor'$threshold
	mkdir $newImageDir
	
	#move into dir	
	cd 'w'$currentWindow'_cor'$threshold
		
	source /home/shared_brain/BrainCode/helpers/pachyPipelineAutomation/pipeline.sh corr $dataPath $newImageDir $threshold $currentWindow
	
	#move back
	cd ..
	
	let COUNTER=COUNTER+1 
	currentWindow=$(($currentWindow+$incrementWindow))
done
 