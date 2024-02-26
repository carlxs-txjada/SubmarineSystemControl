import os
import time
from math import sin, cos

import pygame as pg
from pygame.locals import *
from math import sqrt
import sys

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
seaLevel = 80
SubmarineImagePosYLim = 500
SubmarineImagePosYInit = seaLevel

submarineLeftLimit = 0
submarineRightLimit = 900

gravity = 9.8
density = 1000
volume = 1
ts = 0.05
constantB = 250

pushingForce = - (density * gravity * volume)


# isMissileEnabled = False



class Engine:
    strenght = 0
    horsepower = 0

    def __init__(self, horsepower, horizontalDirection):
        self.strenght = 0  # [-1, 0, 1]
        self.horsepower = horsepower
        self.horizontalDirection = horizontalDirection

    def createDefault(self):
        self.strenght = 0
        self.horizontalDirection = ''
        return Engine

    def stop(self):
        self.strenght = 0



    def moveLeftOrRight(self, horizontalDirection):
        self.horizontalDirection = horizontalDirection
        if horizontalDirection == 'right':
            self.strenght = 1
        elif horizontalDirection == 'left':
            self.strenght = -1
        elif horizontalDirection == "brake":
            self.strenght = self.strenght * 0.999

        return self.strenght

    def getStrenghtDirection(self):
        return self.moveLeftOrRight(self.horizontalDirection)


    def getHorsepower(self):
        return self.horsepower

    def getStrengt(self):
        return self.strenght

class Reservoir:

    def __init__(self, actualLevel, valveFlow, maxCapactity, fluitsoPump):
        self.actualLevel = actualLevel
        self.valveFlow = valveFlow
        self.maxCapactity = maxCapactity
        self.fluitsoPump = fluitsoPump
        # self.actual_level = actual_level

    def createDefault(self):
        self.actualLevel = 0
        self.valveFlow = 0
        self.maxCapactity = 0
        self.fluitsoPump = 0

        return Reservoir

    def pumpingAirWater(self, fluitsoPump):
        if fluitsoPump == 'air':
            if self.actualLevel > 0:
                self.actualLevel = self.actualLevel - self.valveFlow
            else:
                self.actualLevel = 0
        elif fluitsoPump == 'water':
            if self.actualLevel < self.maxCapactity:
                self.actualLevel = self.actualLevel + self.valveFlow
            else:
                self.actualLevel = self.maxCapactity
        elif fluitsoPump == 'brake':
            self.actualLevel = self.maxCapactity / 2

class Misille:
    def __init__(self, power, actualPos):
        self.power = power
        self.mass = 0.5
        self.volume = 0.1
        self.strenght = 0
        self.pushingForceX = self.power * cos(0.785398)
        self.pushingForceY = self.power * sin(0.785398)
        self.actualPosX = actualPos[0]
        self.actualPosY = actualPos[1]
        self.actualVelocityY = 0
        self.actualVelocityX = 0

    def calculateVelocityX(self):
        #self.actualVelocityX = (self.pushingForceX - constantB * self.actualVelocityX) * ts * self.strenght
        self.actualVelocityX = self.strenght * (self.pushingForceX - self.actualVelocityX) * ts

    def calculevelocityY(self):
        #self.actualVelocityY = (self.pushingForceY - constantB * self.actualVelocityY) * ts
        self.actualVelocityY = 1

    def calculePosition(self):
        self.calculePositionX()
        self.calculePositionY()

    def calculePositionY(self):
        self.actualPosY += self.actualVelocityY

    def calculePositionX(self):
        self.actualPosX += self.actualVelocityX
        """if self.actualPosX >= submarineRightLimit:
            self.actualPosX = submarineLeftLimit
        elif self.actualPosX <= submarineLeftLimit:
            self.actualPosX = submarineRightLimit"""

    def setCoords(self, coords):
        self.actualPosX = coords[0]
        self.actualPosY = coords[1]

    def isMissileCrashed(self):
        if self.actualPosY > SubmarineImagePosYLim:
            return True

class Submarine:

    def __init__(self, mass, actualVelocityY, actualVelocityX, posY, posX):
        self.posY = posY
        self.posX = posX
        self.mass = mass
        self.actualVelocityY = actualVelocityY
        self.actualVelocityX = actualVelocityX
        self.tank = Reservoir.createDefault(self)
        self.engine = Engine.createDefault(self)
        self.missile = Misille(10, [posX, posY])

    def createTank(self, tank):
        self.tank = tank

    def createEngine(self, engine):
        self.engine = engine

    def calculateMass(self):
        self.mass = self.tank.actualLevel

    def calculateVelocityY(self):
        self.actualVelocityY = ts * (
                (pushingForce / self.mass) + gravity - (
                (constantB * self.actualVelocityY) / self.mass)) + self.actualVelocityY

    def calculateVelocityX(self):
        self.actualVelocityX = ts * ((-constantB * self.actualVelocityX / self.mass) + (
                (self.engine.getHorsepower() * self.engine.getStrenghtDirection()) / self.mass)) + self.actualVelocityX

    def calculatePosition(self):
        Submarine.calculatePositionX(self)
        Submarine.calculatePositionY(self)

    def calculatePositionX(self):
        self.posX = self.posX + self.actualVelocityX
        if self.posX >= submarineRightLimit:
            self.posX = submarineLeftLimit
        elif self.posX <= submarineLeftLimit:
            self.posX = submarineRightLimit

    def calculatePositionY(self):
        self.posY = self.posY + self.actualVelocityY

        if self.posY > SubmarineImagePosYLim:
            self.posY = SubmarineImagePosYLim
        elif self.posY < seaLevel:
            self.posY = seaLevel

    def goToCursorCoords(self, coordX, coordY):
        if self.posX < coordX:
            self.engine.moveLeftOrRight('right')
        else:
            self.engine.moveLeftOrRight('left')
        self.calculateVelocityX()

        for _ in range(19):
            if self.posY > coordY:
                self.tank.pumpingAirWater('fullWater')
            else:
                self.tank.pumpingAirWater('fullAir')
            self.calculateVelocityY()
            self.calculatePosition()

        return self.getCoords()

    def getCoords(self):
        return [self.posX, self.posY]

    def shootMissile(self):
        self.missile.setCoords(self.getCoords())
        self.missile.strenght = self.engine.strenght

def main():
    isMissileEnabled = False
    transparency = 0

    pg.init()
    submarine1 = Submarine(2, 2, 0, 150, 50)
    submarine1.shootMissile()
    submarine1.createTank(Reservoir(1005, 2, 50000, 'air'))
    submarine1.createEngine(Engine(20, 'None'))

    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Submarine game")

    #BACKGROUND
    background_image = pg.image.load("mar.jpg").convert()
    # SUBMARINE
    submarine_sprites_folder = os.path.join("sprites", "submarine3")
    original_submarine_image = [
        pg.transform.scale(pg.image.load(os.path.join(submarine_sprites_folder, f"sub{i}.png")).convert_alpha(), (126, 98)) for i
        in range(12)]
    inverted_submarine_image = []
    for sprite in original_submarine_image:
        inverted_sprite = pg.transform.flip(sprite, True, False)
        inverted_submarine_image.append(inverted_sprite)
    submarineCurrentFrame = 0
    currentDirection = "right"
    # MISSILE
    missile_sprites_folder = os.path.join("sprites", "boom")
    missileImage = [
        pg.transform.scale(pg.image.load(os.path.join(missile_sprites_folder, f"b{i}.png")).convert_alpha(), (100,100)) for i
        in range(1, 13)]
    missileImage.insert(0, pg.transform.scale(pg.image.load(os.path.join(missile_sprites_folder, f"b0.png")), (50, 50)))
    isBoom = False
    missileCurrentFrame = 0
    #misileImage = pg.image.load("torpedo.png").convert_alpha()

    screen.blit(inverted_submarine_image[submarineCurrentFrame], (submarine1.posX, SubmarineImagePosYInit))
    screen.blit(missileImage[0], (200, 200))
    screen.blit(background_image, (0, 0))
    pg.display.flip()

    while True:
        submarine1.calculateVelocityY()
        submarine1.calculateVelocityX()
        submarine1.calculatePosition()

        if currentDirection == "left":
            submarine_image = original_submarine_image
        else:
            submarine_image = inverted_submarine_image

        isBoom = submarine1.missile.isMissileCrashed()
        if isMissileEnabled and not isBoom:
            missileCurrentFrame = 0
            missileImage[missileCurrentFrame].set_alpha(255)
            submarine1.missile.calculateVelocityX()
            submarine1.missile.calculevelocityY()
            submarine1.missile.calculePosition()
        elif submarine1.missile.isMissileCrashed():
            if missileCurrentFrame == 12:
                missileImage[missileCurrentFrame].set_alpha(0)
            else:
                missileCurrentFrame = int(time.time() * 8) % len(missileImage)
                submarine1.missile.actualVelocityY = 0
                submarine1.missile.actualVelocityX = 0
        else:
            missileImage[missileCurrentFrame].set_alpha(0)
            submarine1.missile.actualVelocityY = 0
            submarine1.missile.actualVelocityX = 0

        screen.blit(background_image, (0, 0))
        screen.blit(submarine_image[submarineCurrentFrame], (submarine1.posX, submarine1.posY))
        submarineCurrentFrame = int(time.time() * 30) % len(submarine_image)
        screen.blit(missileImage[missileCurrentFrame], (submarine1.missile.actualPosX, submarine1.missile.actualPosY))

        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            elif event.type == pg.KEYDOWN:
                if event.key == K_UP:
                    submarine1.tank.pumpingAirWater('air')

                elif event.key == K_DOWN:
                    submarine1.tank.pumpingAirWater('water')

                if event.key == K_LEFT:
                    currentDirection = "left"
                    submarine1.engine.strength = 0
                    submarine1.engine.moveLeftOrRight('left')

                elif event.key == K_RIGHT:
                    currentDirection = "right"
                    submarine1.engine.strength = 0
                    submarine1.engine.moveLeftOrRight("right")

                elif event.key == K_SPACE:  # Movimiento estático
                    submarine1.engine.moveLeftOrRight('brake')

                elif event.key == K_x:
                    isMissileEnabled = True
                    submarine1.shootMissile()
                    isBoom = False

        submarine1.calculateMass()


if __name__ == "__main__":
    main()
