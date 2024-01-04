import pathlib


class PathUtils:
    @staticmethod
    def folder(name: str, current: str) -> pathlib.Path:
        """
        从当前文件路径获取期望开始的绝对路径
        :param name: 期望开始的文件夹名
        :type name: str
        :param current: __file__
        :type current: str
        :return: Path
        :rtype: pathlib.Path
        """
        path = pathlib.Path(current).parent
        while path.name != name:
            path = path.parent
        return path
