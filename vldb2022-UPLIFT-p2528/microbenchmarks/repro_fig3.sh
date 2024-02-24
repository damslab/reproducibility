#!/bin/bash
# Figure 3

# Figure 3a: Speedup with threads
./runSpeedupThreads.sh

# Figure 3b: Speedup with rows
./runSpeedupRows.sh

# Figure 3c: Transformation phases
./runTimebreak.sh

# Figure 3d: Row partitions
./runRowpartitions.sh

rm *.mtd
