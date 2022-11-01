import imageio.v2 as imageio
import numpy as np
import subprocess
import os

sizes = (2**4, 2**5, 2**6, 2**7, 2**8, 2**9, 2**10, 2**11, 2**12, 2**13)
threads = (1, 2, 4, 8, 16, 32)

parallel_programs = ("./mandelbrot_pth_io", "./mandelbrot_omp_io")
sequential_program = "./mandelbrot_seq_io"

nsize = len(sizes)
input_mandelbrot =  ["2.5 1.5 -2.0 2.0", "-0.8 -0.7 0.05 0.15", "0.175 0.375 -0.1 0.1", "-0.188 -0.012 0.554 0.754"]

filename_seq = "output_seq.ppm"
filename_pth = "output_pth.ppm"
filename_omp = "output_omp.ppm"

subprocess.check_call(['make'])

for size in sizes:
    for input in input_mandelbrot:
        print("Running "+sequential_program+"  "+input+"  "+str(size))
        subprocess.run(sequential_program+"  "+input+"  "+str(size), shell=True)
        img_seq = imageio.imread(filename_seq)
        # Run parallel_programs
        for nthread in threads:
            print("Running "+parallel_programs[0]+"  "+input+"  "+str(size)+"  "+str(nthread))
            subprocess.run(parallel_programs[0]+" "+input+"  "+str(size)+"  "+str(nthread), shell=True)
            img_pth = imageio.imread(filename_pth)

            print("Running "+parallel_programs[1]+"  "+input+"  "+str(size)+"  "+str(nthread))
            subprocess.run(parallel_programs[1]+" "+input+"  "+str(size)+"  "+str(nthread), shell=True)
            img_omp = imageio.imread(filename_omp)
            os.remove(filename_pth)
            os.remove(filename_omp)
            error_pth = np.amax(abs(img_pth-img_seq))
            error_omp = np.amax(abs(img_omp-img_seq))
            if (error_omp !=0 or error_pth != 0):
               print("Error found!")
               exit()
        os.remove(filename_seq)
