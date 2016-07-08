#!/bin/bash


COUNTER=0
repetitions=30

STARTTIME=$(date +%s)

while [ $COUNTER -lt $repetitions ]; do
   # move there
   cd run$COUNTER
   echo "Commdy for run"$COUNTER
   
   #execute coomdy
   source /home/shared_brain/BrainCode/helpers/pachyPipelineAutomation/commdyScript.sh
   
	let COUNTER=COUNTER+1 
   cd ..
done


ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."
