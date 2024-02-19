import pygame as pg
from pygame.locals import *
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
ts = 1
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

    def brake(self):
        pass

    def moveLeftOrRight(self, horizontalDirection):
        if horizontalDirection == 'right':
            self.strenght = 1
        elif horizontalDirection == 'left':
            self.strenght = -1

    def brake(self):
        self.strenght = 0

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

        if fluitsoPump == 'water':
            if self.actualLevel < self.maxCapactity:
                self.actualLevel = self.actualLevel + self.valveFlow
            else:
                self.actualLevel = self.maxCapactity


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
            (self.engine.horsepower * self.engine.strenght) / self.mass)) + self.actualVelocityY

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
        if self.posY < seaLevel:
            self.posY = seaLevel


def main():
    pg.init()
    submarine1 = Submarine(2, 2, 0, 150, 50)
    submarine1.createTank(Reservoir(1005, 2, 50000, 'air'))
    submarine1.createEngine(Engine(150, 'None'))

    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pg.display.set_caption("Submarine game")

    background_image = pg.image.load("mar.jpg").convert()
    submarine_image = pg.image.load("sub.jpg").convert_alpha()

    screen.blit(submarine_image, (submarine1.posX, SubmarineImagePosYInit))
    screen.blit(background_image, (0, 0))
    pg.display.flip()

    while True:
        submarine1.calculateVelocityY()
        submarine1.calculatePosition()
        print(submarine1.actualVelocityY)

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
                    submarine1.calculateVelocityX()
                    submarine1.engine.moveLeftOrRight('left')
                elif event.key == K_RIGHT:
                    submarine1.calculateVelocityX()
                    submarine1.engine.moveLeftOrRight("right")
                elif event.key is not K_LEFT or event.key is not K_RIGHT:
                    submarine1.calculateVelocityX()
                    submarine1.engine.brake()

                # Movimiento estático
                if event.key == K_SPACE:
                    pass

                # Movimiento teledirigido
                # $pygame.mouse.get_pos()

        submarine1.calculateMass()


if __name__ == "__main__":
    main()
