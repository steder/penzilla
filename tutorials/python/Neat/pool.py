#!/usr/bin/env python
#-----------------------------------------------------------------------------
# pool.py:          Resource Pool management
#
# See __doc__ string below.
#
# Requires:
#   Python 1.5.2 or >
#   OS: portable
#
# TODO
#
# $Id: //depot/rgutils/rgutils/pool.py#1 $
#-----------------------------------------------------------------------------
'''
Resource pool management.

B{Classes}
   - L{Pool}  -- a pool of resources.
'''
__version__ = '1.1.' + '$Revision: #1 $'[12:-2]
__author__ = 'Richard Gruet', 'rjgruet@yahoo.com'
__date__    = '$Date: 2003/05/23 $'[7:-2], '$Author: rgruet $'[9:-2]
__since__ = '2000/11/10'
__doc__ += '\n@author: %s (U{%s})\n@version: %s' % (__author__[0],
                                            __author__[1], __version__)


import threading, types

true, false = -1, 0

class PoolError(Exception):
    ''' Exception raised by the pool module.
    '''
    pass

#-----------------------------------------------------------------------------
class Pool:
#-----------------------------------------------------------------------------
    ''' A pool of resources to be shared by threads of a (same) process.

        All resources are supposed of the same kind. They are created
        externally and passed on creation.

        The class defines 2 methods:

          - L{acquire}(timeout)    -- acquire a resource
          - L{release}(resource)   -- release a resource

    '''
    FREE = 0        # resource is available.
    ALLOCATED = 1   # resource is allocated

    def __init__(self, resources):
        ''' Creates a pool containing the given resources.

            @param resources: A sequence of arbitrary objects that must be of
                              the same kind (not checked).
        '''
        if (not isinstance(resources, types.TupleType) and
            not isinstance(resources, types.ListType)):
            raise TypeError('Arg resources must be a list or a tuple.')
        if not resources:
            raise ValueError('Resource list is empty.')

        self.resDict = {}   # { id resource: (resource, state FREE/ALLOCATED,
                            #                 None/owner),...}
        for res in resources:
            key = id(res)
            assert not self.resDict.has_key(key), 'Duplicate resource key'
            self.resDict[key] = (res, self.FREE, None)

        self.resAvailable = threading.Condition(threading.Lock())
        self.freeCnt = len(self.resDict)     # nb of avail. resources

    def __del__(self):
        pass

    def __repr__(self):
        return '<Pool, %d resources, %d free>' % (len(self.resDict),
                                                  self.freeCnt)

    def acquire(self, blocking=true):
        '''Requests the allocation of a resource.

           @param blocking: if true, waits until a resource is available.
           @return: The allocated resource, or None if C{blocking} false
                   and no available resource.
        '''
        self.resAvailable.acquire()
        try:
            while self.freeCnt == 0:
                if not blocking:
                    return None
                self.resAvailable.wait()
            else: # locate avail resource:
                for res, state, owner in self.resDict.values():
                    if state == self.FREE:
                        # Allocate the resource to caller:
                        callerId = threading.currentThread()
                        self.resDict[id(res)] = (res, self.ALLOCATED, callerId)
                        self.freeCnt = self.freeCnt - 1
                        return res
                raise PoolError('BUG! freeCnt>0 but no free resource found')
        finally:
            self.resAvailable.release()

    def release(self, resource):
        '''Releases a resource.

           @param resource: The resource to release.
           @exception PoolError: The resource doesn't belong to the pool,
                        is not allocated or the caller is not the owner.
         '''
        self.resAvailable.acquire()
        try:
            key = id(resource)
            try:
                res, state, owner = self.resDict[key]
            except KeyError:
                raise PoolError("Can't release unknown resource.")
            if state != self.ALLOCATED:
                raise PoolError('Resource not allocated.')
            if owner != threading.currentThread():
                raise PoolError('Not owner (owner ID is %d).' % owner)
            self.resDict[key] = (resource, self.FREE, None)
            self.freeCnt = self.freeCnt + 1
            self.resAvailable.notify()
        finally:
            self.resAvailable.release()


#-----------------------------------------------------------------------------
#                               T E S T S
#-----------------------------------------------------------------------------
def test():

    resCnt = 3          # Nb of resources in pool.
    clientCnt = 10      # Nb of concurrent clients.
    acquireCnt = 10     # Nb of resource acquires for each client

    print 'Testing Pool (%d resources, %d consumers)...' % (resCnt, clientCnt)

    resources = []
    for i in range(resCnt):
        resources.append('res%d' % i)
    pool = Pool(resources)
    #print pool

    # Create <clientCnt> x threads to represent consumers
    threads = []
    for i in range(clientCnt):
        name = 'client#%d' % (i+1)
        threads.append(threading.Thread(target=_threadMain,
                                          args=(name, pool, acquireCnt)))
    for thread in threads:
        thread.start()

    # Wait for termination of all clients:
    import time
    while threads:
        threads = filter(lambda t: t.isAlive(), threads)
        if threads:
            time.sleep(0.5)

    print '=> Tests passed.'

def _threadMain(name, pool, acquireCnt):
    import time, random
    print '%s started.' % name
    for i in range(acquireCnt):
        res = pool.acquire()
        print '%s acquired by %s' % (res, name)
        time.sleep(random.random()/2 + 0.01)
        pool.release(res)
        print '%s released by %s' % (res, name)
        time.sleep(0.01)
    print '%s ended.' % name

#-----------------------------------------------------------------------------
#                               M A I N
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    test()
