from abc import ABC, abstractmethod
import copy
from pathlib import Path
import shutil

from .template import process_folder
from .userinput import get_toml, get_user_input, set_template_dir

PRJ_FOLDER = 'prj'
PARAM_TARGET = '%tgt%'
PARAM_PROJECT = '%prj%'

class Gen(ABC):
    def __init__(self, path: str) -> None:
        self.template_dir = set_template_dir(path)
        self.params = {}

    def get_toml(self):
        self.toml = get_toml(self.template_dir)

    @classmethod
    @abstractmethod
    def pre_process(cls, ctx:dict, params:dict):
        pass

    def _pre_process(self):
        r = copy.copy(self.config)
        p = copy.copy(self.params)
        self.pre = r
        self.pre_process(r, p)

    @classmethod
    @abstractmethod
    def post_process(cls, ctx:dict, params:dict):
        pass

    def _post_process(self):
        r = copy.copy(self.pre)
        p = copy.copy(self.params)
        self.post = r
        self.post_process(r, p)

    @classmethod
    def select_project(cls, ctx:dict, params:dict):
        return PRJ_FOLDER

    def _select_project(self):
        r = copy.copy(self.config)
        p = copy.copy(self.params)
        return self.select_project(r, p)

    @classmethod
    def special_content(cls, ctx:dict, params:dict, toml:dict):
        raise NotImplementedError('Override "special_content" for content generation.')

    def _special_content(self, toml:dict):
        r = copy.copy(self.pre)
        p = copy.copy(self.params)
        return self.special_content(r, p, toml)

    def run(self, tgt:Path) -> bool:
        try:
            self._run(tgt)
        except Exception as err:
            shutil.rmtree(tgt)
            raise
    
    def _run(self, tgt:Path):
        self.params[PARAM_TARGET] = tgt.absolute().as_posix()
        self.get_toml()
        self.config = get_user_input(self.toml)
        self.params[PARAM_PROJECT] = self._select_project()
        self._pre_process()
        process_folder(self, self.template_dir.joinpath(self.params[PARAM_PROJECT]), tgt, self.pre)
        self._post_process()

    def update_params(self, params:dict):
        self.params.update(params)
    