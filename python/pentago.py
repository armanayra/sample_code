"""
    CS 380 - Artificial Intelligence
    Professor Popyack

    Programming Assignment 4
    -- Pentago --

    Arman Ayrapetyan
    ava35@drexel.edu
"""
import random
import re
from operator import itemgetter, attrgetter
import copy

class Human(object):
    def __init__(self):
        self.name = raw_input("Name of Human?  ")
        self.color = ""

    def makeMove(self):
        playerMove = raw_input("What is your move? (Format: e.g. 3/8 1R)\n")
        inputIntegrity = validateInput(playerMove)
        while inputIntegrity is not True:
            playerMove = raw_input("What is your move? (Format: e.g. 3/8 1R)\n")
            inputIntegrity = validateInput(playerMove)
        return playerMove

class CPU(object):
    def __init__(self):
        self.name = selectCPUName()
        self.color = ""
        self.moveRating = None

    def makeCPUMove(self, state):
        availablePegs = applicableRules(state.board)
        moveRating, moves = heuristic(availablePegs)
        #self.moveRating = moveRating[0]
        pMove = getRandomTopThreeMoves(moves)
        newState = self.applyMove(pMove, state)
        newState = self.cpuBoardRotation(newState)
        rotateDesiredDirection(newState)
        #maxMove = minimax(state, moves, self)
        return newState

    def applyMove(self, move, state):
        state.board[move[1][0]][move[1][1]] = self.color
        return state

    def cpuBoardRotation(self, state):
        availableDirections = ["R", "L"]
        availableGamePieces = [1, 2, 3, 4]
        selectedDirection = random.choice(availableDirections)
        selectedGamePiece = random.choice(availableGamePieces)
        state.blockToRotate = selectedGamePiece
        state.rotationDirection = selectedDirection
        return state


def applicableRules(state):
    listOfApplicableRules = []
    listOfAvailablePegs = []
    for index, val in enumerate(state):
        for deepIndex, deepVal in enumerate(val):
            if deepVal in ["."]:
                listOfAvailablePegs.append([index, deepIndex])

    #print "The list of availablePegs is {0}".format(listOfAvailablePegs)
    return listOfAvailablePegs

def heuristic(pegs):
    unorderedList = [[0, x] for x in pegs]
    #print "The unordered list is {0}".format(unorderedList)
    for item in unorderedList:
        blockSpot = item[1][1]
        if blockSpot in [4]:
            item[0] += 4
        if blockSpot in [0, 2, 6, 8]:
            item[0] += 3
        if blockSpot in [3, 5]:
            item[0] += 2
        if blockSpot in [1, 7]:
            item[0] += 1
    #print "The new unordered list is {0}".format(unorderedList)
    sortedList = sorted(unorderedList, key=itemgetter(0))
    sortedList.reverse()
    #print "The new ordered list is {0}".format(sortedList)
    finalSortedList = []
    for pair in sortedList:
        finalSortedList.append(sortedList[0])
    if len(finalSortedList) < 1:
        return None
    return finalSortedList[0][0], finalSortedList

def getRandomTopThreeMoves(pList):
    topThreeList = []
    topThreeList.append(pList[0])
    topThreeList.append(pList[1])
    topThreeList.append(pList[2])
    randomMove = random.choice(topThreeList)
    return randomMove

def selectCPUName():
    cpuNames = ["Roger", "Jennifer", "Zach", "Jessica", "Sam", "Don", "Hanna", "Elliott"]
    return random.choice(cpuNames)

def minimax(state, moves, player):
    infinity = 100000000
    max = -(infinity + 1)
    for move in moves:
        nextState = player.applyMove(move, state)
        min = (infinity + 1)
        availablePegs = applicableRules(state.board)
        moveRating, oppMoves = heuristic(availablePegs)
        for oppMove in oppMoves:
            newState = player.applyMove(oppMove, state)
            if player.moveRating < min:
                min = player.moveRating
        if ( min > max ):
            max = min
            oppMove  = move
    return max

def initializePlayers():
    print """ Select a game mode.
    1. Human vs CPU
    2. Human vs Human
    3. CPU vs CPU
    """
    selection = raw_input("Game mode? ")
    while selection not in ("1", "2", "3"):
        print "Invalid mode. Please try again."
        selection = raw_input("Game mode? ")

    if selection == "1":
        print "Selected Human vs CPU"
        print "Player 1:"
        humanA = Human()
        print "Player 2 is CPU:"
        cpuA = CPU()
        print "Game between {0}(Human) and {1}(CPU) now starting!".format(humanA.name, cpuA.name)
        return humanA, cpuA
    if selection == "2":
        print "Selected Human vs Human"
        print "Player 1:"
        humanA = Human()
        print "Player 2:"
        humanB = Human()
        print "Game between {0}(Human) and {1}(Human) now starting!".format(humanA.name, humanB.name)
        return humanA, humanB
    if selection == "3":
        print "Selected CPU vs CPU"
        print "Player 1 is CPU:"
        cpuA = CPU()
        print "Player 2 is CPU:"
        cpuB = CPU()
        print "Game between {0}(CPU) and {1}(CPU) now starting!".format(cpuA.name, cpuB.name)
        return cpuA, cpuB


gameBlockOne = [
    ".", ".", ".",
    ".", ".", ".",
    ".", ".", "."
]
gameBlockTwo = [
    ".", ".", ".",
    ".", ".", ".",
    ".", ".", "."
]
gameBlockThree = [
    ".", ".", ".",
    ".", ".", ".",
    ".", ".", "."
]
gameBlockFour = [
    ".", ".", ".",
    ".", ".", ".",
    ".", ".", "."
]

initialPentagoBoard = [gameBlockOne, gameBlockTwo,
                       gameBlockThree, gameBlockFour]

class GameBoard(object):
    def __init__(self):
        self.board = initialPentagoBoard
        self.changeBlock = None
        self.changeBlockIndex = None
        self.blockToRotate = None
        self.rotationDirection = None

    def setMove(self, move):
        self.changeBlock = move[0]
        self.changeBlockIndex = move[2]
        self.blockToRotate = move[4]
        self.rotationDirection = move[5]

    def validateOpenBlock(self):
        if self.board[int(self.changeBlock) - 1][int(self.changeBlockIndex) - 1] not in ["."]:
            print "Spot is not empty"
            return False
        else:
            return True

    def applyMove(self, color):
        if self.validateOpenBlock():
            self.board[int(float(self.changeBlock)) - 1][int(float(self.changeBlockIndex)) - 1] = color
            return True
        else:
            return False

def rotateDesiredDirection(gameboard):
    rotDir = gameboard.rotationDirection
    print "The desired direction is {0}".format(rotDir)
    rotatedBoard = None
    if rotDir == "R":
        rotatedBoard = rotateRight(gameboard)
    elif rotDir == "L":
        rotatedBoard = rotateLeft(gameboard)
    else:
        print "Direction Unclear..."
        return None
    return rotatedBoard

def rotateRight(gameboard):
    tempBoard = []
    rotateIndex = int(gameboard.blockToRotate) - 1
    tempBoard = gameboard.board[rotateIndex]
    newBoard = gameboard

    finalBlock = []
    finalBlock.append(tempBoard[6])
    finalBlock.append(tempBoard[3])
    finalBlock.append(tempBoard[0])
    finalBlock.append(tempBoard[7])
    finalBlock.append(tempBoard[4])
    finalBlock.append(tempBoard[1])
    finalBlock.append(tempBoard[8])
    finalBlock.append(tempBoard[5])
    finalBlock.append(tempBoard[2])
    newBoard.board[rotateIndex] = finalBlock
    return newBoard

def rotateLeft(gameboard):
    tempBoard = []
    rotateIndex = int(gameboard.blockToRotate) - 1
    tempBoard = gameboard.board[rotateIndex]
    newBoard = gameboard

    finalBlock = []
    finalBlock.append(tempBoard[2])
    finalBlock.append(tempBoard[5])
    finalBlock.append(tempBoard[8])
    finalBlock.append(tempBoard[1])
    finalBlock.append(tempBoard[4])
    finalBlock.append(tempBoard[7])
    finalBlock.append(tempBoard[0])
    finalBlock.append(tempBoard[3])
    finalBlock.append(tempBoard[6])
    newBoard.board[rotateIndex] = finalBlock
    return newBoard

def printBoard(gameboard):
    board = gameboard.board
    print "+---------+---------+"
    print "|  {0} {1} {2}  |  {3} {4} {5}  |".format(board[0][0], board[0][1], board[0][2], board[1][0], board[1][1], board[1][2])
    print "|  {0} {1} {2}  |  {3} {4} {5}  |".format(board[0][3], board[0][4], board[0][5], board[1][3], board[1][4], board[1][5])
    print "|  {0} {1} {2}  |  {3} {4} {5}  |".format(board[0][6], board[0][7], board[0][8], board[1][6], board[1][7], board[1][8])
    print "+---------+---------+"
    print "|  {0} {1} {2}  |  {3} {4} {5}  |".format(board[2][0], board[2][1], board[2][2], board[3][0], board[3][1], board[3][2])
    print "|  {0} {1} {2}  |  {3} {4} {5}  |".format(board[2][3], board[2][4], board[2][5], board[3][3], board[3][4], board[3][5])
    print "|  {0} {1} {2}  |  {3} {4} {5}  |".format(board[2][6], board[2][7], board[2][8], board[3][6], board[3][7], board[3][8])
    print "+---------+---------+"


def goal():
    return None

def check_for_fiveInARow(gameboard):
    # Columns
    colOneIndices =   [[0, 0], [0, 3], [0, 6], [2, 0], [2, 3], [2, 6]]
    colTwoIndices =   [[0, 1], [0, 4], [0, 7], [2, 1], [2, 4], [2, 7]]
    colThreeIndices = [[0, 2], [0, 5], [0, 8], [2, 2], [2, 5], [2, 8]]
    colFourIndices =  [[1, 0], [1, 3], [1, 6], [3, 0], [3, 3], [3, 6]]
    colFiveIndices =  [[1, 1], [1, 4], [1, 7], [3, 1], [3, 4], [3, 7]]
    colSixIndices =   [[1, 2], [1, 5], [1, 8], [3, 2], [3, 5], [3, 8]]

    # Rows
    rowOneIndices =   [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2]]
    rowTwoIndices =   [[0, 2], [0, 4], [0, 5], [1, 3], [1, 4], [1, 5]]
    rowThreeIndices = [[0, 6], [0, 7], [0, 8], [1, 6], [1, 7], [1, 8]]
    rowFourIndices =  [[2, 0], [2, 1], [2, 2], [3, 0], [3, 1], [3, 2]]
    rowFiveIndices =  [[2, 2], [2, 4], [2, 5], [3, 3], [3, 4], [3, 5]]
    rowSixIndices =   [[2, 6], [2, 7], [2, 8], [3, 6], [3, 7], [3, 8]]

    # Diagonals
    # Starting Top-Left by Indices
    block1DiagonalA = [[0, 1], [0, 5], [1, 6], [3, 1], [3, 5]]
    block1DiagonalB = [[0, 0], [0, 4], [0, 8], [3, 0], [3, 4], [3, 8]]
    block1DiagonalC = [[0, 3], [0, 7], [2, 2], [3, 3], [3, 7]]
    # Top-Right
    block2DiagonalA = [[1, 1], [1, 3], [0, 8], [2, 1], [2, 3]]
    block2DiagonalB = [[1, 2], [1, 4], [1, 6], [2, 2], [2, 4], [2, 6]]
    block2DiagonalC = [[1, 5], [1, 7], [3, 0], [2, 5], [2, 7]]
    # Bottom-Left
    block3DiagonalA = [[2, 7], [2, 5], [3, 0], [1, 7], [1, 5]]
    block3DiagonalB = [[2, 6], [2, 4], [2, 2], [1, 6], [1, 4], [1, 2]]
    block3DiagonalC = [[2, 3], [2, 1], [0, 8], [1, 3], [1, 1]]
    # Bottom-Right
    block4DiagonalA = [[3, 7], [3, 3], [2, 2], [0, 7], [0, 3]]
    block4DiagonalB = [[3, 8], [3, 4], [3, 0], [0, 8], [0, 4], [0, 0]]
    block4DiagonalC = [[3, 5], [3, 1], [1, 6], [0, 5], [0, 1]]

    allApplicableDirections = [colOneIndices, colTwoIndices, colThreeIndices, colFourIndices, colFiveIndices, colSixIndices,
                               rowOneIndices, rowTwoIndices, rowThreeIndices, rowFourIndices, rowFiveIndices, rowSixIndices,
                               block1DiagonalA, block1DiagonalB, block1DiagonalC,
                               block2DiagonalA, block2DiagonalB, block2DiagonalC,
                               block3DiagonalA, block3DiagonalB, block3DiagonalC,
                               block4DiagonalA, block4DiagonalB, block4DiagonalC]

    foundFiveBs = False
    foundFiveWs = False
    string = ""
    print "Searching board for solution..."

    for direction in allApplicableDirections:
        for indexPair in direction:
            string += gameboard.board[indexPair[0]][indexPair[1]]
            fiveBs = re.search("bbbbb", string)
            fiveWs = re.search("wwwww", string)
            if fiveBs:
                foundFiveBs = True
            if fiveWs:
                foundFiveWs = True
        string = ""

    if foundFiveBs and foundFiveWs:
        print "Found 5 b's and 5 w's in a row! Tie game!"
        return True
    elif foundFiveBs:
        print "Found 5 b's in a row! Winner!"
        return True
    elif foundFiveWs:
        print "Found 5 w's in a row! Winner!"
        return True
    else:
        print "No winner found. Continuing game."
        return False


def decideWhoGoesFirst(player1, player2):
    randomNumber = random.randint(0, 100)
    print "Flipping coin to decide first player."
    print "(Player 1 if < 50 === Player 2 if >= 50)"
    print randomNumber

    if randomNumber < 50:
        return player1
    else:
        return player2

def validateInput(playerMove):
    match = re.search("[1-4]/[1-9] [1-4][R|L]", playerMove)
    if match:
        print "Found match {0}".format(match.group())
        return True
    else:
        print "No match found."
        return False

def playGame():
    player1, player2 = initializePlayers()
    print "Player 1's name is {0}".format(player1.name)
    print "Player 2's name is {0}".format(player2.name)
    initiator = decideWhoGoesFirst(player1, player2)
    print "{0} will be going first (black (b)).".format(initiator.name)

    turnOrder = []
    availablePlayers = [player1, player2]
    turnOrder.append(initiator)
    if initiator.name == player1.name:
        player1.color = "b"
        player2.color = "w"
        turnOrder.append(player2)
    else:
        player1.color = "w"
        player2.color = "b"
        turnOrder.append(player1)

    print "The player turn order is {0}".format([x.name for x in turnOrder])
    newBoard = GameBoard()
    printBoard(newBoard)
    result = check_for_fiveInARow(newBoard)
    if result == True:
        print "Winner Found! Game over!"

    count = 1
    turnNumber = 0

    while result == False:
        for player in turnOrder:
            if result == True:
                pass
            if isinstance(player, Human):
                print "-- {0} Turn --".format(player.name)
                if turnNumber > 1:
                    turnNumber = 0
                humanMove = player.makeMove()
                newBoard.setMove(humanMove)
                moveAllowed = newBoard.applyMove(turnOrder[turnNumber].color)
                while moveAllowed == False:
                    humanMove = player.makeMove()
                    newBoard.setMove(humanMove)
                    moveAllowed = newBoard.applyMove(turnOrder[turnNumber].color)
                rotatedBoard = rotateDesiredDirection(newBoard)
                newBoard = rotatedBoard
                turnNumber += 1
                printBoard(rotatedBoard)
                result = check_for_fiveInARow(newBoard)
                if result == True:
                    print "{0}('{1}') Wins! Game over!".format(player.name, player.color)
                    exit()
            if isinstance(player, CPU):
                print "-- CPU Turn --"
                if turnNumber > 1:
                    turnNumber = 0
                newBoard = player.makeCPUMove(newBoard)
                printBoard(newBoard)
                result = check_for_fiveInARow(newBoard)

                #maxMove = minimax(newBoard, cpuMoves, player)
                turnNumber += 1
                if result == True:
                    print "{0}('{1}') Wins! Game over!".format(player.name, player.color)
                    exit()

        count += 1



def main():
    playGame()

if  __name__ =='__main__':
    main()