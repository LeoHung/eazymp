from lazymp.helpers import join_dict
from lazymp.helpers import join_shared
import os
import re
import os.path
from datetime import datetime
def top1(dir_path):
    top1_value = None
    for filename in os.listdir(dir_path):
        path = dir_path + "/" + filename
        if os.path.isfile(path):
            f = open(path, "r")
            for l in f:
                v = int(l)
                if top1_value == None or v > top1_value:
                    top1_value = v
            f.close()
    return top1_value

def top1_mp(dir_path, num_process):
    top1_value = None

    from multiprocessing import Manager
    __manager = Manager()
    __lock = __manager.Lock()

    ns = __manager.Namespace()
    ns.top1_value = top1_value

    def core(filename):
        path = dir_path + "/" + filename
        if os.path.isfile(path):
            f = open(path, "r")
            for l in f:
                v = int(l)
                with __lock:
                    if ns.top1_value == None or v > ns.top1_value:
                        ns.top1_value = v
            f.close()

    from pathos.multiprocessing import ProcessingPool
    ProcessingPool(num_process).map(core, os.listdir(dir_path))

    return top1_value

def main(argv):
    dir_path = argv[1]
    num_process = int(argv[2])

    # original version
    start = datetime.now()
    resultA = top1(dir_path)
    end = datetime.now()
    slow_time = (end - start).total_seconds()

    # multi-process version
    start = datetime.now()
    resultB = top1_mp(dir_path, num_process)
    end = datetime.now()
    fast_time = (end - start).total_seconds()

    # check if result is correct
    if resultA != resultB:
      print "ERROR: results do not match!"
      exit(0)

    # print "slow runtime: %s, max %d" % (str(slow_time), resultA)
    print "fast runtime: %s, max %d" % (str(fast_time), resultB)
    print "speed up: %f" % (slow_time / fast_time)

if __name__ == "__main__":
    import sys
    main(sys.argv)
