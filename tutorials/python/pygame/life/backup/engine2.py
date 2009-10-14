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

## IMPORTS
import random

try:
    import Numeric
except ImportError:
    print 'Couldn\'t locate Numeric Python Module.'
    print 'which is required to run this application'

#Version Number
VERSION = 0.50

# The whole engine is a class:

#  The basic creature type which is essential to the engine
class Creature:
    def __init__(self,type='e',x = -1,y = -1):
        self.type = type
        self.x = x
        self.y = y
        self.age = 0
        self.eaten = 0
        self.mated = 0
        self.pregnent = 0
        self.moved = 0
    def settype(self,type):
        self.type = type
    def setcoord(self, x, y):
        self.x = x
        self.y = y
    def ageday(self):
        self.age = self.age + 1
        if self.moved:
            self.moved = 0
            
    def move(self):
        """Let's Move This Creature on out!"""
        
        
        
    

        
#  The Engine
class Simulation:
    def __init__(self,xdim=10, ydim=10, numplants=10, numherbs=10,
                 numcarns=10,deathsteps=5, eatsteps=3, MAXAGE=.01,
                 PLANTREPRODUCTION=.03):
        # The percentage chance of dying increases every deathsteps steps
        # and a creature is checked to see if they die every deathsteps steps
        # eatsteps is max number of days a creature can go without eating
        # Initialize and Store Simulation Variables
        self.xdim = xdim
        self.ydim = ydim
        self.numplants = numplants
        self.numherbs = numherbs
        self.numcarns = numcarns
        self.deathsteps = deathsteps
        self.eatsteps = eatsteps
        self.environment = None
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

        print 'Setting up plants'
        i = 0 # self.numplants
        while i < self.numplants:
            x = self.randomx()
            y = self.randomy()
            if environment[x][y].type=='e':
               environment[x][y].settype('p')
               environment[x][y].setcoord(x,y)
               print i,"- (",x,",",y,")","- Created!"
            else:
               print i,"- (",x,",",y,")",environment[x][y].type    
               i+=1

        print 'Setting up Herbivores'
        i = 0 # self.numherbs
        while i < self.numherbs:
            x = self.randomx()
            y = self.randomy()
            if environment[x][y].type=='e':
                environment[x][y].settype('h')
                environment[x][y].eaten = 5
                environment[x][y].setcoord(x,y)
                print i,"- (",x,",",y,")","- Created!"
            else:
                print i,"- (",x,",",y,")",environment[x][y].type   
            i+=1

        print 'Setting up Carnivors'
        i = 0 # self.numcarns
        while i < self.numcarns:
            x = self.randomx()
            y = self.randomy()
            if environment[x][y].type=='e':
                environment[x][y].settype('c')
                environment[x][y].setcoord(x,y)
                print i,"- (",x,",",y,")","- Created!"
            else:
                dosomething = 0
                print i,"- (",x,",",y,")",environment[x][y].type         
            i+=1
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
        for i in xrange(0,self.xdim-1):
            for j in xrange(0,self.ydim-1):
                item = self.environment[i][j]
                if item.type != 'e':
                    self.move(item)

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
    if sys.argc > 1:
        steps = sys.argv[1]
    else:
        steps = 365
    while i < steps:
        model.timestep()
        i+=1
    print 'Complete'
