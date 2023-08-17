#!/usr/bin/env bash

cgexec -g cpu:limitcpu8 "$PWD/duckdb-polr/build/release/benchmark/benchmark_runner" "$@"
