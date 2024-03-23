import re

names = [
    "{#hello#}",
    "{##}.sc",
    "{##}.",
    "{##}",
    "{#hello#}.",
    "{#hello#}.ext",
    "djj.ch",
]

def fixname(name):
    m = re.match(r"^{#(.+)#}(.*)$", name)
    if m is None:
        print(name, m)
    else:
        print(f'"{name}", "{m.group(1)}", "{m.group(2)}"')

for i in names:
    fixname(i)