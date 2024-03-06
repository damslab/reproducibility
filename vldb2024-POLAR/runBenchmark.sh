#!/usr/bin/env bash

BENCHMARK="imdb"
STRATEGY="adaptive_reinit"
REGRET_BUDGET="0.01"
THREADS=1

usage() {
  cat << EOF
Usage: ./runBenchmark.sh [-h] [-b benchmark] [-s strategy] [-r regret_budget] [-t threads]

Available options:

-h, --help
-b, --benchmark       imdb,ssb,ssb-skew (default: imdb)
-s, --strategy        init_once,opportunistic,adapt_tuple_count,adapt_window_size (default: adapt_window_size)
-r, --regret_budget   float (default: 0.01)
-t, --threads         integer (default: 1)
EOF
  exit
}

msg() {
  echo >&2 -e "${1-}"
}

die() {
  local msg=$1
  local code=${2-1} # default exit status 1
  msg "$msg"
  exit "$code"
}

parse_params() {
  while :; do
    case "${1-}" in
    -h | --help) usage ;;
    -b | --benchmark)
      BENCHMARK="${2-}"
      shift
      ;;
    -s | --strategy)
      if [[ "${2-}" = "adapt_tuple_count" ]]; then
        STRATEGY="dynamic"
      elif [[ "${2-}" = "adapt_window_size" ]]; then
        STRATEGY="adaptive_reinit"
      else
        STRATEGY="${2-}"
      fi
      shift
      ;;
    -r | --regret_budget)
      REGRET_BUDGET="${2-}"
      shift
      ;;
    -t | --threads)
      THREADS="${2-}"
      shift
      ;;
    -?*) die "Unknown option: $1" ;;
    *) break ;;
    esac
    shift
  done

  return 0
}

parse_params "$@"

if [[ ! -f "$PWD/duckdb-polr/duckdb_benchmark_data/$BENCHMARK.duckdb" ]]; then
  echo "Loading data... (this may take a moment)"
fi

./duckdb-polr/build/release/benchmark/benchmark_runner "benchmark/${BENCHMARK}/.*" --polr_mode=bushy --multiplexer_routing="${STRATEGY}" --regret_budget="${REGRET_BUDGET}" --threads="${THREADS}"
