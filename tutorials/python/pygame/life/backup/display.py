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

# for optimizing drawing:
from pygame import surfarray

def drawfield(screen,x,y,environment, plantcolor, herbcolor, carncolor, emptycolor, SCALE):
    for i in xrange(0,x-1):
        for j in xrange(0,y-1):
            type = environment[i][j].type
            if type == 'p':
                pos = [i,j]
                screen.set_at(pos, plantcolor)
            elif type == 'h':
                pos = [i,j]
                screen.set_at(pos, herbcolor)
            elif type == 'c':
                pos = [i,j]
                screen.set_at(pos, carncolor)
            elif type == 'e':
                pos = [i,j]
                screen.set_at(pos, emptycolor)

def drawfield_fast( screen, scale_surface, pixels ):
    surfarray.blit_array( scale_surface, pixels )
    temp = pygame.transform.scale(scale_surface, screen.get_size())
    screen.blit(temp, (0,0))


if __name__=='__main__':
    print 'PYTHON POPULATION SIMULATION ( Version',VERSION,')'
    WINSIZE = 640,480
    SCALE = 4
    ARRAYSIZE = WINSIZE[0]/SCALE, WINSIZE[1]/SCALE
    
    # Initialize the Pygame Engine!
    pygame.init()
    screen = pygame.display.set_mode(WINSIZE,0,8)
    scale_screen = pygame.surface.Surface( ARRAYSIZE,0,8 )
    pygame.display.set_caption('Python Population Model')
    white = 255,240,200
    black = 20,20, 40
    red = 255, 20, 40
    green = 20,255,40
    blue = 20,20,255
    screen.fill(black)
    scale_screen.fill(black)
    screen.set_palette( [black, red, green, blue, white] )
    scale_screen.set_palette( [black, red, green, blue, white] )
    
    # Initialize the model:
    # 2,3,1,0 correspond to palette colors set above (0=black, 1=red, etc)
    # the order of the Simulation constructor is: plant color, herbivore color, carnivore color, empty color
    model = Simulation(ARRAYSIZE[0],ARRAYSIZE[1],
                                          2,3,1,0,
                                          1000,1000,1000,
                                          2, # if ( age % 5 ) then the creature might die on this timestep
                                          3, # if ( age % 3 ) then you have to eat on this timestep or die
                                              # Currently eating isn't modeled...  so this does nothing.
                                          .11, # chance of death from natural causes ( .1 * creature age, max age is 10 years )
                                          .7, # chance a creature will reproduce (increases with age)
                                          )
    i = 0
    pop = 0
    timesteps = 365
    elapsedtime = 0.0
    drawtime = 0.0
    updatetime = 0.0
    totaltime=0.0
    fps = 0.0
    sumfps = 0.0
    avgfps = 0.0
    done = False
    while not done:
        # print 'timestep> ', i, '-',drawtime, '-',updatetime,'-',elapsedtime,model.numplants,model.numherbs,model.numcarns
        #print  i, '-',drawtime, '-',updatetime,'-',elapsedtime,'-',avgfps

        print i,'-',elapsedtime,'-',avgfps,'-',pop

        starttime = time.time()
        #drawfield(screen,100,100,model.environment,green,blue,red,black,SCALE)
        drawfield_fast( screen, scale_screen, model.pixel_data ) 
        endtime = time.time()
        drawtime = endtime - starttime
        starttime = time.time()
        pygame.display.update()
        endtime = time.time()
        updatetime = endtime - starttime
        starttime = time.time()
        model.timestep2()
        endtime = time.time()
        elapsedtime = endtime-starttime
        totaltime = (drawtime + updatetime + elapsedtime)
        sumfps += (1.0 / totaltime )
        i += 1    
        avgfps =  sumfps / i
        pop = model.numplants + model.numherbs + model.numcarns  
        
        # Handle someone closing the window or pressing escape
        events = pygame.event.get( )
        for e in events:
            if( e.type == QUIT ):
                done = True
                break
            elif (e.type == KEYDOWN):
                if( e.key == K_ESCAPE ):
                    done = True
                    break

    print "Exiting!"
