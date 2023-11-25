#!/usr/bin/env python3

import csv
import glob
import multiprocessing as mp
import subprocess as sp
import os

routing_strategies = {"static": ["init_once", "opportunistic", "backpressure"],
                      "dynamic": ["adaptive_reinit", "dynamic"],
                      "debug": ["alternate", "default_path"]}

regret_budgets = ["0.00001", "0.0001", "0.001", "0.01", "0.1", "0.2", "0.4", "0.8", "1.6", "2.4", "3.2"]

benchmarks = {
    "imdb": ["01a", "01b", "01c", "01d", "02a", "02b", "02c", "02d", "03a", "03b", "03c",
             "04a", "04b", "04c", "05a", "05b", "05c", "06a", "06b", "06c", "06d", "06e",
             "06f", "07a", "07b", "07c", "08a", "08b", "08c", "08d", "09a", "09b", "09c",
             "09d", "10a", "10b", "10c", "11a", "11b", "11c", "11d", "12a", "12b", "12c",
             "13a", "13b", "13c", "13d", "14a", "14b", "14c", "15a", "15b", "15c", "15d",
             "16a", "16b", "16c", "16d", "17a", "17b", "17c", "17d", "17e", "17f", "18a",
             "18b", "18c", "19a", "19b", "19c", "19d", "20a", "20b", "20c", "21a", "21b",
             "21c", "22a", "22b", "22c", "22d", "23a", "23b", "23c", "24a", "24b", "25a",
             "25b", "25c", "26a", "26b", "26c", "27a", "27b", "27c", "28a", "28b", "28c",
             "29a", "29b", "29c", "30a", "30b", "30c", "31a", "31b", "31c", "32a", "32b",
             "33a", "33b", "33c"],
    "ssb": ["q1-1", "q1-2", "q1-3", "q2-1", "q2-2", "q2-3", "q3-1", "q3-2", "q3-3", "q4-1",
            "q4-2", "q4-3"],
    "ssb-skew": ["q1-1", "q1-2", "q1-3", "q1-4", "q2-1", "q2-2", "q2-3", "q2-4"]
}


def move_files(source, match, target):
    files = glob.glob(os.path.join(source, match))
    if target == "":
        for file in files:
            os.remove(file)
    else:
        for file in files:
            filename = file.split("/")[-1]
            os.rename(file, f"{target}/{filename}")


def execute_benchmark_0(i, s, r, b):
    nthreads = 1
    cwd = os.getcwd()
    sp.call(["mkdir", "-p", f"{cwd}/duckdb-polr/tmp/{i}"])

    target_path = f"{cwd}/experiment-results/2_5_init_tuple/{b}/{s}"
    if s in routing_strategies["dynamic"]:
        target_path += f"/{r}"

    sp.call(["mkdir", "-p", target_path])

    sp.call([f"{cwd}/duckdb-polr/build/release/benchmark/benchmark_runner",
             f"benchmark/{b}/.*",
             "--polr_mode=bushy",
             f"--multiplexer_routing={s}",
             "--log_tuples_routed",
             "--nruns=1",
             f"--threads={nthreads}",
             f"--dir_prefix={i}",
             f"--regret_budget={r}"
             ])
    move_files(f"{cwd}/duckdb-polr/tmp/{i}", "*-enumeration.csv", "")
    move_files(f"{cwd}/duckdb-polr/tmp/{i}", "*", target_path)

def execute_benchmark_1(i, s, r, b):
    nthreads = 1 if s != "backpressure" else 24
    cwd = os.getcwd()
    sp.call(["mkdir", "-p", f"{cwd}/duckdb-polr/tmp/{i}"])

    target_path = f"{cwd}/experiment-results/2_3_routing/{b}/{s}"
    if s in routing_strategies["dynamic"]:
        target_path += f"/{r}"

    sp.call(["mkdir", "-p", target_path])

    sp.call([f"{cwd}/duckdb-polr/build/release/benchmark/benchmark_runner",
             f"benchmark/{b}/.*",
             "--polr_mode=bushy",
             f"--multiplexer_routing={s}",
             "--log_tuples_routed",
             "--nruns=1",
             f"--threads={nthreads}",
             f"--dir_prefix={i}",
             f"--regret_budget={r}"
             ])
    move_files(f"{cwd}/duckdb-polr/tmp/{i}", "*-enumeration.csv", "")
    move_files(f"{cwd}/duckdb-polr/tmp/{i}", "*", target_path)


def gather_pipeline_durations(s, b, q, path):
    csv_files = glob.glob(os.path.join(path, "*.csv"))
    assert len(csv_files) > 0

    pipeline_ids = {}
    for file in csv_files:
        pipeline_id = file.split("-")[-1]
        if pipeline_id not in pipeline_ids:
            pipeline_ids[pipeline_id] = []
        with open(file) as f:
            line = f.readline()
            pipeline_ids[pipeline_id].append(float(line))

    for pipeline_id in pipeline_ids:
        tmp = pipeline_ids[pipeline_id]
        result_str = ""
        for j in tmp:
            result_str += f"{j}\n"
        with open(f"{os.getcwd()}/experiment-results/3_1_pipeline/{b}/{s}/{q}-{pipeline_id}", "w") as f:
            f.write(result_str)

def execute_benchmark_2():
    nruns = 20
    cwd = os.getcwd()

    for b in benchmarks:
        for s in routing_strategies["static"]:
            sp.call(["mkdir", "-p", f"{cwd}/experiment-results/3_1_pipeline/{b}/{s}"])
        for s in routing_strategies["dynamic"]:
            for r in regret_budgets:
                sp.call(["mkdir", "-p", f"{cwd}/experiment-results/3_1_pipeline/{b}/{s}/{r}"])
        sp.call(["mkdir", "-p", f"{cwd}/experiment-results/3_1_pipeline/{b}/default"])

        for q in benchmarks[b]:
            move_files(f"{cwd}/duckdb-polr/tmp", "*", "")
            sp.call([f"{cwd}/duckdb-polr/build/release/benchmark/benchmark_runner",
                     f"benchmark/{b}/{q}.*",
                     "--polr_mode=bushy",
                     "--threads=1",
                     "--log_tuples_routed",
                     "--nruns=1"
                     ])
            path = f"{cwd}/duckdb-polr/tmp"
            csv_files = glob.glob(os.path.join(path, "*.csv"))
            if len(csv_files) > 0:
                move_files(f"{cwd}/duckdb-polr/tmp", "*", "")
                sp.call([f"{cwd}/experiments/util/runDuckDBRestrict1.sh",
                         f"benchmark/{b}/{q}.benchmark",
                         "--measure_pipeline",
                         "--threads=1",
                         f"--nruns={nruns}"
                         ])
                gather_pipeline_durations("default", b, q, path)

                for s in routing_strategies["static"]:
                    nthreads = 1 if s != "backpressure" else 24
                    move_files(f"{cwd}/duckdb-polr/tmp", "*", "")
                    sp.call([f"{cwd}/experiments/util/runDuckDBRestrict1.sh",
                             f"benchmark/{b}/{q}.benchmark",
                             "--polr_mode=bushy",
                             f"--multiplexer_routing={s}",
                             "--measure_pipeline",
                             f"--threads={nthreads}",
                             f"--nruns={nruns}"
                             ])
                    gather_pipeline_durations(s, b, q, path)
                for s in routing_strategies["dynamic"]:
                    for r in regret_budgets:
                        move_files(f"{cwd}/duckdb-polr/tmp", "*", "")
                        sp.call([f"{cwd}/experiments/util/runDuckDBRestrict1.sh",
                                 f"benchmark/{b}/{q}.benchmark",
                                 "--polr_mode=bushy",
                                 f"--multiplexer_routing={s}",
                                 f"--regret_budget={r}",
                                 "--measure_pipeline",
                                 "--threads=1",
                                 f"--nruns={nruns}"
                                 ])
                        gather_pipeline_durations(f"{s}/{r}", b, q, path)


def execute_benchmark_3():
    nruns = 20
    routing_strategy = "adaptive_reinit"
    cwd = os.getcwd()

    for b in benchmarks:
        for r in regret_budgets:
            move_files(f"{cwd}/duckdb-polr/tmp", "*", "")
            sp.call([f"{cwd}/duckdb-polr/build/release/benchmark/benchmark_runner",
                     f"benchmark/{b}/.*",
                     "--polr_mode=bushy",
                     f"--multiplexer_routing={routing_strategy}",
                     f"--regret_budget={r}",
                     "--threads=1",
                     f"--nruns={nruns}",
                     "--out=tmp/results.csv"
                     ])
            sp.call(["mkdir", "-p", f"{cwd}/experiment-results/3_2_query/{b}/{r}"])
            sp.call(["mv", f"{cwd}/duckdb-polr/tmp/results.csv", f"{cwd}/experiment-results/3_2_query/{b}/{r}/polar.csv"])

        move_files(f"{cwd}/duckdb-polr/tmp", "*", "")
        sp.call([f"{cwd}/duckdb-polr/build/release/benchmark/benchmark_runner",
                 f"benchmark/{b}/.*",
                 "--threads=1",
                 f"--nruns={nruns}",
                 "--out=tmp/results.csv"
                 ])
        sp.call(["mv", f"{cwd}/duckdb-polr/tmp/results.csv", f"{cwd}/experiment-results/3_2_query/{b}/duckdb.csv"])


if __name__ == "__main__":
    sp.call(["rm", "-rf", f"{os.getcwd()}/experiment-results/2_3_routing"])
    sp.call(["rm", "-rf", f"{os.getcwd()}/experiment-results/3_1_pipeline"])
    sp.call(["rm", "-rf", f"{os.getcwd()}/experiment-results/3_2_query"])
    sp.call(["rm", "-rf", f"{os.getcwd()}/duckdb-polr/tmp"])
    sp.call(["mkdir", "-p", f"{os.getcwd()}/duckdb-polr/tmp"])
    pool = mp.Pool(max(mp.cpu_count(), 16))

    idx = 0
    for benchmark in benchmarks.keys():
        for static_strategy in routing_strategies["static"]:
            pool.apply_async(execute_benchmark_1, args=(idx, static_strategy, 0, benchmark))
            idx += 1
        for debug_strategy in routing_strategies["debug"]:
            pool.apply_async(execute_benchmark_1, args=(idx, debug_strategy, 0, benchmark))
            idx += 1
        for dynamic_strategy in routing_strategies["dynamic"]:
            for regret in regret_budgets:
                pool.apply_async(execute_benchmark_1, args=(idx, dynamic_strategy, regret, benchmark))
                idx += 1

    pool.close()
    pool.join()
    sp.call(["rm", "-rf", f"{os.getcwd()}/duckdb-polr/tmp"])
    sp.call(["mkdir", "-p", f"{os.getcwd()}/duckdb-polr/tmp"])
    execute_benchmark_2()
    sp.call(["rm", "-rf", f"{os.getcwd()}/duckdb-polr/tmp"])
    sp.call(["mkdir", "-p", f"{os.getcwd()}/duckdb-polr/tmp"])
    execute_benchmark_3()
