import configparser

def slurm_header(job_name: str, conf: configparser.ConfigParser):
    ncpu = conf["ncpu"]
    cpu_mem = conf["cpu_mem"]
    ngpu = conf["ngpu"]
    tlimit = conf["time_limit"]
    email = conf["user_email"]
    return [
         "#!/bin/bash",
        f"#SBATCH --job-name={job_name}     # create a short name for your job",
         "#SBATCH --nodes=1                # node count",
         "#SBATCH --ntasks=1               # total number of tasks across all nodes",
        f"#SBATCH --cpus-per-task={ncpu}        # cpu-cores per task (>1 if multi-threaded tasks)",
        f"#SBATCH --mem-per-cpu={cpu_mem}         # memory per cpu-core (4G is default)",
        f"#SBATCH --gres={ngpu}             # number of gpus per node",
        f"#SBATCH --time={tlimit}           # total run time limit (HH:MM:SS)",
         "#SBATCH --mail-type=begin        # send email when job begins",
         "#SBATCH --mail-type=end          # send email when job ends",
         "#SBATCH --mail-type=fail         # send email if job fails",
        f"#SBATCH --mail-user={email}"
        "",
        "conda init bash",
        "source ~/.bashrc",
        ""
    ]