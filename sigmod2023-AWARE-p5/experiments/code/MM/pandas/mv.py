import argparse
import timeit

import numpy as np
import pandas as pd

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--rep', type=int, help='number of repetitions')
parser.add_argument('--data', type=str, help='The filepath to csv file input')
args = parser.parse_args()

matrix = pd.read_csv(args.data, header=None)
vector = pd.DataFrame(np.random.random_sample((1,matrix.shape[0])))

start_time = timeit.default_timer()
for i in range(args.rep):
    vector.dot(matrix)
elapsed = timeit.default_timer() - start_time

print(str(elapsed) + "," + str(args.rep))
