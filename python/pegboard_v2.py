"""
    CS 380 - Artificial Intelligence
    Professor Popyack

    Programming Assignment 3

    Arman Ayrapetyan
    ava35@drexel.edu
"""

import random
from operator import itemgetter, attrgetter
import copy

class CustomWinException(Exception):
    pass

finalPath = "\n==Path:==\n"
btCountWithoutHeuristic = 0
btCountWithHeuristic = 0
heuristicSwitch = False
nonHeuristicFailures = 0
heuristicFailures = 0

initialState = [ 1, 1, 1, 1,
                 1, 1, 1, 1,
                 0, 1, 1, 1,
                 1, 1, 1, 1 ]

def goal(state):
    goalState = [ 0, 0, 0, 0,
                  0, 0, 0, 0,
                  1, 0, 0, 0,
                  0, 0, 0, 0 ]
    if state == goalState:
        return True
    else:
        return False

def canMoveUp(state, currentpos):
    if ((currentpos - 4) < 0) or ((currentpos - 8) < 0):
        return False
    else:
        return True

def canMoveDown(state, currentpos):
    if ((currentpos + 4) > 15) or ((currentpos + 8) > 15):
        return False
    else:
        return True

def canMoveLeft(state, currentpos):
    if currentpos not in [2, 3, 6, 7, 10, 11, 14, 15]:
        return False
    else:
        return True

def canMoveRight(state, currentpos):
    if currentpos not in [0, 1, 4, 5, 8, 9, 12, 13]:
        return False
    else:
        return True

def canMoveDiagonalDownRight(state, currentpos):
    if currentpos not in [0, 1, 4, 5]:
        return False
    else:
        return True

def canMoveDiagonalDownLeft(state, currentpos):
    if currentpos not in [2, 3, 6, 7]:
        return False
    else:
        return True

def canMoveDiagonalUpLeft(state, currentpos):
    if currentpos not in [10, 11, 14, 15]:
        return False
    else:
        return True

def canMoveDiagonalUpRight(state, currentpos):
    if currentpos not in [8, 9, 12, 13]:
        return False
    else:
        return True

def getApplicableDirections(state, pegPosition):
    applicableDirections = []
    if canMoveUp(state, pegPosition):
        applicableDirections.append("up")
    if canMoveDown(state, pegPosition):
        applicableDirections.append("down")
    if canMoveLeft(state, pegPosition):
        applicableDirections.append("left")
    if canMoveRight(state, pegPosition):
        applicableDirections.append("right")
    if canMoveDiagonalDownRight(state, pegPosition):
        applicableDirections.append("diagonalDownRight")
    if canMoveDiagonalDownLeft(state, pegPosition):
        applicableDirections.append("diagonalDownLeft")
    if canMoveDiagonalUpLeft(state, pegPosition):
        applicableDirections.append("diagonalUpLeft")
    if canMoveDiagonalUpRight(state, pegPosition):
        applicableDirections.append("diagonalUpRight")
    return applicableDirections

def applicableRules(state):
    global heuristicSwitch
    listOfApplicableRules = []
    for index, val in enumerate(state):
        if val == 1:
            applicableDirections = getApplicableDirections(state, index)
            matchFound = False
            while len(applicableDirections) > 0:
                if matchFound == True:
                        break
                applicableDirection = random.choice(applicableDirections)
                rule = preCondition(state, index, applicableDirection)
                if rule is None:
                    if applicableDirection in applicableDirections:
                        applicableDirections.remove(applicableDirection)
                if rule is not None:
                    matchFound = True
                    for dirLeft in applicableDirections:
                        applicableDirections.remove(dirLeft)
                    newRule = [index, applicableDirection]
                    listOfApplicableRules.append(newRule)
    if heuristicSwitch is False:
        return listOfApplicableRules
    else:
        reorderedRules = heuristic(state, listOfApplicableRules)
        return reorderedRules

def heuristic(state, rules):
    print "Heuristic finds rules {0}".format(rules)
    directionRatingDict = {
        'up': 3,
        'down': 1,
        'left': 0,
        'right': 4,
        'diagonalDownRight': 4,
        'diagonalDownLeft': 2,
        'diagonalUpLeft': 3,
        'diagonalUpRight': 1
    }

    reverseDirectionRatingDict = {
        'up': 1,
        'down': 3,
        'left': 4,
        'right': 0,
        'diagonalDownRight': 0,
        'diagonalDownLeft': 2,
        'diagonalUpLeft': 1,
        'diagonalUpRight': 3
    }

    selectedDirectionRatingDict = {
        'up': 4,
        'down': 1,
        'left': 0,
        'right': 7,
        'diagonalDownRight': 6,
        'diagonalDownLeft': 3,
        'diagonalUpLeft': 5,
        'diagonalUpRight': 2
    }

    ratingIndex = []
    finalRuleSet = []
    for rule in rules:
        #ratingIndex.append([directionRatingDict[rule[1]], rule])
        #ratingIndex.append([reverseDirectionRatingDict[rule[1]], rule])
        ratingIndex.append([selectedDirectionRatingDict[rule[1]], rule])
    print "The rating index is as follows: {0}".format(ratingIndex)

    reOrderedRules = sorted(ratingIndex, key=itemgetter(0))
    for reOrderedRule in reOrderedRules:
        finalRuleSet.append(reOrderedRule[1])
    print "The reordered rules are {0}".format(finalRuleSet)

    return finalRuleSet

def getAvailablePegs(state):
    pegsAvailable = []
    for index, val in enumerate(state):
        if val == 1:
            applicableDirections = getApplicableDirections(state, index)
            pegsAvailable.append(index)
    print "Pegs " + str(pegsAvailable) + " remain. "
    return pegsAvailable

def preCondition(state, curPosition, direction):
    if direction == "up":
        upJumpNode = curPosition - 4
        upLandNode = curPosition - 8
        if state[upJumpNode] == 1 and state[upLandNode] == 0:
            return [curPosition, upJumpNode, upLandNode]
    if direction == "down":
        downJumpNode = curPosition + 4
        downLandNode = curPosition + 8
        if state[downJumpNode] == 1 and state[downLandNode] == 0:
            return [curPosition, downJumpNode, downLandNode]
    if direction == "left":
        leftJumpNode = curPosition - 1
        leftLandNode = curPosition - 2
        if state[leftJumpNode] == 1 and state[leftLandNode] == 0:
            return [curPosition, leftJumpNode, leftLandNode]
    if direction == "right":
        rightJumpNode = curPosition + 1
        rightLandNode = curPosition + 2
        if state[rightJumpNode] == 1 and state[rightLandNode] == 0:
            return [curPosition, rightJumpNode, rightLandNode]
    if direction == "diagonalDownRight":
        diagonalDownRightJumpNode = curPosition + 5
        diagonalDownRightLandNode = curPosition + 10
        if state[diagonalDownRightJumpNode] == 1 and state[diagonalDownRightLandNode] == 0:
            return [curPosition, diagonalDownRightJumpNode, diagonalDownRightLandNode]
    if direction == "diagonalDownLeft":
        diagonalDownLeftJumpNode = curPosition + 3
        diagonalDownLeftLandNode = curPosition + 6
        if state[diagonalDownLeftJumpNode] == 1 and state[diagonalDownLeftLandNode] == 0:
            return [curPosition, diagonalDownLeftJumpNode, diagonalDownLeftLandNode]
    if direction == "diagonalUpLeft":
        diagonalUpLeftJumpNode = curPosition - 5
        diagonalUpLeftLandNode = curPosition - 10
        if state[diagonalUpLeftJumpNode] == 1 and state[diagonalUpLeftLandNode] == 0:
            return [curPosition, diagonalUpLeftJumpNode, diagonalUpLeftLandNode]
    if direction == "diagonalUpRight":
        diagonalUpRightJumpNode = curPosition - 3
        diagonalUpRightLandNode = curPosition - 6
        if state[diagonalUpRightJumpNode] == 1 and state[diagonalUpRightLandNode] == 0:
            return [curPosition, diagonalUpRightJumpNode, diagonalUpRightLandNode]

def applyRule(rule, state):
    jumper = rule[0]
    goner = rule[1]
    newPos = rule[2]

    newState = list(state)
    newState[jumper] -= 1
    newState[goner] -= 1
    newState[newPos] += 1
    return newState

def describeState(state):
    print ("-----------------")
    print ("| " + str(state[0]) + " | " + str(state[1]) + " | " + str(state[2]) + " | " + str(state[3]) + " |")
    print ("-----------------")
    print ("| " + str(state[4]) + " | " + str(state[5]) + " | " + str(state[6]) + " | " + str(state[7]) + " |")
    print ("-----------------")
    print ("| " + str(state[8]) + " | " + str(state[9]) + " | " + str(state[10]) + " | " + str(state[11]) + " |")
    print ("-----------------")
    print ("| " + str(state[12]) + " | " + str(state[13]) + " | " + str(state[14]) + " | " + str(state[15]) + " |")
    print ("-----------------")

def describeRule(rule):
    print "The peg in slot {0} jumps over the peg in slot {1} and lands in slot {2}".format(rule[0], rule[1], rule[2])

def describeRuleList(ruleList):
    print "---- Rules ----"
    print "---------------"
    for rule in ruleList:
        print str(rule) + "\n"

def noMoves():
    print "No moves left. Game Over."
    exit(0)

def flailWildly(state):
    print ("Begin Flailing wildly...")
    moveCount = 0
    describeState(state)
    while not goal(state):
        print "Attempting move {0}.".format(moveCount + 1)
        if moveCount > 40:
            break
        # Get list of applicable rules
        #listOfApplicableRules = applicableRules(state)
        randomPeg = random.choice(getAvailablePegs(state))
        currentPeg = randomPeg
        rule = []
        print "Random peg selects {0} from {1}.".format(currentPeg, getAvailablePegs(state))
        applicableDirections = getApplicableDirections(state, currentPeg)
        matchFound = False
        while len(applicableDirections) > 0:
            if matchFound == True:
                break
            applicableDirection = random.choice(getApplicableDirections(state, currentPeg))
            print "An applicable direction for {0} is {1}".format(currentPeg, applicableDirection)
            print ("Checking rule...")
            rule = preCondition(state, currentPeg, applicableDirection)
            if rule is None:
                if applicableDirection in applicableDirections:
                    applicableDirections.remove(applicableDirection)
                    print "Directions left: {0}".format(applicableDirections)
            else:
                print "(MATCHED) Move found. Jumping {0}".format(rule)
                matchFound = True
        #print ("The rule is {0}".format(rule))
        if rule is not None:
            describeRule(rule)
            applyRule(rule, state)
        describeState(state)
        moveCount += 1

    print "Out of Moves. Game Over."

def backtrackCounter():
    global heuristicSwitch
    if heuristicSwitch is False:
        incrementBtWithoutHeuristic()
    elif heuristicSwitch is True:
        incrementBtWithHeuristic()
    else:
        pass

def backTrackFailureCounter():
    global nonHeuristicFailures
    global heuristicFailures
    global heuristicSwitch
    if heuristicSwitch is False:
        nonHeuristicFailures += 1
    elif heuristicSwitch is True:
        heuristicFailures += 1
    else:
        pass

def backTrack(stateList, count):
    backtrackCounter()
    moveCount = count
    message = ""
    if moveCount > 50:
        noMoves()
    print "Attempting move {0}.".format(moveCount + 1)
    print "The provided statelist is {0}".format(stateList)
    state = stateList[0]
    print "The selected state is      {0}".format(state)

    availablePegs = getAvailablePegs(state)

    describeState(state)
    ruleSet = applicableRules(state)
    print "RULESET: {0}".format(ruleSet)

    if state in stateList[1:]:
        message += "State in rest of stateList"
        print "FAILED. " + message
        backTrackFailureCounter()
        return False
    if goal(state):
        message += "Goal reached."
        print "SUCCESS. " + message
        backTrackFailureCounter()
        return True
    if len(ruleSet) < 1:
        message += "Found Dead End state."
        print "FAILED. " + message
        backTrackFailureCounter()
        return False
    if len(stateList) > 5000:
        message += "Exceeded max tree level."
        print "FAILED. " + message
        backTrackFailureCounter()
        return False

    if ruleSet is None or len(ruleSet) < 1:
        message += "Empty rule set."
        print "FAILED. " + message
        backTrackFailureCounter()
        return False

    for rule in ruleSet:
        print "Rule[0] is '{0}' and Rule[1] is '{1}' from {2}".format(rule[0], rule[1], ruleSet)
        pc = preCondition(state, int(rule[0]), rule[1])
        print "pc is {0}".format(pc)
        newState = applyRule(pc, state)
        describeState(newState)
        newStateList = addToFront(newState, stateList)
        count += 1
        print "== BACKTRACKING ==\n"
        path = backTrack(newStateList, count)
        if path is not False:
            return appendPath(path, rule)
        else:
            backTrackFailureCounter()
    return False

def addToFront(state, stateList):
    #print "Adding to front of stateList..."
    #print "stateList before is {0}".format(stateList)
    stateList.insert(0, state)
    #print "stateList after is {0}".format(stateList)
    return stateList

def appendPath(path, rule):
    global finalPath
    finalPath += str(rule) + " :: " + str(path) + "\n"

def printFinalPath():
    global finalPath
    print finalPath

def incrementBtWithoutHeuristic():
    global btCountWithoutHeuristic
    btCountWithoutHeuristic += 1
    print "Incrementing w_o Heuristic to {0}".format(btCountWithoutHeuristic)

def incrementBtWithHeuristic():
    global btCountWithHeuristic
    btCountWithHeuristic += 1
    print "Incrementing with Heuristic to {0}".format(btCountWithHeuristic)

def main():
    #flailWildly(initialState)
    global btCountWithoutHeuristic
    global btCountWithHeuristic
    global nonHeuristicFailures
    global heuristicFailures
    global heuristicSwitch
    global finalPath

    print "Running Backtrack Algorithm without Heuristic."
    backTrack([initialState], 0)
    printFinalPath()

    heuristicSwitch = True
    finalPath = "\n==Path:==\n"

    print "Running Backtrack Algorithm with Heuristic."
    backTrack([initialState], 0)
    printFinalPath()
    print "Number of calls to backtrack without Heuristic: {0}".format(btCountWithoutHeuristic)
    print "Reported Failures: {0}\n".format(nonHeuristicFailures)
    print "Number of calls to backtrack with Heuristic: {0}".format(btCountWithHeuristic)
    print "Reported Failures: {0}".format(heuristicFailures)


if  __name__ =='__main__':
    main()