#! /bin/bash

    set -o xtrace

MEASUREMENTS=10
ITERATIONS=10
INITIAL_SIZE=16


NAMES_parallel=('mandelbrot_pth'  'mandelbrot_pth_io')

NTHREAD='16'

make
mkdir results

# Run pthreads parallel programs
for NAME in ${NAMES_parallel[@]}; do
    dir="${NAME}_${NTHREAD}"
    mkdir results/$dir
    
    SIZE=$INITIAL_SIZE
    for ((i=1; i<=$ITERATIONS; i++)); do
        echo $NTHREAD $SIZE
        for ((j=1; j<=$MEASUREMENTS; j++)); do
                ( time ./$NAME -2.5 1.5 -2.0 2.0 $SIZE  ls )>> full$SIZE.log 2>&1
                ( time ./$NAME -0.8 -0.7 0.05 0.15 $SIZE ls )>> seahorse$SIZE.log 2>&1
                ( time ./$NAME 0.175 0.375 -0.1 0.1 $SIZE ls )>> elephant$SIZE.log 2>&1
                ( time ./$NAME -0.188 -0.012 0.554 0.754 $SIZE ls )>> triple_spiral$SIZE.log 2>&1
        done
        SIZE=$(($SIZE * 2))
    done
    mv *.log results/$dir
    rm *.ppm
done
