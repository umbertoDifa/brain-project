#!/bin/bash
#
#<dataPath> <imagePath> <correlation> <window>
#
#
dataPath="$1"
imagePath="$2"
correlation="$3"
window="$4"

echo 'Starting Correlation script with threshold '$correlation' window '$window
#set up number of threads
#export OMP_NUM_THREADS=8

#rename files in order to be processed by the cor_img algorithm
python /home/shared_brain/BrainCode/helpers/renameFilesByNumber.py $dataPath

#run the correlation algorithm
/home/shared_brain/BrainCode/cor_img $window 1 0 $correlation 0 n $dataPath $imagePath
