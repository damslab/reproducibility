import argparse
import timeit

import numpy as np

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--rep', type=int, help='number of repetitions')
parser.add_argument('--data', type=str, help='The filepath to csv file input')
args = parser.parse_args()

matrix = np.genfromtxt(args.data, delimiter=',')
vector = np.random.random_sample((1,matrix.shape[0]))

# print(dfv)
start_time = timeit.default_timer()
for i in range(args.rep):
    np.dot(vector, matrix)
elapsed = timeit.default_timer() - start_time

print(str(elapsed) + "," + str(args.rep))
