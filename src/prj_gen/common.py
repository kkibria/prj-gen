import json
from pathlib import Path
from urllib.request import urlopen
from .userinput import get_choices_from_list
from requests_cache import CachedSession

KEY = "key"

# Grab license from github
def get_license(path, name): 
    session = CachedSession(f'~/.{name}/http_cache', backend='sqlite')
    response = session.get('https://api.github.com/licenses')
    lics = response.json()
    if len(lics) < 1:
        return
    names = []
    urls = []  
    for i in lics:
        names.append(i["name"])
        urls.append(i["url"])
    i_lic = get_choices_from_list(key="License", ch=names, df=0, pr="License")
    with urlopen(urls[i_lic[KEY]]) as url:
        lic = json.load(url)
    dst = Path(path).joinpath("LICENSE.txt")
    with dst.open("w") as f:
        f.write(lic["body"])