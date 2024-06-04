# Reproducibility Info

**Paper:** POLAR: Adaptive and Non-invasive Join Order Selection via Plans of Least Resistance [[link](https://www.vldb.org/pvldb/vol17/p1185-justen.pdf)]

#### Source Code Info
- Repository: POLAR (https://github.com/d-justen/duckdb-polr)
- Programming Language: C++
- Additional Programming Language info: At least a C++-11 compliant compiler is required

#### Hardware Info to Reproduce Experiment Results

- Processor: AMD EPYC 7443P CPU @ 2.85 GHz
- Cores: 24 physical cores (48 vCores)
- Memory: 256 GB
- Disk: SSD, at least 500 GB.

#### Experimentation Info

- Environment: Ubuntu 20.04 LTS is used for the experiments.
- Compiler: Clang-12

Please note that we assume `python3` and `python3-venv` to be pre-installed and texlive **not** to be installed yet
(check with `apt search texlive | grep -i install`). Also note that some experiments use cgroup virtualization, which 
Docker does not support.

## Usage

The experiments can either be run in a DuckDB-only mode (simple setup, minimal requirements) or extensive mode
(complex setup, reproduce third-party system baselines). The DuckDB-only mode executes all experiments on POLAR
as well as DuckDB and Lookahead Information Passing as baselines. For the remaining baselines it reuses previous
experiment results obtained from our own hardware setup. The extensive mode requires installing 
[SkinnerDB](https://github.com/cornelldbgroup/skinnerdb), 
[SkinnerMT](https://github.com/cornelldbgroup/skinnerdb/tree/skinnermt), and [Postgres](https://www.postgresql.org), 
which serve as additional baselines. Both options run the experiments, generate the figures and tables from the
experiments section and compile the resulting paper as a PDF. We advise you to run the experiment within a `tmux`
session as they may take a few days.

### DuckDB-only Mode

Please make sure to use the environment and compiler from the **Experimentation Info** above and hardware similar to
the specifications in **Hardware Info**.

#### Instructions

1. Run `./installDependenciesDuckDB.sh`. Installs the dependencies and generates the benchmark data (JOB, SSB, 
SSB-skew). *Estimated time: 1-2 hours.*
2. Run `./runAllExperiments.sh duckdb-only`. Executes the experiments and generates the paper artifacts. *Estimated
time: 2-3 days.*
3. Open `paper/main.pdf` to check the results.

#### Required Packages

In this mode, the following required dependencies are installed by the install script:
- *cgroup-tools*: For thread limiting
- *cmake*: For building
- *git*: For checking out the POLAR and DBGen repositories
- *libssl-dev*: For building DuckDB
- *python3-pip*: For python requirements
- *TeX Live*: For paper PDF compilation (including `tex-common`, `texinfo`, `equivs`, `perl-tk`, `perl-doc`)
- *wget*: For texlive installation

### Extensive Mode

Please make sure to use the environment and compiler from the **Experimentation Info** above and hardware similar to
the specifications in **Hardware Info**.

#### Instructions

1. Run `./installDependencies.sh`. Installs the dependencies and generates the benchmark data (JOB, SSB,
   SSB-skew). This script is **explicitly** only tested for Ubuntu 20.04. Alternatively, 
   [SkinnerDB](https://github.com/cornelldbgroup/skinnerdb),
   [SkinnerMT](https://github.com/cornelldbgroup/skinnerdb/tree/skinnermt), and [Postgres](https://www.postgresql.org)
   can be installed manually according to their individual instructions. The remaining (DuckDB-based) 
   requirements can then be installed with `installDependenciesDuckDB.sh`. *Estimated time: 2-3 hours.*
2. Run `./runAllExperiments.sh`. Executes the experiments and generates the paper artifacts. *Estimated
   time: 3-4 days.*
3. Open `paper/main.pdf` to check the results.

#### Required Packages

In this mode, the following required dependencies are installed by the install script:
- *cgroup-tools*: For thread limiting
- *cmake*: For building
- *git*: For checking out the POLAR and DBGen repositories
- *libssl-dev*: For building DuckDB
- *openjdk-8-jre-headless*: For running SkinnerDB
- *openjdk-16-jre-headless*: For running SkinnerMT
- *postgresql-12*: For Postgres baseline experiments
- *python3-pip*: For python requirements
- *software-properties-common*: For SkinnerMT installation
- *TeX Live*: For paper PDF compilation (including `tex-common`, `texinfo`, `equivs`, `perl-tk`, `perl-doc`)
- *unzip*: For SkinnerDB/MT installation
- *wget*: For texlive installation

### Sandbox Mode

With `runBenchmark.sh` you can execute benchmarks (JOB, SSB or SSB-skew) and specify a routing strategy, regret budget,
and number of threads.

#### Instructions

1. Run `./installDependenciesDuckDB.sh`. Installs the dependencies and generates the benchmark data (JOB, SSB,
   SSB-skew). *Estimated time: 1-2 hours.*
2. Run `./runBenchmark.sh`. For usage, see below.

```
Usage: ./runBenchmark.sh [-h] [-b benchmark] [-s strategy] [-r regret_budget] [-t threads]

Available options:

-h, --help
-b, --benchmark       imdb,ssb,ssb-skew (default: imdb)
-s, --strategy        init_once,opportunistic,adapt_tuple_count,adapt_window_size (default: adapt_window_size)
-r, --regret_budget   float (default: 0.01)
-t, --threads         integer (default: 1)
```

## Citation

If you use POLAR, please cite our paper.

```
@article{justen2024polar,
  author       = {David Justen and
                  Daniel Ritter and
                  Campbell Fraser and
                  Andrew Lamb and
                  Nga Tran and
                  Allison Lee and
                  Thomas Bodner and
                  Mhd Yamen Haddad and
                  Steffen Zeuch and
                  Volker Markl and
                  Matthias Boehm},
  title        = {POLAR: Adaptive and Non-invasive Join Order Selection via Plans of Least Resistance},
  journal      = {Proc. {VLDB} Endow.},
  volume       = {17},
  number       = {6},
  pages        = {1350--1363},
  year         = {2024},
  url          = {https://www.vldb.org/pvldb/vol17/p1185-justen.pdf},
  doi          = {10.14778/3648160.3648175}
}
```