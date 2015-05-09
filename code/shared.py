def function():

    my_dict = dict() #pragma shared

    for i in range(100):
        ... do something ...

        my_dict[i] = result

>>>>>>>>>>>>>> after translate >>>>>>>>>>>>>>>>>>>

def function():

    my_dict = dict()

    # launch a shared dictionary proxy for my dict
    from multiprocessing import Manager
    _manager = Manager()
    _shared_my_dict = _manager.dict()

    for i in range(100):
        ... do something ...
        # replace my_dict with proxy
        _shared_my_dict[i] = result

    # copy the data from proxy to the original dictionary
    for k, v in _shared_my_dict.items():
        my_dict[k] = v