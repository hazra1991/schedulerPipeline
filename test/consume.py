import pika, sys, os

with open('WORKER.pid','w') as fd:
    fd.write(str(os.getppid())+'\n')
    fd.write(str(os.getpid()))

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(f"{ch}\n=========== \n {method}\n=========== \n {properties.headers}\n=========== \n{body}")
        print(" [x] Received %r" % body)
        import time 
        # time.sleep(10)
        ch.basic_ack(delivery_tag=method.delivery_tag) # ack to rabit , till not set the message wont be deleted from queue

    '''this value define how many messages from the queue can be taken at a time and processed and sent ack 
       for this case programm will accept 10 messages from queue and will process and give 10 ack then only
       it will accept more 10 message from the queue . the ack in imp as the auto_ack is False and the basic_ack is set 
    '''    
    channel.basic_qos(prefetch_count=10)   # for 
                                            

    channel.basic_consume(queue='task-queue', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

main()