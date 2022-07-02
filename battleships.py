import math
import random
import check
import copy

###board setup functions

piecesDictionary = {"Aircraft Carrier": 5, "Battleship": 4, "Frigate": 3, "Submarine": 2, "Minesweeper": 2}

class Player:
    playerunPopulatedBoard = [[" " for j in range(10)] for i in range(10)]
    def __init__(self):
        self.hitBoard = [["o" for j in range(10)] for i in range(10)]
        self.fleetLeft = {"Aircraft Carrier": 5, "Battleship": 4, "Frigate": 3, "Submarine": 2, "Minesweeper": 2}
        self.fleetLeftCheck = copy.deepcopy(self.fleetLeft)
        self.ownBoard = check.populateBoard(piecesDictionary, self.playerunPopulatedBoard)
        self.ownBoardCheck = copy.deepcopy(self.ownBoard)
        self.movesMade = []
    
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
        if enemy.fleetLeft[enemyBoard[x][y]] == 0:
            print("{} Sunk!".format(enemyBoard[x][y]))
            enemy.fleetLeft.pop(enemyBoard[x][y])
            return True

    def checkFleet(self):
        if len(enemy.fleetLeft) == 0:
            print("Enemy has no ships!")
            return True
        return False

    def checkHit(self, x, y, enemyBoard):
        self.movesMade.append((x, y))
        if enemyBoard[x][y] != " ":
            self.enemyHit(x, y)
            enemy.fleetLeft[enemyBoard[x][y]] -= 1
            print("Hit!")
            self.checkSunk(enemyBoard, x, y)
        else:
            self.enemyMiss(x, y)
            print("Miss!")

class Enemy:

    def __init__(self):
        self.fleetLeft = {"Aircraft Carrier": 5, "Battleship": 4, "Frigate": 3, "Submarine": 2, "Minesweeper": 2}
        self.ownUnBoard = [[" " for j in range(10)] for i in range(10)]
        self.moveList = []
        self.ownBoard = check.populateBoard(self.fleetLeft, self.ownUnBoard)
        self.potentialMoves =  check.populateList2(player.ownBoard)
        self.newList = check.moveGeneration(self.potentialMoves, player.fleetLeftCheck, player.ownBoardCheck, self.moveList)

    def makeMove(self):
        move = self.moveList.pop(0)
        if move[2] == True:
            ##access player fleet, knockdown by one
            key = player.ownBoard[move[0]][move[1]]
            player.fleetLeft[key] -= 1
            if player.fleetLeft[key] == 0:
                print("Enemy has sunk our {} at x: {}, y: {}".format(key, move[0], move[1]))
                player.fleetLeft.pop(key)
            else:
                print("Enemy has hit at x: {}, y: {}".format(move[0], move[1]))
        else:
            print("Enemy has missed at x: {}, y: {}".format(move[0], move[1]))
    
    def checkPlayerFleet(self):
        if len(player.fleetLeft) == 0:
            return True
        else:
            return False

class Error(Exception):
    pass

class numberOutOfRange(Error):
    #raised when value out of range
    pass

class alreadyTriedError(Error):
    pass

def inputChecker():
    x = -1
    y = -1
    while True:
        try:
            x = int(input("x: "))
            if x < 0 or x > 10:
                raise numberOutOfRange
            y = int(input("y: "))
            if y < 0 or y > 10:
                raise numberOutOfRange
            if (x, y) in player.movesMade:
                raise alreadyTriedError
        except numberOutOfRange:
            print("You fool")
        except ValueError:
            print("Enter a number!")
        except alreadyTriedError:
            print("You've already tried {}, {}".format(x, y))
        else:
            break

    return x, y


print("\nWelcome, Commander! What would you like to do?")
print("\nYour options: \n Start Game\n Quit\n")
commandList = ["start game", "quit"]
commandListInGame = ["shoot", "see our ships", "quit"]

while True:
    winflag = False
    lossFlag = False
    command = input("> ")
    if command.lower() not in commandList:
        print("You can't do that!")
    if command.lower() == commandList[0].lower():
        print("\nStarting game...")
        player = Player()
        enemy = Enemy()
        print("\nWelcome to the Battle Space, commander. What would you like to do?\n")
        print("Your options:\n\nShoot \nSee our ships \nQuit")
        while winflag == False and lossFlag == False:
            command = input("> ")
            if command.lower() not in commandListInGame:
                print("You can't do that!")
            if command.lower() == commandListInGame[0]:
                player.printBoard()
                x, y = inputChecker()
                player.checkHit(x, y, enemy.ownBoard)
                winFlag = player.checkFleet()
                if winFlag == True:
                    print("Congratulations! We've sunk the enemy fleet.\n")
                    print("Our remaining fleet:\n\n")
                    print(player.fleetLeft)
                    print("Would you like to play again? (y/n)")
                    while True:
                        command = input()
                        if command != "y" or command != "n":
                            print("Make a choice!")
                        elif command == "y":
                            winflag = True
                        elif command == "n":
                            quit()
                enemy.makeMove()
                lossFlag = enemy.checkPlayerFleet()
                if lossFlag == True:
                    print("Oh no! Our fleet has been sunk!\n")
                    print("Their remaining fleet:\n\n")
                    print(enemy.fleetLeft)
                    print("Would you like to play again? (y/n)")
                    while True:
                        command = input()
                        if command != "y" or command != "n":
                            print("Make a choice!")
                        elif command == "y":
                            lossFlag = True
                        elif command == "n":
                            quit()
            if command.lower() == commandListInGame[1]:
                print(player.fleetLeft)
            if command.lower() == commandListInGame[2]:
                quit()

    if command.lower() == commandList[1].lower():
        quit()
    
