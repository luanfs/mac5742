import numpy as np
import re

#------------------------------------------------------------------------------------
datadir = "data/"
resultsdir = "results/"
measurements = 10

sizes = (2**4, 2**5, 2**6, 2**7, 2**8, 2**9, 2**10, 2**11, 2**12, 2**13)
iterations = len(sizes)

threads = (1, 2, 4, 8, 16, 32)
nthreads = len(threads)

sequential_programs_dir = ("mandelbrot_seq_io", "mandelbrot_seq")
parallel_programs_dir = ("mandelbrot_pth_io", "mandelbrot_omp_io", "mandelbrot_pth", "mandelbrot_omp")

regions  = ('Full', 'Seahorse', 'Elephant', 'Triple Spiral')
logfiles = ('/full', '/seahorse', '/elephant', '/triple_spiral')
nregions = len(regions)

average_time_parallel = np.zeros((len(regions), len(threads), 4, iterations))
average_time_seq = np.zeros((len(regions), 2, iterations))

variance_time_parallel = np.zeros((len(regions), len(threads), 4, iterations))
variance_time_seq = np.zeros((len(regions), 2, iterations))

times = np.zeros(measurements)

for s in range(0, iterations):
    for reg in range(0, nregions):
        # Get sequential program times
        for p in range(0, 2):
            filename = resultsdir+sequential_programs_dir[p]+logfiles[reg]+str(sizes[s])+".log"
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
                #print(string, string[0:index], string[index+1:], times[k])
                k = k+1
            average_time_seq[reg, p, s] = np.average(times)
            variance_time_seq[reg, p, s] = np.var(times)
            #print(average_time_seq[reg, p ,s], variance_time_seq[reg, p ,s])

        # Get parallel program times for different threads
        for nt in range(0, nthreads):
            for p in range(0, 4):
                filename = resultsdir+parallel_programs_dir[p]+"_"+str(threads[nt])+logfiles[reg]+str(sizes[s])+".log"
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
                average_time_parallel[reg, nt, p, s] = np.average(times)
                variance_time_parallel[reg, nt, p, s] = np.var(times)
                #print(average_time_parallel[reg, nt, p ,s], variance_time_parallel[reg, nt, p ,s])

np.save(datadir+"average_time_seq", average_time_seq)
np.save(datadir+"variance_time_seq", variance_time_seq)
np.save(datadir+"average_time_parallel", average_time_parallel)
np.save(datadir+"variance_time_parallel", variance_time_parallel)
