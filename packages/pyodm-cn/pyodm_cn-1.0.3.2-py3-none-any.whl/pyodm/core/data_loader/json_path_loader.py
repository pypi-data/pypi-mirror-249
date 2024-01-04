from pyodm.core.support.abstract_path_loader import AbstractPathDataLoader
import json


class JsonPathLoader(AbstractPathDataLoader):
    def load(self):
        with open(self.file, 'r') as f:
            return json.load(f)
