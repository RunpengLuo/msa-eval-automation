import configparser
from lib.utils import *
from lib.conf_slurm import slurm_header

def vcmsa_cmd(conf: configparser.ConfigParser, 
              dataset: str, method: str, 
              fa_file: str):
    confd = conf["DEFAULT"]
    confm = conf[method]
    job_dir = get_dir(parse_quote(confd["job_dir"]))
    job_sfx = parse_quote(confd["job_sfx"])
    out_dir = f"{job_dir}/dir_{method}_{dataset}_{job_sfx}"
    scratch_dir = get_dir(parse_quote(confd["scratch_dir"]))
    cache_path = f"{scratch_dir}/.cache"

    vcmsa_path = parse_quote(confm["prog_path"])

    conda_env = confm["conda_env"]
    model = confm["model"]
    padding = confm["padding"]
    mi = confm["max_iterations"]
    sst = confm["seqsimthresh"]
    layers = confm["layers"]

    s_header = slurm_header(f"j_{method}_{dataset}_{job_sfx}", confd)
    s_body = [
        f"conda activate {conda_env}",
        "",
        f"export TRANSFORMERS_CACHE=\"{cache_path}\"",
        f"export HF_HOME=\"{cache_path}\"",
        f"export HF_DATASETS_CACHE=\"{cache_path}\"",
        f"export TORCH_HOME=\"{cache_path}\"",
        "",
        f"mkdir -p {out_dir}",
        "",
        f"time python -u {vcmsa_path}/bin/vcmsa \\",
        f"    -m {model} \\",
        f"    -i {fa_file} \\",
        f"    -o {out_dir}/alignment.aln \\",
        f"    -p {padding} \\",
        f"    -st {sst} \\",
        f"    -mi {mi} \\",
        f"    -l {layers} \\",
        f"    -eout {out_dir}/embedding \\",
        f"    -pca \\",
        f"    --rbh_outfile {out_dir}/rbh \\",
        f"    --sim_outfile {out_dir}/seq_similarity \\",
        f"    --log INFO",
    ]

    s_end = []

    return s_header + s_body + s_end