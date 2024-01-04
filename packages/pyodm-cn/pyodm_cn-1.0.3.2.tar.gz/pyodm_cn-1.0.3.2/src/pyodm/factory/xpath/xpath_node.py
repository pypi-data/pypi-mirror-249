class XpathNode:
    def __init__(self, name):
        self.name = name
        self.parent: list[int] = []
        self.children: list[int] = []

    def __eq__(self, other):
        return self.name == other.name

    def isRoot(self): return len(self.parent) == 0
