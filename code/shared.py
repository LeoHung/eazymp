def function():

    my_dict = dict() #pragma shared dict

    for i in range(100):
        ... do something ...

        from eazymp.atomic import Atomic
        with Atomic():
            my_dict[i] = result

>>>>>>>>>>>>>> after translate >>>>>>>>>>>>>>>>>>>

def function():

    my_dict = dict()

    # launch a shared dictionary proxy for my dict
    from multiprocessing import Manager
    _manager = Manager()
    proxy_my_dict = _manager.dict()
    _lock = _manager.Lock()

    def core(i):
        ... do something ...
        # replace my_dict with proxy
        with _lock:
            proxy_my_dict[i] = result

    from pathos.multiprocessing import ProcessingPool
    ProcessingPool(num_process).map(core, range(100))

    # copy the data from proxy to the original dictionary
    for k, v in proxy_my_dict.items():
        my_dict[k] = v