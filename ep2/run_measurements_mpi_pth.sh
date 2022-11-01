#! /bin/bash

set -o xtrace

MEASUREMENTS=15
SIZE=4096

NAMES_parallel=('mandelbrot_mpi_pth_io'  'mandelbrot_mpi_pth')

NTHREAD='32'

NPROCS=('1' '8' '16' '32' '64')

make
mkdir results
 
# Run mpi parallel programs
for NAME in ${NAMES_parallel[@]}; do
    for NPROC in ${NPROCS[@]}; do
        dir="${NAME}_${NPROC}_pth_${NTHREAD}"
        mkdir results/$dir
        for ((j=1; j<=$MEASUREMENTS; j++)); do
            echo $NAME $NPROC $j 
            ( time mpirun --host localhost:$NPROC ./$NAME -0.188 -0.012 0.554 0.754 $SIZE ls )>> triple_spiral$SIZE.log 2>&1
        done
        mv *.log results/$dir
        rm *.ppm
    done
done
