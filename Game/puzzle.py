import tkinter as tk
import random as ran
import time
import json
from datetime import datetime

from Game.logic import *
from Game.alphaBetaAi import *
from Game.Minimax import *
from Game.expectiMax import *

SIZE = 500
GRID_LEN = 4
GRID_PADDING = 10

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e"
}
CELL_COLOR_DICT = {
    2: "#776e65",
    4: "#776e65",
    8: "#f9f6f2",
    16: "#f9f6f2",
    32: "#f9f6f2",
    64: "#f9f6f2",
    128: "#f9f6f2",
    256: "#f9f6f2",
    512: "#f9f6f2",
    1024: "#f9f6f2",
    2048: "#f9f6f2"
}
FONT = ("Verdana", 40, "bold")

KEY_UP_ALT = "\'\\uf700\'"
KEY_DOWN_ALT = "\'\\uf701\'"
KEY_LEFT_ALT = "\'\\uf702\'"
KEY_RIGHT_ALT = "\'\\uf703\'"

KEY_UP = "'w'"
KEY_DOWN = "'s'"
KEY_LEFT = "'a'"
KEY_RIGHT = "'d'"

data = {
    "timeTaken": 0,
    "startTime": 0,
    "score": 0,
    "moves": 0,
    "maxTile": 0,
    "win?": 0,
    "statesScanned": 0
}


class GameGrid(tk.Frame):
    def __init__(self, times, type):
        tk.Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)
        self.type = type
        # self.gamelogic = gamelogic
        self.commands = {
            KEY_UP: up,
            KEY_DOWN: down,
            KEY_LEFT: left,
            KEY_RIGHT: right,
            KEY_UP_ALT: up,
            KEY_DOWN_ALT: down,
            KEY_LEFT_ALT: left,
            KEY_RIGHT_ALT: right
        }

        self.grid_cells = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()
        self.time = datetime.now()
        self.times = times
        self.playTimes()
        self.mainloop()

    def init_grid(self):
        background = tk.Frame(
            self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        background.grid()
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = tk.Frame(
                    background,
                    bg=BACKGROUND_COLOR_CELL_EMPTY,
                    width=SIZE / GRID_LEN,
                    height=SIZE / GRID_LEN)
                cell.grid(
                    row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                # font = tk.Font(size=FONT_SIZE, family=FONT_FAMILY, weight=FONT_WEIGHT)
                t = tk.Label(
                    master=cell,
                    text="",
                    bg=BACKGROUND_COLOR_CELL_EMPTY,
                    justify=tk.CENTER,
                    font=FONT,
                    width=4,
                    height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def gen(self):
        return randint(0, GRID_LEN - 1)

    def init_matrix(self):
        self.matrix = new_game(4)
        self.time = datetime.now()
        self.matrix = add_two(self.matrix)
        self.matrix = add_two(self.matrix)

    def update_grid_cells(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(
                        text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=BACKGROUND_COLOR_DICT[new_number],
                        fg=CELL_COLOR_DICT[new_number])
        self.update_idletasks()

    def key_down(self, event):
        key = repr(event.char)
        if key in "'r'":
            self.randomPlayer()

        if key in "'b'":
            self.alphaBeta()

        if key in "'m'":
            self.minimax()

        if key in "'e'":
            self.expect()

        if key in self.commands:
            self.makeMove(key)
            self.gameOver()


# checks wether the game is won or lost and updates grid to display state

    def gameOver(self):
        if game_state(self.matrix) == 'win':
            self.grid_cells[1][1].configure(
                text="You", bg=BACKGROUND_COLOR_CELL_EMPTY)
            self.grid_cells[1][2].configure(
                text="Win!", bg=BACKGROUND_COLOR_CELL_EMPTY)
            self.update()
            time.sleep(1)
            return True
        if game_state(self.matrix) == 'lose':
            self.grid_cells[1][1].configure(
                text="You", bg=BACKGROUND_COLOR_CELL_EMPTY)
            self.grid_cells[1][2].configure(
                text="Lose!", bg=BACKGROUND_COLOR_CELL_EMPTY)
            self.update()
            time.sleep(1)
            return True
        return False

    def generate_next(self):
        index = (self.gen(), self.gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (self.gen(), self.gen())
        self.matrix[index[0]][index[1]] = 2

    # take input KEY_UP ,KEY_DOWN ,KEY_LEFT,KEY_RIGHT
    # and updates the grid based on move
    def makeMove(self, move):
        self.matrix, done = self.commands[move](self.matrix)
        if done:
            self.matrix = add_two(self.matrix)
            self.update_grid_cells()
            self.update()

    # Random Moves Player
    def randomPlayer(self):
        while game_state(self.matrix) != 'lose':
            data["moves"] += 1
            data["maxTile"] = max_tile(self.matrix)
            data["score"] = score(self.matrix)
            char = ran.choice([KEY_UP, KEY_RIGHT, KEY_LEFT, KEY_DOWN])
            self.makeMove(char)
            time = datetime.now() - self.time
            data["timeTaken"] = str(time)
        with open("data.txt", "a") as myfile:
            myfile.write(str(data) + '\n')
        self.gameOver()

    # Alpha-Beta Player
    def alphaBeta(self):
        player = alphaBetaPlayer()
        data["startTime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        while not self.gameOver():
            data["moves"] += 1
            move = player.getMove(self.matrix)
            self.makeMove(move)
        if game_state(self.matrix) == 'win':
            data["win?"] = 1
        data["maxTile"] = max_tile(self.matrix)
        data["score"] = score(self.matrix)
        time = datetime.now() - self.time
        data["timeTaken"] = str(time)
        data["statesScanned"] = alphaBetaPlayer.statesScanned
        with open("abResults.txt", "a") as myfile:
            myfile.write(str(data) + '\n')

    # Minimax Player
    def minimax(self):
        player = minimaxPlayer()
        data["startTime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        while not self.gameOver():
            data["moves"] += 1
            move = player.getMove(self.matrix)
            self.makeMove(move)
        if game_state(self.matrix) == 'win':
            data["win?"] = 1
        data["maxTile"] = max_tile(self.matrix)
        data["score"] = score(self.matrix)
        time = datetime.now() - self.time
        data["timeTaken"] = str(time)
        data["statesScanned"] = minimaxPlayer.statesScanned
        with open("minimaxResults.txt", "a") as myfile:
            myfile.write(str(data) + '\n')

    # Expectimax Player
    def expect(self):
        player = expectiMaxPlayer()
        data["startTime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        while not self.gameOver():
            data["moves"] += 1
            move = player.getMove(self.matrix)
            self.makeMove(move)
        if game_state(self.matrix) == 'win':
            data["win?"] = 1
        data["maxTile"] = max_tile(self.matrix)
        data["score"] = score(self.matrix)
        time = datetime.now() - self.time
        data["timeTaken"] = str(time)
        data["statesScanned"] = expectiMaxPlayer.statesScanned
        with open("expectimaxResults.txt", "a") as myfile:
            myfile.write(str(data) + '\n')

    def quit(self):
        self.destroy()

    def resetBoard(self):
        # print " ", minimaxPlayer.nodesVisited, minimaxPlayer.evalCalls
        # minimaxPlayer.nodesVisited =0
        # minimaxPlayer.evalCalls=0
        # print "Min ,Alpha ,Expec ", minimaxPlayer.statesScanned,
        # alphaBetaPlayer.statesScanned, expectiMaxPlayer.statesScanned
        print("game is resetting board")
        minimaxPlayer.statesScanned = 0
        alphaBetaPlayer.statesScanned = 0
        expectiMaxPlayer.statesScanned = 0
        data["timeTaken"] = 0
        data["maxTile"] = 0
        data["startTime"] = 0
        data["score"] = 0
        data["moves"] = 0
        data["win?"] = 0
        self.init_matrix()
        self.update_grid_cells()

    def playTimes(self):

        while self.times > 0:
            if self.type in "'r'":
                self.randomPlayer()

            if self.type in "'b'":
                self.alphaBeta()

            if self.type in "'m'":
                self.minimax()

            if self.type in "'e'":
                self.expect()

            if self.gameOver():
                self.times -= 1
                self.resetBoard()
        if self.times == 0:
            quit()

algotype = "'e'"  # change to either 'b' or 'm' or 'e'
gamegrid = GameGrid(100, algotype)  # change to number of rounds


def quit():
    gamegrid.destroy()
