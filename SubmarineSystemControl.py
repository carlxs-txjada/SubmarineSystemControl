import os
import time
from math import sin, cos
import pygame as pg
from pygame.locals import *
import sys
import matplotlib.pyplot as plt
import numpy as np

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
seaLevel = 50
SubmarineImagePosYLim = 500
SubmarineImagePosYInit = seaLevel

submarineLeftLimit = 0
submarineRightLimit = 900

gravity = 9.8
density = 1000
volume = 1
ts = 0.01
constantB = 250

pushingForce = - (density * gravity * volume)


class RemoteControl:
    isActived = False
    cursorX = 0
    cursorY = 0

    def setCursorCoords(self, coordX, coordY):
        self.cursorX = coordX
        self.cursorY = coordY

    def startRemoteControl(self, coordX, coordY):
        self.isActived = True
        self.setCursorCoords(coordX, coordY)

    def stopRemoteControl(self):
        self.isActived = False


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


class Misille:
    def __init__(self, power, actualPos):
        self.power = power
        self.mass = 0.1
        self.volume = 0.1
        self.strenght = 0
        self.pushingForceX = self.power * cos(0)
        self.pushingForceY = self.power * sin(0) * (density * gravity * self.volume)
        self.actualPosX = actualPos[0]
        self.actualPosY = actualPos[1]
        self.actualVelocityY = 0
        self.actualVelocityX = 0
        self.constantC = constantB / 15

    def calculateVelocityX(self):
        self.actualVelocityX = self.strenght * ((
                    self.pushingForceX - self.constantC * abs(self.actualVelocityX)) * ts / self.mass +
                                                abs(self.actualVelocityX))

    def calculevelocityY(self):
        self.actualVelocityY = ((gravity * self.mass + self.pushingForceY - self.constantC * abs(self.actualVelocityY))
                                * ts / self.mass + self.actualVelocityY)

    def calculePosition(self):
        self.calculePositionX()
        self.calculePositionY()

    def calculePositionY(self):
        self.actualPosY += self.actualVelocityY

    def calculePositionX(self):
        self.actualPosX += self.actualVelocityX

    def setCoords(self, coords):
        self.actualPosX = coords[0] + 50
        self.actualPosY = coords[1] + 50

    def isMissileCrashed(self):
        if self.actualPosY > SubmarineImagePosYLim:
            return True
        elif self.actualPosX < submarineLeftLimit or self.actualPosX > submarineRightLimit:
            return True


class Reservoir:
    def __init__(self, actualLevel, valveFlow, maxCapactity, fluitsToPump):
        self.actualLevel = actualLevel
        self.valveFlow = valveFlow
        self.maxCapactity = maxCapactity
        self.fluisToPump = fluitsToPump
        self.actual_level = actualLevel

    def createDefault(self):
        self.actualLevel = 0
        self.valveFlow = 0
        self.maxCapactity = 0
        self.fluitsToPump = 0

        return Reservoir

    def pumpingAirWater(self, fluitsToPump):
        if fluitsToPump == 'air':
            if self.actualLevel > 0:
                self.actualLevel = self.actualLevel - self.valveFlow
            else:
                self.actualLevel = 0
        elif fluitsToPump == 'water':
            if self.actualLevel < self.maxCapactity:
                self.actualLevel = self.actualLevel + self.valveFlow
            else:
                self.actualLevel = self.maxCapactity
        elif fluitsToPump == 'brake':
            self.actualLevel = 1000
        elif fluitsToPump == 'up':
            self.actualLevel = 998
        elif fluitsToPump == 'down':
            self.actualLevel = 1002


class Submarine:
    def __init__(self, mass, actualVelocityY, actualVelocityX, posY, posX):
        self.posY = posY
        self.posX = posX
        self.mass = mass
        self.actualVelocityY = actualVelocityY
        self.actualVelocityX = actualVelocityX
        self.tank = Reservoir(0, 2, 5000, 'air')
        self.engine = Engine.createDefault(self)
        self.missile = Misille(10, [posX, posY])
        self.remoteControl = RemoteControl()

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

    def getCoords(self):
        return [self.posX, self.posY]

    def shootMissile(self):
        self.missile.setCoords(self.getCoords())
        self.missile.strenght = self.engine.strenght


def main():
    isMissileEnabled = False

    pg.init()
    submarine1 = Submarine(2, 0, 0, 150, 50)
    submarine1.shootMissile()
    submarine1.createTank(Reservoir(1000, 2, 5250, 'air'))
    submarine1.createEngine(Engine(20, 'None'))

    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Submarine game")

    # BACKGROUND
    background_image = pg.image.load("mar.jpg").convert()
    # SUBMARINE
    submarine_sprites_folder = os.path.join("sprites", "submarine3")
    original_submarine_image = [
        pg.transform.scale(pg.image.load(os.path.join(submarine_sprites_folder, f"sub{i}.png")).convert_alpha(),
                           (126, 98)) for i
        in range(12)]
    inverted_submarine_image = []
    for sprite in original_submarine_image:
        inverted_sprite = pg.transform.flip(sprite, True, False)
        inverted_submarine_image.append(inverted_sprite)
    submarineCurrentFrame = 0
    currentDirection = "right"
    # MISSILE
    missile_sprites_folder = os.path.join("sprites", "boom")
    originalMissileImage = [
        pg.transform.scale(pg.image.load(os.path.join(missile_sprites_folder, f"b{i}.png")).convert_alpha(), (100, 100))
        for i
        in range(1, 13)]
    originalMissileImage.insert(0, pg.transform.scale(pg.image.load(os.path.join(missile_sprites_folder, f"b0.png")),
                                                      (50, 50)))
    invertedMissileImage = []
    for sprite in originalMissileImage:
        inverted_sprite = pg.transform.flip(sprite, True, False)
        invertedMissileImage.append(inverted_sprite)
    missileCurrentFrame = 0
    isBoom = False

    screen.blit(inverted_submarine_image[submarineCurrentFrame], (submarine1.posX, SubmarineImagePosYInit))
    screen.blit(originalMissileImage[0], (200, 200))
    screen.blit(background_image, (0, 0))
    pg.display.flip()
    whileCounter = 0

    isOnRemoteControl = False

    submarinePotitionToPrint = []

    while True:
        submarine1.calculateVelocityY()
        submarine1.calculateVelocityX()
        submarine1.calculatePosition()

        if isOnRemoteControl:
            if submarine1.remoteControl.cursorX - 160 > submarine1.posX:
                submarine1.engine.moveLeftOrRight('right')
                submarine1.engine.moveLeftOrRight('brake')
            elif submarine1.remoteControl.cursorX - 160 > submarine1.posX:
                submarine1.engine.moveLeftOrRight('left')
                submarine1.engine.moveLeftOrRight('brake')
            if abs(submarine1.remoteControl.cursorY - submarine1.posY) == 0:
                isOnRemoteControl = False
                submarine1.remoteControl.stopRemoteControl()
            elif abs(submarine1.remoteControl.cursorY - submarine1.posY) < 15:
                submarine1.tank.pumpingAirWater('breake')
            elif submarine1.remoteControl.cursorY > submarine1.posY:
                submarine1.tank.pumpingAirWater('down')
            elif submarine1.remoteControl.cursorY < submarine1.posY:
                submarine1.tank.pumpingAirWater('up')

        if currentDirection == "left":
            submarine_image = original_submarine_image
            missileImage = invertedMissileImage
        else:
            submarine_image = inverted_submarine_image
            missileImage = originalMissileImage

        isBoom = submarine1.missile.isMissileCrashed()
        # pg.draw.circle(background_image, (255, 0, 0), (submarine1.missile.actualPosX,
        # submarine1.missile.actualPosY), 1)
        if isMissileEnabled and not isBoom:
            missileCurrentFrame = 0
            missileImage[missileCurrentFrame].set_alpha(255)
            submarine1.missile.calculevelocityY()
            submarine1.missile.calculePosition()
            submarine1.missile.actualPosX += submarine1.missile.strenght * 0.08
            if whileCounter > 500:
                submarine1.missile.calculateVelocityX()
                submarine1.missile.calculevelocityY()
                submarine1.missile.calculePosition()
                submarine1.missile.pushingForceY = (submarine1.missile.power *
                                                    sin(0) * (density * gravity * submarine1.missile.volume))
            else:
                submarine1.missile.calculePositionY()
                submarine1.missile.calculePositionX()
            whileCounter += 1

        elif submarine1.missile.isMissileCrashed():
            if missileCurrentFrame == 12:
                missileImage[missileCurrentFrame].set_alpha(0)
            else:
                missileCurrentFrame = int(time.time() * 8) % len(originalMissileImage)
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

        submarinePotitionToPrint.append(submarine1.posY)

        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                plt.plot(range(len(submarinePotitionToPrint)), submarinePotitionToPrint)
                plt.xlabel('T')
                plt.ylabel('Y')
                plt.title('y vs t')
                plt.show()
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

                elif event.key == K_SPACE:  # Movimiento estático x
                    submarine1.engine.moveLeftOrRight('brake')

                elif event.key == K_x:
                    isMissileEnabled = True
                    whileCounter = 0
                    submarine1.shootMissile()
                    isBoom = False

            if event.type == pg.MOUSEBUTTONDOWN:
                coords = pg.mouse.get_pos()
                submarine1.remoteControl.startRemoteControl(coords[0], coords[1])
                isOnRemoteControl = True

        submarine1.calculateMass()


if __name__ == "__main__":
    main()
