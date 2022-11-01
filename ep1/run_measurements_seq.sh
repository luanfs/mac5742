#! /bin/bash

    set -o xtrace

MEASUREMENTS=10
ITERATIONS=10
INITIAL_SIZE=16

NAMES_sequential=('mandelbrot_seq'  'mandelbrot_seq_io')

make
mkdir results

# Run sequential programs
for NAME in ${NAMES_sequential[@]}; do
    dir="${NAME}"
    mkdir results/$dir

    SIZE=$INITIAL_SIZE
    for ((i=1; i<=$ITERATIONS; i++)); do
        echo $SIZE
        for ((j=1; j<=$MEASUREMENTS; j++)); do
            ( time ./$NAME -2.5 1.5 -2.0 2.0 $SIZE ls ) >> full$SIZE.log 2>&1
            ( time ./$NAME -0.8 -0.7 0.05 0.15 $SIZE ls) >> seahorse$SIZE.log 2>&1
            ( time ./$NAME 0.175 0.375 -0.1 0.1 $SIZE ls) >> elephant$SIZE.log 2>&1
            ( time ./$NAME -0.188 -0.012 0.554 0.754 $SIZE ls) >> triple_spiral$SIZE.log 2>&1
        done
        SIZE=$(($SIZE * 2))
    done

    mv *.log results/$dir
    rm *.ppm
done
