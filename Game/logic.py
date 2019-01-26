from random import *


def new_game(n):
    matrix = []

    for i in range(n):
        matrix.append([0] * n)
    return matrix


# updated so chances of 2 and 4 being added are correct
def add_two(mat):
    a = randint(0, len(mat) - 1)
    b = randint(0, len(mat) - 1)
    if randint(0, 99) < 100 * 0.9:
        num = 2
    else:
        num = 4
    while mat[a][b] != 0:
        a = randint(0, len(mat) - 1)
        b = randint(0, len(mat) - 1)
    mat[a][b] = num
    return mat


# Find max tile value
def max_tile(mat):
    max_value = 0
    for rows in mat:
        row = rows
        for tile in range(len(row)):
            if row[tile] > max_value:
                max_value = row[tile]
    return max_value


# Find score
def score(mat):
    score_value = 0
    for rows in mat:
        row = rows
        for tile in range(len(row)):
            score_value = score_value + row[tile]
    return score_value


def game_state(mat):
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 2048:
                return 'win'
    # intentionally reduced to check the row on the right and below
    for i in range(len(mat) - 1):
        # more elegant to use exceptions but most likely this will be their solution
        for j in range(len(mat[0]) - 1):
            if mat[i][j] == mat[i + 1][j] or mat[i][j + 1] == mat[i][j]:
                return 'not over'
    # check for any zero entries
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 0:
                return 'not over'
    # to check the left/right entries on the last row
    for k in range(len(mat) - 1):
        if mat[len(mat) - 1][k] == mat[len(mat) - 1][k + 1]:
            return 'not over'
    # check up/down entries on last column
    for j in range(len(mat) - 1):
        if mat[j][len(mat) - 1] == mat[j + 1][len(mat) - 1]:
            return 'not over'
    return 'lose'


def reverse(mat):
    new = []
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):
            new[i].append(mat[i][len(mat[0]) - j - 1])
    return new


def transpose(mat):
    new = []
    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
    return new


# The way to do movement is compress -> merge -> compress again
# Basically if they can solve one side, and use transpose and reverse correctly they should
# be able to solve the entire thing just by flipping the matrix around
# No idea how to grade this one at the moment. I have it pegged to 8 (which gives you like,
# 2 per up/down/left/right?) But if you get one correct likely to get all correct so...
# Check the down one. Reverse/transpose if ordered wrongly will give you wrong result.
def cover_up(mat):
    new = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    done = False
    for i in range(4):
        count = 0
        for j in range(4):
            if mat[i][j] != 0:
                new[i][count] = mat[i][j]
                if j != count:
                    done = True
                count += 1
    return new, done


def merge(mat):
    done = False
    for i in range(4):
        for j in range(3):
            if mat[i][j] == mat[i][j + 1] and mat[i][j] != 0:
                mat[i][j] *= 2
                mat[i][j + 1] = 0
                done = True
    return mat, done


def up(game):
    # return matrix after shifting up
    game = transpose(game)
    game, done = cover_up(game)
    temp = merge(game)
    game = temp[0]
    done = done or temp[1]
    game = cover_up(game)[0]
    game = transpose(game)
    return game, done


def down(game):
    game = reverse(transpose(game))
    game, done = cover_up(game)
    temp = merge(game)
    game = temp[0]
    done = done or temp[1]
    game = cover_up(game)[0]
    game = transpose(reverse(game))
    return game, done


def left(game):
    # return matrix after shifting left
    game, done = cover_up(game)
    temp = merge(game)
    game = temp[0]
    done = done or temp[1]
    game = cover_up(game)[0]
    return game, done


def right(game):
    # return matrix after shifting right
    game = reverse(game)
    game, done = cover_up(game)
    temp = merge(game)
    game = temp[0]
    done = done or temp[1]
    game = cover_up(game)[0]
    game = reverse(game)
    return game, done


def makeMove(game, move):
    if move in "'w'":
        return up(game)
    if move in "'a'":
        return left(game)
    if move in "'s'":
        return down(game)
    if move in "'d'":
        return right(game)
