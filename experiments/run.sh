#!/bin/bash

mkdir -p results
savilerow -help | head -n1 > results/savilerow-version.txt

python3 experiments/createCommandList.py > experiments/commandList.txt

# set nb of threads by: PARALLEL="-j16"
parallel --no-notice \
    --eta \
    --shuf \
    --memfree 8G \
    --joblog gnuparallel.joblog \
    --results gnuparallel.results \
    :::: experiments/commandList.txt

experiments/collectInfo.sh
