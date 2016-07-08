#!/bin/bash
#
#cost is the only parameter
#
#
defaultCost='111'
cost=${1:-$defaultCost}

echo 'Starting commdy with cost'$cost
#run commDy
#1 step
/home/shared_brain/BrainCode/commdy/script/ipc-gams.py louvain.gtm

#2step
/home/shared_brain/BrainCode/commdy/script/gamsout2color.py louvain.gtm louvain_ipc.out > louvain_ipc.gcolor

#3 step
/home/shared_brain/BrainCode/commdy/src/color_ind2 -cost $cost louvain.gtm <louvain_ipc.gcolor >louvain_ipc-c$cost.color2
