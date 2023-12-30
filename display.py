from wall import Wall
from bloc import *

class DisplayInterface():
    def __init__(self) -> None:
        pass

    def refresh(self):
        pass

    def displayHold(self, hold:Hold):
        pass

    def displayRoute(self, route:Route):
        pass


def replace_str_index(text,index=0,replacement=''):
    return f'{text[:index]}{replacement}{text[index+1:]}'


class consoleDisplay(DisplayInterface):
    holdChar = {
        HoldType.FOOT: "o",
        HoldType.HAND: "x",
        HoldType.TOP: "0",
        HoldType.FOOT_START: "O",
        HoldType.HAND_START: "X"
    }

    def __init__(self, wall:Wall) -> None:
        self.wall = wall
        self.displayEmptyWall()
    
    def displayEmptyWall(self):
        self.wallStr = ("| "*self.wall.width+"|\n")*self.wall.height

    def refresh(self) -> None:
        print('\33[2J')
        print(self.wallStr)

    def getHoldPosition(self, hold:Hold) -> int:
        return 1 + hold.x*2 + (self.wall.width*2 +2)*hold.y

    def displayHold(self, hold:Hold)->None:
        self.wallStr = replace_str_index(self.wallStr, self.getHoldPosition(hold), self.holdChar[hold.type])

    def displayRoute(self, route:Route)->None:
        for hold in route.hold_list:
            self.displayHold(hold)


import board
import neopixel

class ledDisplay(DisplayInterface):
    ledStrips = []
    maxBrightness = 255
    holdColor = {
        HoldType.FOOT: (maxBrightness, maxBrightness, 0),
        HoldType.HAND: (0, maxBrightness, 0),
        HoldType.TOP: (maxBrightness, 0, 0),
        HoldType.FOOT_START: (0,0,maxBrightness),
        HoldType.HAND_START: (0,maxBrightness,maxBrightness)
    }

    def __init__(self, wall:Wall) -> None:
        self.wall = wall
        # self.displayEmptyWall()

    def initMapping(self, mapping)-> None:
        """Sets the mapping between (X,Y) wall coordinates and (led strip,led)

        :param mapping:  dict with {(X, Y): (led strip,led)}
        """
        self.ledMapping = mapping
    
    def initControlPin(self, mapping)-> None:
        """Sets the mapping of led strip to digital output

        :param mapping: array with [DO0, DO1, DO2, ...]
        """
        self.doMapping = mapping
    
    def initPixel(self) -> None:
        for do in self.doMapping:
            self.ledStrips.append(neopixel.NeoPixel(do, 30))

    def displayEmptyWall(self):
        for ls in self.ledStrips:
            ls.fill((0,0,0))

    def refresh(self) -> None:
        for ls in self.ledStrips:
            ls.show()

    def displayHold(self, hold:Hold)->None:
        doIndex, ledIndex = self.ledMapping[(hold.x, hold.y)]
        self.ledStrips[doIndex][ledIndex] = self.holdColor[hold.type]

    def displayRoute(self, route:Route)->None:
        for hold in route.hold_list:
            self.displayHold(hold)


from mapping import ledMapping, doMapping
import time

if __name__ == "__main__":
    w = Wall(10, 10)
    h0 = Hold(4, 4, HoldType.HAND, 0)
    r = Route([Hold(0, 0, HoldType.FOOT_START, 0),
               Hold(0, 1, HoldType.HAND_START, 0),
               Hold(0, 2, HoldType.HAND_START, 0),
               Hold(0, 3, HoldType.HAND, 1),
               Hold(0, 4, HoldType.HAND, 2),
               Hold(0, 5, HoldType.TOP, 3)])
    # cd = consoleDisplay(w)
    # cd.displayRoute(r)
    # cd.refresh()

    ld = ledDisplay(w)
    ld.initMapping(ledMapping)
    ld.initControlPin(doMapping)
    ld.initPixel()
    ld.displayRoute(r)
    ld.refresh()
    time.sleep(5)
    ld.displayEmptyWall()
