#! /bin/bash

CC=python3

data_script='mandelbrot_stats_data.py'
graph_script='mandelbrot_stats_graphs.py'
table_script='mandelbrot_stats_tables.py'

datadir='data'
graphdir='graphs'
tabledir='tables'

# Data directory
mkdir $datadir

# Run data script
echo "Running " $data_script
$CC $data_script
echo "Data have been save in" $datadir


# Figures directory
mkdir $graphdir

# Run graphs script
echo "Running " $graph_script
$CC $graph_script
echo "Graphs have been plotted in" $graphdir

# Excel tables directory
mkdir $tabledir

echo "Running " $table_script
$CC $table_script
echo "Tables have been saved in" $tabledir
