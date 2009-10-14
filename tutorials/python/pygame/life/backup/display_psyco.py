######################################################################
##  PYTHON POPULATION SIMULATOR v0.00
##
##  Main Program And Display Functionality
##
##  Contains a script for initial configuration
##  and a Tk canvas widget custom built for displaying
##  the current environment of the engine object.
######################################################################

## IMPORTS
from engine import *
import time
import string

# PyGame Constants
import pygame
from pygame.locals import *
WINSIZE = [100,100]


# My Constants
SCALE = 1

## # initialize and prepare pygame
## def initpygame():
##     pygame.init()
##     screen = pygame.display.set_mode(WINSIZE)
##     pygame.display.set_caption('Python Population Model')
##     white = 255,240,200
##     black = 20,20, 40
##     red = 255, 20, 40
##     green = 20,255,40
##     yellow = 20, 200, 200
##     screen.fill(black)

# Draw the environment



def drawfield(screen,x,y,environment, plantcolor, herbcolor, carncolor, emptycolor):
    for i in xrange(0,x-1):
        for j in xrange(0,y-1):
            type = environment[i][j].type
            if type == 'p':
                pos = [i*SCALE,j*SCALE]
                screen.set_at(pos, plantcolor)
                pos = [i*SCALE+1,j*SCALE]
                screen.set_at(pos, plantcolor)
                pos = [i*SCALE,j*SCALE+1]
                screen.set_at(pos, plantcolor)
                pos = [i*SCALE+1,j*SCALE+1]
                screen.set_at(pos, plantcolor)
            elif type == 'h':
                pos = [i*SCALE,j*SCALE]
                screen.set_at(pos, herbcolor)
                pos = [i*SCALE+1,j*SCALE]
                screen.set_at(pos, herbcolor)
                pos = [i*SCALE,j*SCALE+1]
                screen.set_at(pos, herbcolor)
                pos = [i*SCALE+1,j*SCALE+1]
                screen.set_at(pos, herbcolor)
            elif type == 'c':
                pos = [i*SCALE,j*SCALE]
                screen.set_at(pos, carncolor)
                pos = [i*SCALE+1,j*SCALE]
                screen.set_at(pos, carncolor)
                pos = [i*SCALE,j*SCALE+1]
                screen.set_at(pos, carncolor)
                pos = [i*SCALE+1,j*SCALE+1]
                screen.set_at(pos, carncolor)
            elif type == 'e':
                pos = [i*SCALE,j*SCALE]
                screen.set_at(pos, emptycolor)
                pos = [i*SCALE+1,j*SCALE]
                screen.set_at(pos, emptycolor)
                pos = [i*SCALE,j*SCALE+1]
                screen.set_at(pos, emptycolor)
                pos = [i*SCALE+1,j*SCALE+1]
                screen.set_at(pos, emptycolor)

## Testing Out psyco!
## optimizing stuff that's already been included
import psyco
psyco.bind(drawfield)
psyco.bind(Simulation)


if __name__=='__main__':
    print 'PYTHON POPULATION SIMULATION ( Version',VERSION,')'
    model = Simulation(100,100,1000,1000,1000)
    i = 0
    timesteps = 365

    # Initialize the Pygame Engine!
    pygame.init()
    screen = pygame.display.set_mode(WINSIZE)
    pygame.display.set_caption('Python Population Model')
    white = 255,255,255
    black = 0,0, 0
    red = 255, 0, 0
    green = 0,255,0
    blue = 0,0,255
    screen.fill(black)

    t = 0.0
    elapsedtime = 0.0
    dtime = 0.0
    while 1:#i < timesteps:
        print 'timestep> ', i, '-',t, '-',dtime,'-',elapsedtime,model.numplants,model.numherbs,model.numcarns
        #output.display(model.environment)

        starttime = time.time()
        drawfield(screen,100,100,model.environment,green,blue,red,black)
        endtime = time.time()
        t = endtime - starttime
        starttime = time.time()
        pygame.display.update()
        endtime = time.time()
        dtime = endtime - starttime
        starttime = time.time()
        model.timestep()
        endtime = time.time()
        elapsedtime = endtime-starttime
        i = i + 1    
    raw_input('Press Enter To Exit')
