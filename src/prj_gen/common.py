from pathlib import Path
from .userinput import get_choices_from_list
from requests_cache import CachedSession

KEY = "key"

def get_license(path, name):
    """
    Fetch license list from GitHub, let the user choose one,
    then write its body to LICENSE.txt in `path`.
    """
    # Cache location: ~/.<name>/http_cache
    session = CachedSession(f'~/.{name}/http_cache', backend='sqlite')

    # 1) Get list of licenses
    response = session.get('https://api.github.com/licenses', timeout=10)
    response.raise_for_status()
    lics = response.json()
    if not lics:
        print("No licenses returned from GitHub.")
        return

    names = [item["name"] for item in lics]
    urls = [item["url"] for item in lics]

    # 2) Let user choose a license (your existing helper)
    i_lic = get_choices_from_list(key="License", ch=names, df=0, pr="License")
    idx = i_lic[KEY]

    # 3) Fetch the full license JSON using the SAME session
    detail_resp = session.get(urls[idx], timeout=10)
    detail_resp.raise_for_status()
    lic = detail_resp.json()

    # 4) Write body to LICENSE.txt
    dst = Path(path).joinpath("LICENSE.txt")
    dst.write_text(lic["body"], encoding="utf-8")

    print(f"Saved license '{lic.get('name', names[idx])}'.\nPlease read it carefully and update anything necesary.")
