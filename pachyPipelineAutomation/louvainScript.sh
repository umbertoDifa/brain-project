#!/bin/bash
#
#Take the correlation value as a parameter (e.g. 0.70) because in this way
#it can look for the right file
#

echo 'Starting Louvain make'
#copy the Louvain Makefile to the current folder
cp /home/shared_brain/BrainCode/Louvain/Makefile .

#MANUALLY REMOVE SMALL FILES
#execute Louvain
make

