import os
import sys

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
        os.system(f"sbatch {jfile}")
        num_jobs += 1
    
    print(f"Number of jobs submitted: {num_jobs}")
    sys.exit(0)