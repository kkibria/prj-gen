from abc import ABC
import copy
from .user_input import get_toml, get_user_input, set_template_dir

class Gen(ABC):
    def __init__(self, path: str) -> None:
        self.template_dir = set_template_dir(path)

    def get_toml(self):
        self.toml = get_toml(self.template_dir)

    def pre_process(self):
        r = copy.copy(self.config)
        r["pre_injected"]= "pre_injected_value"
        self.pre = r

    def post_process(self):
        r = copy.copy(self.pre)
        r["post_injected"] = "post_injected_value"
        self.post = r

    def run(self):
        self.get_toml()
        self.config = get_user_input(self.toml)
        self.pre_process()
        print(self.pre)  
        self.post_process()  
        print(self.post)  

    