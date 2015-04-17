def run_busyloop(loop_round):
    for l in xrange(loop_round):  #pragma omp parallel for
        i = 0
        while i < 5000 * 1000 :
            i += 1


if __name__ == "__main__":
    from sys import argv
    loop_round = int(argv[1])
    run_busyloop(loop_round)
