import html
from jinja2 import Environment
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.styles import Style
from prompt_toolkit import HTML
import toml
from pathlib import Path

SECTION_CONFIG = 'config'
KEY_DEFAULT = "default"
KEY_PROMPT = "prompt"
KEY_CHOICES = "choices"

TRUE_FALSE = {
    "t":True,
    "true": True,
    "f":False,
    "false":False,
}

YES_NO = {
    "y":True,
    "yes": True,
    "n":False,
    "no":False,
}

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

def expand(s:str, e:Environment, ctx:dict):
    try:
        template = e.from_string(s)
        r = template.render(ctx)
    except:
        r = s
    return r

def esc(s):
    r = s
    if isinstance(s, str):
        r = html.escape(s)
    return r

def get_user_input(toml_obj: dict):
    env = Environment()
    r = {}
    for key, value, in toml_obj[SECTION_CONFIG].items():
        if KEY_DEFAULT not in value.keys():         
            raise Exception(f'Error: default for "{key}" does not exist in "prj.toml"')
        df = expand(value[KEY_DEFAULT], env, r)
        if KEY_PROMPT in value.keys():         
            pr = expand(value[KEY_PROMPT], env, r)
            if KEY_CHOICES in value.keys():
                ch = value[KEY_CHOICES]
                df = get_choices(key, ch, df, pr)
            elif isinstance(df, bool):
                df = get_bool(df, pr, TRUE_FALSE)
            else:
                v = prompt(HTML(f'{esc(pr)} <skyblue>({esc(df)})</skyblue>: '))
                if len(v) > 0:
                    df = v
        r[key] = df
    return r

def get_choices(key, ch, df, pr):
    print(f'{pr} choices,')
    chidx = int(df)
    if chidx >= 0 and chidx < len(ch):
        pass
    else:
        raise Exception(f'Error: default for "{key}" is not valid in "prj.toml"')
    while True:
        for i in range(len(ch)):
            print(f'    [{i+1}] {ch[i]}')
        v = prompt(HTML(f'{esc(pr)} <skyblue>({esc(chidx+1)})</skyblue>: '))
        if len(v) > 0:
            chidx = int(v)-1
            if chidx >= 0 and chidx < len(ch):
                df = ch[chidx]
                break
        else:
            df = ch[chidx]
            break
    return df

def get_bool(df, pr, bool_dict):
    val = f'{df}'.lower()
    while True:
        v = prompt(HTML(f'{esc(pr)} <skyblue>({val})</skyblue>: '))
        if len(v) > 0:
            try:
                df = bool_dict[v.lower().strip()]
                break
            except KeyError:
                pass
        else:
            break
    return df