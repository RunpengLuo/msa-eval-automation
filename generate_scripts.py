import os
import sys
import configparser

from lib.utils import *

from lib.conf_vcmsa import vcmsa_cmd
from lib.conf_tcoffee import tcoffee_cmd

cmds = {
    "VCMSA": vcmsa_cmd,
    "T-COFFEE": tcoffee_cmd
}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{sys.argv[0]} <conf.ini>")
        sys.exit(1)

    _, cfile = sys.argv
    conf = configparser.ConfigParser(inline_comment_prefixes="#")
    conf.read(cfile)

    ddir = get_dir(parse_quote(conf["DEFAULT"]["dataset_dir"]))
    assert os.path.isdir(ddir), f"{ddir} does not exists"
    dsfx = parse_quote(conf["DEFAULT"]["dataset_sfx"])
    jsfx = parse_quote(conf["DEFAULT"]["slurm_sfx"])

    sdir = get_dir(parse_quote(conf["DEFAULT"]["slurm_dir"]))
    os.makedirs(sdir, exist_ok=True)

    datasets = [*map(parse_quote, conf["DEFAULT"]["datasets"].split())]
    methods = [*map(parse_quote, conf["DEFAULT"]["methods"].split())]

    fasta_files = []
    for dataset in datasets:
        fa_file = f"{ddir}/{dataset}{dsfx}"
        assert os.path.isfile(fa_file), f"{fa_file} does not exists"
        fasta_files.append((dataset, fa_file))

    for method in methods:
        for (dataset, fa_file) in fasta_files:
            print(f"generate script for {method} - {dataset}")
            assert (method in conf.sections() and method in cmds), \
                f"{method} config does not exists"
            ofile = f"{sdir}/job_{method}_{dataset}_{jsfx}.sh"
            cmd = cmds[method](conf, dataset, method, fa_file)
            with open(ofile, 'w') as fd:
                for l in cmd:
                    fd.write(f"{l}\n")
                fd.close()
