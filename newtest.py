##Enhancements
# TODO     logging into a log file using the provided thread lock
# TODO     publish using lru_cache for faster and resuing the connections 
# TODO/BUG create a shared memory space for  multiprocessing 
# TODO     Add logging mechanism 

##TO BE DONE AFTER DISCUSSED 
# TODO implement the scheduler and delay mechanish after dicsussion 
# TODO implement yml config file for easier scheduler configuration
# TBD :- the metric functions proper definition , the function should run per each indivisual customer one by one 
# TBD :- the timezone info should be saved during registration for easiar calculations , an do the customer will have time choosing fasility 
#======================================================

# try:

def testfun(*a):

    print(to,frm,sub)
    print("======fun1=========")

def testfun2(to,frm,sub):

    print(to,frm,sub)
    print("=======func2========")

#### create DB connection ####
from peewee import *


# call this aonce evry day 
db = PostgresqlDatabase('patient', user='postgres', password='test123',host='127.0.0.1',port=5432)
cur = db.execute_sql('select phone,username,timezone from patient')
val = cur.fetchall()
from pprint import pprint

# var = with the data i will calcutlate each customer calling time 
from Scheduler.manageworker import Manager
c = Manager(multiprocessing=True)
c.startworker(max_workers=5)

c.register(testfun2)



for args in range(10):
    # c.registerAndPublish(testfun,delay=5000)
    c.registerAndPublish(testfun2,1,2,3,delay=4)
    # break
print(c._jobmapper)
print(type(c._jobmapper))
print('done sending ')
import time
time.sleep(2)
# print(c._W_connections)
# from threading import Thread
# from multiprocessing import Process
# t1 = Process(target=c.startworker()).start()
try:
    # c.startworker(max_workers=4,multiprocessing=True)

    import time



    print("waiting")
    # time.sleep(10)
except KeyboardInterrupt:
    print("interupt=============================")
    # c.close_worker_Conenctions()

# # c.startworker()x

print('hi')
# print(c._jobmapper)

# print('hellow')

print('pausing')

time.sleep(20)
c.join()
print('done pausing')

c.stopProcess()






