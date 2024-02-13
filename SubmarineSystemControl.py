import pygame
from pygame.locals import *
import sys

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
seaLevel = 80
SubmarineImagePosYLim = 500
SubmarineImagePosYInit = seaLevel

gravity = 9.8
density = 1000
volume = 1
ts = 1
constantB = 250

pushingForce = - (density * gravity * volume)

class Engine:
    def __init__(self, strenght, horizontalDirection):
        self.strenght = strenght
        self.horizontalDirection = horizontalDirection

        def getStrength(self):
            return self.strenght

        def moveLeftRight(self, horizontalDirection):
            if horizontalDirection == 'right':
                pass
            elif horizontalDirection == 'left':
                pass

class Reservoir:

    def __init__(self, actualLevel, valveFlow, maxCapactity, fluitsoPump):
        self.actualLevel = actualLevel
        self.valveFlow = valveFlow
        self.maxCapactity = maxCapactity
        self.fluitsoPump = fluitsoPump

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

    # def turn_on_turbine(self, direction):


class Submarine:

    def __init__(self, tank, mass, actualVelocityY, actualVelocityX, posY, posX, engine):
        self.posY = posY
        self.posX = posX
        self.mass = mass
        self.actualVelocityY = actualVelocityY
        self.actualVelocityX = actualVelocityX
        self.tank = tank
        self.engine = engine

    def calculateMass(self):
        self.mass = self.tank.actualLevel

    def calculateVelocityY(self):
        self.actualVelocityY = ts * (
                (pushingForce / self.mass) + gravity - (
                    (constantB * self.actualVelocityY) / self.mass)) + self.actualVelocityY

    def calculateVelocityX(self):
        self.actualVelocityX = ts * ((-constantB * self.actualVelocityX / self.mass) + (
                    self.engine / self.mass)) + self.actualVelocityY

    def calculatePosition(self):
        self.posY = self.posY + self.actualVelocityY

        if self.posY > SubmarineImagePosYLim:
            self.posY = SubmarineImagePosYLim
        if self.posY < seaLevel:
            self.posY = seaLevel

        return self.posY


def main():
    pygame.init()
    tank1 = Reservoir(1005, 2, 50000, 'air')
    engine1 = Engine(1000, 'None')

    submarine1 = Submarine(tank1, 2, 2, 0, 150, 50, engine1)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.display.set_caption("Submarine game")

    background_image = pygame.image.load("mar.jpg").convert()
    submarine_image = pygame.image.load("sub.jpg").convert_alpha()

    screen.blit(submarine_image, (submarine1.posX, SubmarineImagePosYInit))
    screen.blit(background_image, (0, 0))
    pygame.display.flip()

    while True:
        submarine1.calculateVelocityY()
        submarine1.calculatePosition()
        print(submarine1.actualVelocityY)

        screen.blit(background_image, (0, 0))
        screen.blit(submarine_image, (submarine1.posX, submarine1.posY))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    tank1.pumpingAirWater('air')
                elif event.key == K_DOWN:
                    tank1.pumpingAirWater('water')
                if event.key == K_LEFT:
                    tank1.pumpingAirWater('')

        submarine1.calculateMass()


if __name__ == "__main__":
    main()
