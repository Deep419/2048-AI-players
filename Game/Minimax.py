from sysconfig import sys
from random import *
from logic import *
import copy
import math
sys.setrecursionlimit(4000)

class minimaxPlayer():
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

    def evalfn(self, grid):
        cell = self.getAvailableCells(grid)
        maxTiles = self.getMaxTiles(grid)
        maxSum = sum(maxTiles)
        evalScore = len(cell) * 10 + maxSum * 0.8+maxTiles[4]*5
        return (evalScore)

    def getNewTileValue(self):
        if randint(0, 99) < 100 * 0.9:
            return 2
        else:
            return 4
    def getAvailableMoves(self,grid):
        directions = ["'w'","'a'","'s'","'d'"]
        moves = []
        for dir in directions:
            tmpgrid = copy.deepcopy(grid)
            tmpgrid,done= makeMove(tmpgrid,dir)
            if done:
                moves.append(dir)
        return moves

    def isTerminalState(self,grid):
        if self.getMaxTiles(grid)==2048 or not len(self.getAvailableCells(grid)) == 0:
            return True
        return False

    #main minimax method
    def minimax(self,grid,depth,maximizingPlayer):
        if depth == 0 or self.isTerminalState(grid):                                   #add terminal case ?
            e = self.evalfn(grid)
            return [e, -1]
        if maximizingPlayer:
            bestValue = -float('inf')
            moves = self.getAvailableMoves(grid)
            valueList=[]
            for move in moves:
                tmpGrid = copy.deepcopy(grid)
                tmpGrid,done=makeMove(tmpGrid,move)
                val = self.minimax(tmpGrid,depth-1,False)
                #bestValue = max(bestValue, val[0])
                if val[0] > bestValue:
                    bestValue=val[0]
                    bestMove=move
                if val[0] == -float('inf'):
                    bestMove=move
            return [bestValue, bestMove]
        else:
            #bestValue = float('inf')
            cells = self.getAvailableCells(grid)
            if cells == []:
                return [self.evalfn(grid), "'w'"]
            i = cells[randint(0, len(cells) - 1)]
            tmpGrid = copy.deepcopy(grid)
            tmpGrid[i[0]][i[1]] = self.getNewTileValue()
            val = self.minimax(tmpGrid, depth - 1, True)
            return [val[0],val[1]]


    def getMove(self, grid):
        moves = self.getAvailableMoves(grid)
        print(moves)
        result = self.minimax(grid, 12, True)
        print("Expected Score",result[0])
        print("Direction",result[1])
        return result[1]

#gameState is a matrix (list of list), representing all tile numbers on board
#matrix = [[0 for x in range(4)] for y in range(4)] #matrix[1][2] means row 1, column 2

    #for e in a:
        #for each in e:
            #print "each",each
        #print a

        #depth = to what depth are we checking
        #isPlayer = true if player's turn in tree, false if computer's move
