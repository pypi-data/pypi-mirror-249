from pyodm.exceptions import ParserException
from pyodm.factory.xpath.direction import Direction
from pyodm.factory.xpath.xpath import Xpath
from pyodm.factory.xpath.xpath_node import XpathNode


class XpathTree:
    """
    特殊的树形结构,非通用数据结构,仅适用 XPATH 功能
    目标 : 解析并保存 Class 的树形结构
    """
    def __init__(self):
        self._nodes: list[XpathNode] = []

    def count(self):
        return len(self._nodes)

    def add(self, parent, children):
        self._add_parent(parent)
        self._add_child(parent, children)

    def find(self, node: XpathNode) -> int:
        try:
            return self._nodes.index(node)
        except ValueError as e:
            return -1

    def _add_parent(self, parent):
        i = self.find(parent)
        if i == -1:
            self._nodes.append(parent)

    def _add_child(self, parent, children):
        # 获取父节点索引
        i = self.find(parent)
        for child in children:
            j = self.find(child)
            if j == -1:
                # 如果子节点不存在
                self._nodes.append(child)
                child.parent.append(i)
                self._nodes[i].children.append(self.count() - 1)
            else:
                # 如果子节点已存在
                self._nodes[j].parent.append(i)
                self._nodes[i].children.append(j)

    def children_by_name(self, node_name: str) -> list[XpathNode]:
        for node in self._nodes:
            if node.name == node_name:
                return [self._nodes[i] for i in node.children]
        return []

    def children_by_node(self, node: XpathNode) -> list[XpathNode]:
        return [self._nodes[i] for i in node.children]

    def roots(self) -> list:
        results = []
        for i, node in enumerate(self._nodes):
            if node.isRoot(): results.append(i)
        return results

    def _sub_paths(self, node: int) -> list:
        path = []
        for child in self._nodes[node].children:
            if child == node: continue  # 如果子节点含有父亲节点
            sub_path = [node]
            if self._nodes[child].children:
                for branch in self._sub_paths(child):
                    new_branch = sub_path.copy()
                    new_branch.extend(branch)
                    if new_branch not in path:
                        path.append(new_branch)
            else:
                sub_path.append(child)
                if sub_path not in path:
                    path.append(sub_path)
        return path

    def _all_path_index(self):
        path = []
        for root in self.roots():
            if self._nodes[root].children:
                new_branch = self._sub_paths(root)
                if new_branch not in path:
                    path.extend(self._sub_paths(root))
        return path

    def _all_path_name(self):
        return [[self._nodes[i].name for i in indexes] for indexes in self._all_path_index()]

    def xpath(self, node_name=None, direction: Direction = Direction.FROM):
        paths = self._all_path_name()
        if node_name is not None:
            if direction == Direction.FROM:
                paths = Xpath(paths).start(name=node_name).paths
            elif direction == Direction.TO:
                paths = Xpath(paths).end(name=node_name).paths
            elif direction == Direction.INCLUDE:
                paths = Xpath(paths).contain(name=node_name).paths
            else:
                raise ParserException("direction is wrong")
        return list(set(["/".join(path) for path in paths]))

    def xpath_range(self, start: str, end: str):
        paths = self._all_path_name()
        paths = Xpath(paths).start(start).end(end).paths
        return list(set(["/".join(path) for path in paths]))
