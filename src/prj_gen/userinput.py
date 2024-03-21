import html
from jinja2 import Environment, FileSystemLoader
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.styles import Style
from prompt_toolkit import HTML
import toml
from pathlib import Path

SECTION_CONFIG = 'config'
KEY_DEFAULT = "default"
KEY_PROMPT = "prompt"
KEY_CHOICES = "choices"
KEY_YN = "yesno"

TF2BOOL = {
    "t":True,
    "true":True,
    "f":False,
    "false":False,
}

BOOL2TF = {
    True: "true",
    False: "false",
}

YN2BOOL = {
    "y":True,
    "yes":True,
    "n":False,
    "no":False,
}

BOOL2YN = {
    True: "yes",
    False: "no",
}

def get_toml(td:Path):
    fn = 'prj.toml'
    fp = td.joinpath(fn)
    if not fp.exists():
        raise Exception(f'Error: "{fn}" does not exist')
    if not fp.is_file():
        raise Exception(f'Error: "{fn}" is not a file')
    with open(fp, 'r', encoding='utf-8') as f:
    	return toml.load(f)

def set_template_dir(path: str):
    td = Path(path)
    if not td.exists():
        raise Exception(f'Error: template path "{path}" does not exist')
    if not td.is_dir():
        raise Exception(f'Error: template path "{path}" is not a folder')
    return td

def expand(s:str, e:Environment, ctx:dict):
    if not isinstance(s, str):
        return s
    template = e.from_string(s)
    r = template.render(ctx)
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
                if isinstance(ch, list):
                    df = get_choices_from_list(key, ch, df, pr)
                elif isinstance(ch, dict):
                    df = get_choices_from_dict(key, ch, df, pr)
                elif isinstance(ch, str):
                    df = get_choices_from_dict(key, ch.split(), df, pr)
                else:
                    raise Exception(f'Error: choices for "{key}" is not valid in "prj.toml"')

            elif isinstance(df, bool):
                useyn = False
                if KEY_YN in value.keys():
                    yn = value[KEY_YN]
                    if not isinstance(yn, bool):
                        raise Exception(f'Error: "yesno" value for "{key}" is not valid in "prj.toml"')
                    if yn:
                        useyn = True
                if useyn:
                    df = get_bool(df, pr, BOOL2YN, YN2BOOL)
                else:         
                    df = get_bool(df, pr, BOOL2TF, TF2BOOL)
            else:
                v = prompt(HTML(f'{esc(pr)} <skyblue>({esc(df)})</skyblue>: '))
                if len(v) > 0:
                    df = v
        r[key] = df
    return r

def get_choices_from_dict(key:str, ch:dict, df:str, pr:str):
    print(f'{pr} choices,')
    if df not in ch.keys():
        raise Exception(f'Error: default for "{key}" is not valid in "prj.toml"')
    while True:
        for i in ch.keys():
            print(f'    [{i}] {ch[i]}')
        v = prompt(HTML(f'{esc(pr)} <skyblue>({esc(df)})</skyblue>: '))
        if len(v) > 0:
            if v in ch.keys():
                df = v
                break
        else:
            break
    return {"key":df, "val":ch[df]}

def get_choices_from_list(key, ch, df, pr):
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
                break
        else:
            break
    return {"key":chidx, "val":ch[chidx]}

def get_bool(df:bool, pr:str, bool2str:dict, str2bool:dict):
    while True:
        v = prompt(HTML(f'{esc(pr)} <skyblue>({bool2str[df]})</skyblue>: '))
        if len(v) > 0:
            try:
                df = str2bool[v.lower().strip()]
                break
            except KeyError:
                pass
        else:
            break
    return df
