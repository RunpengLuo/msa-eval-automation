import os
import sys

import subprocess

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{sys.argv[0]} <slurm_dir>")
        sys.exit(1)

    _, slurm_dir = sys.argv
    num_jobs = 0
    for jf in os.listdir(slurm_dir):
        jfile = os.path.join(slurm_dir, jf)
        if not jfile.endswith(f".sh"):
            continue
        print(f"submit job: {jf}")
        p = subprocess.run(["sbatch", jfile], text=True, capture_output=True)
        print(f"jobid={p.stdout.split()[-1]}")
        num_jobs += 1
    
    print(f"Number of jobs submitted: {num_jobs}")
    sys.exit(0)