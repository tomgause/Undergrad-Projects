global Grid
global foodTiles
global powerTiles
global wallTiles
global emptyTiles

from sprites import *
from pyprocessing import *

Grid = [[0 for y in range(31)] for x in range(28)]

class tile():
    
    def __init__(self, x = -1, y = -1, playable = False,startType = 'food'):
        """
        Initialize the two properties.
        """
        self.x = x
        self.y = y
        self.playable = playable
        self.startType = startType
    
    def adjacentN(self):
        try:
            return Grid[self.x][self.y+1]
        except IndexError:
            adjacentN = tile(startType = 'nullspace')
        return adjacentN
    def adjacentE(self):
        if self.x==25 and self.y==16:
            adjacentE = Grid[4][16]
        else:
            try:
                return Grid[self.x+1][self.y]
            except IndexError:
                adjacentE = tile(startType = 'nullspace')
        return adjacentE
    def adjacentS(self):
        try:
            return Grid[self.x][self.y-1]
        except IndexError:
            adjacentS = tile(startType = 'nullspace')
        return adjacentS
    def adjacentW(self):
        if self.x==2 and self.y==16:
            adjacentW = Grid[25][16]
        else:
            try:
                return Grid[self.x-1][self.y]
            except IndexError:
                adjacentW = tile(startType = 'nullspace')
        return adjacentW
            
    def adjacent(self):
        return [self.adjacentN(),self.adjacentE(),self.adjacentS(),self.adjacentW()]
    
    def directionalTile(self,direction):
        """
        Returns the adjacent tile in the direction currently facing
        """
        if direction == 'n':
            try:              
                return self.adjacentN()
            except AttributeError:
                return Grid[1][1]
        
        elif direction == 'e':
            try:              
                return self.adjacentE()
            except AttributeError:
                return Grid[1][1]

        elif direction == 's':
            try:              
                return self.adjacentS()
            except AttributeError:
                return Grid[1][1]
        
        else:
            try:              
                return self.adjacentW()
            except AttributeError:
                return Grid[1][1]

    def __str__(self):
        """
        This returns a long version string describing the tile.
        
        Overriding this function provides this string to str() and print().
        """
        return '({},{}), playable = {}, startType = {}'.format(self.x,self.y,self.playable,self.startType)
    
    def __repr__(self):
        """
        This returns a short version string describing the tilep.
        """
        return '({},{}),{}'.format(self.x,self.y,self.startType)
    
    def __eq__(self, rhs):
        return self.x == rhs.x and self.y == rhs.y
        
###############################################################################
########################## TILE ASSIGNMENT ####################################
###############################################################################

Grid = [[tile(x,y,True,'food') for y in range(31)] for x in range(28)]

# DEFAULT TYPE = FOOD
foodTiles = []
powerTiles = []
wallTiles = []
emptyTiles = []
            
### POWER TILES ###
for tile in [Grid[1][7],Grid[26][7],Grid[27][1],Grid[26][27]]:
    tile.startType = 'power'
    powerTiles.append(tile)

#### WALL TILES ###
y0walls = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]
y1walls = [0,27]
y2walls = [0,2,3,4,5,6,7,8,9,10,11,13,14,16,17,18,19,20,21,22,23,24,25,27]
y3walls = [0,2,3,4,5,6,7,8,9,10,11,13,14,16,17,18,19,20,21,22,23,24,25,27]
y4walls = [0,7,8,13,14,19,20,27]
y5walls = [0,1,2,4,5,7,8,10,11,12,13,14,15,16,17,19,20,22,23,25,26,27]
y6walls = [0,1,2,4,5,7,8,10,11,12,13,14,15,16,17,19,20,22,23,25,26,27]
y7walls = [0,4,5,22,23,27]
y8walls = [0,2,3,4,5,7,8,9,10,11,13,14,16,17,18,19,20,22,23,24,25,27]
y9walls = [0,2,3,4,5,7,8,9,10,11,13,14,16,17,18,19,20,22,23,24,25,27]
y10walls = [0,13,14,27]
y11walls = [0,1,2,3,4,5,7,8,10,11,12,13,14,15,16,17,19,20,22,23,24,25,26,27]
y12walls = [0,1,2,3,4,5,7,8,10,11,12,13,14,15,16,17,19,20,22,23,24,25,26,27]
y13walls = [0,1,2,3,4,5,7,8,19,20,22,23,24,25,26,27]
y14walls = [0,1,2,3,4,5,7,8,10,11,12,13,14,15,16,17,19,20,22,23,24,25,26,27]
y15walls = [0,1,2,3,4,5,7,8,10,11,12,13,14,15,16,17,19,20,22,23,24,25,26,27]
y16walls = [10,11,12,13,14,15,16,17]
y17walls = [0,1,2,3,4,5,7,8,10,11,12,13,14,15,16,17,19,20,22,23,24,25,26,27]
y18walls = [0,1,2,3,4,5,7,8,10,11,12,13,14,15,16,17,19,20,22,23,24,25,26,27]
y19walls = [0,1,2,3,4,5,7,8,19,20,22,23,24,25,26,27]
y20walls = [0,1,2,3,4,5,7,8,9,10,11,13,14,16,17,18,19,20,22,23,24,25,26,27]
y21walls = [0,1,2,3,4,5,7,8,9,10,11,13,14,16,17,18,19,20,22,23,24,25,26,27]
y22walls = [0,7,8,13,14,19,20,27]
y23walls = [0,2,3,4,5,7,8,10,11,12,13,14,15,16,17,19,20,22,23,24,25,27]
y24walls = [0,2,3,4,5,7,8,10,11,12,13,14,15,16,17,19,20,22,23,24,25,27]
y25walls = [0,27]
y26walls = [0,2,3,4,5,7,8,9,10,11,13,14,16,17,18,19,20,22,23,24,25,27]
y27walls = [0,2,3,4,5,7,8,9,10,11,13,14,16,17,18,19,20,22,23,24,25,27]
y28walls = [0,2,3,4,5,7,8,9,10,11,13,14,16,17,18,19,20,22,23,24,25,27]
y29walls = [0,13,14,27]
y30walls = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]
walls = [y0walls,y1walls,y2walls,y3walls,y4walls,y5walls,y6walls,y7walls,y8walls,y9walls,y10walls,y11walls,y12walls,y13walls, \
         y14walls,y15walls,y16walls,y17walls,y18walls,y19walls,y20walls,y21walls,y22walls,y23walls,y24walls,y25walls,y26walls,\
         y27walls,y28walls,y29walls,y30walls]
ycor = 0
for wall in walls:
    for x in wall:
        Grid[x][ycor].startType = 'wall'
        Grid[x][ycor].playable = False
        wallTiles.append(Grid[x][ycor])
    ycor += 1

### EMPTY TILES ###
y11empty = [9,18]
y12empty = [9,18]
y13empty = [9,10,11,12,13,14,15,16,17,18]
y14empty = [9,18]
y15empty = [9,18]
y16empty = [0,1,2,3,4,5,7,8,9,18,19,20,22,23,24,25,26,27]
y17empty = [9,18]
y18empty = [9,18]
y19empty = [9,10,11,12,13,14,15,16,17,18]
y20empty = [12,15]
y21empty = [12,15]
empties = [y11empty,y12empty,y13empty,y14empty,y15empty,y16empty,y17empty,y18empty,y19empty,y20empty,y21empty]
ycor = 11
for empty in empties:
    for x in empty:
        Grid[x][ycor].startType = 'empty'
        Grid[x][ycor].playable = True
        emptyTiles.append(Grid[x][ycor])
    ycor += 1

### FOOD TILES ###
    
for y in Grid:
    for x in y:
        if x.startType == 'food':
            foodTiles.append(x)

###############################################################################
########################## TILE ASSIGNMENT END ################################
###############################################################################

def printGrid():
    for x in Grid:
        textwall = []
        for y in x:
            textwall.append(y.startType[0])
        print(textwall)
        
def printGridPlayable():
    for x in Grid:
        textwall = []
        for y in x:
            if y.playable == True:
                textwall.append('O')
            else:
                textwall.append('.')
        print(textwall)

def callMap():
    return loadImage("Map.jpg")