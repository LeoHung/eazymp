from experiment import Desc, Experiment


if __name__ == "__main__":
    # for size in [50, 100, 200, 500]:
    print "Mandelbort-py-thread: number of work x speedup"
    for size in [50, 100, 200, 500, 700, 1000]:
        print "Size: %d" % size
        exp = Experiment(Desc("python mandelbrot-threads.py %d %d" % (1, size), "base"),
                [
                    Desc("python mandelbrot-threads.py %d %d" % (p, size), "%d" %(p)) for p in [2, 4, 6, 8, 12, 16, 18, 32, 64]
                ])
        exp.table()
