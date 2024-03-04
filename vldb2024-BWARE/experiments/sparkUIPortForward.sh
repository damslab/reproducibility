#!/bin/bash

## Main server.
ssh -f -N -L 8088:so001:8088 so001 & 
