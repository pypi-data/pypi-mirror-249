from enum import Enum, auto
from typing import Optional


class Task(Enum):
    RECT = 0
    POINT = auto()
    POLYGON = auto()

    def map_str(self):
        return {
            0: "rectangle",
            1: "point",
            2: "polygon",
        }[self.value]


class Mode(Enum):
    READ = 0
    MARK = auto()
    DOODLE = auto()

    def map_str(self):
        return {
            0: "reading",
            1: "marking",
            2: "doodling",
        }[self.value]
