#################################################################
##  Population Simulation in Python
##  PYTHON POPULATION SIMULATOR v0.5
##
##  Simulation Engine Object
##  engine.py
##
##  "this object generates a field/universe for our creatures
##   and distributes them.  A call to a step method timesteps
##   the entire 'civilization' of creatures once.  Behaviors
##   are defined in an list or dictionary so that many Behaviors
##   can be applied without hardcoding each case.
##
##   Currently the model follows the following rules:
##   There are 3 types of creature
##    * Carrot Dudes - Plants
##    * Swahini Girls - Cute Fuzzy Herbivores
##    * Icecream Men - Psychopathic Carnivores
##   They Move and Act According to the following rules
##    * A timestep is a day and a year is 365 Timesteps
##    * Behaviours:
##      * Lifespan
##        * Creatures have no max lifespan
##        * Only odds of continuing to live which get worse as
##          Age increases.  Essentially a newborn has a chance of
##          dying.  In fact at the extremes of age the creature
##          should have the worst chances.  Possibly in 5 day/step
##          increments.
##        * Death checks every 5 to 10 steps.
##      * Movement & Nourishment & Mating
##        * Animals Move Every Cycle/Step
##        * Plants don't move, but they do reproduce every 5/10 Steps
##          * Reproduction Produces a plant on an adjacent coordinate.
##          * If the plant can't reproduce, it's surrounded, it will
##            exhibit  some other behaviour, as yet undisclosed...???
##        * Animals Must Eat Every 2/3 Days Or Die
##          * An Herbivore Eat's Plants (essentially killing and replacing
##            the plant on that section of the environement.
##          * An Herbivore cannot move onto a carnivore
##          * A Carnivore Eat's Herbivores But leaves Plants unharmed
##        * Animals of the same type that move onto each other will mate.
##          * The odd's of mating are good.  If the creatures mate,
##            One creature becomes marked as pregnent
##            and the new creature is born the next day if there is a square
##            adjacent to 'mom'
##            else:  the newborn dies due to overcrowding 
#################################################################

import sys
import random
import time

try:
    import Numeric
except ImportError:
    print 'Couldn\'t locate Numeric Python Module.'
    print 'which is required to run this application'

#Version Number
VERSION = 0.50

# The whole engine is a class:

# Coords = [UP, UP-RIGHT, RIGHT, etc] clockwise
COORDS = [(0,-1),(1,-1),(1,0),(0,1),(-1,1),(-1,0),(-1,-1)]

#  The basic creature type which is essential to the engine
class Creature:
    def __init__(self,type='e',x = -1,y = -1):
        self.type = type
        self.x = x
        self.y = y
        self.age = 0
        self.eaten = 0
        self.mated = 0
        self.pregnant = 0
        self.moved = 0
    def settype(self,type):
        self.type = type
    def setcoord(self, x, y):
        self.x = x
        self.y = y
    def ageday(self):
        self.age = self.age + 1
        if self.eaten>0:
            self.eaten = self.eaten - 1
        if self.mated>0:
            self.mated = self.mated - 1
        if self.pregnant>0:
            self.pregnant= self.pregnant - 1
        if self.moved:
            self.moved = 0
    def setmated(self,mated):
        if mated > 0:
            self.mated = mated
        else:
            print 'Invalid Value for \'mated\''
    def seteaten(self,eaten):
        if eaten > 0:
            self.eaten = eaten
        else:
            print 'Invalid Value for \'eaten\''
    def setpregnant(self,pregnant):
        if pregnant > 0:
            self.pregnant = pregnant
        else:
            print 'Invalid Value for \'pregnant\''
        
#  The Engine
class Simulation:
    def __init__(self,xdim=10, ydim=10,
                 # colors will all be real palette values
                 plantcolor=0, herbcolor=0,
                 carncolor=0, emptycolor=0,
                 numplants=10, numherbs=10,
                 numcarns=10,deathsteps=5,
                 eatsteps=3, MAXAGE=.1 ,
                 PLANTREPRODUCTION=.7 ):
        # The percentage chance of dying increases every deathsteps steps
        # and a creature is checked to see if they die every deathsteps steps
        # eatsteps is max number of days a creature can go without eating
        # Initialize and Store Simulation Variables
        self.xdim = xdim
        self.ydim = ydim
        self.xrange = range(0,self.xdim)
        self.yrange = range(0, self.ydim )
        self.range = range(0, self.xdim * self.ydim)
        self.plantcolor=plantcolor
        self.herbcolor=herbcolor
        self.carncolor=carncolor
        self.emptycolor=emptycolor
        self.numplants = numplants
        self.numherbs = numherbs
        self.numcarns = numcarns
        self.deathsteps = deathsteps
        self.eatsteps = eatsteps
        self.environment = None
        self.lut = None
        self.pixel_data = Numeric.zeros( (xdim,ydim), 'i' )
        self.init_environment()
        self.MAXAGE = MAXAGE
        self.PLANTREPRODUCTION = PLANTREPRODUCTION
        
    def init_environment(self):
        #Make environment a structure of empty/None type creature objects.
        #create = Creature()
        x = 0
        environment = []
        while x < self.xdim:
            env = []
            y = 0
            while y < self.ydim:
                env.append(Creature())
                y+=1
            environment.append(env)
            del env
            x+=1
        print "Created environment - Two Dim Array Of Creatures"

        environment = Numeric.array(environment,copy=1)

        print "Setting up pixel_data array:"
        for i in xrange(self.xdim):
            for j in xrange(self.ydim):
                try:
                    self.pixel_data[i][j] = self.emptycolor
                except IndexError:
                    print "Tried to set pixel_data[%s][%s]! (xdim=%s,ydim=%s)"%(i,j,self.xdim,self.ydim)
                except TypeError:
                    print "i=%s,j=%s,self.emptycolor=%s"%(i,j,self.emptycolor)

        print "Setting up Lookup Table:"
        self.lut = {}
                    
        print 'Setting up plants'
        i = 0 # self.numplants
        iterations = 0
        while i < self.numplants:
            x = self.randomx()
            y = self.randomy()
            if environment[x][y].type=='e':
               environment[x][y].settype('p')
               environment[x][y].setcoord(x,y)
               self.pixel_data[x][y] = self.plantcolor
               if( i % 100 == 0 ):
                   print i,"- (",x,",",y,")","- Created!"
               i+=1
               iterations += 1
               self.lut[(x,y)] = (x,y)
            else:
                # Duplicate location, something's already living here.
                # Try again!
                iterations += 1
                continue
        print "Plants setup in %s iterations."%(iterations)

        print 'Setting up Herbivores'
        i = 0 # self.numherbs
        iterations = 0
        while i < self.numherbs:
            x = self.randomx()
            y = self.randomy()
            if environment[x][y].type=='e':
                environment[x][y].settype('h')
                environment[x][y].eaten = 5
                environment[x][y].setcoord(x,y)
                self.pixel_data[x][y] = self.herbcolor
                if( i % 100 == 0 ):
                    print i,"- (",x,",",y,")","- Created!"
                i+=1
                iterations += 1
                self.lut[(x,y)] = (x,y)
            else:
                # try again
                iterations +=1
                continue
        print "Herbivores setup in %s iterations."%(iterations)

        print 'Setting up Carnivors'
        i = 0 # self.numcarns
        iterations = 0
        while i < self.numcarns:
            x = self.randomx()
            y = self.randomy()
            if environment[x][y].type=='e':
                environment[x][y].settype('c')
                environment[x][y].setcoord(x,y)
                self.pixel_data[x][y] = self.carncolor
                if( i % 100 == 0 ):
                    print i,"- (",x,",",y,")","- Created!"
                i+=1
                iterations += 1
                self.lut[(x,y)] = (x,y)
            else:
                # try again
                iterations += 1
                continue
        print "Carnivores setup in %s iterations."%(iterations)
        
        self.environment = environment # End of initenvironment 

    ### Determine random starting locations
    def randomx(self):
        x = random.randrange(0,self.xdim-1)
        return x
    def randomy(self):
        y = random.randrange(0,self.ydim-1)
        return y

    def timestep(self):
        #print 'timestep'
        # Set move options and call move
        for i in self.xrange:
            for j in self.yrange:
                item = self.environment[i][j]
                if item.type == 'p':
                    self.movePlant(item)
                if item.type == 'h':
                    self.moveHerbivore(item)
                if item.type == 'c':
                    self.moveCarnivore(item)
        return
    
    def timestep2(self):
        #print 'timestep'
        # Set move options and call move
        values = self.lut.values()
        moves = len(values)
        avgmove = 0.0
        startstep = time.time()
        for coords in values:
            item = self.environment[coords[0]][coords[1]]
            startmove = time.time()
            if item.type == 'p':
                self.movePlant(item)
            if item.type == 'h':
                self.moveHerbivore(item)
            if item.type == 'c':
                self.moveCarnivore(item)
            endmove = time.time()
            avgmove += (endmove - startmove)
        endstep = time.time()
        #print "timestep2: avgmove = %s, step = %s"%( avgmove/moves, endstep-startstep)
        return
    
    def movePlant(self,creature):
        # Creature is a plant, to move a plant
        # you check it's age and see if it reproduces
        if creature.age % self.deathsteps == 0:
            # This is one of those possible days
            # either die or reproduce or neither
            chance = random.random()
            # this statement implies a max age of 100
            # Because MAXAGE is currently .01
            percentdie = (self.MAXAGE * creature.age)
            # Calculate Plant Reproduction Percentage
            percentreproduce = self.PLANTREPRODUCTION * creature.age
            if chance < percentdie:
                # you die
                self.numplants-=1
                self.environment[creature.x][creature.y].type = 'e' # type equals empty -> dead!
                self.pixel_data[creature.x][creature.y] = self.emptycolor
                del self.lut[ (creature.x,creature.y) ] 
            elif chance < percentreproduce and creature.mated==0:
                # you (the plant) reproduce
                random.shuffle(COORDS)
                for item in COORDS:
                    x = creature.x + item[0]
                    y = creature.y + item[1]
                    if (x > self.xdim - 1) or (x < 0) or (y < 0) or (y > self.ydim - 1):
                        pass
                    elif self.environment[x][y].type=='e':
                        newplant = Creature('p',x,y)
                        self.environment[x][y]=newplant
                        self.pixel_data[x][y] = self.plantcolor
                        self.lut[(x,y)] = (x,y)
                        creature.mated = 3
                        self.numplants+=1
                        break
        creature.ageday()
        return
                    
    def moveHerbivore(self, creature):
        # Creature is a plant, to move a plant
        # you check it's age and see if it reproduces
        if creature.age % self.deathsteps == 0:
            # This is one of those possible days
            # either die or reproduce or neither
            chance = random.random()
            # this statement implies a max age of 100
            # Because MAXAGE is currently .01
            percentdie = (self.MAXAGE * creature.age)
            # Calculate Plant Reproduction Percentage
            percentreproduce = self.PLANTREPRODUCTION * creature.age
            if chance < percentdie:
                # you die
                self.numherbs-=1
                self.environment[creature.x][creature.y].type = 'e' # type equals empty -> dead!
                self.pixel_data[creature.x][creature.y] = self.emptycolor
                del self.lut[ (creature.x,creature.y) ] 
            elif chance < percentreproduce and creature.mated==0:
                # you (the herbivore) reproduce
                random.shuffle(COORDS)
                for item in COORDS:
                    x = creature.x + item[0]
                    y = creature.y + item[1]
                    if (x > self.xdim - 1) or (x < 0) or (y < 0) or (y > self.ydim - 1):
                        pass
                    elif self.environment[x][y].type=='e':
                        newherb = Creature('h',x,y)
                        self.environment[x][y]=newherb
                        self.pixel_data[x][y]= self.herbcolor
                        self.lut[(x,y)] = (x,y)
                        creature.mated = 3
                        self.numherbs+=1
                        break
        creature.ageday()
        return


    def moveCarnivore( self, creature ):
        # Creature is a plant, to move a plant
        # you check it's age and see if it reproduces
        if creature.age % self.deathsteps == 0:
            # This is one of those possible days
            # either die or reproduce or neither
            chance = random.random()
            # this statement implies a max age of 100
            # Because MAXAGE is currently .01
            percentdie = (self.MAXAGE * creature.age)
            # Calculate Plant Reproduction Percentage
            percentreproduce = self.PLANTREPRODUCTION * creature.age
            if chance < percentdie:
                # you die
                self.numcarns-=1
                self.environment[creature.x][creature.y].type = 'e' # type equals empty -> dead!
                self.pixel_data[creature.x][creature.y] = self.emptycolor
                del self.lut[ (creature.x,creature.y) ]
            elif chance < percentreproduce and creature.mated==0:
                # you (the carnivore) reproduce
                random.shuffle(COORDS)
                for item in COORDS:
                    x = creature.x + item[0]
                    y = creature.y + item[1]
                    if (x > self.xdim - 1) or (x < 0) or (y < 0) or (y > self.ydim - 1):
                        pass
                    elif self.environment[x][y].type=='e':
                        newcarn = Creature('c',x,y)
                        self.environment[x][y]=newcarn
                        self.pixel_data[x][y] = self.carncolor
                        self.lut[(x,y)] = (x,y)
                        creature.mated = 3
                        self.numcarns+=1
                        break
        creature.ageday()
        return
        

if __name__=='__main__':
    model = Simulation()
    print 'Simulation Initialized!'
##    i = 0
##    for list in model.environment:
##        for item in list:
##            print i,item.type
##            i+=1
    print 'Begin Timestepping!'
    i = 0
    if len(sys.argv) > 1:
        steps = sys.argv[1]
    else:
        steps = 365
    while i < steps:
        model.timestep()
        i+=1
    print 'Complete'
