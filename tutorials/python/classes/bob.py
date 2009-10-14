"""
Bob.py
Defines the Bob class and methods.  Bob is a simple model of a creature.
Bob might be a good basis for a Sprite class in a simple game, or
it might make a decent AI entity.
"""

"""
class Blob
Blobs are the basic lifeform on this planet.  They don't do much.
"""
class Blob:
    """
    """
    # Variables that are shared between all Blob objects
    POP = 0 # Population of the Blob Species
    TINY = 1
    MEDIUM = 2
    LARGE = 3
    """
    __init__(self):
    Create a new Bob object.  Initialize various data variables.
    """
    def __init__(self):
        self.AGE = 0
        self.SIZE = TINY

    def tick(self):
        self.AGE += 1
        if self.AGE % 3 == 0:
            self.SIZE += 1
        if self.SIZE == 3:
            return self.divide()
        else:
            return None

"""
Bob's hunt and eat blobs.  Using Bob's and Blob's we can create a simple ecosytem.  The Bob class can hunt, eat, die, multiply, and drink Eggnog.
"""
class Bob(Blob):
    def __init__(self):
        self.TASK = "Nothing"

    def tick(self):
        self.AGE += 1
        if self.AGE % 10 == 0:
            self.SIZE +=1
        if self.SIZE == 3:
            self.die()
        else:
            return None
        
