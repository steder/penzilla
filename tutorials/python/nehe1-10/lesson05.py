#!/usr/bin/env python
# pygame + PyOpenGL version of Nehe's OpenGL lesson05
# Paul Furber 2001 - m@verick.co.za

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

rtri = rquad = rdiamond = 0.0

def resize((width, height)):
    if height==0:
        height=1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0*width/height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init():
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

def clear():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);	

def drawTri():
    global rtri
    
    glLoadIdentity();					
    glTranslatef(-1.5,1.0,-6.0)

    glRotatef(rtri,0.0,1.0,0.0)			

    glBegin(GL_TRIANGLES)				

    glColor3f(1.0,0.0,0.0)
    glVertex3f( 0.0, 1.0, 0.0)		
    glColor3f(0.0,1.0,0.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glColor3f(0.0,0.0,1.0)	
    glVertex3f( 1.0,-1.0, 1.0)
    
    glColor3f(1.0,0.0,0.0)	
    glVertex3f( 0.0, 1.0, 0.0)
    glColor3f(0.0,0.0,1.0)	
    glVertex3f( 1.0,-1.0, 1.0)
    glColor3f(0.0,1.0,0.0)	
    glVertex3f( 1.0,-1.0, -1.0)

    glColor3f(1.0,0.0,0.0)	
    glVertex3f( 0.0, 1.0, 0.0)
    glColor3f(0.0,1.0,0.0)	
    glVertex3f( 1.0,-1.0, -1.0)
    glColor3f(0.0,0.0,1.0)	
    glVertex3f(-1.0,-1.0, -1.0)
			
    glColor3f(1.0,0.0,0.0)	
    glVertex3f( 0.0, 1.0, 0.0)
    glColor3f(0.0,0.0,1.0)	
    glVertex3f(-1.0,-1.0,-1.0)
    glColor3f(0.0,1.0,0.0)	
    glVertex3f(-1.0,-1.0, 1.0)
    glEnd()
    rtri  = rtri + 0.2
    
def drawSquare():
    global rquad
    glLoadIdentity()
    glTranslatef(1.5,1.0,-7.0)
    glRotatef(rquad,1.0,1.0,1.0)
    glBegin(GL_QUADS)	

    glColor3f(0.0,1.0,0.0)
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)		
    glVertex3f(-1.0, 1.0, 1.0)		
    glVertex3f( 1.0, 1.0, 1.0)		

    glColor3f(1.0,0.5,0.0)	
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)		
    glVertex3f(-1.0,-1.0,-1.0)		
    glVertex3f( 1.0,-1.0,-1.0)		

    glColor3f(1.0,0.0,0.0)		
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)		
    glVertex3f(-1.0,-1.0, 1.0)		
    glVertex3f( 1.0,-1.0, 1.0)		

    glColor3f(1.0,1.0,0.0)	
    glVertex3f( 1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)		
    glVertex3f( 1.0, 1.0,-1.0)		

    glColor3f(0.0,0.0,1.0)	
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0,-1.0)		
    glVertex3f(-1.0,-1.0,-1.0)		
    glVertex3f(-1.0,-1.0, 1.0)		

    glColor3f(1.0,0.0,1.0)	
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)		
    glVertex3f( 1.0,-1.0,-1.0)	
    glEnd()	              
    rquad = rquad - 0.15             
    
def drawDiamond():
    global rdiamond
    glLoadIdentity()
    glTranslatef(1.0,1.0,-7.0)
    glRotatef(rdiamond,1.0,1.0,1.0)
    glBegin(GL_TRIANGLES)	

    # Front face.
    glColor3f(1.0,1.0,1.0)
    glVertex3f(0.0,1.0,0.0) #top point
    glColor3f(1.0,1.0,1.0)
    glVertex3f(-1.0,0.0,1.0)
    glColor3f(1.0,1.0,1.0)
    glVertex3f(1.0,0.0,1.0)
    glColor3f(0.0,0.0,1.0)
    glVertex3f(0.0,-1.0,0.0) #Bottom point
    glColor3f(0.0,0.0,1.0)
    glVertex3f(-1.0,0.0,1.0)
    glColor3f(0.0,0.0,1.0)
    glVertex3f(1.0,0.0,1.0)
    # Back Face
    glColor3f(0.0,0.0,1.0)
    glVertex3f(0.0,1.0,0.0) #top point
    glColor3f(0.0,0.0,1.0)
    glVertex3f(-1.0,0.0,-1.0)
    glColor3f(0.0,0.0,1.0)
    glVertex3f(1.0,0.0,-1.0)
    glColor3f(1.0,1.0,1.0)
    glVertex3f(0.0,-1.0,0.0) #Bottom point
    glColor3f(1.0,1.0,1.0)
    glVertex3f(-1.0,0.0,-1.0)
    glColor3f(1.0,1.0,1.0)
    glVertex3f(1.0,0.0,-1.0)

    # Side 1 - Vertexs only change in x and z directions
    glColor3f(0.0,0.0,1.0)
    glVertex3f(0.0,1.0,0.0) # top is always the same.
    glVertex3f(-1.0,0.0,-1.0)
    glVertex3f(-1.0,0.0,1.0)
    glColor3f(0.0,0.0,1.0)
    glVertex3f(0.0,1.0,0.0) # Bottom is always the same.
    glVertex3f(1.0,0.0,-1.0)
    glVertex3f(1.0,0.0,1.0)
    glEnd()
    rdiamond -= 0.15

def drawCircle(): # Diamonds suck, let's draw a circle.
    """
    """
    return

def main():
    video_flags = OPENGL|DOUBLEBUF
    
    pygame.init()
    pygame.display.set_mode((640,480), video_flags)

    resize((640,480))
    init()

    frames = 0
    ticks = pygame.time.get_ticks()
    while 1:
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break
        clear()
        drawTri()
        drawSquare()
        drawDiamond()
        pygame.display.flip()
        frames = frames+1

    print "fps:  %d" % ((frames*1000)/(pygame.time.get_ticks()-ticks))


if __name__ == '__main__': main()

