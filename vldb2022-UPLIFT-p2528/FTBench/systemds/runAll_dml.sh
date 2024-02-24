#!/bin/bash
# Figure 4

# Figure 4a
./repro_ftbench_systemds.sh T1

# Figure 4b
./repro_ftbench_systemds.sh T8
./repro_ftbench_systemds.sh T5
./repro_ftbench_systemds.sh T2

# Figure 4c
./repro_ftbench_systemds.sh T3
./repro_ftbench_systemds.sh T4
./repro_ftbench_systemds.sh T6
./repro_ftbench_systemds.sh T7
./repro_ftbench_systemds.sh T9
./repro_ftbench_systemds.sh T12

# Figure 4d
./repro_ftbench_systemds.sh T10
./repro_ftbench_systemds.sh T11

# Figure 4e
./runFig4e.sh

# Figure 4f
./repro_ftbench_systemds.sh T13

# Figure 4g
./repro_ftbench_systemds.sh T14

# Figure 4h
./repro_ftbench_systemds.sh T15

rm *.mtd
