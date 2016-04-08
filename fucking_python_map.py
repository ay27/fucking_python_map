from __future__ import print_function
import copy
import multiprocessing as mp
import math
import sys
import platform

# author: ay27


PY_VERSION = sys.version_info.major
if PY_VERSION == 3:
    range = range
elif PY_VERSION == 2:
    range = xrange


def _auto_split(length, count):
    if length < count:
        raise AttributeError('length must >= count')
    if count <= 0:
        raise AttributeError('count must > 0')
    start = []
    end = []
    fr = int(math.ceil(length / float(count)))
    tt = fr * count - length
    pc = 0
    for ii in range(count - tt):
        start.append(pc)
        pc += fr
        end.append(pc)
    fr -= 1
    for ii in range(tt):
        start.append(pc)
        pc += fr
        end.append(pc)
    end[-1] = length
    return start, end


class _Worker(mp.Process):
    def __init__(self, func, input_data, result, start_index, end_index):
        super(_Worker, self).__init__()
        self.func = func
        self.data = input_data
        self.start_index = start_index
        self.end_index = end_index
        self.result = result

    def run(self):
        for ii in range(self.start_index, self.end_index):
            self.result[ii] = self.func(self.data[ii])


def fucking_map(func, iterable, process_count=mp.cpu_count()):
    # fucking windows
    if "Windows" in platform.platform():
        return list(map(func, iterable))
    manager = mp.Manager()
    data = manager.list(iterable)
    start_index, end_index = _auto_split(len(data), process_count)
    process_count = min(process_count, len(start_index))
    result = manager.list(range(len(iterable)))
    p = [_Worker(func, data, result, start_index[ii], end_index[ii]) for ii in range(process_count)]
    for ii in range(process_count):
        p[ii].start()
    for ii in range(process_count):
        p[ii].join()
    return copy.deepcopy(result)


if __name__ == '__main__':
    def func(xx, yy):
        return xx * yy


    print(fucking_map(lambda kk: func(kk, 2), range(100), 6))
