import random
import time
from pyprocessing import *
from sprites import *
from map import *

def setup():
    
    global mode
    global timeCounter
    global play
    global map
    global Ambulance
    global Ambulance1
    global Ambulance2
    global Fieri
    global destinationTileAmbulance
    global destinationTileAmbulance1
    global destinationTileAmbulance2
    global foodTiles
    global currentFood
    global score
    global difficulty
    
    # Starting values
    play = False
    score = 0
    mode = 'h'
    timeCounter = 0
    currentFood = []
    difficulty = 1
    
    # Background
    imageMode(CORNER)
    size(28*25,31*25)
    background(0)
    background(callMap())
    frameRate(40)
    
    # Starting Text
    textSize(15)
    textAlign(CENTER,CENTER)
    fill(183,187,255)
    text('PRESS P',13.7*25+12,(31-16.5)*25-12)
    text('TO PLAY',13.7*25+12,(31-15.2)*25-12)
    fill(0,255,0)
    textSize(15)
    text('SCORE',2.5*25+12,(31-19)*25-12)
    textSize(10)
    fill(255,0,0)
    text('DIFFICULTY',24.5*25+12,(31-19)*25-12)
    
    # Spawns starting food
    imageMode(CENTER)
    for i in range(5):
        foodID = random.randint(1,243)
        Food = ''
        Food = foodTiles[foodID]
        realFood = food(Food.x,Food.y,False)
        print(realFood)
        realFood.initFood()
        currentFood.append(realFood)
    
    # Creates Entities
    Fieri = guy()
    Ambulance = enemy()
    Ambulance1 = enemy(17,19)
    Ambulance2 = enemy(17,13)
    
    #Reaper = enemy()
    FTILE = Fieri.tile
    Ambulance.huntAmbulance(FTILE)
    Ambulance1.huntAmbulance1(FTILE)
    Ambulance2.huntAmbulance2(FTILE)
    
    imageMode(CENTER)

def draw():
    
    global mode
    global timeCounter
    global play
    global map
    global Fieri
    global Ambulance
    global Ambulance1
    global Ambulance2
    global score
    global difficulty
    global steer
    from sprites import destinationTileAmbulance
    from sprites import destinationTileAmbulance1
    from sprites import destinationTileAmbulance2
    
    # Increasing Difficulty
    frameRate(15 + 5*difficulty)
    
    # Score and Difficulty visuals
    textSize(35)
    fill(0,0,0)
    # Blacks out old values
    text(str(score),2.5*25+12,(31-13)*25-12)
    text(str(difficulty),24.5*25+12,(31-13)*25-12)
    
    # Checks for food consumed, increases score, increases difficulty
    for e in currentFood:
        if e.x == Fieri.tile.x and e.y == Fieri.tile.y:
            score += 5 + difficulty
            e.consumed = True
        e.initFood()
    if currentFood[0].consumed == True:
        currentFood.pop(0)
        #score += 5 + difficulty
    if len(currentFood) == 0:
        difficulty += 1
        for i in range(5):
            foodID = random.randint(1,243)
            Food = ''
            Food = foodTiles[foodID]
            realFood = food(Food.x,Food.y,False)
            realFood.initFood()
            currentFood.append(realFood)
    
    # Shows new values
    fill(0,255,0)
    text(str(score),2.5*25+12,(31-13)*25-12)
    fill(255,0,0)
    text(str(difficulty),24.5*25+12,(31-13)*25-12)
    
    # Visuals on all entities
    
    if play == True:
        Fieri.initFieri()
        Ambulance.initEnemy()
        Ambulance1.initEnemy()
        Ambulance2.initEnemy()
        
    ### DETECTS AMBULANCES
    
    if Ambulance.tile == Fieri.tile or Ambulance1.tile == Fieri.tile or Ambulance2.tile == Fieri.tile:
        play = 'end'
        textSize(80)
        textAlign(CENTER,CENTER)
        fill(183,187,255)
        text('GAME OVER',13.7*25+12,(31-16)*25-12)
        time.sleep(1)
    
    ### TIMER ###
    
    timeCounter += 1
    if timeCounter == 400:
        mode = 's'
    if timeCounter == 650:
        mode = 'h'
        timeCounter = 0
    
    ### PAUSE FUNCTION ###
    
    if key.pressed == True:

        if key.char == 'p':
            if play == True:
                textSize(25)
                textAlign(CENTER,CENTER)
                fill(255,0,0)
                text('PAUSED',13.7*25+12,(31-16)*25-12)
                play = not play
                time.sleep(1)
            if play == False:
                fill(0)
                textSize(15)
                text('PRESS P',13.7*25+12,(31-16.5)*25-12)
                text('TO PLAY',13.7*25+12,(31-15.2)*25-12)
                textSize(25)
                text('PAUSED',13.7*25+12,(31-16)*25-12)
                play = not play
                time.sleep(1)
    
    ### UNPAUSED ###
    
    if play == True:
        
        Fieri.move()
        Fieri.initFieri()
        Ambulance.initEnemy()
        Ambulance1.initEnemy()
        Ambulance2.initEnemy()
        
        #print('Fieri:{},{}'.format(Fieri.x,Fieri.y))

        timeCounter += 1
        if timeCounter == 400:
            mode = 's'
        if timeCounter == 650:
            mode = 'h'
            timeCounter = 0
        
        ### FIERI ###
        
        if key.pressed == True:
            
            if key.char == 'w':
                #print('w')
                Fieri.steer = 'n'
                if Fieri.tile.adjacentN().playable == False:
                    #print('impassable')
                    pass
                #elif Fieri.direction == 's':
                    #pass
                else:
                    Fieri.direction = 'n'
                
            elif key.char == 'd':
                #print('d')
                Fieri.steer = 'e'
                if Fieri.tile.adjacentE().playable == False:
                    #print('impassable')
                    pass
                #elif Fieri.direction == 'w':
                    #pass
                else:
                    Fieri.direction = 'e'
                
            elif key.char == 's':
                #print('s')
                Fieri.steer = 's'
                if Fieri.tile.adjacentS().playable == False:
                    #print('impassable')
                    pass
                #elif Fieri.direction == 'n':
                    #pass
                else:
                    Fieri.direction = 's'
                
            elif key.char == 'a':
                #print('a')
                Fieri.steer = 'w'
                if Fieri.tile.adjacentW().playable == False:
                    #print('impassable')
                    pass
                #elif Fieri.direction == 'e':
                    #pass
                else:
                    Fieri.direction = 'w'
        
        ### FIERI END ###
        
        ### ENEMIES ###
        
        ### AMBULANCE ###
                    
        if [round(Ambulance.x,2),round(Ambulance.y,2)] == [destinationTileAmbulance.x,destinationTileAmbulance.y]:
            FTILE = Fieri.tile
            if mode == 'h':
                FTILE = Fieri.tile
                Ambulance.huntAmbulance(FTILE)
            else:
                Ambulance.scatterAmbulance(Grid[26][29])
        else:
            #print('{},{}'.format(Ambulance.x,Ambulance.y))
            Ambulance.move(destinationTileAmbulance)
        
        ### AMBULANCE1 ###
            
        if [round(Ambulance1.x,2),round(Ambulance1.y,2)] == [destinationTileAmbulance1.x,destinationTileAmbulance1.y]:
            FTILE = Fieri.tile
            if mode == 'h':
                FTILE = Fieri.tile
                Ambulance1.huntAmbulance1(FTILE)
            else:
                Ambulance1.scatterAmbulance1(Grid[1][1])
        else:
            
            Ambulance1.move(destinationTileAmbulance1)
            
        ### AMBULANCE2 ###
            
        if [round(Ambulance2.x,2),round(Ambulance2.y,2)] == [destinationTileAmbulance2.x,destinationTileAmbulance2.y]:
            FTILE = Fieri.tile
            if mode == 'h':
                FTILE = Fieri.tile
                Ambulance2.huntAmbulance2(FTILE)
            else:
                Ambulance2.scatterAmbulance2(Grid[1][29])
        else:
            
            Ambulance2.move(destinationTileAmbulance2)
    
        ### ENEMIES END ###
    
run()