#! /bin/bash

set -o xtrace

MEASUREMENTS=15
SIZE=4096

NAMES_sequential=('mandelbrot_seq_io' 'mandelbrot_seq')

make
mkdir results

# Run sequential programs
for NAME in ${NAMES_sequential[@]}; do
    dir="${NAME}"
    mkdir results/$dir
    for ((j=1; j<=$MEASUREMENTS; j++)); do
        echo $NAME $SIZE $j
        ( time ./$NAME -0.188 -0.012 0.554 0.754 $SIZE ls) >> triple_spiral$SIZE.log 2>&1
    done

    mv *.log results/$dir
    rm *.ppm
done
