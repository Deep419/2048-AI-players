from Tkinter import *
from logic import *
from alphaBetaAi import *
from numpy import random
from datetime import datetime
from Minimax import *
from expectiMax import *
SIZE = 500
GRID_LEN = 4
GRID_PADDING = 10

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563", \
                         32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61", \
                         512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"}
CELL_COLOR_DICT = {2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2", \
                   32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2", 256: "#f9f6f2", \
                   512: "#f9f6f2", 1024: "#f9f6f2", 2048: "#f9f6f2"}
FONT = ("Verdana", 40, "bold")

KEY_UP_ALT = "\'\\uf700\'"
KEY_DOWN_ALT = "\'\\uf701\'"
KEY_LEFT_ALT = "\'\\uf702\'"
KEY_RIGHT_ALT = "\'\\uf703\'"


KEY_UP = "'w'"
KEY_DOWN = "'s'"
KEY_LEFT = "'a'"
KEY_RIGHT = "'d'"


data = {"time":0,"currTime":0,"Depth":4,"score":0,"moves":0,"maxTile":0,"win":False}

class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)

        # self.gamelogic = gamelogic
        self.commands = {KEY_UP: up, KEY_DOWN: down, KEY_LEFT: left, KEY_RIGHT: right,
                         KEY_UP_ALT: up, KEY_DOWN_ALT: down, KEY_LEFT_ALT: left, KEY_RIGHT_ALT: right}

        self.grid_cells = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()
        self.time = datetime.now()
        self.mainloop()
    def init_grid(self):
        background = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        background.grid()
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE / GRID_LEN, height=SIZE / GRID_LEN)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                # font = Font(size=FONT_SIZE, family=FONT_FAMILY, weight=FONT_WEIGHT)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4,
                          height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)
    def gen(self):
        return randint(0, GRID_LEN - 1)
    def init_matrix(self):
        self.matrix = new_game(4)

        self.matrix = add_two(self.matrix)
        self.matrix = add_two(self.matrix)

    def update_grid_cells(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=BACKGROUND_COLOR_DICT[new_number],
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

#checks wether the game is won or lost and updates grid to display state
    def gameOver(self):
        if game_state(self.matrix) == 'win':
            self.grid_cells[1][1].configure(text="You", bg=BACKGROUND_COLOR_CELL_EMPTY)
            self.grid_cells[1][2].configure(text="Win!", bg=BACKGROUND_COLOR_CELL_EMPTY)
            return True
        if game_state(self.matrix) == 'lose':
            self.grid_cells[1][1].configure(text="You", bg=BACKGROUND_COLOR_CELL_EMPTY)
            self.grid_cells[1][2].configure(text="Lose!", bg=BACKGROUND_COLOR_CELL_EMPTY)
            return True
        return False
    def generate_next(self):
        index = (self.gen(), self.gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (self.gen(), self.gen())
        self.matrix[index[0]][index[1]] = 2

#take input KEY_UP ,KEY_DOWN ,KEY_LEFT,KEY_RIGHT and updates the grid based on move
    def makeMove(self,move):
        self.matrix, done = self.commands[move](self.matrix)
        if done:
            self.matrix = add_two(self.matrix)
            self.update_grid_cells()
            self.update()
            
# this is a random ai player.
    def randomPlayer(self):
        while game_state(self.matrix) != 'lose':
            data["moves"] += 1
            data["maxTile"] = max_tile(self.matrix)
            data["score"] = score(self.matrix)
            char = random.choice([KEY_UP, KEY_RIGHT, KEY_LEFT, KEY_DOWN])
            self.makeMove(char)
            time = datetime.now() - self.time
            data["time"] = str(time)
        with open("data.txt", "a") as myfile:
            myfile.write(str(data)+'\n')
        self.gameOver()

    def alphaBeta(self):
        player = alphaBetaPlayer()
        while not self.gameOver():
            data["moves"] += 1
            move=player.getMove(self.matrix)
            self.makeMove(move)
        if game_state(self.matrix) == 'win':
            data["win"] = True
        data["maxTile"] = max_tile(self.matrix)
        data["score"] = score(self.matrix)
        time = datetime.now() - self.time
        data["time"] = str(time)
        with open("abResults.txt", "a") as myfile:
            myfile.write(str(data)+'\n')

    def minimax(self):
        player = minimaxPlayer()
        while not self.gameOver():
            data["moves"] += 1
            move=player.getMove(self.matrix)
            self.makeMove(move)
        if game_state(self.matrix) == 'win':
            data["win"] = True
        data["maxTile"] = max_tile(self.matrix)
        data["score"] = score(self.matrix)
        time = datetime.now() - self.time
        data["time"] = str(time)
        with open("minimaxResults.txt", "a") as myfile:
            myfile.write(str(data)+'\n')

    def expect(self):
        player= expectiMaxPlayer()
        data["currTime"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        while not self.gameOver():
            data["moves"] += 1
            move=player.getMove(self.matrix)
            self.makeMove(move)
        if game_state(self.matrix) == 'win':
            data["win"] = True
        data["maxTile"] = max_tile(self.matrix)
        data["score"] = score(self.matrix)
        time = datetime.now() - self.time
        data["time"] = str(time)
        with open("expectimaxResults.txt", "a") as myfile:
            myfile.write(str(data)+'\n')
gamegrid = GameGrid()
