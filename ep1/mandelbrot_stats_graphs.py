import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import t

#------------------------------------------------------------------------------------
# Parameters
datadir = "data/"
graphdir = "graphs/"
measurements = 10

sizes = (2**4, 2**5, 2**6, 2**7, 2**8, 2**9, 2**10, 2**11, 2**12, 2**13)
iterations = len(sizes)

threads = (1, 2, 4, 8, 16, 32)
nthreads = len(threads)

regions  = ('Full', 'Seahorse', 'Elephant', 'Triple Spiral')
nregions = len(regions)

parallel_program_titles = ("Pthreads with I/O", "OpenMP with I/O", "Pthreads without I/O", "OpenMP without I/O")

sequential_program_titles = ("Sequential with I/O", "Sequential without I/O")

parallel_program_filename = ("pth_io", "omp_io", "pth", "omp")

sequential_program_filename = ("seq_io", "seq")

#------------------------------------------------------------------------------------
# Load the numpy data
average_time_parallel =  np.load(datadir+"average_time_parallel.npy")
variance_time_parallel =  np.load(datadir+"variance_time_parallel.npy")
average_time_seq =  np.load(datadir+"average_time_seq.npy")
variance_time_seq=  np.load(datadir+"variance_time_seq.npy")

#------------------------------------------------------------------------------------
# Start plotting

# Time vs size (for sequential programs)
colors = ("red", "green")
markers  = ("x", "o")

for reg in range(0, nregions):
    for p in range(0, 2):
        plt.loglog(sizes, average_time_seq[reg, p, :], color=colors[p], marker=markers[p], label=sequential_program_titles[p])
    plt.ylim(10.0**(-3.5), 10**(2.1))
    plt.xlabel('Size')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.grid(True, which="both")
    title = 'Region = '+regions[reg]+" - sequential programs "
    plt.title(title)
    filename = "sequential_"+regions[reg]
    plt.savefig(graphdir+filename+'.png', format='png')
    plt.close()

#------------------------------------------------------------------------------------
# Time vs size for each thread (for parallel programs)
colors = ('red', 'green', 'blue', 'purple', 'brown', 'orange')
markers = ('x','s','<','o','D','*')

for reg in range(0, nregions):
    for p in range(0, 4):
        plt.loglog(sizes, average_time_seq[reg, 1, :], color='gray', marker='+', label='sequential')
        for nt in range(0, nthreads):
            #print(regions[reg], threads[nt], parallel_program_titles[p])
            plt.loglog(sizes, average_time_parallel[reg, nt, p, :], color=colors[nt], marker=markers[nt], label=str(threads[nt])+" threads")
        plt.ylim(10.0**(-3.5), 10**(2.1))

        plt.xlabel('Size')
        plt.ylabel('Time (seconds)')
        plt.legend()
        plt.grid(True, which="both")
        title = 'Region = '+regions[reg]+ ", program = "+parallel_program_titles[p]
        plt.title(title)
        filename = parallel_program_filename[p]+"_ "+regions[reg]
        plt.savefig(graphdir+filename+'.png', format='png')
        plt.close()

#------------------------------------------------------------------------------------
# Compare sequential programs with parallel programs
colors = ("red", "green", "orange")
markers  = ("x", "o", "+")
titles = ("with I/O", "without I/O")
file = ("_io", "")
progs = ("Pthreads ", "OpenMP ")

for reg in range(0, nregions):
    #for p in range(0, 2):
        plt.loglog(sizes, average_time_seq[reg, 1, :], color=colors[0], marker=markers[0], label=sequential_program_titles[0])
        plt.loglog(sizes, average_time_parallel[reg, 5, 2, :], color=colors[1], marker=markers[1], label=progs[0]+str(threads[nt])+" threads")
        plt.loglog(sizes, average_time_parallel[reg, 5, 3, :], color=colors[2], marker=markers[2], label=progs[1]+str(threads[nt])+" threads")
        plt.ylim(10.0**(-3.5), 10**(2.1))
        plt.xlabel('Size')
        plt.ylabel('Time (seconds)')
        plt.legend()
        plt.grid(True, which="both")
        title = 'Region = '+regions[reg]+ ' - '+titles[1]
        plt.title(title)
        filename = regions[reg]+file[1]
        plt.savefig(graphdir+filename+'.png', format='png')
        plt.close()
