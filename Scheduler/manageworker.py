from .utils import consume,publish


################################
#     Primary Manager class    # 
################################
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
                '__routingkey',
                'spawn_child',
                'lock',
                'Multiprocessing',
                '__manager']


    def __init__(self,**kwargs):
        self.Multiprocessing:bool = kwargs.pop('multiprocessing',False)
        if self.Multiprocessing:
            from multiprocessing import Manager as Mr
            from multiprocessing import Process
            self.__manager = Mr()
            self._jobmapper = self.__manager.dict()
            self.lock = self.__manager.Lock()
            self.spawn_child = Process
        else:
            from threading import Thread ,Lock
            self.lock = Lock()
            self.spawn_child = Thread
            self._jobmapper = dict()
            self._W_connections = set()     # worker connections 
        self.__workerlist = set()
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
    
    def startworker(self,max_workers=4):
        if self.__workerstatus:
            self.stopProcess()
            raise RuntimeError('[*] Worker already scheduled for the object')
        self.__workerstatus = True
        for num in range(max_workers):
            p = self.spawn_child(target=consume,args=(self,self.__MQServer,num))
            p.start()
            self.__workerlist.add(p)
        # if self.Multiprocessing:
        #     self.join()
        # TODO the shared memory will break as the main script will just deleter the manager object,hence the code will break
        
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
        if not self.Multiprocessing:
            print(self.__workerlist)
            self.close_worker_Conenctions()
            return 
            
        for worker in self.__workerlist:
            if worker.is_alive:
                worker.terminate()
                # worker.close()
        self.__manager.shutdown()
        self.join()
        del self.__workerlist
        return

    def close_worker_Conenctions(self):
        if self.Multiprocessing:
            self.stopProcess()
            return
        for i in self._W_connections:
            
            if i.is_open:
                print(i)
                i.close()
        del self._W_connections

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



######### pending #########

class CustomSetter:

    '''defining a setter with no getters or deleter
        @CustomeSetter
        def myfun(self,val):
            ........fun defination'''

    def __init__(self,fun):
        self.fun = fun
        raise NotImplementedError('Implementations not done ,work in progress')

    def __set__(self,obj,value):
        ''' will define the setter bofy and call the self.fun with the value'''
        pass