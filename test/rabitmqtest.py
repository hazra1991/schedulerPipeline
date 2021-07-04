import pika

def producer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()

    channel.queue_declare(queue='task-queue',durable=True)
    import time
    # self.content_encoding = content_encoding
    #         self.headers = headers
    #         self.delivery_mode = delivery_mode
    #         self.priority = priority
    #         self.correlation_id = correlation_id
    #         self.reply_to = reply_to
    #         self.expiration = expiration
    #         self.message_id = message_id
    #         self.timestamp = timestamp
    #         self.type = type
    #         self.user_id = user_id
    #         self.app_id = app_id
    #         self.cluster_id = cluster_id

    headers =  {

    }
    pr =  pika.BasicProperties(content_encoding='application/json',headers={"task":"fun"},delivery_mode=2)
    for i in range(1000):
        
        time.sleep(0.5)
        print("sending")
        channel.basic_publish(
        exchange='',
        routing_key='task-queue',
        body="mystring",
        properties=pr
        )
    print(" [x] Sent 'Hello World!'")
    connection.close()

producer()
# from celery import Celery

# c = Celery('mytask',broker='localhost')


# @c.task
# def fun():
#     print("function called")
#     # return "HELLO WORKDdabdkakjsdakjdsakjsdahj"
# from datetime import datetime ,timedelta
# tim = datetime.now() + timedelta(seconds = 60)

# print(tim)

# fun.apply_async(eta =  tim)