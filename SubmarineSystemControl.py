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
submarineRightLimit = 700

gravity = 9.8
density = 1000
volume = 1
ts = 0.05
constantB = 250

pushingForce = - (density * gravity * volume)


class Engine:
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


class Reservoir:

    def __init__(self, actualLevel, valveFlow, maxCapactity, fluitsoPump):
        self.actualLevel = actualLevel
        self.valveFlow = valveFlow
        self.maxCapactity = maxCapactity
        self.fluitsoPump = fluitsoPump

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
        elif fluitsoPump == 'fullAir':
            self.actualLevel = 0
        elif fluitsoPump == 'fullWater':
            self.fluitsoPump = self.maxCapactity



class Submarine:

    def __init__(self, mass, actualVelocityY, actualVelocityX, posY, posX):
        self.posY = posY
        self.posX = posX
        self.mass = mass
        self.actualVelocityY = actualVelocityY
        self.actualVelocityX = actualVelocityX
        self.tank = Reservoir.createDefault(self)
        self.engine = Engine.createDefault(self)

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
                (self.engine.horsepower * self.engine.getStrenghtDirection()) / self.mass)) + self.actualVelocityX

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
            # self.tank.pumpingAirWater('air')

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

def main():
    pg.init()
    submarine1 = Submarine(2, 2, 0, 150, 50)
    submarine1.createTank(Reservoir(1005, 2, 50000, 'air'))
    submarine1.createEngine(Engine(20, 'None'))

    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pg.display.set_caption("Submarine game")

    background_image = pg.image.load("mar.jpg").convert()
    submarine_image = pg.image.load("sub.jpg").convert_alpha()
    #torpedo_image = pg.image.load("torpedo.png").convert_alpha()

    screen.blit(submarine_image, (submarine1.posX, SubmarineImagePosYInit))
    screen.blit(background_image, (0, 0))
    pg.display.flip()

    while True:
        submarine1.calculateVelocityY()
        submarine1.calculateVelocityX()
        submarine1.calculatePosition()
        # print(submarine1.actualVelocityX)
        # print(pg.mouse.)

        screen.blit(background_image, (0, 0))
        screen.blit(submarine_image, (submarine1.posX, submarine1.posY))

        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            elif event.type == pg.KEYDOWN:
                # Movimiento vertical
                if event.key == K_UP:
                    submarine1.tank.pumpingAirWater('air')
                elif event.key == K_DOWN:
                    submarine1.tank.pumpingAirWater('water')

                # Movimiento horizontal
                if event.key == K_LEFT:
                    submarine1.engine.strength = 0
                    # submarine1.calculateVelocityX()
                    submarine1.engine.moveLeftOrRight('left')
                elif event.key == K_RIGHT:
                    # submarine1.calculateVelocityX()
                    submarine1.engine.strength = 0
                    submarine1.engine.moveLeftOrRight("right")
                # Movimiento estático
                elif event.key == K_SPACE:
                    submarine1.engine.moveLeftOrRight('brake')
                elif event.key == K_x:
                    submarine1.actualVelocityY = 0
            # Movimiento teledirigido
            if event.type == pg.MOUSEBUTTONDOWN:
                coords = pg.mouse.get_pos()
                submarineCoords = submarine1.getCoords()
                submarine1.actualVelocityY = 0
                while (int(sqrt(coords[0])) != int(sqrt(submarineCoords[0]))) or (
                        int(sqrt(coords[1])) != int(sqrt(submarineCoords[1]))):
                    submarineCoords = submarine1.goToCursorCoords(coords[0], coords[1])

                    screen.blit(background_image, (0, 0))
                    screen.blit(submarine_image, (submarine1.posX, submarine1.posY))

                    pg.display.flip()

                # $pygame.mouse.get_pos()

        submarine1.calculateMass()


if __name__ == "__main__":
    main()
