

class Line:
    def __init__(self, xticks, y, size):
        self.xticks = xticks
        self.y = y
        self.size = size

import re


def plot(filename, title, lines, xlabel, ylabel):
    import matplotlib.pyplot as plt
    import numpy as np

    # plt.figure(figsize=(8, 4))

    # plt.subplot("121")
    plt.title(title)


    plot_lines = []
    plot_labels = []
    for line in lines:
        x = np.arange(len(line.xticks))
        y = np.array(np.array(line.y))
        plot_line, = plt.plot(x, y, label="size: %s" % line.size)
        plot_lines.append(plot_line)
        plot_labels.append("size: %s" % line.size)

    # plt.legend(plot_lines, plot_labels, bbox_to_anchor=(1.05, 1), loc=0, borderaxespad=0.)
    plt.legend(plot_lines, plot_labels, loc=4)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(np.arange(len(lines[0].xticks)), lines[0].xticks)
    plt.savefig(filename)


def read_lines(filenames):
    break_reg = "Size: (\d+)"
    lines = []
    xticks = None
    y = None
    size = ""
    for filename in filenames:
        f = open(filename)
        title = f.readline()
        for l in f:
            tmp = re.search(break_reg, l)
            if tmp is not None:
                if xticks is not None:
                    lines.append(Line(xticks, y, size))
                size = tmp.group(1)
                xticks = []
                y = []
            else:
                tmp = l.strip().split(",")
                xticks.append(tmp[0])
                y.append(float(tmp[1]))
    if xticks is not None:
        lines.append(Line(xticks, y, size))

    return title, lines

if __name__ == "__main__":
    from sys import argv
    output_filename = argv[1]
    title, lines = read_lines(argv[2:])

    plot(output_filename, title, lines, "number of process", "speedup")
