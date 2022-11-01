import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import t

#------------------------------------------------------------------------------------
# Parameters
tabledir = "tables/"
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

parallel_program_filename = ("pth", "omp")


#------------------------------------------------------------------------------------
# Load the numpy data
average_time_parallel =  np.load(datadir+"average_time_parallel.npy")
variance_time_parallel =  np.load(datadir+"variance_time_parallel.npy")
average_time_seq =  np.load(datadir+"average_time_seq.npy")
variance_time_seq=  np.load(datadir+"variance_time_seq.npy")

#------------------------------------------------------------------------------------
# Confidence interval level
confidence = 0.95
t_crit = np.abs(t.ppf((1-confidence)/2,measurements))

# Compute the confidence interval for sequential programs
confidence_interval_seq_left  = average_time_seq - variance_time_seq*t_crit/np.sqrt(measurements)
confidence_interval_seq_rigth = average_time_seq + variance_time_seq*t_crit/np.sqrt(measurements)
error_seq = confidence_interval_seq_rigth-confidence_interval_seq_left

# Compute the confidence interval for sequential programs
confidence_interval_parallel_left  = average_time_parallel - variance_time_parallel*t_crit/np.sqrt(measurements)
confidence_interval_parallel_rigth = average_time_parallel + variance_time_parallel*t_crit/np.sqrt(measurements)

#------------------------------------------------------------------------------------
# Write sequential time data in excel files

data_array = np.zeros((10, 9))
l=[('Tamanho da entrada', ''), ('Com I/O', 'Tempo médio'),  ('Com I/O', 'Variância'), ('Com I/O', 'Intervalo'), ('Com I/O', ''), ('Sem I/O', 'Tempo médio'),  ('Sem I/O','Variância'), ('Sem I/O','Intervalo'), ('Sem I/O','')]
for reg in range(0, nregions):
    data_array[:, 0] = sizes
    data_array[:, 1] = average_time_seq[reg, 0, :]
    data_array[:, 2] = variance_time_seq[reg, 0, :]
    data_array[:, 3] = confidence_interval_seq_left[reg, 0, :]
    data_array[:, 4] = confidence_interval_seq_rigth[reg, 0, :]
    data_array[:, 5] = average_time_seq[reg, 1, :]
    data_array[:, 6] = variance_time_seq[reg, 1, :]
    data_array[:, 7] = confidence_interval_seq_left[reg, 1, :]
    data_array[:, 8] = confidence_interval_seq_rigth[reg, 1, :]
    data_array = np.round(data_array, 9)
    df = pd.DataFrame(data_array, columns = l)
    df.columns = pd.MultiIndex.from_tuples(df.columns, names=['',''])
    df.to_excel(tabledir+"sequencial_"+regions[reg]+".xlsx")


l=[('Tamanho da entrada', ''),
   ('1 threads - Com I/O', 'Tempo médio'),  ('', 'Variância'), ('', 'Intervalo'), ('',''),
   ('1 threads - Sem I/O', 'Tempo médio'),  ('', 'Variância'), ('', 'Intervalo'), ('',''),
   ('2 threads - Com I/O', 'Tempo médio'),  ('', 'Variância'), ('', 'Intervalo'), ('',''),
   ('2 threads - Sem I/O', 'Tempo médio'),  ('', 'Variância'), ('', 'Intervalo'), ('',''),
   ('4 threads - Com I/O', 'Tempo médio'),  ('', 'Variância'), ('', 'Intervalo'), ('',''),
   ('4 threads - Sem I/O', 'Tempo médio'),  ('', 'Variância'), ('', 'Intervalo'), ('',''),
   ('8 threads - Com I/O', 'Tempo médio'),  ('', 'Variância'), ('', 'Intervalo'), ('',''),
   ('8 threads - Sem I/O', 'Tempo médio'),  ('', 'Variância'), ('', 'Intervalo'), ('',''),
   ('16 threads - Com I/O', 'Tempo médio'), ('', 'Variância'), ('', 'Intervalo'), ('',''),
   ('16 threads - Sem I/O', 'Tempo médio'), ('', 'Variância'), ('', 'Intervalo'), ('',''),
   ('32 threads - Com I/O', 'Tempo médio'), ('', 'Variância'), ('', 'Intervalo'), ('',''),
   ('32 threads - Sem I/O', 'Tempo médio'), ('', 'Variância'), ('', 'Intervalo'), ('','')]

data_array = np.zeros((10, 49))
for reg in range(0, nregions):
    col = 0
    for nt in range(0, nthreads):
        data_array[:, 0] = sizes
        for p in range(0, 2):
         #   print(1+col, 2+col, 3+col, 4+col)
            data_array[:, 1+col] = average_time_parallel[reg, nt, 0, :]
            data_array[:, 2+col] = variance_time_parallel[reg, nt, 0, :]
            data_array[:, 3+col] = confidence_interval_parallel_left[reg, nt,  0,:]
            data_array[:, 4+col] = confidence_interval_parallel_rigth[reg, nt, 0, :]
            data_array[:, 5+col] = average_time_parallel[reg, nt, 2, :]
            data_array[:, 6+col] = variance_time_parallel[reg, nt, 2, :]
            data_array[:, 7+col] = confidence_interval_parallel_left[reg, nt,  2,:]
            data_array[:, 8+col] = confidence_interval_parallel_rigth[reg, nt, 2, :]
            data_array = np.round(data_array, 9)
            df = pd.DataFrame(data_array, columns = l)
            df.columns = pd.MultiIndex.from_tuples(df.columns, names=['',''])
            df.to_excel(tabledir+parallel_program_filename[0]+"_"+regions[reg]+".xlsx")
        col = col+8

data_array = np.zeros((10, 49))
for reg in range(0, nregions):
    col = 0
    for nt in range(0, nthreads):
        data_array[:, 0] = sizes
        for p in range(0, 2):
         #   print(1+col, 2+col, 3+col, 4+col)
            data_array[:, 1+col] = average_time_parallel[reg, nt, 1, :]
            data_array[:, 2+col] = variance_time_parallel[reg, nt, 1, :]
            data_array[:, 3+col] = confidence_interval_parallel_left[reg, nt,  1,:]
            data_array[:, 4+col] = confidence_interval_parallel_rigth[reg, nt, 1, :]
            data_array[:, 5+col] = average_time_parallel[reg, nt, 3, :]
            data_array[:, 6+col] = variance_time_parallel[reg, nt, 3, :]
            data_array[:, 7+col] = confidence_interval_parallel_left[reg, nt,  3,:]
            data_array[:, 8+col] = confidence_interval_parallel_rigth[reg, nt, 3, :]
            data_array = np.round(data_array, 9)
            df = pd.DataFrame(data_array, columns = l)
            df.columns = pd.MultiIndex.from_tuples(df.columns, names=['',''])
            df.to_excel(tabledir+parallel_program_filename[1]+"_"+regions[reg]+".xlsx")
        col = col+8        
for reg in range(0, nregions):
    for nt in range(0, nthreads):
        print(regions[reg], nt, confidence_interval_parallel_left[reg,nt,2,9], confidence_interval_parallel_rigth[reg,nt,2,9])
        print(regions[reg], nt, confidence_interval_parallel_left[reg,nt,0,9], confidence_interval_parallel_rigth[reg,nt,0,9])
