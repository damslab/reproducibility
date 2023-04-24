#!/bin/bash

## Main server.
# ssh -f -N -L 8088:charlie:8088 charlie & 
ssh -f -N -L 8088:so001:8088 so001 & 

# ssh -f -N -L 8042:so002:8042 so002 &
# ssh -f -N -L 8043:so003:8042 so003 &
# ssh -f -N -L 8044:so004:8042 so004 &
# ssh -f -N -L 8045:so005:8042 so005 &
# ssh -f -N -L 8046:so006:8042 so006 &
# ssh -f -N -L 8047:so007:8042 so007 &
# ssh -f -N -L 8048:so008:8042 so008 &