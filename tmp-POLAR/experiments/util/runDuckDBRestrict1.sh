#!/usr/bin/env bash

cgexec -g cpu:limitcpu1 "$PWD/duckdb-polr/build/release/benchmark/benchmark_runner" "$@"
