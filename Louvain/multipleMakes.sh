#!/bin/bash

#Purpose: run the make file several times

#crete folder to store the multiple runs of make
mkdir louvainRuns

cd louvainRuns

COUNTER=0
repetitions=30

STARTTIME=$(date +%s)

while [ $COUNTER -lt $repetitions ]; do
   #create folder for the run and move there
	mkdir run$COUNTER
   cd run$COUNTER
   
   #copy dependecies
   mv ../../*.bin . 
   mv ../../*.weights . 
   mv ../../*.nodes . 
   
      
   #copy the make file 
   cp /home/shared_brain/BrainCode/Louvain/makeForMultipleMakes .

   make -f makeForMultipleMakes
   
   #clean
   mv *.bin ../../
   mv *.weights ../../
   mv *.nodes  ../../

	let COUNTER=COUNTER+1 
   cd ..
done

ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."