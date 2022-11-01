/******************************************************************** 
EP2 - MAC5742 2022
Luan da Fonseca Santos 8556613 
Versão MPI sem input/output
********************************************************************/
#include "mpi.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define  MASTER 0

double c_x_min;
double c_x_max;
double c_y_min;
double c_y_max;

double pixel_width;
double pixel_height;

int iteration_max = 200;

int image_size;
unsigned char *image_buffer_r;
unsigned char *image_buffer_g;
unsigned char *image_buffer_b;

int i_x_max;
int i_y_max;
int image_buffer_size;

int gradient_size = 16;
int colors[17][3] = {
                        {66, 30, 15},
                        {25, 7, 26},
                        {9, 1, 47},
                        {4, 4, 73},
                        {0, 7, 100},
                        {12, 44, 138},
                        {24, 82, 177},
                        {57, 125, 209},
                        {134, 181, 229},
                        {211, 236, 248},
                        {241, 233, 191},
                        {248, 201, 95},
                        {255, 170, 0},
                        {204, 128, 0},
                        {153, 87, 0},
                        {106, 52, 3},
                        {16, 16, 16},
                    };

void allocate_image_buffer(){
    int rgb_size = 3;
    image_buffer_r = (unsigned char *) malloc(sizeof(unsigned char ) * image_buffer_size);
    image_buffer_g = (unsigned char *) malloc(sizeof(unsigned char ) * image_buffer_size);
    image_buffer_b = (unsigned char *) malloc(sizeof(unsigned char ) * image_buffer_size);
};

void init(int argc, char *argv[]){
    if(argc < 6){
        printf("usage: ./mandelbrot_omp c_x_min c_x_max c_y_min c_y_max image_size\n");
        printf("examples with image_size = 11500:\n");
        printf("    Full Picture:         ./mandelbrot_omp -2.5 1.5 -2.0 2.0 11500\n");
        printf("    Seahorse Valley:      ./mandelbrot_omp -0.8 -0.7 0.05 0.15 11500\n");
        printf("    Elephant Valley:      ./mandelbrot_omp 0.175 0.375 -0.1 0.1 11500\n");
        printf("    Triple Spiral Valley: ./mandelbrot_omp -0.188 -0.012 0.554 0.754 11500\n");
        exit(0);
    }
    else{
        sscanf(argv[1], "%lf", &c_x_min);
        sscanf(argv[2], "%lf", &c_x_max);
        sscanf(argv[3], "%lf", &c_y_min);
        sscanf(argv[4], "%lf", &c_y_max);
        sscanf(argv[5], "%d", &image_size);

        i_x_max           = image_size;
        i_y_max           = image_size;
        image_buffer_size = image_size * image_size;

        pixel_width       = (c_x_max - c_x_min) / i_x_max;
        pixel_height      = (c_y_max - c_y_min) / i_y_max;
    };
};

void update_rgb_buffer(int iteration, int x, int y){
    int color;

    if(iteration == iteration_max){
        image_buffer_r[(i_y_max * y) + x] = colors[gradient_size][0];
        image_buffer_g[(i_y_max * y) + x] = colors[gradient_size][1];
        image_buffer_b[(i_y_max * y) + x] = colors[gradient_size][2];
    }
    else{
        color = iteration % gradient_size;
        image_buffer_r[(i_y_max * y) + x] = colors[color][0];
        image_buffer_g[(i_y_max * y) + x] = colors[color][1];
        image_buffer_b[(i_y_max * y) + x] = colors[color][2];
    };
};

void write_to_file(){
    FILE * file;
    char * filename               = "output_mpi.ppm"; /* Figura do output*/
    char * comment                = "# ";

    int max_color_component_value = 255;

    file = fopen(filename,"wb");

    fprintf(file, "P6\n %s\n %d\n %d\n %d\n", comment,
            i_x_max, i_y_max, max_color_component_value);

    for(int i = 0; i < image_buffer_size; i++){
        fwrite(&image_buffer_r[i], 1 , 1, file);
        fwrite(&image_buffer_g[i], 1 , 1, file);
        fwrite(&image_buffer_b[i], 1 , 1, file);
    };

    fclose(file);
};


/******************************************************************** 
 Implentação usando MPI - atribui a cada processo a sua região
 em que irá calcular os pixels
 Baseado em https://github.com/phrb/PPD/blob/main/lectures/tex/mpi/code_samples/mpi_array/mpi_array.c
********************************************************************/
void compute_mandelbrot(int argc, char *argv[]){
    void mandelbrot();
    int   numtasks, taskid, rc, dest, i, j, k, tag1,
        tag2, source, chunksize, leftover;

    int tag_r, tag_g, tag_b;
    int i_y0, i_yend;
    
    MPI_Status status;

    /***** Initializations *****/
    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &numtasks);
    MPI_Comm_rank(MPI_COMM_WORLD, &taskid);
    //printf ("MPI task %d from %d has started...\n", taskid, numtasks);
    chunksize = (image_size / numtasks);
    leftover = (image_size % numtasks);
    tag1 = 1;
    tag2 = 2;
    tag_r = 3;
    tag_g = 4;
    tag_b = 5;

    /***** Master task only ******/
    if (taskid == MASTER){
        /* Send each task its portion of the array - master keeps 1st part plus leftover elements */
        i_y0 = chunksize + leftover;
        i_yend = i_y0 + chunksize;

        for (dest=1; dest<numtasks; dest++) {
            MPI_Send(&i_y0, 1, MPI_INT, dest, tag1, MPI_COMM_WORLD);
            MPI_Send(&i_yend, 1, MPI_INT, dest, tag2, MPI_COMM_WORLD);      
            i_y0 = i_yend;
            i_yend = i_yend + chunksize;
        }    

        /* Master does its part of the work */
        i_y0 = 0;
        i_yend = chunksize + leftover;
        //printf("Master %d works on = %d, %d, %d\n", taskid, i_y0, i_yend, i_yend-i_y0);
        mandelbrot(i_y0, i_yend);

        /* Wait to receive results from each task */
        for (i=1; i<numtasks; i++) {
            source = i;
            MPI_Recv(&i_y0, 1, MPI_INT, source, tag1, MPI_COMM_WORLD, &status);
            MPI_Recv(&i_yend, 1, MPI_INT, source, tag2, MPI_COMM_WORLD, &status);            
            //MPI_Recv(&image_buffer_r[i_y_max*i_y0], chunksize*image_size, MPI_UNSIGNED_CHAR, source, tag_r, MPI_COMM_WORLD, &status);
            //MPI_Recv(&image_buffer_g[i_y_max*i_y0], chunksize*image_size, MPI_UNSIGNED_CHAR, source, tag_g, MPI_COMM_WORLD, &status);
            //MPI_Recv(&image_buffer_b[i_y_max*i_y0], chunksize*image_size, MPI_UNSIGNED_CHAR, source, tag_b, MPI_COMM_WORLD, &status);
        }
        //write_to_file();
    }
    
    
    /***** Non-master tasks only *****/
    if (taskid > MASTER) {
        /* Receive my portion of array from the master task */
        source = MASTER;
        MPI_Recv(&i_y0, 1, MPI_INT, source, tag1, MPI_COMM_WORLD, &status);
        MPI_Recv(&i_yend, 1, MPI_INT, source, tag2, MPI_COMM_WORLD, &status);
        //printf("Task %d works on = %d, %d, %d\n", taskid, i_y0, i_yend, i_yend-i_y0);
        /* Do my part of the work */
        mandelbrot(i_y0, i_yend);
        //printf("Task %d is done! \n", taskid);
        /* Send my results back to the master task */
        dest = MASTER;
        MPI_Send(&i_y0, 1, MPI_INT, dest, tag1, MPI_COMM_WORLD);
        MPI_Send(&i_yend, 1, MPI_INT, dest, tag2, MPI_COMM_WORLD);
        //MPI_Send(&image_buffer_r[i_y_max*i_y0], chunksize*image_size, MPI_UNSIGNED_CHAR, dest, tag_r, MPI_COMM_WORLD);
        //MPI_Send(&image_buffer_g[i_y_max*i_y0], chunksize*image_size, MPI_UNSIGNED_CHAR, dest, tag_g, MPI_COMM_WORLD);
        //MPI_Send(&image_buffer_b[i_y_max*i_y0], chunksize*image_size, MPI_UNSIGNED_CHAR, dest, tag_b, MPI_COMM_WORLD);
    }

    MPI_Finalize();
};

/******************************************************************** 
Calcula o conjunto de mandebrot para pixels com coordenada y entre
i_y0 e i_yend. Esta é a tarefa de cada processo
********************************************************************/
void mandelbrot(int i_y0, int i_yend){
    double z_x;
    double z_y;
    double z_x_squared;
    double z_y_squared;
    double escape_radius_squared = 4;

    int iteration;
    int i_x;
    int i_y;

    double c_x;
    double c_y;

    for(i_y = i_y0; i_y < i_yend; i_y++){
        c_y = c_y_min + i_y * pixel_height;

        if(fabs(c_y) < pixel_height / 2){
            c_y = 0.0;
        };

        for(i_x = 0; i_x < i_x_max; i_x++){
            c_x         = c_x_min + i_x * pixel_width;

            z_x         = 0.0;
            z_y         = 0.0;

            z_x_squared = 0.0;
            z_y_squared = 0.0;

            for(iteration = 0;
                iteration < iteration_max && \
                ((z_x_squared + z_y_squared) < escape_radius_squared);
                iteration++){
                z_y         = 2 * z_x * z_y + c_y;
                z_x         = z_x_squared - z_y_squared + c_x;

                z_x_squared = z_x * z_x;
                z_y_squared = z_y * z_y;
            };

            //update_rgb_buffer(iteration, i_x, i_y);
        };
    };

};

int main(int argc, char *argv[]){
    init(argc, argv);

    //allocate_image_buffer();

    compute_mandelbrot(argc, argv);

    return 0;
};
