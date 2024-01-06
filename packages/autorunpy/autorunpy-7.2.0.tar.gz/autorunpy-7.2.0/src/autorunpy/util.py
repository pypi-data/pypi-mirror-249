import json
from pathlib import Path

class Conf :
    pkg = 'pip_pkg'  # GitHub url of the target repo
    py_ver = 'py_ver'  # python version to use
    module = "module"  # module name to run
    rm_venv = 'rm_venv'  # whether to remove venv

def read_json(fp) :
    # if fp is not entered with .json extension, add it
    fp = Path(fp).with_suffix('.json')

    # assume cd is the GitHub dir
    fp = Path.cwd() / 'auto-run-configs' / fp

    with open(fp , 'r') as f :
        return json.load(f)
