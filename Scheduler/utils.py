import pika, sys, os
import json
import traceback


with open('WORKER.pid','w') as fd:
    fd.write(str(os.getppid())+'\n')
    fd.write(str(os.getpid()))

####-- consumer code ---#####
# TODO logging into a log file using the provided thread lock

def consume(self,host,workernumber,lock):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()
    channel.queue_declare(queue='process-failed',durable=True)
    channel.basic_qos(prefetch_count=1)
    print("worker created", workernumber)
    def callback(ch, method, properties, body):
        try:
            callback_fun = self._jobmapper.get(properties.headers.get('callback'))
            body =  json.loads(body)
            arg =  body['args']
            kw = body['kw']
            callback_fun(*arg,**kw)
             # ack to rabit , till not set the message wont be deleted from queue
        except Exception as e:
            print(e)
            #'''handelling unprocessed messages'''
            channel.basic_publish(
                                exchange='',
                                routing_key='process-failed',
                                body=body,
                                properties=pika.BasicProperties(content_encoding='application/json',headers= {'status':'failed'},delivery_mode=2)
                                )

            # traceback.print_exception(*sys.exc_info(),file=None) # tracebacking the exception theta auccrd and captured by sys.exc_info()
        print(workernumber)
        print(body,"[**8]processing" )
        ch.basic_ack(delivery_tag=method.delivery_tag)
    channel.basic_consume(queue='task-queue', on_message_callback=callback)
    # print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()




### -- producer code --########

def produce(host,callback,*args,**kwargs):
    try:
        headers =  {
            "callback":callback,
        }

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))

        channel = connection.channel()

        channel.queue_declare(queue='task-queue',durable=True)

        pr =  pika.BasicProperties(content_encoding='application/json',headers= headers,delivery_mode=2)
        channel.basic_publish(
        exchange='',
        routing_key='task-queue',
        body=json.dumps({"args":args,"kw":kwargs}),
        properties=pr
        )
        print(" [x] Sent message !!!")
        connection.close()
    except Exception as e:
        print(e)
        traceback.print_exception(*sys.exc_info(),file =None)

# class Threading(Thread):
#     def run()