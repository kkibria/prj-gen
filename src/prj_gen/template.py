from pathlib import Path
import re
from warnings import warn
from jinja2 import Environment, FileSystemLoader
import toml

def process_folder(gen_obj, dir:Path, tgt:Path, ctx:dict):
    tgt.mkdir(exist_ok=True)
    env = Environment(loader=FileSystemLoader(dir))
    for i in dir.iterdir():
        # if i_name is jinja comment then strip the comment tags and set a flag
        special = None
        m = re.match(r"^{#(.+)#}(.*)$", i.name)
        if m is not None:
            fn = m.group(1).strip()
            ext = m.group(2).strip()
            if '.toml' == ext:
                special = i.name
                i_name = fn
            else:
                i_name = fn + ext
        else:
            fntemplate = env.from_string(i.name)
            i_name = fntemplate.render(ctx)

        if len(i_name) > 0:
            i_tgt = tgt.joinpath(i_name)

            if i.is_dir():
                process_folder(gen_obj, i, i_tgt, ctx)

            elif i.is_file():
                if special is None:
                    template = env.get_template(i.name)
                    rend = template.render(ctx)
                else:
                    toml_obj = None
                    with open(dir.joinpath(special), 'r', encoding='utf-8') as f:
                        toml_obj = toml.load(f)
                    try:
                        content = gen_obj._special_content(toml_obj)
                    except NotImplementedError as e:
                        path = "/".join(dir.joinpath(special).parts)
                        raise NotImplementedError(f'Template "{path}" failed. {e.args[0]}') from e

                    template = env.from_string(content)
                    rend = template.render(ctx)

                if i_tgt.exists():
                    path = "/".join(i_tgt.parts)
                    warn(f'overwriting "{path}"')
                    
                with i_tgt.open("w") as fdst:
                    fdst.write(rend)
        else:
            path = "/".join(dir.joinpath(i.name).parts)
            warn(f'"{path}" skipped, name yields to empty string')
