from experiment import Desc, Experiment


if __name__ == "__main__":
    # for size in [50, 100, 200, 500]:
    for size in [50, 100]:
        print "Size: %d" % size
        exp = Experiment(Desc("python sample-mandelbrot.py %d" % size, "base"),
                [
                    Desc("lazymp -p%d sample-mandelbrot.py %d" % (p, size), "%d" %(p)) for p in [2, 4, 6, 8, 12, 16, 18, 32, 64]
                ])
        exp.table()