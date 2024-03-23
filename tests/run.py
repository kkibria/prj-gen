import os
from pathlib import Path
from prj_gen.generator import Gen

class MyGen(Gen):
    def pre_process(cls, r, params):
        print(params)
        r["pre_injected"] = "pre_injected_value"

    def post_process(cls, r, params):
        r["post_injected"] = "post_injected_value"

    # def select_project(cls, ctx:dict, params):
    #     return 'prj1'

g = MyGen("template")
dst = Path("target")
g.update_params({"path": "../abc"})
g.run(dst)
print(g.pre)
print(g.post)
