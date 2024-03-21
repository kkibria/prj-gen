from pathlib import Path
from prj_gen.generator import Gen

class MyGen(Gen):
    def pre_process(cls, r):
        r["pre_injected"] = "pre_injected_value"

    def post_process(cls, r):
        r["post_injected"] = "post_injected_value"

def main():
    g = MyGen("template")
    dst = Path("target")
    g.run(dst)
    print(g.pre)
    print(g.post)
