from datetime import datetime
from os import system
import numpy as np


class Desc:
    def __init__(self, cmd, xTick):
        self.cmd = cmd
        self.xTick = xTick


class Experiment:
    # def __init__(self, base_command, compare_commands):
    def __init__(self, base_desc, compare_descs):

        self.base_desc = base_desc
        self.compare_descs = compare_descs

    def run(self):
        base_runtime = evaluate(self.base_desc.cmd)

        compare_runtimes = []
        for compare_desc in self.compare_descs:
            compare_runtimes.append(evaluate(compare_desc.cmd))

        return (base_runtime, compare_runtimes)

    def plot(self, filename):
        import matplotlib.pyplot as plt
        base_runtime, compare_runtimes = self.run()

        all_runtimes = []
        all_runtimes.append(base_runtime)
        all_runtimes.extend(compare_runtimes)

        x = np.array(range(len(compare_runtimes) + 1))
        y = np.array([(base_runtime / all_runtimes[i]) for i in xrange(len(all_runtimes))])

        plt.plot(x, y)

        all_xTicks = []
        all_xTicks.append(self.base_desc.xTick)
        all_xTicks.extend([desc.xTick for desc in self.compare_descs])
        plt.xticks(x, all_xTicks)

        plt.savefig(filename)

        for i in xrange(len(all_xTicks)):
            print "%s,%f" % (all_xTicks[i], y[i])

    def table(self):
        base_runtime, compare_runtimes = self.run()
        all_runtimes = []
        all_runtimes.append(base_runtime)
        all_runtimes.extend(compare_runtimes)
        x = np.array(range(len(compare_runtimes) + 1))
        y = np.array([(base_runtime / all_runtimes[i]) for i in xrange(len(all_runtimes))])

        all_xTicks = []
        all_xTicks.append(self.base_desc.xTick)
        all_xTicks.extend([desc.xTick for desc in self.compare_descs])

        for i in xrange(len(all_xTicks)):
            print "%s,%f" % (all_xTicks[i], y[i])


def evaluate(command):
    start_time = datetime.now()
    system(command)
    end_time = datetime.now()
    return (end_time - start_time).total_seconds()
