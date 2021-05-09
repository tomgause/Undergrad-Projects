#AOPIASPODIAPOSDJKPAJSDKPJOSA

class foo():
    def __init__(self,y=1,x=1):
        self.x = x
        
    @property
    def y(self):
        return 2 * self.x
    

class boo():
    def __init__(self,y=1,x=1):
        self.x = x
        
    @property
    def y(self):
        return self.x * 2
    
from pyprocessing import *
from Tescode2 import *

global A
A = 'hello'

    def huntAmbulance(self,ftile):
        """
        Targets tile towards which distance to Fieri is lowest
        Cannot do 180 turns
        """
        global destinationTileAmbulance1
        target = ftile
        destinationTileAmbulance1 = ''
        separation = 10000
        adj = self.tile.adjacent()
        try adj.remove(Grid[22][16])
        
        for tile in adj:
            if tile != self.tile.directionalTile(oppositeDirection(self.direction)):
                if tile.playable == True:
                    if distance(target.x,target.y,tile.x,tile.y) <= separation:
                        separation = distance(target.x,target.y,tile.x,tile.y)
                        destinationTileAmbulance1 = tile
                        print(tile)
    
    def scatterAmbulance(self,ftile):
        """
        Runs away from Fieri, targets nearby tile that increases distance from Fieri
        Can do 180 turns
        """
        global destinationTileAmbulance1
        
        target = ftile
        destinationTileAmbulance1 = ''
        separation = 10000
        adj = self.tile.adjacent()
        for tile in adj:
            if tile != self.tile.directionalTile(oppositeDirection(self.direction)):
                if tile.playable == True:
                    if distance(target.x,target.y,tile.x,tile.y) <= separation:
                        separation = distance(target.x,target.y,tile.x,tile.y)
                        destinationTileAmbulance1 = tile