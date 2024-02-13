import pygame
from pygame.locals import *
import sys

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
sea_level = 80
submarine_image_pos_x = 500
submarine_image_pos_yLim = 500
submarine_image_pos_y_init = sea_level

g = 9.8
p = 1000
v = 1
dt = 1
b = 250

e = - (p * g * v)

class Reservoir:

   def __init__(self, actual_level, valve_flow, max_capacity, fluid_to_pump):
       self.actual_level = actual_level
       self.valve_flow = valve_flow
       self.max_capacity = max_capacity
       self.fluid_to_pump = fluid_to_pump


   def pumping_air_water(self, fluid_to_pump):
       if fluid_to_pump == 'air':
           if self.actual_level > 0:
               self.actual_level = self.actual_level - self.valve_flow
           else:
               self.actual_level = 0

       if fluid_to_pump == 'water':
           if self.actual_level < self.max_capacity:
               self.actual_level = self.actual_level + self.valve_flow
           else:
               self.actual_level = self.max_capacity

    #def turn_on_turbine(self, direction):


class Submarine:

   def __init__(self, tank, mass, actual_velocity, pos_y):
       self.pos_y = pos_y
       self.mass = mass
       self.actual_velocity = actual_velocity
       self.tank = tank


   def calculate_mass(self):
       self.mass = self.tank.actual_level

   def calculate_velocity_y(self):
       self.actual_velocity = dt * ((e / self.mass) + g - ((b * self.actual_velocity) / self.mass)) + self.actual_velocity
       self.actual_velocity = dt * ((e / self.mass) + g - ((b * self.actual_velocity) / self.mass)) + self.actual_velocity

   def calculate_velocity_x(self):
        pass

   def calculate_position(self):
       self.pos_y = self.pos_y + self.actual_velocity

       if self.pos_y > submarine_image_pos_yLim:
           self.pos_y = submarine_image_pos_yLim
       if  self.pos_y < sea_level:
           self.pos_y = sea_level

       return self.pos_y


def main():
   pygame.init()
   tank1 = Reservoir(1005, 2, 50000, 'air')

   submarine1 = Submarine(tank1, 2, 2,150)
   screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

   pygame.display.set_caption("Submarine game")

   background_image = pygame.image.load("mar.jpg").convert()
   submarine_image = pygame.image.load("sub.jpg").convert_alpha()

   screen.blit(submarine_image, (submarine_image_pos_x, submarine_image_pos_y_init))
   screen.blit(background_image, (0, 0))
   pygame.display.flip()

   while True:
       submarine1.calculate_velocity_y()
       submarine1.calculate_position()
       print(submarine1.actual_velocity)

       screen.blit(background_image, (0, 0))
       screen.blit(submarine_image, (submarine_image_pos_x, submarine1.pos_y))

       pygame.display.flip()

       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               sys.exit()

           elif event.type == pygame.KEYDOWN:
               if event.key == K_UP:
                   tank1.pumping_air_water('air')
               elif event.key == K_DOWN:
                   tank1.pumping_air_water('water')

       submarine1.calculate_mass()


if __name__ == "__main__":
   main()
