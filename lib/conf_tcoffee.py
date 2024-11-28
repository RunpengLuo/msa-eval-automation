import configparser
from lib.utils import *
from lib.conf_slurm import slurm_header


def tcoffee_cmd(conf: configparser.ConfigParser, 
                dataset: str, method: str, 
                fa_file: str):
    confd = conf["DEFAULT"]
    confm = conf[method]
    job_dir = get_dir(parse_quote(confd["job_dir"]))
    job_sfx = parse_quote(confd["job_sfx"])
    out_dir = f"{job_dir}/dir_{method}_{dataset}_{job_sfx}"
    scratch_dir = get_dir(parse_quote(confd["scratch_dir"]))
    cache_path = f"{scratch_dir}/.cache"

    tcoffee_path = parse_quote(confm["prog_path"])

    s_header = slurm_header(f"j_{method}_{dataset}_{job_sfx}", confd)
    s_body = []
    s_end = []

    return s_header + s_body + s_end