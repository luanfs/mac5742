import numpy as np
import re
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import t
#------------------------------------------------------------------------------------
datadir = "data/"
graphdir = "graphs/"
resultsdir = "results/"

# Parameters
measurements = 15

size = 4096

proc = (1, 8, 16, 32, 64)
nproc = len(proc)

threads = (1, 2, 4, 8, 16, 32)
nthreads = len(threads)

sequential_programs_dir = ("mandelbrot_seq_io", "mandelbrot_seq")
mpi_programs_dir = ( "mandelbrot_mpi_io", "mandelbrot_mpi")
mpi_pth_programs_dir = ( "mandelbrot_mpi_pth_io", "mandelbrot_mpi_pth")
mpi_omp_programs_dir = ( "mandelbrot_mpi_omp_io", "mandelbrot_mpi_omp")
pth_programs_dir = ( "mandelbrot_pth_io", "mandelbrot_pth")
omp_programs_dir = ( "mandelbrot_omp_io", "mandelbrot_omp")

region  = 'Triple Spiral'
logfile = '/triple_spiral'

average_time_mpi     = np.zeros((2, nproc))
average_time_mpi_pth = np.zeros((2, nproc, nthreads))
average_time_mpi_omp = np.zeros((2, nproc, nthreads))
average_time_pth     = np.zeros((2, nthreads))
average_time_omp     = np.zeros((2, nthreads))
average_time_seq     = np.zeros(2)

variance_time_mpi     = np.zeros((2, nproc))
variance_time_mpi_pth = np.zeros((2, nproc, nthreads))
variance_time_mpi_omp = np.zeros((2, nproc, nthreads))
variance_time_pth     = np.zeros((2, nthreads))
variance_time_omp     = np.zeros((2, nthreads))
variance_time_seq     = np.zeros(2)

times = np.zeros(measurements)

# Get sequential program times
for p in range(0, 2):
    filename = resultsdir+sequential_programs_dir[p]+logfile+str(size)+".log"
    #print("Running "+filename)
    file = open(filename,'r')
    sfile = file.read()

    k = 0
    for i in re.finditer('real', sfile):
        index = i.start()
        string = sfile[index:index+14]
        string = string.replace('real','')
        string = string.replace('s','')
        string = string.replace(',','.')
        string = string.replace('  ','')
        index = string.find('m')
        times[k] = float(string[0:index])*60.0 + float(string[index+1:])
        #print(k, string, string[0:index], string[index+1:], times[k])
        k = k+1
    average_time_seq[p] = np.average(times)
    variance_time_seq[p] = np.var(times)
    #print(average_time_seq[p], variance_time_seq[p])

# Get mpi program times for different processes
for pr in range(0, nproc):
    for p in range(0, 2):
        filename = resultsdir+mpi_programs_dir[p]+"_"+str(proc[pr])+logfile+str(size)+".log"
        #print(filename)
        file = open(filename,'r')
        sfile = file.read()
        k = 0
        for i in re.finditer('real', sfile):
            index = i.start()
            string = sfile[index:index+14]
            #print(string)
            string = string.replace('real','')
            string = string.replace('s','')
            string = string.replace(',','.')
            string = string.replace('  ','')
            index = string.find('m')
            times[k] = float(string[0:index])*60.0 + float(string[index+1:])
            #print(string[0:index], string[index+1:], times[k])
            k = k+1
            #print(np.shape(times))
        average_time_mpi[p, pr] = np.average(times)
        variance_time_mpi[p, pr] = np.var(times)
        #print(proc[pr], average_time_mpi[p, pr], variance_time_mpi[p, pr])

# Get mpi+pthreads program times for different processes and threads
for nt in range(0, nthreads):
    for pr in range(0, nproc):
        for p in range(0, 2):
            filename = resultsdir+mpi_pth_programs_dir[p]+"_"+str(proc[pr])+"_pth_"+str(threads[nt])+logfile+str(size)+".log"
            #print(filename)
            file = open(filename,'r')
            sfile = file.read()
            k = 0
            for i in re.finditer('real', sfile):
                index = i.start()
                string = sfile[index:index+14]
                #print(string)
                string = string.replace('real','')
                string = string.replace('s','')
                string = string.replace(',','.')
                string = string.replace('  ','')
                index = string.find('m')
                times[k] = float(string[0:index])*60.0 + float(string[index+1:])
                #print(string[0:index], string[index+1:], times[k])
                k = k+1
                #print(np.shape(times))
            average_time_mpi_pth[p, pr, nt] = np.average(times)
            variance_time_mpi_pth[p, pr, nt] = np.var(times)
            #print(proc[pr], threads[nt], average_time_mpi_pth[p, pr, nt], variance_time_mpi_pth[p, pr, nt])

# Get mpi+omp program times for different processes and threads
for nt in range(0, nthreads):
    for pr in range(0, nproc):
        for p in range(0, 2):
            filename = resultsdir+mpi_omp_programs_dir[p]+"_"+str(proc[pr])+"_omp_"+str(threads[nt])+logfile+str(size)+".log"
            #print(filename)
            file = open(filename,'r')
            sfile = file.read()
            k = 0
            for i in re.finditer('real', sfile):
                index = i.start()
                string = sfile[index:index+14]
                #print(string)
                string = string.replace('real','')
                string = string.replace('s','')
                string = string.replace(',','.')
                string = string.replace('  ','')
                index = string.find('m')
                times[k] = float(string[0:index])*60.0 + float(string[index+1:])
                #print(string[0:index], string[index+1:], times[k])
                k = k+1
                #print(np.shape(times))
            average_time_mpi_omp[p, pr, nt] = np.average(times)
            variance_time_mpi_omp[p, pr, nt] = np.var(times)
            #print(proc[pr], threads[nt], average_time_mpi_omp[p, pr, nt], variance_time_mpi_omp[p, pr, nt])

# Get pthreads program times for different threads
for nt in range(0, nthreads):
    for p in range(0, 2):
        filename = resultsdir+pth_programs_dir[p]+"_"+str(threads[nt])+logfile+str(size)+".log"
        #print(filename)
        file = open(filename,'r')
        sfile = file.read()
        k = 0
        for i in re.finditer('real', sfile):
            index = i.start()
            string = sfile[index:index+14]
            #print(string)
            string = string.replace('real','')
            string = string.replace('s','')
            string = string.replace(',','.')
            string = string.replace('  ','')
            index = string.find('m')
            times[k] = float(string[0:index])*60.0 + float(string[index+1:])
            #print(string[0:index], string[index+1:], times[k])
            k = k+1
            #print(np.shape(times))
        average_time_pth[p, nt] = np.average(times)
        variance_time_pth[p, nt] = np.var(times)
        #print(threads[nt], average_time_pth[p, nt], variance_time_pth[p, nt])

# Get omp program times for different threads
for nt in range(0, nthreads):
    for p in range(0, 2):
        filename = resultsdir+omp_programs_dir[p]+"_"+str(threads[nt])+logfile+str(size)+".log"
        #print(filename)
        file = open(filename,'r')
        sfile = file.read()
        k = 0
        for i in re.finditer('real', sfile):
            index = i.start()
            string = sfile[index:index+14]
            #print(string)
            string = string.replace('real','')
            string = string.replace('s','')
            string = string.replace(',','.')
            string = string.replace('  ','')
            index = string.find('m')
            times[k] = float(string[0:index])*60.0 + float(string[index+1:])
            #print(string[0:index], string[index+1:], times[k])
            k = k+1
            #print(np.shape(times))
        average_time_omp[p, nt] = np.average(times)
        variance_time_omp[p, nt] = np.var(times)
        #print(threads[nt], average_time_omp[p, nt], variance_time_omp[p, nt])


#------------------------------------------------------------------------------------
# Confidence interval level
confidence = 0.95
t_crit = np.abs(t.ppf((1-confidence)/2,measurements))

# Compute the confidence interval for sequential programs
confidence_interval_seq_left  = average_time_seq - variance_time_seq*t_crit/np.sqrt(measurements)
confidence_interval_seq_rigth = average_time_seq + variance_time_seq*t_crit/np.sqrt(measurements)
error_seq = confidence_interval_seq_rigth-confidence_interval_seq_left

# Compute the confidence interval for mpi programs
confidence_interval_mpi_left  = average_time_mpi - variance_time_mpi*t_crit/np.sqrt(measurements)
confidence_interval_mpi_rigth = average_time_mpi + variance_time_mpi*t_crit/np.sqrt(measurements)

# Compute the confidence interval for mpi+pth programs
confidence_interval_mpi_pth_left  = average_time_mpi_pth - variance_time_mpi_pth*t_crit/np.sqrt(measurements)
confidence_interval_mpi_pth_rigth = average_time_mpi_pth + variance_time_mpi_pth*t_crit/np.sqrt(measurements)

# Compute the confidence interval for mpi+omp programs
confidence_interval_mpi_omp_left  = average_time_mpi_omp - variance_time_mpi_omp*t_crit/np.sqrt(measurements)
confidence_interval_mpi_omp_rigth = average_time_mpi_omp + variance_time_mpi_omp*t_crit/np.sqrt(measurements)

# Compute the confidence interval for pth programs
confidence_interval_pth_left  = average_time_pth - variance_time_pth*t_crit/np.sqrt(measurements)
confidence_interval_pth_rigth = average_time_pth + variance_time_pth*t_crit/np.sqrt(measurements)

# Compute the confidence interval for omp programs
confidence_interval_omp_left  = average_time_omp - variance_time_omp*t_crit/np.sqrt(measurements)
confidence_interval_omp_rigth = average_time_omp + variance_time_omp*t_crit/np.sqrt(measurements)
#------------------------------------------------------------------------------------

average_time_seq = np.round(average_time_seq, 4)
variance_time_seq = np.round(variance_time_seq, 4)
confidence_interval_seq_left = np.round(confidence_interval_seq_left, 4)
confidence_interval_seq_rigth = np.round(confidence_interval_seq_rigth, 4)

average_time_mpi = np.round(average_time_mpi, 4)
variance_time_mpi = np.round(variance_time_mpi, 4)
confidence_interval_mpi_left = np.round(confidence_interval_mpi_left, 4)
confidence_interval_mpi_rigth = np.round(confidence_interval_mpi_rigth, 4)

average_time_mpi_pth = np.round(average_time_mpi_pth , 4)
variance_time_mpi_pth  = np.round(variance_time_mpi_pth , 4)
confidence_interval_mpi_pth_left = np.round(confidence_interval_mpi_pth_left, 4)
confidence_interval_mpi_pth_rigth = np.round(confidence_interval_mpi_pth_rigth, 4)

average_time_mpi_omp = np.round(average_time_mpi_omp , 4)
variance_time_mpi_omp  = np.round(variance_time_mpi_omp , 4)
confidence_interval_mpi_omp_left = np.round(confidence_interval_mpi_omp_left, 4)
confidence_interval_mpi_omp_rigth = np.round(confidence_interval_mpi_omp_rigth, 4)

average_time_pth = np.round(average_time_pth , 4)
variance_time_pth  = np.round(variance_time_pth , 4)
confidence_interval_pth_left = np.round(confidence_interval_pth_left, 4)
confidence_interval_pth_rigth = np.round(confidence_interval_pth_rigth, 4)

average_time_omp = np.round(average_time_omp , 4)
variance_time_omp  = np.round(variance_time_omp , 4)
confidence_interval_omp_left = np.round(confidence_interval_omp_left, 4)
confidence_interval_omp_rigth = np.round(confidence_interval_omp_rigth, 4)

p = 1
#print(average_time_seq[p], variance_time_seq[p], confidence_interval_seq_left[p], confidence_interval_seq_rigth[p])
for pr in range(0, nproc):
    #print(average_time_mpi[p,pr], variance_time_mpi[p,pr], confidence_interval_mpi_left[p,pr], confidence_interval_mpi_rigth[p,pr])
    for nt in range(0, nthreads):
        print(average_time_mpi_pth[p,pr,nt], variance_time_mpi_pth[p,pr,nt], confidence_interval_mpi_pth_left[p,pr,nt], confidence_interval_mpi_pth_rigth[p,pr,nt])
    print("------------------------------------------------------------------------------------")

for nt in range(0, nthreads):
    print(average_time_pth[p,nt], variance_time_pth[p,nt], confidence_interval_pth_left[p,nt], confidence_interval_pth_rigth[p,nt])


#------------------------------------------------------------------------------------
print("==========================================================================================")
p = 1
for pr in range(0, nproc):
    #print(average_time_mpi[p,pr], variance_time_mpi[p,pr], confidence_interval_mpi_left[p,pr], confidence_interval_mpi_rigth[p,pr])
    for nt in range(0, nthreads):
        print(average_time_mpi_omp[p,pr,nt], variance_time_mpi_omp[p,pr,nt], confidence_interval_mpi_omp_left[p,pr,nt], confidence_interval_mpi_omp_rigth[p,pr,nt])
    print("------------------------------------------------------------------------------------")

for nt in range(0, nthreads):
    print(average_time_omp[p,nt], variance_time_omp[p,nt], confidence_interval_omp_left[p,nt], confidence_interval_omp_rigth[p,nt])

#------------------------------------------------------------------------------------
# Time vs number of processes for each thread (for MPI+OMP programs)
colors = ('red', 'green', 'blue', 'purple', 'brown', 'orange')
markers = ('x','s','<','o','D','*')
titles = ('With IO', 'Without IO')
pfile = ('_io', '')
for p in range(0, 2):
    plt.plot(proc, average_time_mpi[p, :], color='black', marker='+', label='MPI')
    plt.xlabel('Number of processes')
    plt.ylabel('Time (seconds)')
    for nt in range(0, nthreads):
        plt.plot(proc, average_time_mpi_omp[p, :, nt], color=colors[nt], marker=markers[nt], label='MPI+OMP - '+str(threads[nt])+' threads')
    plt.ylim(10.0**(0.5), 10**(1.45))
    plt.legend()
    plt.grid(True, which="both")
    title = 'Region = Triple Spiral Valley, ' +titles[p]
    plt.title(title)
    filename = 'triple_mpi_omp_proc'+pfile[p]
    plt.savefig(graphdir+filename+'.png', format='png')
    plt.close()

# Time vs number of processes for each thread (for MPI+PTH programs)
colors = ('red', 'green', 'blue', 'purple', 'brown', 'orange')
markers = ('x','s','<','o','D','*')
titles = ('With IO', 'Without IO')
pfile = ('_io', '')
for p in range(0, 2):
    plt.plot(proc, average_time_mpi[p, :], color='black', marker='+', label='MPI')
    plt.xlabel('Number of processes')
    plt.ylabel('Time (seconds)')
    for nt in range(0, nthreads):
        plt.plot(proc, average_time_mpi_pth[p, :, nt], color=colors[nt], marker=markers[nt], label='MPI+PTH - '+str(threads[nt])+' threads')
    plt.ylim(10.0**(0.5), 10**(1.45))
    plt.legend()
    plt.grid(True, which="both")
    title = 'Region = Triple Spiral Valley, ' +titles[p]
    plt.title(title)
    filename = 'triple_mpi_pth_proc'+pfile[p]
    plt.savefig(graphdir+filename+'.png', format='png')
    plt.close()

# Time vs number of processes for each thread (for MPI+OMP programs)
colors = ('red', 'green', 'blue', 'purple', 'brown', 'orange')
markers = ('x','s','<','o','D','*')
titles = ('With IO', 'Without IO')
pfile = ('_io', '')
for p in range(0, 2):
    plt.plot(threads, average_time_omp[p, :], color='black', marker='+', label='OMP')
    plt.xlabel('Number of threads')
    plt.ylabel('Time (seconds)')
    for pr in range(0, nproc):
        plt.plot(threads, average_time_mpi_omp[p, pr, :], color=colors[pr], marker=markers[pr], label='MPI+OMP - '+str(proc[pr])+' processes')
    plt.ylim(10.0**(0.5), 10**(1.45))
    plt.legend()
    plt.grid(True, which="both")
    title = 'Region = Triple Spiral Valley, ' +titles[p]
    plt.title(title)
    filename = 'triple_mpi_omp_threads'+pfile[p]
    plt.savefig(graphdir+filename+'.png', format='png')
    plt.close()

# Time vs number of processes for each thread (for MPI+PTH programs)
colors = ('red', 'green', 'blue', 'purple', 'brown', 'orange')
markers = ('x','s','<','o','D','*')
titles = ('With IO', 'Without IO')
pfile = ('_io', '')
for p in range(0, 2):
    plt.plot(threads, average_time_pth[p, :], color='black', marker='+', label='PTH')
    plt.xlabel('Number of threads')
    plt.ylabel('Time (seconds)')
    for pr in range(0, nproc):
        plt.plot(threads, average_time_mpi_pth[p, pr, :], color=colors[pr], marker=markers[pr], label='MPI+PTH - '+str(proc[pr])+' processes')
    plt.ylim(10.0**(0.5), 10**(1.45))
    plt.legend()
    plt.grid(True, which="both")
    title = 'Region = Triple Spiral Valley, ' +titles[p]
    plt.title(title)
    filename = 'triple_mpi_pth_threads'+pfile[p]
    plt.savefig(graphdir+filename+'.png', format='png')
    plt.close()
