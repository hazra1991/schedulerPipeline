##Enhancements
# TODO logging into a log file using the provided thread lock
# TODO publish using lru_cache for faster and resuing the connections 

##TO BE DISCUSSED 
# TODO implement the scheduler and delay mechanish after dicsussion 
# TODO implement yml config file for easier scheduler configuration
# TBD :- the metric functions proper definition , the function should run per each indivisual customer one by one 
# TBD :- the timezone info should be saved during registration for easiar calculations , an do the customer will have time choosing fasility 
#======================================================



def testfun(to,frm,sub):

    print(to,frm,sub)
    print("======fun1=========")

def testfun2(to,frm,sub):

    print(to,frm,sub)
    print("=======func2========")

#### create DB connection ####
from peewee import *

db = PostgresqlDatabase('patient', user='postgres', password='test123',host='127.0.0.1',port=5432)
cur = db.execute_sql('select phone,username,timezone from patient')
val = cur.fetchall()
from pprint import pprint

from Scheduler.manageworker import Manager
c = Manager()

for args in val:
    c.registerAndPublish(callback,1232423,delay=5000)
    # c.registerAndPublish(testfun2,*args,delay=5000)
    # c.registerAndPublish(testfun3,*args)
    # c.registerAndPublish(testfun4,*args)
    # break

from threading import Thread
from multiprocessing import Process
# t1 = Process(target=c.startworker()).start()
try:
    c.startworker(max_workers=1,multiprocessing=True)

    import time



    print("waiting")
    time.sleep(10)
except KeyboardInterrupt:
    print("interupt=============================")
    c.close_worker_Conenctions()

# # c.startworker()x

print('hi')
# exit()

# print('hellow')





