#!/bin/bash

## Main server.
ssh -f -N -L 8088:charlie:8088 charlie & 
