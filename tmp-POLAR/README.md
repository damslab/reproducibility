**Paper name:** POLAR: Adaptive and Non-invasive Join Order Selection via Plans of Least Resistance

Source Code Info
- Repository: POLAR [1] (https://github.com/d-justen/duckdb-polr)
- Programming Language: C++
- Additional Programming Language info: Clang-12 is recommended but other compilers may work as well

Hardware Info to Reproduce Experiment Results

- Processor: AMD EPYC 7443P CPU @ 2.85 GHz
- Cores: 24 physical cores (48 vCores)
- Memory: 256GB
- Disk: SSD, at least 20GB.

Experimentation Info

- Environment: Ubuntu 20.04 LTS is used for the experiments.

**Usage**

Run `./installDependencies.sh` to install the dependencies and generate the benchmark data.
The following packages are required:
- *git*: For checking out the POLAR and DBGen repositories 
- *libssl-dev*: For building DuckDB
- *pigz*: For compressing the benchmark data

Execute benchmarks with `./runBenchmark.sh`. You can specify the benchmark, routing strategy, regret budget, and
number of threads.

```
Usage: ./runBenchmark.sh [-h] [-b benchmark] [-s strategy] [-r regret_budget] [-t threads]

Available options:

-h, --help
-b, --benchmark       imdb,ssb,ssb-skew (default: imdb)
-s, --strategy        init_once,opportunistic,adapt_tuple_count,adapt_window_size (default: adapt_window_size)
-r, --regret_budget   float (default: 0.1)
-t, --threads         integer (default: 1)
```
