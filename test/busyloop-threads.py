def run_busyloop(loop_round, p):
    def core(l):
        i = 0
        while i < 5000 * 1000 :
            i += 1
    from multiprocessing.pool import ThreadPool
    ThreadPool(p).map(core, xrange(loop_round))


if __name__ == "__main__":
    from sys import argv
    p = int(argv[1])
    loop_round = int(argv[2])
    run_busyloop(loop_round, p)
