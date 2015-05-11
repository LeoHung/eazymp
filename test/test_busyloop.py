from experiment import Desc, Experiment


if __name__ == "__main__":
    # for size in [50, 100, 200, 500]:
    print "Test BusyLoop"
    for size in [50, 100]:
        print "Size: %d" % size
        exp = Experiment(Desc("python busyloop.py %d" % size, "base"),
                [
                    Desc("eazymp -p%d busyloop.py %d" % (p, size), "%d" % p) for p in [2, 4, 6, 8, 12, 16, 32, 64]
                ])
        exp.table()
