#!/usr/bin/env python3

import os
import subprocess as sp

nruns = 5
threads = ["1", "8"]
benchmarks = ["imdb", "ssb", "ssb-skew"]

# TODO copy static files


# Run DuckDB
def run_duckdb():
    cwd = os.getcwd()

    sp.call(["rm", "-rf", f"{os.getcwd()}/duckdb-polr/tmp"])
    sp.call(["mkdir", "-p", f"{os.getcwd()}/duckdb-polr/tmp"])
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
def run_polar():
    cwd = os.getcwd()

    sp.call(["rm", "-rf", f"{os.getcwd()}/duckdb-polr/tmp"])
    sp.call(["mkdir", "-p", f"{os.getcwd()}/duckdb-polr/tmp"])
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
def run_lip():
    cwd = os.getcwd()

    sp.call(["rm", "-rf", f"{os.getcwd()}/duckdb-polr/tmp"])
    sp.call(["mkdir", "-p", f"{os.getcwd()}/duckdb-polr/tmp"])
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


if __name__ == "__main__":
    run_duckdb()
    run_polar()
    run_lip()

    # Use previous third-party system experiment results
    for system in ["postgres", "skinnerdb", "skinnermt"]:
        for benchmark in benchmarks:
            if system == "skinnerdb" or system == "skinnermt":
                if benchmark != "imdb":
                    continue

            sp.call(["mkdir", "-p", f"{os.getcwd()}/experiment-results/4_1_endtoend/{benchmark}/{system}"])
            for nthreads in threads:
                sp.call(["cp", f"{os.getcwd()}/static/4_1_endtoend/{benchmark}/{system}/{system}-{nthreads}.csv",
                         f"{os.getcwd()}/experiment-results/4_1_endtoend/{benchmark}/{system}/{system}-{nthreads}.csv"])

                # Copy results for SkinnerDB intermediate count experiment
                if nthreads == "1" and system == "skinnerdb":
                    sp.call(["mkdir", "-p", f"{os.getcwd()}/experiment-results/3_5_intermediates/{benchmark}/{system}"])
                    sp.call(["cp", f"{os.getcwd()}/experiment-results/4_1_endtoend/{benchmark}/{system}/{system}-1.csv",
                            f"{os.getcwd()}/experiment-results/3_5_intermediates/{benchmark}/{system}/{system}-1.csv"])

            # Copy results for Postgres intermediate count experiment
            if system == "postgres":
                sp.call(["mkdir", "-p", f"{os.getcwd()}/experiment-results/3_5_intermediates/{benchmark}/{system}"])
                sp.call(["cp", f"{os.getcwd()}/static/3_5_intermediates/{benchmark}/{system}/{system}.log",
                         f"{os.getcwd()}/experiment-results/3_5_intermediates/{benchmark}/{system}/{system}.log"])
