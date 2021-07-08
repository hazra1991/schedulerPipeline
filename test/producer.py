import pika, sys, os
import json
import traceback

def produce(*args,**kwargs):
    try:
        headers =  {
            "x-delay":5000,
        }

        # connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        connection ,channel =  connect()

        # channel = connection.channel()


        pr =  pika.BasicProperties(content_encoding='application/json',headers= headers,delivery_mode=2)
        pk = pika.BasicProperties(content_encoding='application/json',headers= {'x-delay':60000},delivery_mode=2)
        channel.basic_publish(
        exchange="schedule-delay",
        routing_key='Default-key',
        body=json.dumps({"args":args,"kw":kwargs}),
        properties=pr
        )
        channel.basic_publish(
        exchange="schedule-delay",
        routing_key='Default-key',
        body=json.dumps({"args":args,"kw":kwargs}),
        properties=pk
        )
        # print(" [x] Sent message !!!")
        # connection.close()
    except Exception as e:
        print(e)
        traceback.print_exception(*sys.exc_info(),file =None)


# class Threading(Thread):
#     def run()



def fproduce():
    for i in range(100):
        produce()
    # import time
    # time.sleep(1)

from functools import lru_cache

@lru_cache(maxsize=1)
def connect():
    c = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    ch =  c.channel()
    ch.queue_declare(queue='task-queue',durable=True)
    ch.exchange_declare('even-delay',exchange_type='x-delayed-message',durable=True,arguments={'x-delayed-type':'direct'})
    # print(c,ch)
    return c ,ch
# connect.cache_info()
# connect.cache_clear()


fproduce()
# import cProfile
# import pstats

# with cProfile.Profile() as pr:

#     fproduce()

# stats = pstats.Stats(pr)
# stats.sort_stats(pstats.SortKey.TIME)
# stats.print_stats()

# breakpoint()

