class BaseClass:
    # This data will exist in all
    # BaseClasses (even uninstantiated ones)
    Name = "BaseClass"
    # __init__ is a class constructor
    # __****__ is usually a special class method.
    def __init__(self, arg1, arg2):
        # These values are created
        # when the class is instantiated.
        self.value1 = arg1
        self.value2 = arg2

    # Self is used as an argument to
    # pretty much all class functions.
    # However, you do NOT need to pass
    # the argument self if you call this method
    # from a Class, because the class provides
    # the value of itself.
    def display(self):
        print self.Name
        print self.value1
        print self.value2

        
