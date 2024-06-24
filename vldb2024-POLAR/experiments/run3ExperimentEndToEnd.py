#!/usr/bin/env python3

import glob
import os
import psycopg2
import subprocess as sp
import time
from run3ExperimentEndToEndStatic import run_duckdb, run_polar, run_lip

nruns = 5
threads = ["1", "8"]
benchmarks = ["imdb", "ssb", "ssb-skew"]
cwd = os.getcwd()


def extract_join_intermediates(qp):
    counter = 0
    if qp["Node Type"] == "Nested Loop" or qp["Node Type"] == "Hash Join" or qp["Node Type"] == "Merge Join":
        counter += qp["Actual Rows"] * qp["Actual Loops"]
    if "Plans" in qp:
        for plan in qp["Plans"]:
            counter += extract_join_intermediates(plan)
    return counter


# Run Postgres
def run_postgres():
    pg_con = psycopg2.connect(user="postgres")
    cur = pg_con.cursor()

    for benchmark in benchmarks:
        sp.call(["mkdir", "-p", f"{cwd}/experiment-results/4_1_endtoend/{benchmark}/postgres"])
        print(f"Loading {benchmark} data...")
        cur.execute(open(f"{os.getcwd()}/experiments/util/schema-{benchmark}.sql", "r").read())
        tables = glob.glob(os.path.join(f"{os.getcwd()}/data/{benchmark}", "*.tbl"))
        tables.sort()
        for table in tables:
            with open(table, "r") as tbl_file:
                tbl_name = table.split("/")[-1].split(".")[0]
                cur.copy_from(tbl_file, tbl_name, sep="|", null="")
        cur.execute(open(f"{os.getcwd()}/experiments/util/fkidx-{benchmark}.sql", "r").read())
        cur.execute("commit;")
        print("Done.")

        path = ""
        if benchmark == "imdb":
            path = f"{os.getcwd()}/duckdb-polr/benchmark/{benchmark}_plan_cost/queries"
        else:
            path = f"{os.getcwd()}/duckdb-polr/benchmark/{benchmark}/queries"
        queries = glob.glob(os.path.join(path, "*.sql"))
        queries.sort()

        # Execution Time Evaluation
        for worker_count in threads:
            print(f"Run {benchmark} with {worker_count} workers...")
            w = 0 if worker_count == 1 else worker_count
            cur.execute(f"set max_parallel_workers_per_gather = {w}")
            cur.execute("commit;")

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
                    output += f"{query_name},{timing:.4f}\n"

            with open(f"{cwd}/experiment-results/4_1_endtoend/{benchmark}/postgres/postgres-{worker_count}.csv",
                      "w") as file:
                file.write(output)

        # Intermediate Count Evaluation
        cur.execute(f"set max_parallel_workers_per_gather = 0")
        cur.execute("commit;")

        output = "query,join_intermediates\n"
        for query_path in queries:
            query_name = query_path.split("/")[-1]
            query = open(query_path).read()
            cur.execute(f"EXPLAIN (FORMAT JSON, ANALYZE, COSTS 0) {query}")
            query_plan = cur.fetchone()[0][0]
            cur.execute("commit;")
            output += f"{query_name},{extract_join_intermediates(query_plan['Plan'])}\n"

        sp.call(["mkdir", "-p", f"{cwd}/experiment-results/3_5_intermediates/{benchmark}/postgres"])
        with open(f"{cwd}/experiment-results/3_5_intermediates/{benchmark}/postgres/postgres.csv", "w") as file:
            file.write(output)

    cur.close()
    pg_con.close()


# SkinnerDB
def run_skinnerdb():
    for benchmark in ["imdb"]:
        sp.call(["mkdir", "-p", f"{cwd}/experiment-results/4_1_endtoend/{benchmark}/skinnerdb"])
        for nthreads in threads:
            sp.call([f"{cwd}/experiments/util/runSkinnerDB.sh", benchmark, nthreads])
            if nthreads == "1":
                sp.call(["mkdir", "-p", f"{cwd}/experiment-results/3_5_intermediates/{benchmark}/skinnerdb"])
                sp.call(["cp", f"{cwd}/experiment-results/4_1_endtoend/{benchmark}/skinnerdb/skinnerdb-1.csv",
                         f"{cwd}/experiment-results/3_5_intermediates/{benchmark}/skinnerdb/skinnerdb-1.csv"])


# SkinnerMT
def run_skinnermt():
    for benchmark in ["imdb"]:
        sp.call(["mkdir", "-p", f"{cwd}/experiment-results/4_1_endtoend/{benchmark}/skinnermt"])
        for nthreads in threads:
            sp.call([f"{cwd}/experiments/util/runSkinnerMT.sh", benchmark, nthreads])


if __name__ == "__main__":
    run_duckdb()
    run_polar()
    run_lip()
    run_postgres()
    run_skinnerdb()
    run_skinnermt()
