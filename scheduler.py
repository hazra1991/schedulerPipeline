
# @sched.scheduled_job('interval', minutes=1)
# def scale_out_to_three():
#     print('done')
# sched.start()

# import threading 
# def fun():
#     print('function eran ')


# threading.Timer(2,fun).start()


# print("this is working ")


# import time 
# time.sleep(10)
# print("this is working too")

# runatintervals()
# runatspecifictime()
# converttolocaltimeandrun()
# @register
# moniter() blocking call 

import sched,time

s = sched.scheduler(time.monotonic,time.sleep)
def fun():
    print('function ran')
def fun2():
    print("this is fun2")

s.enterabs(10,1,fun)
s.enterabs(5,1,fun2)
print(s.queue, "this is runnit ")

print("Waiting")
print(time.monotonic())
print(s.queue)
s.run(blocking=True)
print('waited')


