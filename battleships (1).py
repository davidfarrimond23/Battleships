import math
import random

"""
Battleships game

1: Set list of pieces with a set amount of space
    Easy- Dictionary; i.e. Battleship: 4

2:
    Board will essentially be a 2d list of set size.
    Each item in the dictionary takes up a set amount of spaces on the board.
    Adjacent vertically or horizontally.

3:
    We will need to:
        Iterate through the dictionary of available pieces.
        Randomly choose whether the pieces are to be laid vertically or horizontally.
        Choose a board space.
            If the board space is occupied to right or down, we need to choose a different space until it isn't occupied

4:
    Place the pieces. Each list index can contain the key for the dictionary part.
    We can use the value to track the hits. When hits == 0, we can return the key hit.
    This will run until all values hit Zero!

5:
    We probably need a player class to track score
    When each "kill" occurs we can update the player class with the points
    We can also mark hits and misses in this and call a checkhits method with a prompt

"""

def randOrientation():
    check = 0.5
    if random.random() > check:
        #horizontal, x values
        #print("Returning 1")
        return 1
    else:
        #vertical, y values
        #print("Returning 0")
        return 0

def checkAdjacent(spaces, board, direction, x, y):
    #if horizontal
    if direction == 1:
        for i in range(spaces):
            #print("Checking {}, {}".format((x + i), y))
            #print(len(board[0]))
            #print(x + spaces)
            if (x + (spaces)) < len(board[0]):
                if board[x + i][y] != " ":
                    return False
            else:
                return False
        return True
    else:
        for i in range(spaces):
            #print("Checking {}, {}".format(x, (y + i)))
            if (y + (spaces)) < len(board[0]):
                if board[x][y+i] != " ":
                    return False
            else:
                return False
        return True

def generateStart(spaces, board):
    x = random.randrange(0, len(board[0]), 1)
    y = random.randrange(0, len(board[0]), 1)
    #print(x, y)
    checkedx = []
    checkedy = []
    genDirection = randOrientation()
    while checkAdjacent(spaces, board, genDirection, x, y) != True:
        #print(checkedx)
        checkedx.append(x)
        checkedy.append(y)
        genDirection = randOrientation()
        x = random.randrange(len(board[0]))
        y = random.randrange(len(board[0]))
    #print("Returning {}, {}".format(x, y))
    return x, y, genDirection


def populateBoard(dictionary, board):
    for key, value in dictionary.items():
        x, y, tempDirection = generateStart(value, board)
        if tempDirection == 1:
            for i in range(x, x + (value)):
                board[i][y] = key
                #print(x + i)
        else:
            for i in range(y, y + (value)):
                board[x][i] = key
                #print(y + i)
    return board

piecesDictionary = {"Aircraft Carrier": 5, "Battleship": 4, "Frigate": 3, "Submarine": 2, "Minesweeper": 2}

unPopulatedBoard = [[" " for j in range(10)] for i in range(10)]
#print(len(unPopulatedBoard))
populatedBoard = populateBoard(piecesDictionary, unPopulatedBoard)

#The algorithm for hunt & kill begins:

"""
The Hunt & Kill algorithm is simple:

1: break the board into odds;
    i.e. check 0, 0;
                0, 1;
                0, 3;
2: pick one of these at random.
    :: if hit:
        "Kill" function begins until a "Kill" is called.
            Kill Function:
                1: fire at adjacent squares until a hit is made;
                    keep a running "hit list"
                    (So [x+1][y], [x-1][y], [x][y-1], [x][y+1])
                    when hit:
                        continue on that path until a hit is made
            count a "Kill" in the kill dictionary. Knock out from ship left dictionary, whatever equals hit list
    :: if Miss:
        add miss to miss list. knock one off attempts.

"""
def populateList(populatedBoard):
    potentialList = []
    for x in range(len(populatedBoard[0])):
        if x % 2 != 0 or x == 0:
            for y in range(len(populatedBoard[0])):
                if y % 2 != 0 or y == 0:
                    potentialList.append((x, y))
    return potentialList

def checkHit(board, x, y, potentialList):
    if board[x][y] != " ":
        potentialList.remove((x, y))
        return True
    else:
        potentialList.remove((x, y))
        return False

def randomCheck(board, potentialList):
    x, y = random.choice(potentialList)
    if checkHit(board, x, y, potentialList):
        return True, x, y, board[x][y]
    else:
        return False, x, y, board[x][y]


"""
huntList = {"Aircraft Carrier": 5, "Battleship": 4, "Frigate": 3, "Submarine": 2, "Minesweeper": 2}
while len(huntList) != 0:
    hit, x, y, ship = checkBoard(populatedBoard, potentialList)
    if hit == True:
        if (x - max(huntList.values() >= 0 )):
            hit = checkHit(populatedBoard, x-1, y)
            if hit == True:
                for j in range(1, max(huntList.values())):
                    hit = checkHit(populatedBoard, x-j, y)
            else:
                hit = checkHit(populatedBoard, x+1, y)
                if hit == True:
                    for j in range(1, max(huntList.values())):
                        hit = checkHit(populatedBoard, x-j, y)
                else:
                    hit = checkHit(populatedBoard, x, y-1)
                    if hit == True:
                        for j in range(1, max(huntList.values())):
                            hit = checkHit(populatedBoard, x, y-j)
                    else:
                        hit = checkHit(populatedBoard, x, y+1)
                        if hit == True:
                            for j in range(1, max(huntList.values())):
                                hit = checkHit(populatedBoard, x, y+j)
"""
#print(potentialList)
#print(populatedBoard)

class Player:
    unPopulatedBoard = [[" " for j in range(10)] for i in range(10)]
    def __init__(self):
        self.hitBoard = [["o" for j in range(10)] for i in range(10)]
        self.fleetLeft = {"Aircraft Carrier": 5, "Battleship": 4, "Frigate": 3, "Submarine": 2, "Minesweeper": 2}
        self.ownBoard = populateBoard(piecesDictionary, unPopulatedBoard)
    
    def printBoard(self):
        for row in self.hitBoard:
            for column in row:
                print("| " + column, end = " ")
            print("|")

    def enemyHit(self, x, y):
        self.hitBoard[x][y] = "x"

    def enemyMiss(self, x, y):
        self.hitBoard[x][y] = "-"

    def checkSunk(self, enemyBoard, x, y):
        if self.fleetLeft[enemyBoard[x][y]] == 0:
            print("{} Sunk!".format(enemyBoard[x][y]))
            self.fleetLeft.pop(enemyBoard[x][y])
            return True

    def checkFleet(self):
        if len(self.fleetLeft) == 0:
            print("Enemy has no ships!")
            return True

    def checkHit(self, x, y, enemyBoard):
        if enemyBoard[x][y] != " ":
            self.enemyHit(x, y)
            self.fleetLeft[enemyBoard[x][y]] -= 1
            print("Hit!")
            self.checkSunk(enemyBoard, x, y)
        else:
            self.enemyMiss(x, y)
            print("Miss!")


player = Player()

class Error(Exception):
    pass

class numberOutOfRange(Error):
    #raised when value out of range
    pass

def inputChecker():
    x = -1
    y = -1
    while True:
        try:
            x = int(input("x: "))
            if x <= 0 or x > 10:
                raise numberOutOfRange
            y = int(input("y: "))
            if y <= 0 or x > 10:
                raise numberOutOfRange
        except numberOutOfRange:
            print("You fool")
        except ValueError:
            print("Enter a number!")
        else:
            break

    return x, y
    


while True:
    x, y = inputChecker()
    player.checkHit(x, y, populatedBoard)
    player.checkFleet()
    player.printBoard()