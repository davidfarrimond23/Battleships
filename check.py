import math
import random

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

def populateList(populatedBoard):
    potentialList = []
    for x in range(len(populatedBoard[0])):
        if x % 2 != 0 or x == 0:
            for y in range(len(populatedBoard[0])):
                if y % 2 != 0 or y == 0:
                    potentialList.append((x, y))
    return potentialList

def populateList2(populatedBoard):
    potentialList2 = []
    for x in range(len(populatedBoard[0])):
        for y in range(len(populatedBoard[0])):
            potentialList2.append((x, y))
    return potentialList2

def randomPick(potMoves, oBoard):
    x, y = random.choice(potMoves)
    if oBoard[x][y] != " ":
        return x, y, True
    else:
        return x, y, False

def directionListPop(x, y, board):
    directionList = []
    if x == 0 and y == 0:
        directionList  = [(x+1, 0), (0, y+1)]

    elif x == 0 and y != (len(board[0]) -1):
        directionList = [(x, y-1), (x, y+1), (x+1, y)]
    
    elif y == 0 and x != (len(board[0]) - 1):
        directionList = [(x-1, y), (x, y+1), (x+1, y)]

    elif x == (len(board[0])-1) and y != (len(board[0])- 1):
        directionList = [(x -1, y), (x, y -1), (x, y+1)]

    elif y == (len(board[0])-1) and x != (len(board[0])-1):
        directionList = [(x -1, y), (x, y -1), (x +1, y)]

    elif y == (len(board[0])-1) and x == (len(board[0])-1):
        directionList = [(x - 1, y), (x, y-1)]

    else:
        directionList = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

    return directionList

def randomChoiceList(list):
    toReturn =  random.choice(list)
    list.remove(toReturn)
    return toReturn

def hitCheck(checkPls, board, fleet):
    if board[checkPls[0]][checkPls[1]] != " ":
        key = board[checkPls[0]][checkPls[1]]
        if key in fleet.keys():
            fleet[key] -= 1
            if fleet[key] == 0:
                fleet.pop(key)
        return True
    else:
        return False

def removeCheck(x, y, listToRemove):
    if (x, y) in listToRemove:
        listToRemove.remove((x, y))
        return True
    else:
        return False

def moveGeneration(potentialMoves, fleetLeft, ownBoard, moveList):
    while len(potentialMoves) > 0 and len(fleetLeft) > 0:
        #set test flag to false
        test = False
        #while we don't have a hit and we have potential moves left
        while test == False and len(potentialMoves) > 0 and len(fleetLeft) > 0:
            #print(potentialMoves)
            #pick a random move from move list
            x, y, test = randomPick(potentialMoves, ownBoard)
            #check the hit
            hitCheck((x, y), ownBoard, fleetLeft)
            #remove it from the list
            removeCheck(x, y, potentialMoves)
            #append it to the MoveList with the result
            moveList.append((x, y, test))
        if test == True and len(fleetLeft) > 0:
            tempCheckList = directionListPop(x, y, ownBoard)
            for item in tempCheckList:
                toCheck = randomChoiceList(tempCheckList)
                if hitCheck(toCheck, ownBoard, fleetLeft) == True and len(fleetLeft) > 0:
                    #we need a direction check;
                    if toCheck[0] == x and toCheck[1] == (y - 1):
                        ##set i and j iterators to move backwards:
                        i, j = toCheck[0], toCheck[1]
                        ##make sure j iterator (for y) does not overrun and is not larger than the largest ship:
                        while len(fleetLeft) > 0 and j > 0 and y - j < max(fleetLeft.values()) and hitCheck((i, j), ownBoard, fleetLeft) == True:
                            moveList.append((i, j, True))
                            removeCheck(i, j, potentialMoves)
                            j -= 1
                        moveList.append((i, j, False))
                        removeCheck(i, j, potentialMoves)
                    if toCheck[0] == x and toCheck[1] == (y + 1):
                        i, j = toCheck[0], toCheck[1]
                        while len(fleetLeft) > 0 and j < (len(ownBoard[0]) - 1) and j - y < max(fleetLeft.values()) and hitCheck((i, j), ownBoard, fleetLeft) == True:
                            moveList.append((i, j, True))
                            removeCheck(i, j, potentialMoves)
                            j += 1
                        moveList.append((i, j, False))
                        removeCheck(i, j, potentialMoves)
                    if toCheck[0] == (x - 1) and toCheck[1] == y:
                        i, j = toCheck[0], toCheck[1]
                        while len(fleetLeft) > 0 and i > 0 and x - i < max(fleetLeft.values()) and hitCheck((i, j), ownBoard, fleetLeft) == True:
                            moveList.append((i, j, True))
                            removeCheck(i, j, potentialMoves)
                            i -= 1
                        moveList.append((i, j, False))
                        removeCheck(i, j, potentialMoves)
                    if toCheck[0] == (x + 1) and toCheck[1] == y:
                        i, j = toCheck[0], toCheck[1]
                        while len(fleetLeft) > 0 and i < (len(ownBoard[0])) and i - x < max(fleetLeft.values()) and hitCheck((i, j), ownBoard, fleetLeft) == True:
                            moveList.append((i, j, True))
                            removeCheck(i, j, potentialMoves)
                            i += 1
                        moveList.append((i, j, False))
                        removeCheck(i, j, potentialMoves)
                else:
                    moveList.append((toCheck[0], toCheck[1], False))
                    removeCheck(toCheck[0], toCheck[1], potentialMoves)
                    test == False
    return moveList

#fletLeft = {"Aircraft Carrier": 5, "Battleship": 4, "Frigate": 3, "Submarine": 2, "Minesweeper": 2}
#unBoard = [[" " for j in range(10)] for i in range(10)]
#movList = []
#onBoard = populateBoard(fletLeft, unBoard)
#potMoves = populateList2(onBoard)
#moveGeneration(potMoves, fletLeft, onBoard, movList)
#print(movList)