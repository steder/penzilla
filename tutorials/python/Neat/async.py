#!/usr/bin/env python
#----------------------------------------------------------------------------
# async.py:             Asynchronous utilities
#
# See __doc__ string below.
#
# Package: 
# Requires:
#    - Python 2.1 or newer (www.python.org)
#    - OS: portable
#
# $Id: //depot/rgutils/rgutils/async.py#1 $
#----------------------------------------------------------------------------
'''
Asynchronous utilities.

Classes
=======
 L{TimedOutCaller} Wraps a function to allow calls w/ timeout.

Functions
=========
 L{callWithTimeout}(timeout, func, *args, **kwargs) Helper fct.
'''
__version__ = '0.1.' + '$Revision: #1 $'[12:-2]
__author__ = 'Richard Gruet', 'rjgruet@yahoo.com'
__date__    = '$Date: 2003/05/23 $'[7:-2], '$Author: rgruet $'[9:-2]
__since__ = '2000-04-11'
__doc__ += '\n@author: %s (U{%s})\n@version: %s' % (__author__[0],
                                            __author__[1], __version__)
__all__ = ['TimedOutCaller', 'AsyncError', 'TimeoutError', 'callWithTimeout']


from __future__ import nested_scopes
import sys, thread, threading, types 

if sys.version[:3] < '2.2':
    True, False = 1, 0  # built-in in Python 2.2

# Exceptions:
# ----------
class AsyncError(Exception):
    ''' Exceptions raised by this module.'''
    pass

class TimeoutError(AsyncError):
    ''' Timeout during a call.'''
    pass

#----------------------------------------------------------------------------
class TimedOutCaller:
#----------------------------------------------------------------------------
    ''' Function wrapper to make them callable with a timeout.
    
        Allows to call a function with a timeout, to avoid get stuck if
        the function freezes.
        Each instance wraps a function (changeable) which can be
        called many times with different arguments, using the operator().
    
        Methods
        =======
            L{__call__(*args, **kwargs)} -- Calls the default function w/ timeout.
            
            L{callFunc(func, *args, **kwargs)} -- Calls a function w/ timeout.
            
            L{setFunc(func)} -- Change default function.
            
            L{setTimeout(timeout)} -- Change timeout.
            
            L{getTimeoutCnt()} -- Gets nb of timeouts occurred.
            
            L{cleanUp()} -- clean up before exit.
            
        Usage
        =====
          Typical code::
            from async import TimedOutCaller
            
            # The function to call:
            def lazyFunc(x, y=3, z=0):
                sleep(2)
                return x
            
            # The function wrapper:
            lazyFunc_to = TimedOutCaller(lazyFunc, 4)
            
            # Call the function. No timeout occurs since the fct executes
            # in less than 4 sec:
            lazyFunc_to(1, z=2)  --> return 1
            
            # Change the timeout value so that lazyFunc fails:
            lazyFunc_to.setTimeout(1)
            lazyFunc_to(1) ==> raise TimeoutError
            
            # Call cleanUp when you no longer use the TimedOutCaller:
            lazyFunc_to.cleanUp()
            
        Limitations
        ===========
            Everytime a timeout occurs, a zombie thread stays alive. This is
            because there is no way to kill a thread in Python (it is a design
            decision), they have to terminate by themselves.
            The caller will still get control back, thanks to the timeout,
            but the called fct continues to consume the CPU in the background,
            which may or may not be acceptable. However if the called function
            exits later, the thread will automatically exits.
            
            TODO: on windows, we might call (via calldll) the WIN32API 
            fct TerminateThread to kill the thread.
    '''
    DEFAUT_TIMEOUT = 5.0
    # Max time waiting for a call before the "call" thread exits :
    THREAD_MAX_IDLE_TIME = 5.0
    
    def __init__(self, func=None, timeout=DEFAUT_TIMEOUT):
    
        self._lock = threading.RLock() #[RLock] Avoids reentrant calls.
        if func is None:
            func = lambda:None
        self._func = func           # [function] The function to call.
        self.setFunc(func)
        self._args = None           # [tuple] Arguments.
        self._kwargs = None         # [tuple] keyword arguments.
        self._callResult = None     # holds return value
        self._callException = None  # holds exception if any
        
        self._timeout = None        # [float>0] timeout in sec.
        self.setTimeout(timeout)
        self._timeoutCnt = 0        # [int] Nb of timeouts occurred

        # Sync between __call__ and the thread performing calls is ensured
        # via a pair of events:
        self._doCall = threading.Event()   # [Event] Set=perform the call
        self._callDone = threading.Event() # [Event] Set=call completed
        
        self._callThread = None     # [Thread] thread in which call executes
        self._threadId = 0          # [int] System thread identifier.
        self._stops = {}    # (dict] call threads in timeout, for which stop
                            # is requested: { threadId: T/F, ...}

    def __del__(self):
        try:
            self.cleanUp()
        except: 
            pass

    def __repr__(self):
        if self._func: fn = self._func.__name__
        else: fn = '(None)'
        return '<TimedOutCaller for function %s, timeout=%f>' % (
                                                    fn, self._timeout)
    def cleanUp(self):
        ''' Clean-up before exit.
        '''
        self._lock.acquire()
        try:
            for id in self._stops.keys():
                self._stops[id] = True
        finally:
            self._lock.release()
        
    def __call__(self, *args, **kwargs):
        ''' [synchronized] Calls associated function with the given args.

            The call is performed in a separate thread. If the fct
            is not completed within <timeout> seconds, an Exception
            is raised. If an exception occurs in the fct, it is forwarded
            here.
            @return: The result of the fct call.
            @exception TimeoutError: in case of time out.
            @see: L{setFunc}
            @see: L{callFunc}
        '''
        #print '%s(%s, %s)' % (self._func.__name__, args, kwargs) ####
        self._lock.acquire()
        try:
            self._args = args
            self._kwargs = kwargs
            self._callResult = None
            self._callException = None
            
            self._callDone.clear()
            if self._callThread is None or not self._callThread.isAlive():
                self._createCallThread()
            self._doCall.set()  # signal the call thread to do the call
            self._callDone.wait(self._timeout) # wait for end of exec.
            
            if self._callDone.isSet():  # OK
                if self._callException is not None:
                    raise self._callException
                else:
                    return self._callResult
            else:   # timeout:
                self._timeoutCnt += 1
                ## Try to kill the thread under win32 (TerminateThread)????
                self._stops[self._threadId] = True  # request stop
                self._callThread = None # (will create new thread when needed)
                raise TimeoutError('Time out (%.02f sec) while calling %s' %
                                    (self._timeout, self._func.__name__))
        finally:
            self._lock.release()
    
    def callFunc(self, func, *args, **kwargs):
        ''' Calls the given function with the given arguments.
        
            C{func} becomes the default function for next calls.
            @param func: [function] The new function.
            @see: L{__call__}
        '''
        self.setFunc(func)
        return self.__call__(*args, **kwargs)

    def setFunc(self, func):
        ''' Changes the function called.
            @param func: [function|Method] The new function.
        '''
        if not isinstance(func, types.FunctionType) and (
           not isinstance(func, types.MethodType)):
            raise TypeError('argument "func" must be a function|Method.')
        self._lock.acquire()
        self._func = func
        self._lock.release()
        
    def setTimeout(self, timeout):
        ''' Changes the timeout.
            @param timeout: [float|int >0] The new timeout.
        '''
        timeout = float(timeout) # (TypeError possible)
        if timeout <= 0:
            raise ValueError('setTimeout: timeout must be >0.')
        self._lock.acquire()
        self._timeout = timeout
        self._lock.release()
    
    def getTimeoutCnt(self):
        ''' Returns the number of timeouts that occured so far.'''
        return self._timeoutCnt

    # Private:
    # -------
    def _createCallThread(self):
        self._callThread = threading.Thread(target=self._callThreadMain)
        self._callThread.start()

    def _callThreadMain(self):
        ''' Call thread main loop.
            Waits for a call to perform, do it, signal end, and loop.
        '''
        id = self._threadId = thread.get_ident()
        self._stops[id] = False
        
        while not self._stops[id]:
            # Wait for a function to call; if idle for too long, or stop
            # requested or instance finalization, exit:
            self._doCall.wait(self.THREAD_MAX_IDLE_TIME)
            
            if (self._stops[id] or not hasattr(self, '_doCall')
                                or not self._doCall.isSet()):
                break

            # Call the function:
            self._doCall.clear()
            try:
                self._callResult = apply(self._func, self._args,
                                         self._kwargs)
            except Exception, e:
                self._callException = e
            if not self._stops[id]:
                self._callDone.set()    # signal end.
        
        # [stop]
        self._callThread = None
        del self._stops[id]
        self._threadId = None
        
            
#end class TimedOutCaller

#-----------------------------------------------------------------------------
def callWithTimeout(timeout, func, *args, **kwargs):
#-----------------------------------------------------------------------------
    " Helper function."
    return TimedOutCaller(func, timeout)(*args, **kwargs)

#-----------------------------------------------------------------------------
#                               T E S T S
#-----------------------------------------------------------------------------
import unittest, time

class TimedOutCallerTestCase(unittest.TestCase):
    ''' Test cases for class TimedOutCaller.
    ''' 
    # Init / finalization for all test cases:
    # -------------------
    def setUp(self):
        "Init, called before each test case."
        TimedOutCaller.THREAD_MAX_IDLE_TIME = 0.1   # speed up !

    def tearDown(self):
        "Finalization, called after each test case (whatever the outcome)."
        pass
    
    # Util functions :
    # --------------
    def _intersect(self, l1, l2):
        if len(l1) <= len(l2):
            return filter(lambda x: x in l2, l1)
        else:
            return filter(lambda x: x in l1, l2)
    def _equalSets(self, l1, l2):
        return len(self._intersect(l1,l2)) == len(l1)

    # Test cases (method names must start with 'test')
    # ----------
    def test01Constructor(self):
        "Check Construction."
        self.assertRaises(TypeError, TimedOutCaller, func=1)
        self.assertRaises(TypeError, TimedOutCaller, timeout=None)
        self.assertRaises(ValueError, TimedOutCaller, timeout='hello')
        self.assertRaises(ValueError, TimedOutCaller, timeout=0)
        toc = TimedOutCaller()  # default args
    
    def test02Repr(self):
        "Check __repr__"
        repr(TimedOutCaller())  # will fail if non string
        
    def test03FuncWithoutArgs(self):
        "Function without args returns a known value."
        self.assertEqual(TimedOutCaller(lambda:3.14159)(), 3.14159)

    def test04CreateWithoutFunc(self):
        "Default function call (none specified at creation) is harmless."
        self.assertEqual(TimedOutCaller()(), None)

    def test05MultipleCalls(self):
        "Multiple calls to same instance are possible."
        def getPi(): return 3.14159
        getPi_ = TimedOutCaller(getPi)
        self.assert_(getPi_() == getPi_() == 3.14159)

    def test06SameCallThreadUsed(self):
        "Same thread for different calls as long as there is no timeout."
        f = TimedOutCaller()
        f() # (will create call thread)
        thread0 = f._callThread
        self.assertEqual(f._callThread, thread0,
                        'Thread has changed between 2 calls without timeout')
        time.sleep(f.THREAD_MAX_IDLE_TIME + 0.1) # ensure > idle time
        self.assertEqual(f._callThread, None)
        f() # (will create call thread)
        self.assertNotEqual(f._callThread, thread0,
                        'Thread idle time expired but thread not changed')
         
    def test07ChangeFunc(self):
        "Function may be changed via setFunc()."
        def getPi(): return 3.14159
        f = TimedOutCaller()
        f.setFunc(getPi)
        self.assertEqual(f(), 3.14159)
        
    def test08CallFunc(self):
        "Method callFunc()"
        f = TimedOutCaller()
        def echo(*args, **kwargs): return args, kwargs
        self.assertEqual(f.callFunc(echo, 1,2,3,x=4), ((1,2,3), {'x':4}))
    
    def test09ArgsPassing(self):
        "Args well passed and returned to/by function called."
        def echo(*args, **kwargs): return args, kwargs
        self.assertEqual(TimedOutCaller(echo)(1,2,3,x=4), ((1,2,3), {'x':4}))
    
    def test10ReturnNone(self):
        "None received when calling a func. returning nothing."
        def returnNothing(): pass
        self.assertEqual(TimedOutCaller(returnNothing)(), None)
    
    def test11ExceptionInFunc(self):
        "Exception raised by function is passed back."
        class FakeException(Exception): pass
        def fail(): raise FakeException('Fake exception for test')
        self.assertRaises(FakeException, TimedOutCaller(fail))
        
    def test12TimeoutInFunc(self):
        "Timeout during a call raises TimeoutError and is counted."
        def sleepy(): time.sleep(0.5)
        f = TimedOutCaller(timeout=0.01)
        f() # (will create a call thread)
        thread0 = f._callThread
        self.assertNotEqual(thread0, None)
        self.assertEqual(f.getTimeoutCnt(), 0)
        self.assertRaises(TimeoutError, f.callFunc, sleepy)
        self.assertEqual(f.getTimeoutCnt(), 1)
        self.assertEqual(f._callThread, None)
        f.setTimeout(1) # be sure to avoid timeout
        f()
        self.assertEqual(f(), None,
                        'First (correct) call after a timeout failed.')
        self.assertNotEqual(f._callThread, thread0,
                        'Thread should have changed after a timeout')
    
    def test14CallsSync(self):
        "Reentrant calls are synced (sequentialized)."
        #print 'thread count = %d ####' % threading.activeCount()
        pass #self.fail("Don't know how to perform this test!")
    
    def test15(self):
        "Test callWithTimeout()"
        def echo(*args, **kwargs):
            return args + tuple(kwargs.values())
        self.assert_(self._equalSets(callWithTimeout(1, echo, 1, 2, x=3, y=4), (1,2,3,4))) 
        
# Builds a TestSuite from the test cases:
#suite = unittest.defaultTestLoader.loadTestsFromTestCase(
#                                       TimedOutCallerTestCase)
    
#----------------------------------------------------------------------------
#       M A I N
#----------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main() # Run all test cases found in this module.
