#return the best move possible using alpha beta pruning
from sysconfig import sys
from random import *
from logic import *
import copy
import math
sys.setrecursionlimit(4000)

class alphaBetaPlayer():
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
        # cell_score = 0
        # empty = 0
        # adjacent = 0
        # snakes = [1]
        # for x in range(4):
        #     for y in range(4):
        #         cell =grid[x][y]
        #         if cell > 0:
        #             cell_score += (cell / 2 - 1)
        #
        #             # Boost if has equal adjacent cells
        #             if x > 0 and cell == grid[x][y-1]:
        #                 adjacent += 1
        #             if y > 0 and cell == grid[x-1][y]:
        #                 adjacent += 1
        #         else:
        #             empty += 1
        # monotonic_up = 0
        # monotonic_down = 0
        # monotonic_left = 0
        # monotonic_right = 0
        # for x in range(4):
        #     current = 0
        #     next = current + 1
        #     while next < 4:
        #         while next < 3 and not grid[x][next]:
        #             next += 1
        #         current_cell = grid[x][current]
        #         current_value = math.log(current_cell, 2) if current_cell else 0
        #         next_cell = grid[x][next]
        #         next_value = math.log(next_cell, 2) if next_cell else 0
        #         if current_value > next_value:
        #             monotonic_up += (next_value - current_value)
        #         elif next_value > current_value:
        #             monotonic_down += (current_value - next_value)
        #         current = next
        #         next += 1
        # for y in range(4):
        #     current = 0
        #     next = current + 1
        #     while next < 4:
        #         while next < 3 and not grid[next][y]:
        #             next += 1
        #         current_cell = grid[current][y]
        #         current_value = math.log(current_cell, 2) if current_cell else 0
        #         next_cell = grid[next][y]
        #         next_value = math.log(next_cell, 2) if next_cell else 0
        #         if current_value > next_value:
        #             monotonic_left += (next_value - current_value)
        #         elif next_value > current_value:
        #             monotonic_right += (current_value - next_value)
        #         current = next
        #         next += 1
        # monotonic = max(monotonic_up, monotonic_down) + max(monotonic_left, monotonic_right)
        #
        # # print "cell_score: %d" % cell_score
        # # print "empty: %d" % empty
        # # print "adjacent: %d" % adjacent
        # # print "snakes: %s" % snakes
        # # print "monotonic: %d" % monotonic
        #
        # return cell_score + empty*32 + adjacent*4 + max(snakes)*9 + monotonic

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

    def alphabeta(self, grid, depth, alpha, beta, maximizingPlayer):
        if depth == 0:
            e = self.evalfn(grid)
            return [e, -1]
        if maximizingPlayer:
            moves = self.getAvailableMoves(grid)
            if moves == []:
                return [alpha, self.direction]
            for move in moves:
                tmpGrid = copy.deepcopy(grid)
                tmpGrid,done=makeMove(tmpGrid,move)
                r = self.alphabeta(tmpGrid, depth - 1, alpha, beta, False)
                if alpha < r[0]:
                    self.direction = move
                if r[0] == -float('inf'):
                    self.direction = move
                alpha = max(alpha, r[0])
                if beta <= alpha:
                    print("I'm in break stmt")
                    break
            result = [alpha, self.direction]
            return result
        else:
            cells = self.getAvailableCells(grid)
            if cells == []:
                return [self.evalfn(grid), "'w'"]
            i = cells[randint(0, len(cells) - 1)]
            tmpGrid = copy.deepcopy(grid)
            tmpGrid[i[0]][i[1]] = self.getNewTileValue()
            r = self.alphabeta(tmpGrid, depth - 1, alpha, beta, True)
            beta = min(beta, r[0])
            result = [beta, r[1]]
            return result


    def getMove(self, grid):
        moves = self.getAvailableMoves(grid)
        print(moves)
        result = self.alphabeta(grid, 12, -float('inf'), float('inf'), True)
        print("Expected Score",result[0])
        print("Direction",result[1])
        return result[1]
