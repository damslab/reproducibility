#!/bin/bash

# This script takes ~12.5 hours to complete

# Figure 6: Lineage Tracing Overhead
./exp_6a.sh   #Runtime Overhead
./exp_6b.sh   #Space Overhead

# Figure 7: Partial Reuse and Multi-level Reuse
./exp_7a.sh   #Partial Reuse
./exp_7b.sh   #Multi-level Reuse

# Figure 8: Cache Eviction Policies
./exp_8a.sh   #Pipeline with Phases
./exp_8b.sh   #Pipeline Comparison

exit
