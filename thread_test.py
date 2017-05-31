import time
import os
from threading import Thread

def myfunc(i, t):
    print("sleeping %d sec from thread %d" % (t, i))
    os.system("sleep " + str(t))
    #~ os.system("sleep " + str(t) + " &")
    #~ time.sleep(t)
    print("finished sleeping from thread %d" % i)

t1=10
t2=5
for i in range(3):
    t = Thread(target=myfunc, args=(i,t1))
    t.start()
    time.sleep(t2)
