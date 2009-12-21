import pygame
from pygame.locals import *

class Box:
    def __init__(self, screen, size, velocities, background, boxcolor):
        self.screen = screen
        screensize = self.screen.get_size()
        self.screenwidth = screensize[0]
        self.screenheight = screensize[1]
        # Position of Box on the Screen
        # Box will start roughly in the middle of the screen.
        self.x = screensize[0]/2
        self.y = screensize[1]/2
        self.width = size[0]
        self.height = size[1]
        # Velocity of the box
        self.vx = velocities[0]
        self.vy = velocities[1]
        self.bgcolor = background
        self.boxcolor = boxcolor
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        # Erase the previous box
        pygame.draw.rect( self.screen, self.bgcolor, self.rect )
        # Update position or reverse direction
        # Check for collision with the sides:
        nx, ny = self.x + self.vx, self.y + self.vy
        bound_x = nx + self.width
        bound_y = ny + self.height
        if( (bound_x >= self.screenwidth) or
             (nx <= 0) ):
            self.vx *= -1 * 0.9 # Bounces decrease velocity slightly
        else:
            self.x = nx
        if( (bound_y >= self.screenheight) or
             (ny <= 0 ) ):
            self.vy *= -1 * 0.9
        else:
            self.y = ny
        # Draw the new box
        self.rect = pygame.rect.Rect(nx, ny, self.width, self.height)
        pygame.draw.rect( self.screen, self.boxcolor, self.rect )
        
        
    def setV(self,x,y):
        self.vx = x
        self.vy = y

    def setBackgroundColor(self, color):
        self.bgcolor=color
    def setBoxColor(self, color):
        self.boxcolor=color
