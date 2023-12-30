# Handling of circuits

# Saves a new route
from ctypes.wintypes import HANDLE
from enum import Enum

"""_summary_
No need to start 
"""
class HoldType(Enum):
    FOOT = 0
    HAND = 1
    TOP = 3
    FOOT_START = 4
    HAND_START = 5
    UNKNWON = 6


class Hold():
    x = -1
    y = -1
    type = HoldType.UNKNWON
    position = 0

    def __init__(self, x:int, y:int, type:HoldType, position:int) -> None:
        self.x = x
        self.y = y
        self.type = type
        self.position = position
        


class Route():
    hold_list = []
    user = "Unknown"
    grade = "unknown"
    length = ""

    def __init__(self) -> None:
        pass

    def __init__(self, hold_list: [Hold]) -> None:
        self.hold_list = hold_list

    def addHold(self, hold: Hold) -> None:
        self.hold_list.append(hold)

    def save(self):
        self.db.save()
