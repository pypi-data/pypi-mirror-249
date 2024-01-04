import abc
import copy


class DFS(abc.ABC):
    def __init__(self, data, cached: bool = False):
        self._data = data
        self._stack = []
        self._cached = cached
        self._scan(self._data)

    @abc.abstractmethod
    def neighbor_node(self, node) -> list:
        ...

    @abc.abstractmethod
    def pruning_strategy(self, node) -> bool:
        ...

    def _scan(self, node):
        if self.pruning_strategy(node):
            self._stack.append(node)
            for child in self.neighbor_node(node):
                self._scan(child)

    def find(self, _lambda):
        __stack = self._stack if not self._cached else copy.deepcopy(self._stack)
        while __stack:
            element = __stack.pop()
            if _lambda(element):
                self.clear_stack()
                return element
        self.clear_stack()
        return None

    def clear_stack(self):
        if not self._cached:
            self._stack = []
