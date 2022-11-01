OUTPUT=mandelbrot

IMAGE=.ppm

CC=gcc
MCC=mpicc
CC_OPT=-std=c11
CC_OMP=-fopenmp
CC_PTH=-pthread

.PHONY: all
all: $(OUTPUT)_seq $(OUTPUT)_seq_io $(OUTPUT)_pth $(OUTPUT)_pth_io  $(OUTPUT)_omp $(OUTPUT)_omp_io $(OUTPUT)_mpi $(OUTPUT)_mpi_io $(OUTPUT)_mpi_pth $(OUTPUT)_mpi_pth_io $(OUTPUT)_mpi_omp $(OUTPUT)_mpi_omp_io


$(OUTPUT)_seq: $(OUTPUT)_seq.c
	$(CC) -o $(OUTPUT)_seq $(CC_OPT) $(OUTPUT)_seq.c

$(OUTPUT)_seq_io: $(OUTPUT)_seq_io.c
	$(CC) -o $(OUTPUT)_seq_io $(CC_OPT) $(OUTPUT)_seq_io.c

$(OUTPUT)_pth: $(OUTPUT)_pth.c
	$(CC) -o $(OUTPUT)_pth $(CC_OPT) $(CC_PTH) $(OUTPUT)_pth.c

$(OUTPUT)_pth_io: $(OUTPUT)_pth_io.c
	$(CC) -o $(OUTPUT)_pth_io $(CC_OPT) $(CC_PTH) $(OUTPUT)_pth_io.c

$(OUTPUT)_omp: $(OUTPUT)_omp.c
	$(CC) -o $(OUTPUT)_omp $(CC_OPT) $(CC_OMP) $(OUTPUT)_omp.c

$(OUTPUT)_omp_io: $(OUTPUT)_omp_io.c
	$(CC) -o $(OUTPUT)_omp_io $(CC_OPT) $(CC_OMP) $(OUTPUT)_omp_io.c

$(OUTPUT)_mpi: $(OUTPUT)_mpi.c
	$(MCC) -o $(OUTPUT)_mpi $(CC_OPT) $(OUTPUT)_mpi.c

$(OUTPUT)_mpi_io: $(OUTPUT)_mpi_io.c
	$(MCC) -o $(OUTPUT)_mpi_io $(CC_OPT) $(OUTPUT)_mpi_io.c

$(OUTPUT)_mpi_pth: $(OUTPUT)_mpi_pth.c
	$(MCC) $(CC_PTH) -o $(OUTPUT)_mpi_pth $(CC_OPT) $(OUTPUT)_mpi_pth.c

$(OUTPUT)_mpi_pth_io: $(OUTPUT)_mpi_pth_io.c
	$(MCC) $(CC_PTH) -o $(OUTPUT)_mpi_pth_io $(CC_OPT) $(OUTPUT)_mpi_pth_io.c

$(OUTPUT)_mpi_omp: $(OUTPUT)_mpi_omp.c
	$(MCC) $(CC_OMP) -o $(OUTPUT)_mpi_omp $(CC_OPT) $(OUTPUT)_mpi_omp.c

$(OUTPUT)_mpi_omp_io: $(OUTPUT)_mpi_omp_io.c
	$(MCC) $(CC_OMP) -o $(OUTPUT)_mpi_omp_io $(CC_OPT) $(OUTPUT)_mpi_omp_io.c


.PHONY: clean
clean:
	rm $(OUTPUT)_omp $(OUTPUT)_pth
	rm $(OUTPUT)_omp_io $(OUTPUT)_pth_io
	rm $(OUTPUT)_seq $(OUTPUT)_seq_io 
	rm $(OUTPUT)_mpi $(OUTPUT)_mpi_io 
	rm $(OUTPUT)_mpi_pth $(OUTPUT)_mpi_pth_io 
	rm $(OUTPUT)_mpi_omp $(OUTPUT)_mpi_omp_io 
	rm *$(IMAGE)
