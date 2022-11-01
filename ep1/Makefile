OUTPUT=mandelbrot

IMAGE=.ppm

CC=gcc
CC_OPT=-std=c11

CC_OMP=-fopenmp
CC_PTH=-pthread

.PHONY: all
all: $(OUTPUT)_omp $(OUTPUT)_pth $(OUTPUT)_seq $(OUTPUT)_omp_io $(OUTPUT)_pth_io $(OUTPUT)_seq_io

$(OUTPUT)_omp: $(OUTPUT)_omp.c
	$(CC) -o $(OUTPUT)_omp $(CC_OPT) $(CC_OMP) $(OUTPUT)_omp.c

$(OUTPUT)_pth: $(OUTPUT)_pth.c
	$(CC) -o $(OUTPUT)_pth $(CC_OPT) $(CC_PTH) $(OUTPUT)_pth.c

$(OUTPUT)_seq: $(OUTPUT)_seq.c
	$(CC) -o $(OUTPUT)_seq $(CC_OPT) $(OUTPUT)_seq.c

$(OUTPUT)_omp_io: $(OUTPUT)_omp_io.c
	$(CC) -o $(OUTPUT)_omp_io $(CC_OPT) $(CC_OMP) $(OUTPUT)_omp_io.c

$(OUTPUT)_pth_io: $(OUTPUT)_pth_io.c
	$(CC) -o $(OUTPUT)_pth_io $(CC_OPT) $(CC_PTH) $(OUTPUT)_pth_io.c

$(OUTPUT)_seq_io: $(OUTPUT)_seq_io.c
	$(CC) -o $(OUTPUT)_seq_io $(CC_OPT) $(OUTPUT)_seq_io.c


.PHONY: clean
clean:
	rm $(OUTPUT)_omp $(OUTPUT)_pth $(OUTPUT)_seq 
	rm $(OUTPUT)_omp_io $(OUTPUT)_pth_io $(OUTPUT)_seq_io *$(IMAGE)
