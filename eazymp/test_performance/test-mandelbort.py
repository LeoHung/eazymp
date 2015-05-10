from PIL import Image
from datetime import datetime

def save_png(filename, data_map, size_x, size_y):
    im = Image.new('RGB', (size_x, size_y))
    pixels1 = im.load()
    for i in xrange(size_x):
        for j in xrange(size_y):
                pixels1[i, j] = data_map[i, j]
    im.save(filename, "PNG")


def mandelbrot(row, col, size_x, size_y):

    data = {}

    ret = [ 0.0 ] *3

    x0 = float(row) / size_x * 3.5 - 2.5
    y0 = float(col) / size_y * 2.0 - 1.0
    assert -2.5 <= x0 <= 1
    assert -1 <= y0 <= 1
    x = 0
    y = 0
    iteration = 0
    max_iteration = 1000
    while (x*x + y*y) < 4 and (iteration < max_iteration):
        xtemp = x*x - y*y + x0
        y = 2*x*y + y0
        x = xtemp
        iteration = iteration + 1
        color = iteration % 255
        #print(iteration, color)
        data[( 0)]  = color 
        data[( 1)] = (color + 75) % 255
        data[( 2)] = (color + 150) % 255

    return data

def slow_mandelbrot(size_x, size_y):
    data = {} #shared

    for row in range(size_x): #parallel_for 
        for col in range(size_y):
            tmp = mandelbrot(row, col, size_x, size_y)
            data[(row, col)] = (tmp[0], tmp[1], tmp[2])

    return data

def join_dict(from_dict, to_dict):
    for k, v in from_dict.items():
        to_dict[k] = v 

def join_shared(shared_variables_list, variables):
    for shared_variables in shared_variables_list:
        for name, value in shared_variables.items():
            if type(value) == dict:
                join_dict(value, variables[name])

def fast_mandelbrot(size_x, size_y):
    data = {}

    def core(row):
        import copy 
        __shared__ = {}
        __shared__['data'] = copy.deepcopy(data)
        for col in range(size_y):
            tmp = mandelbrot(row, col, size_x, size_y)
            
            # data[(row, col)] = (tmp[0], tmp[1], tmp[2])
            __shared__['data'][(row, col)] = (tmp[0], tmp[1], tmp[2])
        
        return __shared__

    from pathos.multiprocessing import ProcessingPool
    __shared__ = ProcessingPool(4).map(core, range(size_x))
    join_shared(__shared__, {'data': data})

    return data

if __name__ == "__main__":
    size_x, size_y = 1000, 1000
    filename = "mandelbrot.png"
    # slow version
    # start = datetime.now()
    # data_map = slow_mandelbrot(size_x, size_y)
    # end = datetime.now()
    # print "slow: runtime: %s" % str(end-start)
    # save_png(filename, data_map, size_x, size_y)

    # multi-process version
    start = datetime.now()
    data_map= fast_mandelbrot(size_x, size_y)
    end = datetime.now()
    print "fast: runtime: %s" % str(end-start)
    save_png("mp-"+filename, data_map, size_x, size_y)    
