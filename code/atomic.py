
def function():

    from eazymp.atmoic import Atomic
    with Atomic():
        ... critical section

>>>>>>>>>>>>>> after translate >>>>>>>>>>>>>>>>>>>


def function():

    from multiprocessing import Manager
    _manager = Manager()
    _lock = _manager.Lock()

    with _lock:
        ... critical section





