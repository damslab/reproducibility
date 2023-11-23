#!/usr/bin/env python3

import csv
import glob
import multiprocessing as mp
import subprocess as sp
import os

enumeration_strategies = ["each_last_once", "each_first_once", "bfs_min_card", "sample"]
optimizer_modes = ["dphyp-equisets"]
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


def move_and_rename(source, match, target):
    files = glob.glob(os.path.join(source, match))
    files.sort()
    for i in range(len(files)):
        os.rename(files[i], f"{target}-{i}.csv")


def execute_benchmark_0(i, s, b):
    cwd = os.getcwd()
    sp.call(["mkdir", "-p", f"{cwd}/duckdb-polr/tmp/{i}"])
    sp.call(["mkdir", "-p", f"{cwd}/experiment-results/2_0_sample_size/{b}/{s}/timings"])

    sp.call([f"{cwd}/duckdb-polr/build/release/benchmark/benchmark_runner",
             f"benchmark/{b}/.*",
             "--polr_mode=bushy",
             "--multiplexer_routing=alternate",
             f"--max_join_orders={s}",
             "--threads=1",
             "--nruns=1",
             "--log_tuples_routed",
             "--disable_caching",
             f"--dir_prefix={i}",
             "--enumerator=sample"
             ])

    move_files(f"{cwd}/duckdb-polr/tmp/{i}", "*-enumeration.csv",
               f"{cwd}/experiment-results/2_0_sample_size/{b}/{s}/timings")
    move_files(f"{cwd}/duckdb-polr/tmp/{i}", "*.txt", "")
    move_files(f"{cwd}/duckdb-polr/tmp/{i}", "*.csv",
               f"{cwd}/experiment-results/2_0_sample_size/{b}/{s}")


def execute_benchmark_1(i, b):
    nruns = 5

    cwd = os.getcwd()
    sp.call(["mkdir", "-p", f"{cwd}/experiment-results/1_1_potential_impact/{b}/pipelines"])
    sp.call(["mkdir", "-p", f"{cwd}/experiment-results/1_1_potential_impact/{b}/queries"])
    sp.call(["mkdir", "-p", f"{cwd}/duckdb-polr/tmp/{i}"])

    sp.call([f"{cwd}/duckdb-polr/build/release/benchmark/benchmark_runner",
             f"benchmark/{b}/.*",
             f"--out=tmp/{i}/results.csv",
             "--measure_pipeline",
             "--threads=1",
             f"--nruns={nruns}",
             f"--dir_prefix={i}"
             ])

    sp.call(["mv", f"{cwd}/duckdb-polr/tmp/{i}/results.csv",
             f"{cwd}/experiment-results/1_1_potential_impact/{b}/queries"])
    move_files(f"{cwd}/duckdb-polr/tmp/{i}", "*", "")

    for query in benchmarks[b]:
        sp.call([f"{cwd}/duckdb-polr/build/release/benchmark/benchmark_runner",
                 f"benchmark/{b}/{query}.benchmark",
                 "--polr_mode=bushy",
                 "--threads=1",
                 "--nruns=1",
                 "--log_tuples_routed",
                 f"--dir_prefix={i}"
                 ])

        path = f"{cwd}/duckdb-polr/tmp/{i}"
        csv_files = glob.glob(os.path.join(path, "*.csv"))

        if len(csv_files) > 0:
            move_files(f"{cwd}/duckdb-polr/tmp/{i}", "*", "")
            sp.call([f"{cwd}/duckdb-polr/build/release/benchmark/benchmark_runner",
                     f"benchmark/{b}/{query}.benchmark",
                     "--measure_pipeline",
                     "--threads=1",
                     f"--nruns={nruns}",
                     f"--dir_prefix={i}"
                     ])
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
                with open(f"{cwd}/experiment-results/1_1_potential_impact/{b}/pipelines/{query}-{pipeline_id}", "w") as f:
                    f.write(result_str)
        move_files(f"{cwd}/duckdb-polr/tmp/{i}", "*", "")


def execute_benchmark_2(i, m, s, b):
    cwd = os.getcwd()
    sp.call(["mkdir", "-p", f"{cwd}/duckdb-polr/tmp/{i}"])
    sp.call(["mkdir", "-p", f"{cwd}/experiment-results/2_2_enumeration_timings/{m}/{b}/{s}"])
    sp.call(["mkdir", "-p", f"{cwd}/experiment-results/2_1_enumeration_intms/{m}/{b}/{s}"])
    for query in benchmarks[b]:
        sp.call([f"{cwd}/duckdb-polr/build/release/benchmark/benchmark_runner",
                 f"benchmark/{b}/{query}.benchmark",
                 "--polr_mode=bushy",
                 "--multiplexer_routing=alternate",
                 "--max_join_orders=24",
                 "--threads=1",
                 "--nruns=1",
                 "--log_tuples_routed",
                 "--disable_caching",
                 f"--dir_prefix={i}",
                 f"--optimizer_mode={m}",
                 f"--enumerator={s}"
                 ])

        move_files(f"{cwd}/duckdb-polr/tmp/{i}", "*-enumeration.csv",
                   f"{cwd}/experiment-results/2_2_enumeration_timings/{m}/{b}/{s}")
        move_files(f"{cwd}/duckdb-polr/tmp/{i}", "*.txt", "")
        files = glob.glob(os.path.join(f"{cwd}/duckdb-polr/tmp/{i}", "*.csv"))
        files.sort()
        for j in range(len(files)):
            os.rename(files[j], f"{cwd}/experiment-results/2_1_enumeration_intms/{m}/{b}/{s}/{query}-{j}.csv")


if __name__ == "__main__":
    sp.call(["rm", "-rf", f"{os.getcwd()}/experiment-results/1_1_potential_impact"])
    sp.call(["rm", "-rf", f"{os.getcwd()}/experiment-results/2_1_enumeration_intms"])
    sp.call(["rm", "-rf", f"{os.getcwd()}/experiment-results/2_2_enumeration_timings"])
    sp.call(["rm", "-rf", f"{os.getcwd()}/duckdb-polr/tmp"])
    sp.call(["mkdir", "-p", f"{os.getcwd()}/duckdb-polr/tmp"])
    pool = mp.Pool(mp.cpu_count())

    idx = 0
    for benchmark in benchmarks.keys():
        pool.apply_async(execute_benchmark_0, args=(idx, 1, benchmark))
        idx += 1

        for sample in range(2, 33, 2):
            pool.apply_async(execute_benchmark_0, args=(idx, sample, benchmark))
            idx += 1

    for benchmark in benchmarks.keys():
        pool.apply_async(execute_benchmark_1, args=(idx, benchmark))
        idx += 1

    for mode in optimizer_modes:
        for strategy in enumeration_strategies:
            for benchmark in benchmarks.keys():
                pool.apply_async(execute_benchmark_2, args=(idx, mode, strategy, benchmark))
                idx += 1

    pool.close()
    pool.join()
