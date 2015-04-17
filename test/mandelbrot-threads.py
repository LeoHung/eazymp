from lazymp.helpers import join_dict
from lazymp.helpers import join_shared
from PIL import Image
from datetime import datetime
from multiprocessing.pool import ThreadPool

IS_TEST = False

# num_thread = 4

# def save_png(filename, data_map, size_x, size_y):
#     im = Image.new('RGB', (size_x, size_y))
#     pixels1 = im.load()
#     for i in xrange(size_x):
#         for j in xrange(size_y):
#                 pixels1[i, j] = data_map[i, j]
#     im.save(filename, "PNG")


def mandelbrot(row, col, size_x, size_y):
    """
        The code is modified from "https://github.com/abingham/mandelbrot"
    """
    data = {}

    # ret = [0.0] * 3

    x0 = float(row) / size_x * 3.5 - 2.5
    y0 = float(col) / size_y * 2.0 - 1.0
    assert -2.5 <= x0 <= 1
    assert -1 <= y0 <= 1
    x = 0
    y = 0
    iteration = 0
    max_iteration = 1000
    while (x * x + y * y) < 4 and (iteration < max_iteration):
        xtemp = x * x - y * y + x0
        y = 2 * x * y + y0
        x = xtemp
        iteration = iteration + 1
        color = iteration % 255
        data[(0)] = color
        data[(1)] = (color + 75) % 255
        data[(2)] = (color + 150) % 255

    return data


def run_mandelbrot(size_x, size_y, num_thread):
    data = {}

    def core(row):
        __shared__ = {}
        import copy
        __shared__['data'] = copy.deepcopy(data)
        for col in xrange(size_y):
            tmp = mandelbrot(row, col, size_x, size_y)
            __shared__['data'][(row, col)] = (tmp[0], tmp[1], tmp[2])
        return __shared__
    __shared__ = ThreadPool(num_thread).map(core, xrange(size_x))
    join_shared(__shared__, {'data': data})

    return data


if __name__ == "__main__":
    from sys import argv
    num_thread = int(argv[1])
    size_x, size_y = int(argv[2]), int(argv[2])
    filename = "mandelbrot.png"

    data_map = run_mandelbrot(size_x, size_y, num_thread)
    # if IS_TEST:
    #     save_png("mp-" + filename, data_map, size_x, size_y)

