from math import sqrt
import pygame as pg


class Node:
    def __init__(self, x, y, isAnchor, world):
        self.x = x
        self.y = y
        self.isAnchor = isAnchor
        self.fixedCount = 0
        self.nextFixedCount = 0
        self.world = world
        self.adj = []
        self.prob = [[1.0 for _ in range(self.world.width - 1)]
                     for _ in range(self.world.height - 1)]

    def distXY(self, x, y):
        return sqrt((self.x - x)**2 + (self.y - y)**2)

    def dist(self, node):
        return self.distXY(node.x, node.y)

    def isClose(self, node):
        return self.dist(node) < self.world.transmitRange

    def isFixed(self):
        return self.isAnchor or self.fixedCount >= 3

    def updateFixed(self):
        self.fixedCount = self.nextFixedCount
        self.nextFixedCount = 0
        for node in self.adj:
            self.nextFixedCount += (1 if node.isFixed() else 0)
        return self.fixedCount != self.nextFixedCount

    def addAdj(self, node):
        self.adj.append(node)
        self.nextFixedCount += (1 if node.isAnchor else 0)

    def multProbGrid(self, node):
        d = self.dist(node)
        for y in range(self.world.height - 1):
            for x in range(self.world.width - 1):
                self.prob[y][x] *= self.world.err(d - node.distXY(x, y))

    def display(self):
        pg.draw.circle(self.world.screen, (255, 0, 0) if self.isAnchor else (0, 0, 255), (self.x *
                                                                                          self.world.blockSize, self.y * self.world.blockSize), 6)


if __name__ == '__main__':
    pass
