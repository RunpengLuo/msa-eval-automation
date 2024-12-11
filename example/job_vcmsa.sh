#!/bin/bash
#SBATCH --job-name=vcmsa-gpu     # create a short name for your job
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=2        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=8G         # memory per cpu-core (4G is default)
#SBATCH --gres=gpu:1             # number of gpus per node
#SBATCH --time=00:10:00           # total run time limit (HH:MM:SS)
#SBATCH --mail-type=begin        # send email when job begins
#SBATCH --mail-type=end          # send email when job ends
#SBATCH --mail-type=fail         # send email if job fails
#SBATCH --mail-user=

conda init bash
source ~/.bashrc

PROJ_PATH=.
VCMSA_PATH=${PROJ_PATH}/vcmsa

conda activate ${PROJ_PATH}/vcmsa_env

CACHE_PATH=${PROJ_PATH}/.cache
export TRANSFORMERS_CACHE=${CACHE_PATH}
export HF_HOME=${CACHE_PATH}
export HF_DATASETS_CACHE=${CACHE_PATH}
export TORCH_HOME=${CACHE_PATH}

layers="-16 -15 -14 -13 -12 -11 -10 -9 -8 -7 -6 -5 -4 -3 -2 -1" #@param  {type:"string"}
sequence_similarity_threshold=0.7 #@param  {type:"number"}
padding=0 #@param {type:"integer"}
max_iterations=100 #@param {type:"integer"}
seqsimthresh=0.7

fasta_file=${PROJ_PATH}/datasets/AAA.top3.fasta
job_dir=${PROJ_PATH}/output_AAA_top3_gpu
model_dir="${PROJ_PATH}/prot_t5_xl_half_uniref50-enc"

echo $fasta_file
echo $job_dir
echo $model_dir
echo $layers
echo $padding
echo $seqsimthresh
echo $max_iterations

mkdir -p $job_dir
time python -u ${VCMSA_PATH}/bin/vcmsa -m $model_dir \
    -i $fasta_file -o ${job_dir}/alignment.aln \
    -p ${padding} -st ${seqsimthresh} \
    -mi ${max_iterations} -l ${layers} \
    -eout ${job_dir}/embedding \
    -pca --rbh_outfile ${job_dir}/rbh \
    --sim_outfile ${job_dir}/seq_similarity \
    --log INFO  |& tee ${job_dir}/vcmsa.log
