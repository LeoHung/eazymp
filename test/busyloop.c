#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv){
    int l_i = 0;
    int l = 0;
    int i = 0;

    if(argc < 2){
        printf("Error: please specify the work size.\n");
        exit(0);
    }

    l = atoi(argv[1]);

    #pragma omp parallel for private(l_i) private(i)
    for(l_i = 0; l_i < l; l_i++){
        i = 0;
        while(i < 5000 * 1000){
            i+=1;
        }
    }

    return 0;
}