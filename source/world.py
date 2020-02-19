from node import Node
from random import randint
from math import sqrt, pi, e
import pygame as pg


class World:
    def __init__(self, width, height, blockSize, transmitRange, agentCount, anchorCount, errDist):
        pg.init()
        pg.display.set_caption("Localization Sim")
        self.width = width
        self.height = height
        self.blockSize = blockSize
        self.screen = pg.display.set_mode(
            (self.width * self.blockSize, self.height * self.blockSize))
        self.nodes = []
        self.transmitRange = transmitRange
        self.errDist = errDist

        for _ in range(agentCount):
            self.addNode(False)
        for _ in range(anchorCount):
            self.addNode(True)
        self.updateFixedStatus()
        self.frame = 0

    def addNode(self, isAnchor):
        ratio = 0.4
        dx = int(self.width * ratio)
        dy = int(self.height * ratio)
        x = self.width // 2 + randint(-dx, dx)
        y = self.height // 2 + randint(-dy, dy)
        a = Node(x, y, isAnchor, self)

        for b in self.nodes:
            if a.isClose(b) and (not a.isAnchor or not b.isAnchor):
                a.addAdj(b)
                b.addAdj(a)
        self.nodes.append(a)

    def err(self, x):
        return (e**(-x * x / (2 * self.errDist))) / sqrt(2 * pi * self.errDist)

    def updateFixedStatus(self):
        isDone = False
        while not isDone:
            isDone = True
            for node in self.nodes:
                if node.updateFixed():
                    isDone = False

    def setProbGrid(self):
        self.prob = [[0.0 for _ in range(self.width - 1)]
                     for _ in range(self.height - 1)]

        # for a in self.nodes:
        a = self.nodes[self.frame % len(self.nodes)]
        fail = 0
        while a.isAnchor or a.fixedCount == 0:
            fail += 1
            if fail >= len(self.nodes):
                print("Fail")
                exit()
            self.frame += 1
            a = self.nodes[self.frame % len(self.nodes)]

        a.prob = [[1.0 for _ in range(self.width - 1)]
                  for _ in range(self.height - 1)]
        for b in a.adj:
            if(b.isFixed()):
                a.multProbGrid(b)
        self.maxProbGrid(a.prob)

        self.normalize(self.prob)

    def maxProbGrid(self, grid):
        # print("BEGIN")
        for y in range(self.height - 1):
            for x in range(self.width - 1):
                self.prob[y][x] = max(self.prob[y][x], grid[y][x])
                # print(x, y, self.prob[y][x])

    def normalize(self, grid):
        maxValue = 0
        for y in range(self.height - 1):
            for x in range(self.width - 1):
                maxValue = max(grid[y][x], maxValue)

        if maxValue > 0:
            for y in range(self.height - 1):
                for x in range(self.width - 1):
                    grid[y][x] /= maxValue

    def display(self):

        for y in range(self.height - 1):
            for x in range(self.width - 1):
                pg.draw.circle(self.screen, (0, 255 * self.prob[y][x], 0), ((x + 1) *
                                                                            self.blockSize, (y + 1) * self.blockSize), 2)
        for a in self.nodes:
            for b in a.adj:
                pg.draw.line(self.screen, (255, 255, 255),
                             (a.x * self.blockSize, a.y * self.blockSize), (b.x * self.blockSize, b.y * self.blockSize))

        for node in self.nodes:
            node.display()

    def run(self):
        clock = pg.time.Clock()
        done = False
        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
            self.setProbGrid()
            self.display()
            pg.display.update()
            clock.tick(1)
            self.frame += 1
            if(self.frame >= 20):
                done = True

        pg.quit()


if __name__ == '__main__':
    pass
