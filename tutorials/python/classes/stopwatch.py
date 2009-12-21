"""
Stopwatch.py:
Define a stopwatch object that can be used to time blocks of code
in a reasonably intuitive way.  (Like a stopwatch :~))
"""
import time
class Stopwatch:
    """
    Stopwatch(self, name='Stopwatch')
    """
    def __init__(self, name="Stopwatch"):
        self.name = name
        self.stopped = 1
        self.init()
        
    def init(self):
        self.starttime = 0.0
        self.stoptime = 0.0
        self.elapsedtime = 0.0
        self.hours, self.mins, self.secs, self.hundredths = 0.0,0.0,0.0,0.0

    def __add__(self, time):
        if type(time) == type(self):
            self.elapsedtime += time.elapsedtime
        elif type(time)==type(self.elapsedtime):
            self.elapsedtime += time
        else:
            raise TypeError
        return self

    def __radd__(self, time):
        return __add__(self, time)
        
    def __cmp__(self):
        return self.__len__()

    def __len__(self):
        return self.elapsedtime

    def start(self):
        if self.stopped == 1:
            self.starttime = time.time()
            self.stopped = 0
            
    def reset(self):
        self.init()
        self.stopped = 1

    def stop(self):
        if self.stopped == 0:
            self.stoptime = time.time()
            self.elapsedtime = self.stoptime - self.starttime
            self.stopped = 1
            
    def display(self):
        if self.stopped == 1:
            print self.str()
        else:
            self.elapsedtime = self.stoptime - self.starttime + self.elapsedtime
            print self.str()

    def str(self):
        self.hours = int(self.elapsedtime / 3600)
        self.elapsedtime -= (self.hours * 3600)
        self.mins = int(self.elapsedtime / 60)
        self.elapsedtime -= (self.mins * 60)
        self.secs = int(self.elapsedtime)
        self.hundredths = int((self.elapsedtime - self.secs)*100)
        string = self.name + ": " + `self.hours` + ":" +\
                 `self.mins`+ ":" + `self.secs`+":" + `self.hundredths`
        return string

    def __repr__(self):
        self.gettime()
        return self.str()

    def __str__(self):
        self.gettime()
        return self.str()



if __name__=="__main__":
    A = Stopwatch("A")
    B = Stopwatch("B")
    A.start()
    time.sleep(1.2)
    B.start()
    time.sleep(0.8)
    A.stop()
    B.stop()
    A.display()
    B.display()
        
        

    
