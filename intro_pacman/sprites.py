from map import *
from pyprocessing import *
import random
import math
import time
global Grid

def distance(myX,myY,targetX,targetY):
    return ((targetX - myX)**2 + (targetY - myY)**2)**.5

def oppositeDirection(direction):
    if direction == 'n':
        return 's'
    elif direction == 'e':
        return 'w'
    elif direction == 's':
        return 'n'
    else:
        return 'e'
    
class guy():
    
    def __init__(self, tile = 0, x = 13, y = 7,direction = 'e',speed = 0,flavortime = False,face = loadImage("guynormal.jpg"),steer = 'e'):
        """
        Initialize the properties.
        """
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.flavortime = flavortime
        self.face = face
        self.steer = steer
        self.faceN = loadImage('guyNorth.jpg')
        self.faceE = loadImage('guyEast.jpg')
        self.faceS = loadImage('guySouth.jpg')
        self.faceW = loadImage('guyWest.jpg')
        self.black = loadImage('black.jpg')

    def __str__(self):
        """
        This returns a long version string describing the guy.
        
        Overriding this function provides this string to str() and print().
        """
        return 'Take me to Flavortown baby'
    
    def __repr__(self):
        """
        This returns a short version string describing the guy.
        """
        return '({},{}),{},flav={}'.format(self.x,self.y,self.direction,self.flavortime)       
    
    def initFieri(self):
        xcor = self.x*25+12
        ycor = (31-self.y)*25-12
        if self.direction == 'n':
            image(self.black,xcor,ycor+5)
            image(self.faceN, xcor, ycor)
            return
        elif self.direction == 'e':
            image(self.black,xcor-5,ycor)
            image(self.faceE, xcor, ycor)
            return
        elif self.direction == 's':
            image(self.black,xcor,ycor-5)
            image(self.faceS, xcor, ycor)
            return
        elif self.direction == 'w':
            image(self.black,xcor+5,ycor)
            image(self.faceW, xcor, ycor)
            return

    def move(self):
        
        ### PORTAL TILES ###
        
        if round(self.x) == 25 and round(self.y) == 16:
            self.x,self.y = 3,16
            image(loadImage('black.jpg'),24.5*25+12,(31-16)*25-12)
            
        if round(self.x) == 2 and round(self.y) == 16:
            self.x,self.y = 24,16
            image(loadImage('black.jpg'),2.5*25+12,(31-16)*25-12)
        
        ### PORTAL TILES END ###
        
        if self.direction == 'n':
            if self.tile.directionalTile(self.direction).playable == True:
                self.y += .25
                self.x = round(self.x)
            return
        elif self.direction == 's':
            if self.tile.directionalTile(self.direction).playable == True:
                self.y += -.25
                self.x = round(self.x)
            return
        elif self.direction == 'e':
            if self.tile.directionalTile(self.direction).playable== True:
                self.x += .25
                self.y = round(self.y)
            return
        elif self.direction == 'w':
            if self.tile.directionalTile(self.direction).playable == True:
                self.x += -.25
                self.y = round(self.y)
            return
                
        self.x,self.y = round(self.x,3),round(self.y,3)
    
    @property
    def tile(self):
        global Grid
        return Grid[round(self.x)][round(self.y)]

Fieri = guy()

class enemy():
    
    def __init__(self, x = 10, y = 13, tile = 0,direction = 'n',separation = 100,target = Fieri,speed = 0,state = 'hunting',scatteringRegion = 0,image = ''):
        """
        Initialize the properties.
        """
        self.x = x
        self.y = y
        self.direction = direction
        self.target = target
        self.separation = ((self.x - self.target.x)**2 + (self.y - self.target.y)**2)**.5
        self.speed = speed
        self.state = state
        self.scatteringRegion = scatteringRegion
        self.image = loadImage("ambulance.jpg")
        self.faceN = loadImage('ambulanceNorth.jpg')
        self.faceE = loadImage('ambulanceEast.jpg')
        self.faceS = loadImage('ambulanceSouth.jpg')
        self.faceW = loadImage('ambulanceWest.jpg')
        self.black = loadImage('black.jpg')
    
    def __repr__(self):
        """
        This returns a short version string describing the guy.
        """
        return '({},{}),{},state={}'.format(self.x,self.y,self.direction,self.state)
    
    def move(self,destination):
        if destination.x > self.x:
            self.direction = 'e'
            self.x += .2
        elif destination.x < self.x:
            self.direction = 'w'
            self.x += -.2
        elif destination.y < self.y:
            self.direction = 's'
            self.y += -.2
        elif destination.y > self.y:
            self.direction = 'n'
            self.y += .2
        self.x = round(self.x,3)
        self.y = round(self.y,3)
        if self.y == 4.1 and self.direction == 's':
            self.y = 4
        if round(self.x) == 25 and round(self.y) == 16:
            self.x,self.y = 3,16
            image(loadImage('black.jpg'),24.5*25+12,(31-16)*25-12)
        if round(self.x) == 2 and round(self.y) == 16:
            self.x,self.y = 24,16
            image(loadImage('black.jpg'),25*2.5+12,(31-16)*25-12)
    
    def go(self,ftile):
        """
        Calls command based on current state
        """
        if self.state == 'hunting':
            self.hunt(ftile)
        if self.state == 'scattering':
            self.scatter(ftile)
        if self.state == 'fleeing':
            self.flee(ftile)
    
    ### AMBULANCE ###
    
    def huntAmbulance(self,ftile):
        """
        Targets tile towards which distance to Fieri is lowest
        Cannot do 180 turns
        """
        global destinationTileAmbulance
        target = ftile
        destinationTileAmbulance = ''
        separation = 10000
        adj = self.tile.adjacent()
        
        try:
            adj.remove(Grid[22][16])
        except ValueError:
            pass
        try:
            adj.remove(Grid[5][16])
        except ValueError:
            pass
        
        for tile in adj:
            if tile != self.tile.directionalTile(oppositeDirection(self.direction)):
                if tile.playable == True:
                    if distance(target.x,target.y,tile.x,tile.y) <= separation:
                        separation = distance(target.x,target.y,tile.x,tile.y)
                        destinationTileAmbulance = tile
    
    def scatterAmbulance(self,ftile):
        """
        Runs away from Fieri, targets nearby tile that increases distance from Fieri
        Can do 180 turns
        """
        global destinationTileAmbulance
        
        target = ftile
        destinationTileAmbulance = ''
        separation = 10000
        adj = self.tile.adjacent()
        
        try:
            adj.remove(Grid[22][16])
        except ValueError:
            pass
        try:
            adj.remove(Grid[5][16])
        except ValueError:
            pass
        
        for tile in adj:
            if tile != self.tile.directionalTile(oppositeDirection(self.direction)):
                if tile.playable == True:
                    if distance(target.x,target.y,tile.x,tile.y) <= separation:
                        separation = distance(target.x,target.y,tile.x,tile.y)
                        destinationTileAmbulance = tile
    
    ### AMBULANCE1 ###
    
    def huntAmbulance1(self,ftile):
        """
        Targets tile towards which distance to Fieri is lowest
        Cannot do 180 turns
        """
        global destinationTileAmbulance1
        target = ftile
        destinationTileAmbulance1 = ''
        separation = 10000
        adj = self.tile.adjacent()
        
        try:
            adj.remove(Grid[22][16])
        except ValueError:
            pass
        try:
            adj.remove(Grid[5][16])
        except ValueError:
            pass
        
        for tile in adj:
            if tile != self.tile.directionalTile(oppositeDirection(self.direction)):
                if tile.playable == True:
                    if distance(target.x,target.y,tile.x,tile.y) <= separation:
                        separation = distance(target.x,target.y,tile.x,tile.y)
                        destinationTileAmbulance1 = tile
    
    def scatterAmbulance1(self,ftile):
        """
        Runs away from Fieri, targets nearby tile that increases distance from Fieri
        Can do 180 turns
        """
        global destinationTileAmbulance1
        
        target = ftile
        destinationTileAmbulance1 = ''
        separation = 10000
        adj = self.tile.adjacent()
        
        try:
            adj.remove(Grid[22][16])
        except ValueError:
            pass
        try:
            adj.remove(Grid[5][16])
        except ValueError:
            pass
        
        for tile in adj:
            if tile != self.tile.directionalTile(oppositeDirection(self.direction)):
                if tile.playable == True:
                    if distance(target.x,target.y,tile.x,tile.y) <= separation:
                        separation = distance(target.x,target.y,tile.x,tile.y)
                        destinationTileAmbulance1 = tile
    
        ### AMBULANCE2 ###
    
    def huntAmbulance2(self,ftile):
        """
        Targets tile towards which distance to Fieri is lowest
        Cannot do 180 turns
        """
        global destinationTileAmbulance2
        target = ftile
        destinationTileAmbulance2 = ''
        separation = 10000
        adj = self.tile.adjacent()
        
        try:
            adj.remove(Grid[22][16])
        except ValueError:
            pass
        try:
            adj.remove(Grid[5][16])
        except ValueError:
            pass
        
        for tile in adj:
            if tile != self.tile.directionalTile(oppositeDirection(self.direction)):
                if tile.playable == True:
                    if distance(target.x,target.y,tile.x,tile.y) <= separation:
                        separation = distance(target.x,target.y,tile.x,tile.y)
                        destinationTileAmbulance2 = tile
    
    def scatterAmbulance2(self,ftile):
        """
        Runs away from Fieri, targets nearby tile that increases distance from Fieri
        Can do 180 turns
        """
        global destinationTileAmbulance2
        
        target = ftile
        destinationTileAmbulance2 = ''
        separation = 10000
        adj = self.tile.adjacent()
        
        try:
            adj.remove(Grid[22][16])
        except ValueError:
            pass
        try:
            adj.remove(Grid[5][16])
        except ValueError:
            pass
        
        for tile in adj:
            if tile != self.tile.directionalTile(oppositeDirection(self.direction)):
                if tile.playable == True:
                    if distance(target.x,target.y,tile.x,tile.y) <= separation:
                        separation = distance(target.x,target.y,tile.x,tile.y)
                        destinationTileAmbulance2 = tile
    
    def initEnemy(self):
        xcor = self.x*25+10
        ycor = (31-self.y)*25-12
        if self.direction == 'n':
            image(self.faceN, xcor, ycor)
        elif self.direction == 'e':
            image(self.faceE, xcor, ycor)
        elif self.direction == 's':
            image(self.faceS, xcor, ycor)
        elif self.direction == 'w':
            image(self.faceW, xcor, ycor)
    
    @property
    def tile(self):
        return Grid[int(self.x)][int(self.y)]

class food():
    
    def __init__(self, x = 0, y = 0, consumed = False,image = ''):
        """
        """
        images = ['burger.jpg','pizza.jpg','cake.jpg']
        self.x = x
        self.y = y
        self.consumed = consumed
        self.image = loadImage(images[random.randint(0,2)])
        self.black = loadImage('black.jpg')
    
    def __repr__(self):
        """
        This returns a short version string describing the food.
        """
        return '({},{}),{}'.format(self.x,self.y,self.consumed)
    
    def initFood(self):
        if self.consumed == False:
            image(self.image,self.x*25+12,(31-self.y)*25-12)
        if self.consumed == True:
            image(self.black,self.x*25+12,(31-self.y)*25-12)