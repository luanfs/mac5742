#! /bin/bash

set -o xtrace

MEASUREMENTS=15
SIZE=4096

NAMES_parallel=('mandelbrot_pth'  'mandelbrot_pth_io')

NTHREAD='32'

make
mkdir results

# Run pthreads parallel programs
for NAME in ${NAMES_parallel[@]}; do
    dir="${NAME}_${NTHREAD}"
    mkdir results/$dir
    
    echo $NTHREAD $SIZE
    for ((j=1; j<=$MEASUREMENTS; j++)); do
        ( time ./$NAME -0.188 -0.012 0.554 0.754 $SIZE ls )>> triple_spiral$SIZE.log 2>&1
    done

    mv *.log results/$dir
    rm *.ppm
done
