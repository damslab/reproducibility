

import statistics
from math import nan
import os
import errno

def r3(d):
    return round(d, 3)


def st(d):
    try:
        return r3(statistics.mean(d)), r3(statistics.stdev(d))
    except:
        try:
            return r3(statistics.mean(d)), 0
        except:
            if (len(d)) == 0:
                return nan, nan
            return d[0], 0


def stats(data):
    if data and data[0]:
        if (len(data[0][0]) > 3):
            return [[st(y[1:]) for y in x] for x in data]
        else:
            return [[st(y) for y in x] for x in data]
    else:
        return None

def stats_list(data):
    if data and data[0] :
       if (len(data[0]) > 3):
           return [st(y[1:]) for y in data] 
       else:
           return [st(y) for y in data] 
    else:
        return None


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
