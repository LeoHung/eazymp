#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <omp.h>

typedef struct Data{
    int r;
    int g;
    int b;
} Data;

Data* mandelbrot(int row, int col, int size_x, int size_y){
    float x0;
    float y0;
    float x, y, xtemp;
    int iteration, maxiteration;
    int color;

    Data *data = (Data *) malloc(sizeof(Data));

    x0 = ((float)(row) / (float)(size_x)) * 3.5 - 2.5;
    y0 = ((float)(col) / (float)(size_y)) * 2.0 - 1.0;

    x = 0;
    y = 0;
    iteration = 0;
    maxiteration = 1000;
    while((x * x + y * y) < 4 && (iteration < maxiteration)){
        xtemp = x * x - y * y + x0 ;
        y = 2.0 * x * y + y0;
        x = xtemp;
        iteration = iteration + 1;
        color = iteration % 255 ;
        data->r = color;
        data->g = (color + 75) % 255;
        data->b = (color + 150) % 255;
    }

    return data;
}

int main(int argc, char **argv){
    int size_x = 0;
    int size_y = 0;
    Data ** data;

    if(argc < 2){
        printf("[Error] please specify the size of mandelbrot.\n");
        exit(0);
    }

    size_x = atoi(argv[1]);
    size_y = atoi(argv[1]);

    data = (Data **) malloc(sizeof(Data *) * size_x);

    for(int row = 0; row < size_x; row++){
        data[row] = (Data *) malloc(sizeof(Data) * size_y);
    }

    #pragma omp parallel for
    for(int row = 0; row < size_x; row++){
        for(int col = 0; col < size_y; col++){
            Data *tmp = mandelbrot(row, col, size_x, size_y);
            data[row][col].r = tmp->r;
            data[row][col].g = tmp->g;
            data[row][col].b = tmp->b;
        }
    }
    //#pragma omp barrier  
    //for(row = 0; row < size_x; row++){
    //    free(data[row]);
    //}
    free(data);
    
    //printf("Testing\n");
    return 0;
}
