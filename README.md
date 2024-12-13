## MSA automation evaluation

```sh
# generate scripts via config file conf.ini
$python generate_scripts.py
generate_scripts.py <conf.ini>

# submit all jobs to SLURM cluster and print JOB ID
$python submit_jobs.py 
submit_jobs.py <slurm_dir>
```