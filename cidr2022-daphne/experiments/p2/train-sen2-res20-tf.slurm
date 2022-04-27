#!/usr/bin/env bash
# These can also be specified on the command-line.
# We place them here so that we don't accidentally forget.
#!/usr/bin/env bash
# These can also be specified on the command-line.
# We place them here so that we don't accidentally forget.
#SBATCH --nodes=1
#SBATCH --gpus-per-node=1
#SBATCH --nodelist=nvcluster-node2
#SBATCH --mail-type=all
#SBATCH --mail-user=dokter@tugraz.at  # Where to send mail
#SBATCH --time=12:34:56               # Time limit hrs:min:sec


# export CUDA_DEVICE_ORDER="PCI_BUS_ID"
# export CUDA_VISIBLE_DEVICES="1"

# Change to local storage on assigned node
cd ~/local

pwd; hostname; date

source ~/daphne/venv/bin/activate

cd ~/daphne/experiments

time python3 resnet20-training.py dataset=sen2 datadir=~/local 

date
