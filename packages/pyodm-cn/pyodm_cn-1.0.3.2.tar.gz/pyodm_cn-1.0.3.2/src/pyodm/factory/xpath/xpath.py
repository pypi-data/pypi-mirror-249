class Xpath:
    def __init__(self, paths: list):
        self._paths = paths

    def start(self, name: str):
        self.contain(name)
        self._paths = [path[path.index(name):len(path)] for path in self._paths]
        return self

    def contain(self, name: str):
        self._paths = list(filter(lambda x: name in x, self._paths))
        return self

    def end(self, name: str):
        self.contain(name)
        self._paths = [path[0:path.index(name)+1] for path in self._paths]
        return self

    @property
    def paths(self): return self._paths
