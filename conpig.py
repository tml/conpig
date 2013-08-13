import sys

from greenlet import greenlet
import signal
from collections import deque
import time

threads = deque([])

def next(argA, argB):
    global threads

    if len(threads) == 0: 
        return

    t = threads.popleft()
    
    if t.dead:
        return next(argA, argB)

    threads.append(t)
    signal.setitimer(signal.ITIMER_REAL, 0.00001)
    t.switch()

def forkIO(method, *args, **kr):
    def methodp():
        method(*args,**kr)
    threads.append(greenlet(methodp))

def runMain(main):
    forkIO(main)
    signal.signal(signal.SIGALRM, next)
    
    next(None,None)
    while len(threads) > 0:
        # I'm told pause sucks
        time.sleep(4)


##################
##  TESTING IT  ##
##################

def test(arg):
    for i in range(0,4000):
        print arg

def main():
    forkIO(test, "X")    
    forkIO(test, "O")

runMain(main)
