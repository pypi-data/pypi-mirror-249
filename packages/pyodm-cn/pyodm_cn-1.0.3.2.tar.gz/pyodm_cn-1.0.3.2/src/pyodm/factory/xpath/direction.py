from enum import Enum


class Direction(Enum):
    FROM = 'from' # 上到下
    TO = "to" # 下到上
    INCLUDE = "include" # 包含