from sysconfig import sys
from random import *
from logic import *
from nTuple import *
import copy

import math

class learner():
    def __init__(self):
        self.bestMove ="stop"

    def getMaxTiles(self, grid):
        maxTile = 0
        dist = 0
        maxTiles = [0, 0, 0, 0]
        for row in range(4):
            for column in range(4):
                dist = dist + (row - column) * grid[row][column] * 3.0
                maxTile = grid[row][column]
                if maxTile > min(maxTiles):
                    maxTiles[0] = maxTile
                    maxTiles.sort()
        maxTiles.append(dist)
        return maxTiles

    def getAvailableCells(self,grid):
        cells = []
        for row in range(4):
            for column in range(4):
                if grid[row][column] == 0:
                    cells.append([row,column])
        return cells

    def getNewTileValue(self):
        if randint(0, 99) < 100 * 0.9:
            return 2
        else:
            return 4
    def getAvailableMoves(self, grid):
        directions = ["'w'","'a'","'s'","'d'"]
        moves = []
        for dir in directions:
            tempgrid = copy.deepcopy(grid)
            tempgrid,done= makeMove(tempgrid,dir)
            if done:
                moves.append(dir)
        return moves

    def learn(self):
        ntuple.lookUpTable =   [[0.1, 0.1, 0.1, 0.1],
                                [0.1, 0.1, 0.1, 0.1],
                                [0.1, 0.1, 0.1, 0.1],
                                [0.1, 0.1, 0.1, 0.1]]
