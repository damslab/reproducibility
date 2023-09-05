#!/usr/bin/env python3

import glob
import os
import psycopg2
import subprocess as sp
import time

threads = ["1", "8"]
benchmarks = ["imdb", "ssb", "ssb-skew"]

cwd = os.getcwd()
sp.call(["rm", "-rf", f"{os.getcwd()}/experiment-results/4_1_endtoend"])
sp.call(["rm", "-rf", f"{os.getcwd()}/duckdb-polr/tmp"])
sp.call(["mkdir", "-p", f"{os.getcwd()}/duckdb-polr/tmp"])

# Run POLAR
nruns = 20
budgets = {"tuned": {"imdb": "0.01", "ssb": "0.001", "ssb-skew": "0.2"},
           "generic": {"imdb": "0.1", "ssb": "0.1", "ssb-skew": "0.1"}}

for benchmark in benchmarks:
    for nthreads in threads:
        for mode in ["tuned", "generic"]:
            sp.call(["mkdir", "-p", f"{cwd}/experiment-results/4_1_endtoend/{benchmark}/polar"])
            sp.call([f"{cwd}/experiments/util/runDuckDBRestrict{nthreads}.sh",
                     f"benchmark/{benchmark}/.*",
                     "--polr_mode=bushy",
                     "--multiplexer_routing=adaptive_reinit",
                     f"--out=tmp/polar-{mode}-{nthreads}.csv",
                     f"--nruns={nruns}",
                     f"--threads={nthreads}",
                     f"--regret_budget={budgets[mode][benchmark]}"
                     ])
            sp.call(["mv", f"{cwd}/duckdb-polr/tmp/polar-{mode}-{nthreads}.csv",
                     f"{cwd}/experiment-results/4_1_endtoend/{benchmark}/polar"])

# Run DuckDB
for benchmark in benchmarks:
    for nthreads in threads:
        sp.call(["mkdir", "-p", f"{cwd}/experiment-results/4_1_endtoend/{benchmark}/duckdb"])
        sp.call([f"{cwd}/experiments/util/runDuckDBRestrict{nthreads}.sh",
                 f"benchmark/{benchmark}/.*",
                 f"--out=tmp/duckdb-{nthreads}.csv",
                 f"--nruns={nruns}",
                 f"--threads={nthreads}"
                 ])
        sp.call(["mv", f"{cwd}/duckdb-polr/tmp/duckdb-{nthreads}.csv",
                 f"{cwd}/experiment-results/4_1_endtoend/{benchmark}/duckdb"])

# Run Postgres
pg_con = psycopg2.connect(user="postgres")
cur = pg_con.cursor()

for benchmark in benchmarks:
    sp.call(["mkdir", "-p", f"{cwd}/experiment-results/4_1_endtoend/{benchmark}/postgres"])
    print(f"Loading {benchmark} data...")
    cur.execute(open(f"{os.getcwd()}/experiments/util/schema-{benchmark}.sql", "r").read())
    cur.execute(open(f"{os.getcwd()}/experiments/util/load-{benchmark}.sql", "r").read())
    cur.execute("commit;")
    print("Done.")

    for worker_count in threads:
        print(f"Run {benchmark} with {worker_count} workers...")
        # TODO: Should worker count for ST be 1 or 0?
        cur.execute(f"set max_parallel_workers_per_gather = {worker_count}")
        cur.execute("SET enable_nestloop TO off")
        cur.execute("commit;")

        path = ""
        if benchmark == "imdb":
            path = f"{os.getcwd()}/duckdb-polr/benchmark/{benchmark}_plan_cost/queries"
        else:
            path = f"{os.getcwd()}/duckdb-polr/benchmark/{benchmark}/queries"
        queries = glob.glob(os.path.join(path, "*.sql"))
        queries.sort()

        output = "query,duration\n"
        for query_path in queries:
            query_name = query_path.split("/")[-1]
            query = open(query_path).read()
            timings = []
            cur = pg_con.cursor()

            for run in range(nruns):
                start = time.time()
                cur.execute(query)
                end = time.time()
                duration = end - start
                results = cur.fetchall()
                timings.append(duration)
                cur.execute("commit;")
                print(f"{query_name} ({run}): {duration:.4f}")

            for timing in timings:
                output += f"{query_name},{duration:.4f}\n"

        with open(f"{cwd}/experiment-results/4_1_endtoend/{benchmark}/postgres/postgres-{worker_count}.csv", "w") as file:
            file.write(output)

cur.close()
pg_con.close()

# SkinnerDB
for benchmark in benchmarks:
    sp.call(["mkdir", "-p", f"{cwd}/experiment-results/4_1_endtoend/{benchmark}/skinnerdb"])
    for nthreads in threads:
        sp.call([f"{cwd}/experiments/util/runSkinnerDB.sh", benchmark, nthreads])

# SkinnerMT
for benchmark in benchmarks:
    sp.call(["mkdir", "-p", f"{cwd}/experiment-results/4_1_endtoend/{benchmark}/skinnermt"])
    for nthreads in threads:
        sp.call([f"{cwd}/experiments/util/runSkinnerMT.sh", benchmark, nthreads])
