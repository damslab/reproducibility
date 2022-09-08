import argparse
import timeit

import numpy as np
import pandas as pd

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--rep', type=int, help='number of repetitions')
parser.add_argument('--data', type=str, help='The filepath to csv file input')
args = parser.parse_args()

matrix = np.genfromtxt(args.data, delimiter=',')
vector = np.random.random_sample((matrix.shape[1]))

start_time = timeit.default_timer()
for i in range(args.rep):
    np.dot(matrix, vector)
elapsed = timeit.default_timer() - start_time

print(str(elapsed) + "," + str(args.rep))
