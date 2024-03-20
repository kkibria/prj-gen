from prompt_toolkit import prompt
import toml
from pathlib import Path

def get_toml(td:Path):
    fn = 'prj.toml'
    fp = td.joinpath(fn)
    if not fp.exists():
        raise Exception(f'Error: "{fn}" does not exist')
    if not fp.is_file():
        raise Exception(f'Error: "{fn}" is not a file')
    with open(fp, 'r') as f:
    	return toml.load(f)

def set_template_dir(path: str):
    td = Path(path)
    if not td.exists():
        raise Exception(f'Error: template path "{path}" does not exist')
    if not td.is_dir():
        raise Exception(f'Error: template path "{path}" is not a folder')
    return td

def get_user_input(toml_obj: dict):
    r = {}
    for key, value, in toml_obj['config'].items():
        df = value["default"]
        v = prompt(f'{value["prompt"]} ({df}): ')
        if len(v) == 0:
            v = df
        r[key] = v
    return r