from experiment import Desc, Experiment


if __name__ == "__main__":
    print "BusyLoop-openmp: work size x speedup"
    for size in [50, 100, 200, 300, 400, 500]:
        print "Size: %d" % size
        exp = Experiment(Desc("./single_busyloop %d" % size, "base"),
                [
                    Desc("OMP_NUM_THREADS=%d ./busyloop %d" % (p, size), "%d" % p) for p in [2, 4, 6, 8, 12, 16, 32, 64]
                ])
        exp.table()
