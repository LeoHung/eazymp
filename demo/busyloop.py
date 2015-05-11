def run_busyloop(loop_round):
    for l in xrange(loop_round):
        i = 0
        while i < 5000 * 1000 :
            i += 1


if __name__ == "__main__":
    from datetime import datetime
    start = datetime.now()
    data_map = run_busyloop(100)
    end = datetime.now()
    print "runtime: %s" % str(end - start)
    slow_time = (end - start).total_seconds()
