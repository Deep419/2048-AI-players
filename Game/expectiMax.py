#return the best move possible using alpha beta pruning
from sysconfig import sys
from random import *
from logic import *
import copy
import math
sys.setrecursionlimit(4000)

class expectiMaxPlayer():
    def _init_(self):
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

    def expectiScore(self, grid):
        score=0
        penalty=0
        #weights=[[6,5,4,3],[5,4,3,2],[4,3,2,1],[3,2,1,0]]
        weights=[[.135759,.121925,.102812,.099937],[.0997992,.0888405,.076711,.0724143],[.06054,.0562579,.037116,.01611889],[.0125498,.00992495,.00575871,.00335193]]
        #caculates postive score
        for x in range(0,4):
            for y in range(0,4):
                score+= weights[x][y]*grid[x][y]
        #calculates penality
        for x in range(0,4):
            for y in range(0,4):
                #all top row
                if x==0:
                    penalty+= abs(grid[x][y]-grid[x+1][y])
                    if y>0:
                        penalty += abs(grid[x][y] - grid[x][y - 1])
                        penalty += abs(grid[x][y] - grid[x + 1][y - 1])
                    if y<3:
                        penalty += abs(grid[x][y] - grid[x][y + 1])
                        penalty += abs(grid[x][y] - grid[x + 1][y + 1])
                #all inner rows
                if x!=0 and x!=3 and y!=0 and y!=3:
                    penalty+= abs(grid[x][y]-grid[x-1][y])
                    penalty+= abs(grid[x][y]-grid[x-1][y+1])
                    penalty+= abs(grid[x][y]-grid[x-1][y-1])
                    penalty+= abs(grid[x][y]-grid[x][y+1])
                    penalty+= abs(grid[x][y]-grid[x][y-1])
                    penalty+= abs(grid[x][y]-grid[x+1][y])
                    penalty+= abs(grid[x][y]-grid[x+1][y+1])
                    penalty+= abs(grid[x][y]-grid[x+1][y-1])
                #all bottom row
                if x==3:
                    penalty+= abs(grid[x][y]-grid[x-1][y])
                    if y>0:
                        penalty += abs(grid[x][y] - grid[x - 1][y - 1])
                        penalty += abs(grid[x][y] - grid[x][y - 1])
                    if y<3:
                        penalty += abs(grid[x][y] - grid[x - 1][y + 1])
                        penalty += abs(grid[x][y] - grid[x][y + 1])
                if x!=0 and x!=3:
                    penalty += abs(grid[x][y] - grid[x - 1][y])
                    penalty += abs(grid[x][y] - grid[x + 1][y])
                    if y==0:
                        penalty+= abs(grid[x][y]-grid[x][y+1])
                        penalty+= abs(grid[x][y]-grid[x-1][y+1])
                        penalty+= abs(grid[x][y]-grid[x+1][y+1])
                    if y==3:
                        penalty += abs(grid[x][y] - grid[x - 1][y - 1])
                        penalty += abs(grid[x][y] - grid[x][y - 1])
                        penalty += abs(grid[x][y] - grid[x + 1][y - 1])
        return (score-penalty)

    def getNewTileValue(self):
        if randint(0, 99) < 100 * 0.9:
            return 2
        else:
            return 4
    def getAvailableMoves(self,grid):
        directions = ["'w'","'a'","'s'","'d'"]
        moves = []
        for dir in directions:
            tempgrid = copy.deepcopy(grid)
            tempgrid,done= makeMove(tempgrid,dir)
            if done:
                moves.append(dir)
        return moves

    def expectiMax(self, grid, depth, player):
        if depth == 0:
            e= self.expectiScore(grid)
            return [e, -1]
        if player:
            score = 0
            moves = self.getAvailableMoves(grid)
            for move in moves:
                tempGrid = copy.deepcopy(grid)
                tempGrid = makeMove(tempGrid,move)
                if score<self.expectiMax(tempGrid, depth-1, False):
                    self.direction=move
                score = max(score, self.expectiMax(tempGrid, depth-1, False))
            return [score, direction]
        else:
            score=0
            cells = self.getAvailableCells(grid)
            print(cells)
            for tile in cells:
                tempGrid = copy.deepcopy(grid)
                tempGrid.insert(tile, 2)
                score += 0.9 * (expectiMax(grid, depth -1, True)[0])

                tempGrid = copy.deepcopy(grid)
                tempGrid.index(tile, 4)
                val = expectiMax(grid, depth - 1, True)
                score +=0.1 * val

            return [(score / len(self.getAvailableMoves(grid))), -1]


    def getMove(self, grid):
        moves = self.getAvailableMoves(grid)
        result = self.expectiMax(grid, 12, True)
        print("Expected Score",result[0])
        print("Direction",result[1])
        return result[1]
