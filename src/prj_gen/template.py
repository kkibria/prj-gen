from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def process_folder(dir:Path, tgt:Path, ctx:dict):
    tgt.mkdir(exist_ok=True)
    env = Environment(loader=FileSystemLoader(dir))
    for i in dir.iterdir():
        fntemplate = env.from_string(i.name)
        i_tgt = tgt.joinpath(fntemplate.render(ctx))
        if i.is_dir():
            process_folder(i, i_tgt, ctx)
        elif i.is_file():
            template = env.get_template(i.name)
            rend = template.render(ctx)
            with i_tgt.open("x") as fdst:
                fdst.write(rend)


