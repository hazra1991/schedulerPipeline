def testfun(to,frm,sub):

    print(to,frm,sub)
    print("======fun1=========")

def testfun2(to,frm,sub):

    print(to,frm,sub)
    print("=======func2========")

def testfun3(to,frm,sub):

    print(to,frm,sub)
    print("======fun3=========")

def testfun4(to,frm,sub):

    print(to,frm,sub)
    print("=====fun4==========")


#### create DB connection ####
from peewee import *

db = PostgresqlDatabase('patient', user='postgres', password='test123',host='127.0.0.1',port=5432)
cur = db.execute_sql('select phone,username,timezone from patient')
val = cur.fetchall()
from pprint import pprint
pprint(len(val))


from Scheduler.manageworker import Manager
from Scheduler.utils import produce
c = Manager()
# c.register(testfun4,testfun,testfun2,testfun3)
co= 0
for args in val:
    co+=1

    # produce("testfun",*args)
    # produce("testfun2",*args)
    # produce("testfun3",*args)
    # produce("testfun4",*args)
    c.registerAndPublishJob(testfun,*args)
    c.registerAndPublishJob(testfun2,*args)
    c.registerAndPublishJob(testfun3,*args)
    c.registerAndPublishJob(testfun4,*args)

print(c._jobmapper)
print(co)
from threading import Thread
from multiprocessing import Process
# t1 = Process(target=c.startworker()).start()
c.startworker(multiprocessing=True)

import time
time.sleep(5)


# c.startworker()x

print('hi')



