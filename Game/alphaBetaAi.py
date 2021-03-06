#return the best move possible using alpha beta pruning
from sysconfig import sys
from random import *
from logic import *
import copy
import math
sys.setrecursionlimit(4000)

class alphaBetaPlayer():
    statesScanned = 0
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
        '''
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

        cell = self.getAvailableCells(grid)
        maxTiles = self.getMaxTiles(grid)
        maxSum = sum(maxTiles)
        # evalScore = len(cell) * 10 + maxSum * 0.8+maxTiles[4]*5
        evalScore = len(cell) * 10 + maxSum * 0.8 + maxTiles[4]  # * 2
        # return (evalScore)

        ###
        scoreTotal = score(grid)

        # cluster
        clusteringScore = 0
        neighbours = [-1, 0, 1]
        i = 0
        for row in grid:
            j = 0
            for cell in row:
                if cell == 0:
                    continue
                numOfNeighbours = 0
                summ = 0
                for k in neighbours:
                    x = i + k
                    if x < 0 or x >= 4:  # 4 is total number of rows or columns
                        continue
                    for l in neighbours:
                        y = j + 1
                        if y < 0 or y >= 4:
                            continue

                        if grid[x][y] > 0:
                            numOfNeighbours += 1
                            summ += int(math.fabs(grid[i][j] - grid[x][y]))

                # print "sum, num",sum,numOfNeighbours
                if not summ == 0:
                    clusteringScore += summ / numOfNeighbours
                j += 1
            i += 1

        val = int(scoreTotal + (math.log(scoreTotal) * len(self.getAvailableCells(grid))) - clusteringScore)
        # print "max, eval",max(val,min(score, 1)),evalScore
        return max(val, min(score, 1)) + evalScore
        '''
        W = [[[10, 9, 7.6, 7.4],
              [7.4, 6.4, 5.7, 5.3],
              [4.5, 4.1, 2.7, 1.2],
              [0.09, 0.07, 0.04, 0.02]], ]
        max_score = 0
        for W_matrix in W:
            # print "w_matrix",W_matrix
            temp = 0
            for r in range(4):
                for c in range(4):
                    temp += W_matrix[r][c] * grid[r][c]
                    # temp += W[r][c] * grid[r][c]
            if temp > max_score:
                max_score = temp
        return max_score

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
    '''
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
    '''
    def alphabeta(self,grid,depth,a,b,maximizingPlayer):
        alphaBetaPlayer.statesScanned += 1
        if depth == 0:
            e = self.evalfn(grid)
            return [e, 1]
        if maximizingPlayer:
            bestValue = -float('inf')
            moves = self.getAvailableMoves(grid)
            flag=False
            if moves == []:
                return [self.evalfn(grid), 1]
            for move in moves:
                tmpGrid = copy.deepcopy(grid)
                tmpGrid,done=makeMove(tmpGrid,move)
                val = self.alphabeta(tmpGrid,depth-1,a,b,False)
                tmp=move
                if val[0] > a:
                    flag=True
                    bestMove = move
                    a=val[0]
                if b<=a:
                    break
                a=max(a,bestValue)
            if flag:
                return [a,bestMove]
            return [a,tmp]

        else:
            cells = self.getAvailableCells(grid)
            if cells == []:
                return [self.evalfn(grid), "'w'"]
            tiles=[2,4]
            flag = False
            flag2= False
            for cell in cells:
                for tile in tiles:
                    tmpGrid = copy.deepcopy(grid)
                    tmpGrid[cell[0]][cell[1]]=tile
                    val = self.alphabeta(tmpGrid, depth - 1,a,b,True)
                    tmp=val[1]
                    if val[0] < b:
                        flag2=True
                        direc = val[1]
                        b=val[0]
                    if b<=a:
                        flag=True
                        break
                if flag:
                    break
            if flag2:
                return [b,direc]
            return [b,tmp]


    def getMove(self, grid):
        '''
        moves = self.getAvailableMoves(grid)
        print(moves)
        result = self.alphabeta(grid, 12, -float('inf'), float('inf'), True)
        print("Expected Score",result[0])
        print("Direction",result[1])
        return result[1]
        '''

        moves = self.getAvailableMoves(grid)
        #print(moves)
        result = self.alphabeta(grid, 3, -float('inf'), float('inf'), True)
        #print("Expected Score",result[0])
        #print("Direction",result[1])
        return result[1]
