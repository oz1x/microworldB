# NAME(S): [PLACE YOUR NAME(S) HERE]
#
# APPROACH: [WRITE AN OVERVIEW OF YOUR APPROACH HERE.]
#     Please use multiple lines (< ~80-100 char) for you approach write-up.
#     Keep it readable. In other words, don't write
#     the whole damned thing on one super long line.
#
#     In-code comments DO NOT count as a description of
#     of your approach.
MAX_TURNS = 150
import random
from collections import deque

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
        self.turn = 0
        self.previousChoice = 'X'
        self.memory = [[[self.TileObj()]]]
        self.memoryLayer = 0
        self.layerTile = [[]]
        self.xPos = [0]
        self.xBound = 0
        self.yPos = [0]
        self.yBound = 0
        self.turnsSinceGoal = 0
        self.doneWithGoals = False
        self.backTrackStack = []
        self.flagNoNewTiles = 0
        self.exitPath = []
        self.foundGoal = False
        self.exitPathGenerated = False
        self.pathToExit = []
        self.opposites = {'N': 'S', 'S': 'N', 'E': 'W', 'W':'E', 'X': 'Y', 'o':'b', 'b':'o', 'y':'p', 'p':'y'}     

    def update(self, percepts, msg):
        self.turn += 1
        message = None
        if self.turn == 900:
            self.doneWithGoals = True


        def genExitPath(self):
            print("\n\nINITIATING EXIT PATH GENERATION\n\n")
            pathToExit = []
            tempMap = self.memory

            # Initialize visited status for each tile
            for sublist in tempMap[self.memoryLayer]:
                for tile in sublist:
                    tile.visited = False

            startX, startY = self.xPos[self.memoryLayer], self.yPos[self.memoryLayer]
            directions = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}
            queue = deque([(startX, startY, [])])  # Store position and path to reach that position
            tempMap[self.memoryLayer][startX][startY].visited = True

            # Perform BFS
            while queue:
                x, y, path = queue.popleft()

                for j in range(len(tempMap[self.memoryLayer][0])):
                    for h in range(len(tempMap[self.memoryLayer])):
                        if h == x and j == y:
                            print("#", end='')
                        elif tempMap[self.memoryLayer][h][j].typeOfTile == 'g':
                            if tempMap[self.memoryLayer][h][j].visited == 1:
                                print('█', end='')
                            else:
                                print(' ', end='')
                        else:
                            print(tempMap[self.memoryLayer][h][j].typeOfTile,end='')
                    print()

                # Check if we've reached the exit
                if tempMap[self.memoryLayer][x][y].typeOfTile == 'r':
                    print("FOUND EXIT, RETURNING PATH")
                    pathToExit = path + ['U']
                    return pathToExit

                # Explore neighboring tiles in all directions
                for direction, (dx, dy) in directions.items():
                    nx, ny = x + dx, y + dy

                    # Check within bounds and for non-wall tiles
                    if 0 <= nx < len(tempMap[self.memoryLayer]) and 0 <= ny < len(tempMap[self.memoryLayer][0]):
                        if not tempMap[self.memoryLayer][nx][ny].visited and tempMap[self.memoryLayer][nx][ny].typeOfTile not in {'w', '@'}:
                            # Mark as visited and add to queue with updated path
                            tempMap[self.memoryLayer][nx][ny].visited = True
                            queue.append((nx, ny, path + [direction]))

            # If no path is found, return an empty path
            print("COULD NOT FIND PATH TO EXIT")
            return []


        #if msg is not None :

        #   if self.turn == 1:
        #        self.memory = msg[0]

        #    else:

        #        if len(self.memory[0]) < len(msg[0][0]):
        #            self.yPos[self.memoryLayer] += (len(msg[0][0]) - len(self.memory[0]))
        #        if len(self.memory) < len(msg[0]):
        #            self.xPos[self.memoryLayer] += (len(msg[0]) - len(self.memory))
        #    
        #        self.memory = msg[0]

        if msg is not None :
            #if self.turn == 1:
                #self.memory = msg[0]
            #else:
             #   if len(self.memory[0]) < len(msg[0][0]):
              #      self.yPos[self.memoryLayer] += (len(msg[0][0]) - len(self.memory[0]))
               # if len(self.memory) < len(msg[0]):
                #    self.xPos[self.memoryLayer] += (len(msg[0]) - len(self.memory))
            
            self.memory = msg[0]
            try:
                self.xPos[self.memoryLayer] += msg[2][self.memoryLayer]
                self.yPos[self.memoryLayer] += msg[3][self.memoryLayer]
            except:
                print()


        if (self.memory[self.memoryLayer][self.xPos[self.memoryLayer]][self.yPos[self.memoryLayer]].isVisited() == 0):
            self.memory[self.memoryLayer][self.xPos[self.memoryLayer]][self.yPos[self.memoryLayer]].setVisited()

        deltaX = [0 for x in range(self.memoryLayer+1)] 
        deltaY = [0 for x in range(self.memoryLayer+1)]
        #mapping function -- complete?
        for direction, path in percepts.items():
            if direction == 'X':
                continue
            i = 1
            if direction == 'N':
                atEdge = 0
                tilesOut = 0
                for tile in path:
                    if self.yPos[self.memoryLayer] - tilesOut == 0:
                        atEdge = 1
                    if atEdge == 1:
                        for sublist in self.memory[self.memoryLayer]:
                            sublist.insert(0, self.TileObj())
                        self.yPos[self.memoryLayer] += 1
                        deltaY[self.memoryLayer] += 1
                    self.memory[self.memoryLayer][self.xPos[self.memoryLayer]][self.yPos[self.memoryLayer]-i].typeOfTile = tile
                    tilesOut += 1
                    i += 1
            i = 1
            if direction == 'E':
                for tile in path:
                    if self.xPos[self.memoryLayer]+i+1 > len(self.memory[self.memoryLayer]):
                        self.memory[self.memoryLayer].append([self.TileObj() for i in range(len(self.memory[self.memoryLayer][0]))])
                    self.memory[self.memoryLayer][self.xPos[self.memoryLayer]+i][self.yPos[self.memoryLayer]].typeOfTile = tile
                    i += 1

            i = 1
            if direction == 'S':
                for tile in path:
                    if self.yPos[self.memoryLayer]+i+1 > len(self.memory[self.memoryLayer][self.xPos[self.memoryLayer]]):
                        for sublist in self.memory[self.memoryLayer]:
                            sublist.append(self.TileObj())
                    self.memory[self.memoryLayer][self.xPos[self.memoryLayer]][self.yPos[self.memoryLayer]+i].typeOfTile = tile
                    i+=1

            i = 1
            if direction == 'W':
                atEdge = 0
                tilesOut = 0
                for tile in path:
                    if self.xPos[self.memoryLayer] - tilesOut == 0:
                        atEdge = 1
                    if atEdge == 1:
                        self.memory[self.memoryLayer].insert(0, [self.TileObj() for i in range(len(self.memory[self.memoryLayer][0]))])
                        self.xPos[self.memoryLayer] += 1
                        deltaX[self.memoryLayer] += 1
                    self.memory[self.memoryLayer][self.xPos[self.memoryLayer]-i][self.yPos[self.memoryLayer]].typeOfTile = tile
                    i+=1
                    tilesOut+=1
            i = 1

        shortestPath = 999
        message = (self.memory, self.previousChoice, deltaX, deltaY)
        print("B MAP:")
        
        for j in range(len(self.memory[self.memoryLayer][0])):
            for h in range(len(self.memory[self.memoryLayer])):
                if h == self.xPos[self.memoryLayer] and j == self.yPos[self.memoryLayer]:
                    print("#", end='')
                elif self.memory[self.memoryLayer][h][j].typeOfTile == 'g':
                    print(' ', end='')
                else:
                    print(self.memory[self.memoryLayer][h][j].typeOfTile,end='')
            print()

        if self.doneWithGoals and self.foundGoal and not self.exitPathGenerated:
            self.pathToExit = genExitPath(self)
            self.exitPathGenerated = True

        if self.doneWithGoals and self.exitPathGenerated:
            if percepts.get('X')[0] == 'r':
                return ('U', message)
            return (self.pathToExit.pop(0), message)

        if percepts.get('X')[0] in  ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            self.turnsSinceGoal = 0
            return ('U', message)
        elif percepts.get('X')[0] in ('y', 'p', 'o', 'b'):
            print("TELEPORTER TIMEEEEEEE")
            self.previousChoice = 'U'
            if ((percepts.get('X')[0] not in self.layerTile) or (self.opposites[percepts.get('X')[0]] not in self.layerTile)):   
                self.layerTile.append(percepts.get('X')[0])
                self.layerTile.append(len(self.memory))
                self.memory.append([[self.TileObj()]])
                self.memoryLayer = self.layerTile[self.layerTile.index(percepts.get('X')[0])+1]
                self.xPos[self.memoryLayer].append(0)
                self.yPos[self.memoryLayer].append(0)
            else:
                self.memoryLayer = self.layerTile[self.layerTile.index(percepts.get('X')[0])+1]
            return ('U', message)
        elif percepts.get('X')[0] == 'r':
            self.foundGoal = True
            if self.doneWithGoals == True:
                return ('U', message)
        elif self.turnsSinceGoal > MAX_TURNS:
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
                while self.memory[self.memoryLayer][self.xPos[self.memoryLayer]][self.yPos[self.memoryLayer]-i].typeOfTile != 'w':
                    if self.memory[self.memoryLayer][self.xPos[self.memoryLayer]][self.yPos[self.memoryLayer]-i].typeOfTile in  ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                        choice = direction
                        self.yPos[self.memoryLayer] -= 1
                        self.backTrackStack.append(choice)
                        self.previousChoice = choice
                        return (choice, message)
                    if self.memory[self.memoryLayer][self.xPos[self.memoryLayer]][self.yPos[self.memoryLayer]-i].isVisited() == 0:
                        numTilesInPath += 1
                    i += 1

                if numTilesInPath < shortestPath and numTilesInPath > 0:
                    shortestPath = numTilesInPath
                    choice = direction

            i = 1
            numTilesInPath = 0
            if direction == 'E':
                while self.memory[self.memoryLayer][self.xPos[self.memoryLayer]+i][self.yPos[self.memoryLayer]].typeOfTile != 'w':
                    if self.memory[self.memoryLayer][self.xPos[self.memoryLayer]+i][self.yPos[self.memoryLayer]].typeOfTile in  ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                        choice = direction
                        self.xPos[self.memoryLayer] += 1
                        self.backTrackStack.append(choice)
                        self.previousChoice = choice
                        return (choice, message)
                    if self.memory[self.memoryLayer][self.xPos[self.memoryLayer]+i][self.yPos[self.memoryLayer]].isVisited() == 0:
                        numTilesInPath += 1
                    i += 1

                if numTilesInPath < shortestPath and numTilesInPath > 0:
                    shortestPath = numTilesInPath
                    choice = direction

            i = 1
            numTilesInPath = 0
            if direction == 'S':
                while self.memory[self.memoryLayer][self.xPos[self.memoryLayer]][self.yPos[self.memoryLayer]+i].typeOfTile != 'w':
                    if self.memory[self.memoryLayer][self.xPos[self.memoryLayer]][self.yPos[self.memoryLayer]+i].typeOfTile in  ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                        choice = direction
                        self.yPos[self.memoryLayer] += 1
                        self.backTrackStack.append(choice)
                        self.previousChoice = choice
                        return (choice, message)
                    if self.memory[self.memoryLayer][self.xPos[self.memoryLayer]][self.yPos[self.memoryLayer]+i].isVisited() == 0:
                        numTilesInPath += 1
                    i += 1

                if numTilesInPath < shortestPath and numTilesInPath > 0:
                    shortestPath = numTilesInPath
                    choice = direction
            
            i = 1
            numTilesInPath = 0
            if direction == 'W':
                while self.memory[self.memoryLayer][self.xPos[self.memoryLayer]-i][self.yPos[self.memoryLayer]].typeOfTile != 'w':
                    if self.memory[self.memoryLayer][self.xPos[self.memoryLayer]-i][self.yPos[self.memoryLayer]].typeOfTile in  ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                        choice = direction
                        self.xPos[self.memoryLayer] -= 1
                        self.backTrackStack.append(choice)
                        self.previousChoice = choice
                        return (choice, message)
                    if self.memory[self.memoryLayer][self.xPos[self.memoryLayer]-i][self.yPos[self.memoryLayer]].isVisited() == 0:
                        numTilesInPath += 1
                    i += 1

                if numTilesInPath > 0:
                    choice = direction
                    self.xPos[self.memoryLayer] -= 1
                    self.backTrackStack.append(choice)
                    self.previousChoice = choice
                    if self.foundGoal == True:
                            self.exitPath.append(choice)
                    return (choice, message)

                
        for direction in percepts:

            if direction == 'X':
                continue

            if direction == 'N':
                if choice == direction:
                    self.yPos[self.memoryLayer] -= 1

            if direction == 'E':
                if choice == direction:
                    self.xPos[self.memoryLayer] += 1

            if direction == 'S':
                if choice == direction:
                    self.yPos[self.memoryLayer] += 1

            if direction == 'W':
                if choice == direction:
                    self.xPos[self.memoryLayer] -= 1

        if choice == 'x':
            try:
                choice = self.opposites[self.backTrackStack.pop()]
            except:
                print("Can't find anything else, let's get outta here!")
                self.doneWithGoals = True 
                self.foundGoal = True
                choice = 'U'
            if choice == 'N':
                self.yPos[self.memoryLayer] -= 1
            if choice == 'E':
                self.xPos[self.memoryLayer] += 1
            if choice == 'S':
                self.yPos[self.memoryLayer] += 1
            if choice == 'W':
                self.xPos[self.memoryLayer] -= 1
            return (choice, message)
        
        self.backTrackStack.append(choice)

        self.previousChoice = choice
        self.turnsSinceGoal += 1

        return (choice, message)
    