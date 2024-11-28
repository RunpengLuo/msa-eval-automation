#!/bin/bash
#SBATCH --job-name=j_VCMSA_AAA_r1     # create a short name for your job
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=4G         # memory per cpu-core (4G is default)
#SBATCH --gres=gpu:1             # number of gpus per node
#SBATCH --time=00:10:00           # total run time limit (HH:MM:SS)
#SBATCH --mail-type=begin        # send email when job begins
#SBATCH --mail-type=end          # send email when job ends
#SBATCH --mail-type=fail         # send email if job fails
#SBATCH --mail-user=rl6004@cs.princeton.edu
conda init bash
source ~/.bashrc

conda activate "vcmsa-env"

export TRANSFORMERS_CACHE="./.cache"
export HF_HOME="./.cache"
export HF_DATASETS_CACHE="./.cache"
export TORCH_HOME="./.cache"

mkdir -p jobs/dir_VCMSA_AAA_r1

time python -u ./vcmsa/bin/vcmsa \
    -m "./prot_t5_xl_half_uniref50-enc" \
    -i ./example/AAA.fasta \
    -o jobs/dir_VCMSA_AAA_r1/alignment.aln \
    -p 0 \
    -st 0.7 \
    -mi 100 \
    -l "-16 -15 -14 -13 -12 -11 -10 -9 -8 -7 -6 -5 -4 -3 -2 -1" \
    -eout jobs/dir_VCMSA_AAA_r1/embedding \
    -pca \
    --rbh_outfile jobs/dir_VCMSA_AAA_r1/rbh \
    --sim_outfile jobs/dir_VCMSA_AAA_r1/seq_similarity \
    --log INFO
