#!/bin/bash

sysctl kernel.kptr_restrict=0
sysctl kernel.perf_event_paranoid=1

