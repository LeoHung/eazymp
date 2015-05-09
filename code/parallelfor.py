for i in range(1000): #pragma omp parallel for

    ... do something

>>>>>>>>>>>>>> after translate >>>>>>>>>>>>>>>>>>>

def core(i):

    ... do something

from pathos.multiprocessing import ProcessingPool
ProcessingPool(num_process).map(core, range(1000))