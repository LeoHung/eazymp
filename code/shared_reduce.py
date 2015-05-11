def function():

    my_dict = dict() #pragma shared dict reduce

    for i in range(100): #pragma omp parallel for
        ... do something ...

        my_dict[i] = result

>>>>>>>>>>>>>> after translate >>>>>>>>>>>>>>>>>>>

def function():

    my_dict = dict() #pragma shared reduce

    def core():
        import copy
        __shared__ = dict()
        __shared__['my_dict'] = copy.deepcopy(my_dict)

        ... do something ...

        __shared__['my_dict'][i] = result
        return __shared__

    from pathos.multiprocessing import ProcessingPool
    __shared__ = ProcessingPool(num_process).map(core, range(100))

    # store data back from __shared__['my_dict'] to my_dict
    join_shared(__shared__, {'my_dict': my_dict})



