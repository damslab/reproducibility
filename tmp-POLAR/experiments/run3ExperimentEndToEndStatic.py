#!/usr/bin/env python3

import glob
import os
import psycopg2
import subprocess as sp
import time

nruns = 20
threads = ["1", "8"]
benchmarks = ["imdb", "ssb", "ssb-skew"]

cwd = os.getcwd()

sp.call(["rm", "-rf", f"{os.getcwd()}/duckdb-polr/tmp"])
sp.call(["mkdir", "-p", f"{os.getcwd()}/duckdb-polr/tmp"])

# Run DuckDB
for benchmark in benchmarks:
    sp.call(["mkdir", "-p", f"{cwd}/experiment-results/4_1_endtoend/{benchmark}/duckdb"])
    sp.call([f"{cwd}/experiments/util/runDuckDBRestrict8.sh",
             f"benchmark/{benchmark}/.*",
             f"--out=tmp/duckdb-8.csv",
             f"--nruns={nruns}",
             f"--threads=8"
             ])
    sp.call(["mv", f"{cwd}/duckdb-polr/tmp/duckdb-8.csv",
             f"{cwd}/experiment-results/4_1_endtoend/{benchmark}/duckdb"])

# Run POLAR
for benchmark in benchmarks:
    sp.call(["mkdir", "-p", f"{cwd}/experiment-results/4_1_endtoend/{benchmark}/polar"])
    sp.call([f"{cwd}/experiments/util/runDuckDBRestrict8.sh",
             f"benchmark/{benchmark}/.*",
             "--polr_mode=bushy",
             f"--out=tmp/polar-8.csv",
             f"--nruns={nruns}",
             f"--threads=8"
             ])
    sp.call(["mv", f"{cwd}/duckdb-polr/tmp/polar-8.csv",
             f"{cwd}/experiment-results/4_1_endtoend/{benchmark}/polar"])

# Run LIP
for benchmark in benchmarks:
    for nthreads in threads:
        sp.call(["mkdir", "-p", f"{cwd}/experiment-results/4_1_endtoend/{benchmark}/lip"])
        sp.call([f"{cwd}/experiments/util/runDuckDBRestrict{nthreads}.sh",
                 f"benchmark/{benchmark}/.*",
                 f"--out=tmp/lip-{nthreads}.csv",
                 f"--nruns={nruns}",
                 f"--threads={nthreads}",
                 "--enable_lip"
                 ])
        sp.call(["mv", f"{cwd}/duckdb-polr/tmp/lip-{nthreads}.csv",
                 f"{cwd}/experiment-results/4_1_endtoend/{benchmark}/lip"])
