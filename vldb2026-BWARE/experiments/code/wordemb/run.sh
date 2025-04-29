#!/bin/bash

exrep=3
profileEnabled=1

# source code/wordemb/preprocess.sh

# as=("1000 3000 10000 30000 100000 300000 1000000 4000000")
# ws=("10000 100000")
timeout=7200

as=("300000 1000000")
ws=("3000")
# source code/wordemb/emb.sh

as=("100000 300000 1000000")
as=("1000000")
as=("1000 3000 10000 30000 100000")
# as=("1000 3000")
# as=("1000")
# as=("100000")
# BUG for 999995
ws=("1000 3000 10000 100000")
ws=("3000 10000 100000")
ws=("3000")
# ws=("10000 100000")
# ws=("100000")
# ws=("10000")
# ws=("1000 10000 100000")
# ws=("100000")
# ws=("10000 100000 999995")
# ws=("100000 999995")

timeout=7200

source code/wordemb/emb.sh

# abstracts
as=("1000 3000 10000 30000 100000 300000 1000000 3000000")
# as=("1000 3000 10000 30000 100000")
# as=("1000")
# as=("1000 3000 10000 30000 100000")
# as=("30000")
# as=("100000")
# as=("1000")
# as=("3000")
# as=("10000")

# unique words
ws=("100 1000 10000")
# ws=("1000")
# ws=("10000")
# ws=("100")
# ws=("10000")

# abstract lengths
al=("10 100 1000")
# al=("1000")
# al=("100")

# neuralnetwork
# source code/wordemb/emb_nn.sh
# source code/wordemb/emb_tf_nn.sh
# source code/wordemb/emb_torch_nn.sh
