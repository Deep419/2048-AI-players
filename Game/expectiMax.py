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
        '''
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
        '''

        cell = self.getAvailableCells(grid)
        maxTiles = self.getMaxTiles(grid)
        maxSum = sum(maxTiles)
        # evalScore = len(cell) * 10 + maxSum * 0.8+maxTiles[4]*5
        evalScore = len(cell) * 10 + maxSum * 0.8 + maxTiles[4]  # * 2
        # return (evalScore)
        e2=evalScore*10

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
        e1=max(val, min(score, 1))
        #print "e1, e2", e1,e2
        return  e1 + e2

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

    '''
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
    '''

    def expectiMax(self, grid, depth, player):
        if depth == 0:
            e= self.expectiScore(grid)
            return [e, -1]
        if player:
            score = -float('inf')
            moves = self.getAvailableMoves(grid)
            if moves == []:
                return [self.expectiScore(grid), 1]
            valueList = []
            for move in moves:
                tempGrid = copy.deepcopy(grid)
                tempGrid,done = makeMove(tempGrid,move)
                val=self.expectiMax(tempGrid, depth-1, False)
                valueList.append((val[0], move))
            for tuple in valueList:                             #iterate through list and find max value along with..
                if tuple[0] > score:                        #.. the move that led to that child node
                    score = tuple[0]
                    direc = tuple[1]
            return [score, direc]
        else:
            weightedScore=0.0
            cells = self.getAvailableCells(grid)
            if cells == []: ##added
                return [self.expectiScore(grid), "'w'"]
            tiles=[2,4]
            probability=1.0/len(cells)

            for cell in cells:
                for tile in tiles:
                    tempGrid = copy.deepcopy(grid)
                    tempGrid[cell[0]][cell[1]] = tile

                    val=self.expectiMax(tempGrid,depth-1,True)
                    if tile==2:
                        weightedScore += (probability*0.9) * float(val[0])
                    else:
                        weightedScore += (probability * 0.1) * float(val[0])

            return [weightedScore, -1]



    def getMove(self, grid):
        '''
        moves = self.getAvailableMoves(grid)
        result = self.expectiMax(grid, 12, True)
        print("Expected Score",result[0])
        print("Direction",result[1])
        return result[1]
        '''

        result = self.expectiMax(grid, 3, True)
        #print("Expected Score",result[0])
        #print("Direction",result[1])
        return result[1]
