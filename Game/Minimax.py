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
        #evalScore = len(cell) * 10 + maxSum * 0.8+maxTiles[4]*5
        evalScore = len(cell) * 10 + maxSum * 0.8 + maxTiles[4]# * 2
        #return (evalScore)

    ###
        scoreTotal = score(grid)

        # cluster
        clusteringScore=0
        neighbours=[-1,0,1]
        i=0
        for row in grid:
            j=0
            for cell in row:
                if cell == 0:
                    continue
                numOfNeighbours=0
                summ=0
                for k in neighbours:
                    x=i+k
                    if x<0 or x >= 4:  #4 is total number of rows or columns
                        continue
                    for l in neighbours:
                        y=j+1
                        if y<0 or y >= 4:
                            continue

                        if grid[x][y]>0:
                            numOfNeighbours+=1
                            summ+=int(math.fabs(grid[i][j]-grid[x][y]))

                #print "sum, num",sum,numOfNeighbours
                if not summ==0:
                    clusteringScore+=summ/numOfNeighbours
                j+=1
            i+=1


        val = int(scoreTotal + (math.log(scoreTotal) * len(self.getAvailableCells(grid))) - clusteringScore)
        #print "max, eval",max(val,min(score, 1)),evalScore
        return max(val,min(score, 1))+evalScore

    ###
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
        if depth == 0:                          #if at required depth, return the hueristics value
            e = self.evalfn(grid)
            return [e, 1]                       #returns value and 2nd value doesnt matter
        if maximizingPlayer:                    #if its maximizing player
            bestValue = -float('inf')           #start with -inf value
            moves = self.getAvailableMoves(grid)     #possible moves
            if moves == []:                     #if no possible moves, return hueristics value
                return [self.evalfn(grid), 1]
            valueList=[]                        #list which will contain all heuristic values
            for move in moves:                  #for each move...
                #print "move",move
                tmpGrid = copy.deepcopy(grid)
                tmpGrid,done=makeMove(tmpGrid,move)             #this will copy current grid into tmp and make the move
                val = self.minimax(tmpGrid,depth-1,False)       #recursive call for tmp (which is successor state) to get heuristic value
                valueList.append((val[0],move))                 #val and current move is appended in list
                #bestValue = max(bestValue, val[0])
                #if val[0] > bestValue:
            for tuple in valueList:                             #iterate through list and find max value along with..
                if tuple[0] > bestValue:                        #.. the move that led to that child node
                    bestValue = tuple[0]
                    bestMove = tuple[1]
                #if val[0] == -float('inf'):
                    #bestMove=move
            return [bestValue, bestMove]                        #returns value and move

        else:                                           #if not maximizing player(i.e AI)
            bestValue = float('inf')
            cells = self.getAvailableCells(grid)        #if number of cells are 0, return value and move ('w') doesnt matter
            if cells == []:
                return [self.evalfn(grid), "'w'"]
            #i = cells[randint(0, len(cells) - 1)]
            #tmpGrid = copy.deepcopy(grid)
            #tmpGrid[i[0]][i[1]] = self.getNewTileValue()
            #val = self.minimax(tmpGrid, depth - 1, True)
            #return [val[0],val[1]]

            tiles=[2,4]                                 #possible tiles 2 or 4
            for cell in cells:                          #for each empty cell
                for tile in tiles:                      #we loop through 2 and 4
                    tmpGrid = copy.deepcopy(grid)
                    tmpGrid[cell[0]][cell[1]]=tile      #cell[0] returns row number, cell[1] returns column number
                    val = self.minimax(tmpGrid, depth - 1, True)        #maximize it recursivly
                    if val[0]<bestValue:                #if heuristic val is less than current best
                        #print"test"
                        bestValue=val[0]
                        direc=val[1]
            return [bestValue,direc]                    #return minimized value and direction (direction doesnt matter)


    def getMove(self, grid):
        moves = self.getAvailableMoves(grid)
        #print(moves)
        result = self.minimax(grid, 4, True)
        #print("Expected Score",result[0])
        #print("Direction",result[1])
        return result[1]

