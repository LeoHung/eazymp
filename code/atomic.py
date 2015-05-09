
def function():

    from lazymp.atmoic import Atomic

    with Atomic():
        ... critical section

>>>>>>>>>>>>>> after translate >>>>>>>>>>>>>>>>>>>


def function():

    from multiprocessing import Manager
    _manager = Manager()
    _lock = _manager.Lock()

    with __lock:
        ... critical section





