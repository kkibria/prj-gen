from abc import ABC, abstractmethod
import copy
from pathlib import Path

from .template import process_folder
from .userinput import get_toml, get_user_input, set_template_dir

PRJ_FOLDER = 'prj'

class Gen(ABC):
    def __init__(self, path: str) -> None:
        self.template_dir = set_template_dir(path)
        self.params = {}

    def get_toml(self):
        self.toml = get_toml(self.template_dir)

    @classmethod
    @abstractmethod
    def pre_process(cls, ctx:dict, params):
        pass

    def _pre_process(self):
        r = copy.copy(self.config)
        self.pre = r
        self.pre_process(r, self.params)

    @classmethod
    @abstractmethod
    def post_process(cls, ctx:dict, params):
        pass

    def _post_process(self):
        r = copy.copy(self.pre)
        self.post = r
        self.post_process(r, self.params)

    def run(self, tgt:Path):
        self.get_toml()
        self.config = get_user_input(self.toml)
        self._pre_process()
        process_folder(self.template_dir.joinpath(PRJ_FOLDER), tgt, self.pre)
        self._post_process()

    def update_params(self, params:dict):
        self.params.update(params)
    