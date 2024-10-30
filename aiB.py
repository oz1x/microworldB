# NAME(S): [PLACE YOUR NAME(S) HERE]
#
# APPROACH: [WRITE AN OVERVIEW OF YOUR APPROACH HERE.]
#     Please use multiple lines (< ~80-100 char) for you approach write-up.
#     Keep it readable. In other words, don't write
#     the whole damned thing on one super long line.
#
#     In-code comments DO NOT count as a description of
#     of your approach.

import random


class AI:

    class TileObj:

        def __init__(self, tileType='@'):
            self.typeOfTile = tileType
            self.visited = 0

        def isVisited(self):
            return self.visited

        def setVisited(self):
            self.visited = 1
        
    
    def __init__(self, max_turns):
        self.turn = -1
        self.previousChoice = 'X'
        self.memory = [[self.TileObj()]]
        self.xPos = 0
        self.xBound = 0
        self.yPos = 0
        self.yBound = 0
        self.turnsSinceGoal = 0
        self.doneWithGoals = False
        self.backTrackStack = []
        self.flagNoNewTiles = 0
        self.goalXPos = 0
        self.goalYPos = 0
        self.exitPath = []
        self.foundGoal = False
        self.exitPathGenerated = False
        self.opposites = {'N': 'S', 'S': 'N', 'E': 'W', 'W':'E', 'X': 'Y'}

    def update(self, percepts, msg):

        message = None
    
        def genExitPath(self):
            print("\n\nINITIATING EXIT PATH GENERATION\n\n")
            numRuns = 1
            pathToExit = []
            tempX = self.xPos
            tempY = self.yPos
            shortestPath = 999
            lenSP = 999
            while self.memory[tempX][tempY].typeOfTile != 'r':
                shortestPath = 999
                lenSP = 999
                for direction in percepts:
                    if direction == 'X':
                        choice = 'x'
                        continue
                    
                    numTilesInPath = 0
                    if direction == 'N':
                        lenPath = 0
                        i = 1
                        numTilesInPath = 0
                        while self.memory[tempX][tempY-i].typeOfTile != 'w':
                            if self.memory[tempX][tempY-i].typeOfTile == 'r':
                                choice = direction
                                return choice
                            if self.memory[tempX][tempY-i].isVisited() == 1:
                                self.memory[tempX][tempY-i].visited = 0
                                numTilesInPath += 1
                            
                            #else:
                            #   numTilesInPath = -999
                            i += 1
                            lenPath += 1

                        if numTilesInPath < shortestPath and numTilesInPath > 0:
                            shortestPath = numTilesInPath
                            lenSP = lenPath
                            choice = direction
        
                    elif direction == 'E':
                        lenPath = 0
                        i = 1
                        numTilesInPath = 0
                        while self.memory[tempX+i][tempY].typeOfTile != 'w':
                            if self.memory[tempX+i][tempY].typeOfTile == 'r':
                                choice = direction
                                return choice
                            if self.memory[tempX+i][tempY].isVisited() == 1:
                                self.memory[tempX+i][tempY].visited = 0
                                numTilesInPath += 1
                            #else:
                            #    numTilesInPath = -999
                            i += 1
                            lenPath += 1

                        if numTilesInPath < shortestPath and numTilesInPath > 0:
                            shortestPath = numTilesInPath
                            lenSP = lenPath
                            choice = direction

                    elif direction == 'S':
                        lenPath = 0
                        i = 1
                        numTilesInPath = 0
                        while self.memory[tempX][tempY+i].typeOfTile != 'w':
                            if self.memory[tempX][tempY+i].typeOfTile == 'r':
                                choice = direction
                                return choice
                            if self.memory[tempX][tempY+i].isVisited() == 1:
                                self.memory[tempX][tempY+i].visited = 0
                                numTilesInPath += 1
                            #else:
                            #    numTilesInPath = -999
                            i += 1
                            lenPath += 1

                        if numTilesInPath < shortestPath and numTilesInPath > 0:
                            shortestPath = numTilesInPath
                            lenSP = lenPath
                            choice = direction
                    
                    elif direction == 'W':
                        lenPath = 0
                        i = 1
                        numTilesInPath = 0
                        while self.memory[tempX-i][tempY].typeOfTile != 'w':
                            if self.memory[tempX-i][tempY].typeOfTile == 'r':
                                choice = direction
                                return choice
                            if self.memory[tempX-i][tempY].isVisited() == 1:
                                self.memory[tempX-i][tempY].visited = 0
                                numTilesInPath += 1
                            #else:
                            #   numTilesInPath = -999
                            i += 1
                            lenPath += 1

                        if numTilesInPath < shortestPath and numTilesInPath > 0:
                            shortestPath = numTilesInPath
                            lenSP = lenPath
                            choice = direction

                if choice != 'x':
                    for i in range(lenSP):
                        print("adding " + str(i) +"st item to list")
                        pathToExit.append(choice)
                        if choice == 'N':
                            tempY -= 1
                        if choice == 'E':
                            tempX += 1
                        if choice == 'S':
                            tempY += 1
                        if choice == 'W':
                            tempX -= 1
                else:

                    self.memory[tempX][tempY].visited = 0
                    choice = self.opposites[pathToExit.pop()]
                    if choice == 'N':
                        tempY -= 1
                    if choice == 'E':
                        tempX += 1
                    if choice == 'S':
                        tempY += 1
                    if choice == 'W':
                        tempX -= 1

                print("iter "+ str(numRuns) + ", choice: " + choice)
                numRuns += 1
            return pathToExit

        #if msg is not None:
        #    if len(self.memory[0]) < len(msg[0][0]):
        #        self.yPos += 1
        #    elif len(self.memory) < len(msg[0]):
        #        self.xPos += 1

        #    self.memory = msg[0]

        if self.doneWithGoals and not self.exitPathGenerated:
            pathToExit = genExitPath(self)
            self.exitPathGenerated = True

        elif self.doneWithGoals and self.exitPathGenerated:
            return (pathToExit.pop(0), message)

        if (self.memory[self.xPos][self.yPos].isVisited() == 0):
            self.memory[self.xPos][self.yPos].setVisited()

        #mapping function -- complete?
        for direction, path in percepts.items():
            if direction == 'X':
                continue
            i = 1
            if direction == 'N':
                atEdge = 0
                tilesOut = 0
                for tile in path:
                    if self.yPos - tilesOut == 0:
                        atEdge = 1
                    if atEdge == 1:
                        for sublist in self.memory:
                            sublist.insert(0, self.TileObj())
                        self.yPos += 1
                    self.memory[self.xPos][self.yPos-i].typeOfTile = tile
                    tilesOut += 1
                    i += 1
            i = 1
            if direction == 'E':
                for tile in path:
                    if self.xPos+i+1 > len(self.memory):
                        self.memory.append([self.TileObj() for i in range(len(self.memory[0]))])
                    self.memory[self.xPos+i][self.yPos].typeOfTile = tile
                    i += 1

            i = 1
            if direction == 'S':
                for tile in path:
                    if self.yPos+i+1 > len(self.memory[self.xPos]):
                        for sublist in self.memory:
                            sublist.append(self.TileObj())
                    self.memory[self.xPos][self.yPos+i].typeOfTile = tile
                    i+=1

            i = 1
            if direction == 'W':
                atEdge = 0
                tilesOut = 0
                for tile in path:
                    if self.xPos - tilesOut == 0:
                        atEdge = 1
                    if atEdge == 1:
                        self.memory.insert(0, [self.TileObj() for i in range(len(self.memory[0]))])
                        self.xPos += 1
                    self.memory[self.xPos-i][self.yPos].typeOfTile = tile
                    i+=1
                    tilesOut+=1
            i = 1

        shortestPath = 999
        message = None
        print("B MAP:")
        
        for j in range(len(self.memory[0])):
            for h in range(len(self.memory)):
                if h == self.xPos and j == self.yPos:
                    print("#", end='')
                else:
                    print(self.memory[h][j].typeOfTile,end='')
            print()

        if percepts.get('X')[0] in  ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            self.turnsSinceGoal = 0
            return ('U', None)
        elif percepts.get('X')[0] == 'r':
            self.foundGoal = True
            if self.doneWithGoals == True:
                return ('U', None)
        elif self.turnsSinceGoal > 150:
            self.doneWithGoals = True
            self.turnsSinceGoal = -999

        #choice function
        choice = 'x'
        for direction in percepts:
            if direction == 'X':
                choice = 'x'
                continue
            
            numTilesInPath = 0
            if direction == 'N':
                while self.memory[self.xPos][self.yPos-i].typeOfTile != 'w':
                    if self.memory[self.xPos][self.yPos-i].typeOfTile in  ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                        choice = direction
                        self.yPos -= 1
                        self.backTrackStack.append(choice)
                        self.previousChoice = choice
                        return (choice, None)
                    if self.memory[self.xPos][self.yPos-i].isVisited() == 0:
                        numTilesInPath += 1
                    i += 1

                if numTilesInPath < shortestPath and numTilesInPath > 0:
                    shortestPath = numTilesInPath
                    choice = direction

            i = 1
            numTilesInPath = 0
            if direction == 'E':
                while self.memory[self.xPos+i][self.yPos].typeOfTile != 'w':
                    if self.memory[self.xPos+i][self.yPos].typeOfTile in  ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                        choice = direction
                        self.xPos += 1
                        self.backTrackStack.append(choice)
                        self.previousChoice = choice
                        return (choice, None)
                    if self.memory[self.xPos+i][self.yPos].isVisited() == 0:
                        numTilesInPath += 1
                    i += 1

                if numTilesInPath < shortestPath and numTilesInPath > 0:
                    shortestPath = numTilesInPath
                    choice = direction

            i = 1
            numTilesInPath = 0
            if direction == 'S':
                while self.memory[self.xPos][self.yPos+i].typeOfTile != 'w':
                    if self.memory[self.xPos][self.yPos+i].typeOfTile in  ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                        choice = direction
                        self.yPos += 1
                        self.backTrackStack.append(choice)
                        self.previousChoice = choice
                        return (choice, None)
                    if self.memory[self.xPos][self.yPos+i].isVisited() == 0:
                        numTilesInPath += 1
                    i += 1

                if numTilesInPath < shortestPath and numTilesInPath > 0:
                    shortestPath = numTilesInPath
                    choice = direction
            
            i = 1
            numTilesInPath = 0
            if direction == 'W':
                while self.memory[self.xPos-i][self.yPos].typeOfTile != 'w':
                    if self.memory[self.xPos-i][self.yPos].typeOfTile in  ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                        choice = direction
                        self.xPos -= 1
                        self.backTrackStack.append(choice)
                        self.previousChoice = choice
                        return (choice, None)
                    if self.memory[self.xPos-i][self.yPos].isVisited() == 0:
                        numTilesInPath += 1
                    i += 1

                if numTilesInPath > 0:
                    choice = direction
                    self.xPos -= 1
                    self.backTrackStack.append(choice)
                    self.previousChoice = choice
                    if self.foundGoal == True:
                            self.exitPath.append(choice)
                    return (choice, None)

                
        for direction in percepts:

            if direction == 'X':
                continue

            if direction == 'N':
                if choice == direction:
                    self.yPos -= 1

            if direction == 'E':
                if choice == direction:
                    self.xPos += 1

            if direction == 'S':
                if choice == direction:
                    self.yPos += 1

            if direction == 'W':
                if choice == direction:
                    self.xPos -= 1

        if choice == 'x':
            choice = self.opposites[self.backTrackStack.pop()]
            if choice == 'N':
                self.yPos -= 1
            if choice == 'E':
                self.xPos += 1
            if choice == 'S':
                self.yPos += 1
            if choice == 'W':
                self.xPos -= 1
            return (choice, None)
        
        self.backTrackStack.append(choice)

        self.previousChoice = choice
        self.turnsSinceGoal += 1


        return (choice, message)
    