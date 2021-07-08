import pika, sys, os
import json
import traceback


with open('WORKER.pid','w') as fd:
    fd.write(str(os.getppid())+'\n')
    fd.write(str(os.getpid()))

####-- consumer code ---#####
# TODO logging into a log file using the provided thread lock
# TODO publish using lru_cache for faster and resuing the connections 

def consume(self,host,workernumber,lock):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()
    channel.exchange_declare(self.exchange_name,
                                exchange_type=self.exchange_type,
                                durable=True,
                                arguments=self.exchange_after_delay)

    channel.queue_declare(queue=self.queue_name,durable=True)
    channel.queue_declare(queue=self.dead_queue,durable=True)
    channel.queue_bind(exchange=self.exchange_name,queue=self.queue_name,routing_key=self.routingkey)

    channel.basic_qos(prefetch_count=1)
    self._W_connections.add(connection)

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
            # print("=================",body) 
            print(e)
            #'''handelling unprocessed messages'''
            channel.basic_publish(
                                exchange='',
                                routing_key=self.dead_queue,
                                body=str(body),
                                properties=pika.BasicProperties(content_encoding='application/json',
                                                                headers= {'status':'failed','message':str(e)},
                                                                delivery_mode=2)
                                )
            # traceback.print_exception(*sys.exc_info(),file=None) # tracebacking the exception theta auccrd and captured by sys.exc_info()
        # print(workernumber)
        # print(body,"[**8]processing" )
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=self.queue_name, on_message_callback=callback)
    # print(' [*] Waiting for messages. To exit press CTRL+C')
    try:
        channel.start_consuming()
    except (Exception,KeyboardInterrupt) as err:
        print(err)
        print("[X] EXception ;; closing connecitons for worker : - ",workernumber)
        if connection.is_open:
            connection.close()
            self._W_connections.remove(connection)
        




### -- producer code --########

def publish(self:'Manager Object',host,callback,*args,**kwargs): # passing the parent object for the env reference 
    delay = kwargs.pop('delay',0)
    queue_name =kwargs.pop('queue_name',self.queue_name)
    exchange_name =  self.exchange_name
    try:
        headers =  {
            "callback":callback,
            "x-delay":delay
        }

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        channel = connection.channel()
        channel.exchange_declare(exchange_name,
                                exchange_type=self.exchange_type,
                                durable=True,
                                arguments=self.exchange_after_delay)

        channel.queue_declare(queue=queue_name,durable=True)

        pr =  pika.BasicProperties(content_encoding='application/json',headers= headers,delivery_mode=2)
        channel.basic_publish(
        exchange=exchange_name,
        routing_key=self.routingkey,
        body=json.dumps({"args":args,"kw":kwargs}),
        properties=pr
        )
        print(" [x] Sent message !!!")
        connection.close()
    except (Exception,KeyboardInterrupt) as e:
        print(e)
        print('Could not pulish')
        if connection.is_open:
            connection.close()
        traceback.print_exception(*sys.exc_info(),file =None)

# class Threading(Thread):
#     def run()