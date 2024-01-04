from enum import Enum


class WriteStatus(Enum):

    IGNORE = 100
    """该节点未使用"""

    PASS = 400
    """该节点的类型不对,判断是否另外的类型"""

    OK = 200
    """该节点正确处理"""