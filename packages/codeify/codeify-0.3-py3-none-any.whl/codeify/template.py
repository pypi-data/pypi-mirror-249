from jinja2 import Environment, FileSystemLoader
from typing import List

class Template:
    def __init__(self, template_paths: List[str]):
        self._env = Environment(loader=FileSystemLoader(template_paths, followlinks=True))
