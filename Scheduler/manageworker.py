from .utils import consume,publish

class CustomSetter:
    '''defining a setter with no getters or deleter
        @CustomeSetter
        def myfun(self,val):
            ........fun defination'''

    def __init__(self,fun):
        self.fun = fun

    def __set__(self,obj,value):
        ''' will define the setter bofy and call the self.fun with the value'''
        pass

class Manager:
    
    __slots__ = ['_jobmapper',
                '__workerlist',
                '_W_connections',
                '__workerstatus',
                '__MQServer',
                '__exchange_name',
                '__exchange_type',
                '__delay_exchange_args',
                '__all_exchange_types',
                '__default_queue_name',
                '__dead_queue_name',
                '__routingkey']


    def __init__(self,**kwargs):
        self._jobmapper = dict()
        self.__workerlist = set()
        self._W_connections = set()     # worker connections 
        self.__workerstatus:bool = False
        self.__MQServer:str = kwargs.get('host','localhost')
        self.__exchange_name:str = 'schedule-delay'
        self.__exchange_type:str = 'x-delayed-message'
        self.__delay_exchange_args:dict = {'x-delayed-type':'direct'}
        self.__all_exchange_types:set = {'direct','topic','headers','fanout'}
        self.__default_queue_name = 'Message-Queue'
        self.__dead_queue_name = 'Dead-Queue'
        self.__routingkey = 'Default-key'

    def register(self,*arg):
        for fun in arg:
            self._jobmapper.setdefault(fun.__name__,fun)
    
    def startworker(self,max_workers=4,multiprocessing = False):
        if self.__workerstatus:
            self.stopProcess()
            raise RuntimeError('[*] Worker already scheduled for the object')
        self.__workerstatus = True
        if multiprocessing:
            from multiprocessing import Process,Lock
            lock = Lock()
            for num in range(max_workers):
                p = Process(target=consume,args=(self,self.__MQServer,num,lock))
                p.start()
                self.__workerlist.add(p)
                
        else:
            from threading import Thread ,Lock
            lock = Lock()
            for num in range(max_workers):
                p = Thread(target=consume,args=(self,self.__MQServer,num,lock))
                p.start()
                self.__workerlist.add(p)

        print("this is printing")

    def registerAndPublish(self,fun,*args,**kwargs):
        self._jobmapper.setdefault(fun.__name__,fun)
        self.publishJob(fun.__name__,*args,**kwargs)
    
    def publishJob(self,funname,*args,**kw):
        if not self._jobmapper.get(funname):
            raise ValueError(f'{funname} Job not registered')
        
        publish(self,self.__MQServer,funname,*args,**kw)


    def join(self):
        ''' blocking call ''' 
        if not self.__workerlist:
            raise ValueError('No workers available')
        for worker in self.__workerlist:
            worker.join()
        return True
        
            
    def stopProcess(self):
        print("[*] Stoping all execution")
        for worker in self.__workerlist:
            if worker.is_alive:
                worker.terminate()
    def close_worker_Conenctions(self):
        for i in self._W_connections:
            if i.is_open:
                i.close()
            self._W_connections.remove(i)


    @property
    def exchange_name(self):
        return self.__exchange_name
    
    @exchange_name.setter
    def exchange_name(self,name):
        if not isinstance(name,str):
            raise ValueError(f'Exchange name {name} is not a proper name')
        self.__exchange_name = name

    @property
    def exchange_type(self):
        return self.__exchange_type
    

    @property
    def exchange_after_delay(self):
        return self.__delay_exchange_args
    
    @exchange_after_delay.setter
    def exchange_after_delay(self,name):
        if not name in self.__all_exchange_types:
            raise ValueError(f'Name {name} not a valid Exchange type')
        
        self.__delay_exchange_args = {'x-delayed-type':name}

    @property
    def queue_name(self):
        return self.__default_queue_name

    @property
    def dead_queue(self):
        return self.__dead_queue_name
    
    @property
    def routingkey(self):
        return self.__routingkey
