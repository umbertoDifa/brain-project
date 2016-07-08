#!/bin/bash
#
#takes as argument the color2 file on which to do the statistics
#
#
defaultFile='louvain_ipc-c111.color2'
file=${1:-$defaultFile}

echo 'Starting brain stats on file '$file
#run statistics
Rscript /home/shared_brain/BrainCode/Rstatistics/brainStats.R $file

